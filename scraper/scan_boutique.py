"""
Orchestrateur : un seul appel catalogue + une seule recherche par boutique et
par cycle de scan, dont le resultat alimente ENSUITE deux logiques d'alerte
independantes :
  - bonne_affaire_shopify.py  (seuil de prix / cote -> alerte 🔥)
  - alerte_stock.py           (retour en stock -> alerte 📦)

Chaque logique garde ses propres regles et son propre canal Telegram ; seule
la recuperation de donnees (appel reseau /products.json + matching des
titres) est mutualisee, pour ne jamais interroger deux fois la meme
boutique dans un meme cycle.

Boucle sur plusieurs boutiques (cf. boutiques_shopify.py) :
  - delai de politesse (DELAI_ENTRE_BOUTIQUES) entre deux boutiques, en plus
    du delai deja existant entre pages d'un meme site (connecteur_shopify.py)
    -- evite de reproduire un rate-limit comme celui de nexthobby.fr.
  - une boutique qui echoue (timeout, 403, 429, DNS...) est loguee et
    SAUTEE : le cycle continue sur les boutiques suivantes plutot que de
    s'arreter entierement pour un seul site en panne.
"""

import logging
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alerte_stock import charger_memoire, detecter_retours_en_stock, envoyer_telegram_retours_stock, sauvegarder_memoire
from bonne_affaire_shopify import charger_cotes, charger_regles, detecter_bonnes_affaires, envoyer_telegram_bonnes_affaires
from connecteur_shopify import ConnecteurShopify
from memoire_supabase import charger_memoire_supabase, sauvegarder_memoire_supabase
from watchlist_shopify import CarteWatchlist

# Sans ceci, les log.info()/log.warning() emis par les ponts SaaS appeles
# depuis cet orchestrateur (connecteur_supabase.py, watchlist_saas.py,
# notifications_saas.py) restaient INVISIBLES dans les logs GitHub Actions
# -- seul main.py configurait le logger racine jusqu'ici. Trouve le
# 31/08/2026 en verifiant en conditions reelles le correctif du 409
# watchlist_alerts (PR #88) : impossible de confirmer la ligne de succes
# "[Supabase] N alerte(s) watchlist enregistree(s)" dans les logs du run,
# alors que le code s'executait bien (seuls les log.warning() apparaissaient,
# via le handler de secours de Python, jamais les log.info()). Meme format
# que main.py, pour rester coherent entre orchestrateurs.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)

# Cle de la memoire stock dans la table Supabase scraper_memoire (cf.
# memoire_supabase.py) -- migration du 24/08/2026, remplace le fichier Git
# data/stock_boutiques_tcg.json pour ne plus committer cet etat a chaque
# cycle (30 min). Meme nom que l'ancien fichier, sans l'extension.
CLE_MEMOIRE_STOCK = "stock_boutiques_tcg"

DELAI_ENTRE_BOUTIQUES = 2.5  # secondes -- politesse a l'echelle de 40 sites d'un coup

# Meme pattern que main.py de PokeDeals : le token vient des secrets/env,
# jamais en dur dans le code. chat_id deja confirme pour PokeDeals (cf.
# config.yaml -> telegram.chat_id, verifie via getUpdates le 13/07/2026).
TELEGRAM_CHAT_ID = "1245330032"


def scanner_boutique_complet(
    domaine: str,
    cartes: list[CarteWatchlist],
    memoire_stock: dict,
    cotes: dict,
    regles: dict,
) -> tuple[list[dict], list[dict]]:
    """Scanne UNE boutique pour la liste de cartes donnee et retourne
    (deals_bonne_affaire, evenements_retour_stock).

    Un seul appel reseau (recuperer_tout_le_catalogue) et un seul passage de
    matching (rechercher_dans_catalogue), partages entre les deux logiques.
    `memoire_stock` est mise a jour en place (cf. alerte_stock.py).

    Ne catch AUCUNE exception ici -- c'est la responsabilite de l'appelant
    (scanner_plusieurs_boutiques) de faire en sorte qu'un echec sur cette
    boutique ne bloque pas les suivantes.
    """
    cartes_par_critere = {carte.cle_recherche: carte for carte in cartes}
    criteres = list(cartes_par_critere.keys())

    connecteur = ConnecteurShopify(domaine)
    catalogue = connecteur.recuperer_tout_le_catalogue()                       # 1 seul appel reseau
    resultats_par_critere = connecteur.rechercher_dans_catalogue(catalogue, criteres)  # 1 seul passage

    deals = detecter_bonnes_affaires(resultats_par_critere, cartes_par_critere, cotes, regles)
    evenements_stock = detecter_retours_en_stock(domaine, resultats_par_critere, cartes_par_critere, memoire_stock)

    return deals, evenements_stock


def scanner_plusieurs_boutiques(
    boutiques: list[str],
    cartes: list[CarteWatchlist],
    memoire_stock: dict,
    cotes: dict,
    regles: dict,
) -> dict:
    """Boucle sur toutes les boutiques avec delai de politesse et resilience
    aux echecs individuels. Retourne un resume complet du cycle :
    {deals, evenements_stock, boutiques_ok, boutiques_echec, duree_secondes}.
    """
    debut = time.monotonic()
    tous_les_deals: list[dict] = []
    tous_les_evenements: list[dict] = []
    boutiques_ok: list[str] = []
    boutiques_echec: list[dict] = []  # [{"domaine":..., "raison":...}]

    for i, domaine in enumerate(boutiques):
        try:
            deals, evenements = scanner_boutique_complet(domaine, cartes, memoire_stock, cotes, regles)
            tous_les_deals.extend(deals)
            tous_les_evenements.extend(evenements)
            boutiques_ok.append(domaine)
            print(f"[{i + 1}/{len(boutiques)}] {domaine} : OK — {len(deals)} deal(s), {len(evenements)} retour(s) en stock")
        except Exception as e:  # noqa: BLE001 -- volontaire : une boutique en echec ne doit jamais arreter le cycle
            raison = f"{type(e).__name__}: {e}"
            boutiques_echec.append({"domaine": domaine, "raison": raison})
            print(f"[{i + 1}/{len(boutiques)}] {domaine} : ECHEC — {raison}")

        if i < len(boutiques) - 1:
            time.sleep(DELAI_ENTRE_BOUTIQUES)

    duree = time.monotonic() - debut
    return {
        "deals": tous_les_deals,
        "evenements_stock": tous_les_evenements,
        "boutiques_ok": boutiques_ok,
        "boutiques_echec": boutiques_echec,
        "duree_secondes": duree,
    }


if __name__ == "__main__":
    from boutiques_decouvertes import BOUTIQUES_SHOPIFY_AUTO
    from boutiques_shopify import BOUTIQUES_SHOPIFY
    from watchlist_saas import cartes_watchlist_saas, notifier_deals_boutique_saas
    from watchlist_shopify import charger_watchlist_config

    # Test cible : `python scan_boutique.py kyoriyu.fr questcorner.fr` ne
    # scanne QUE les domaines passes en argument, au lieu de la liste
    # complete. Sans argument : boutiques curees a la main + boutiques
    # ajoutees automatiquement par decouverte_boutiques.py (radar AFNIC).
    boutiques = sys.argv[1:] if len(sys.argv) > 1 else list(BOUTIQUES_SHOPIFY) + list(BOUTIQUES_SHOPIFY_AUTO)

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    cle_anthropic = os.environ.get("ANTHROPIC_API_KEY", "")

    cartes = charger_watchlist_config()
    # SaaS (saas/) : ajoute les cartes des watchlists utilisateur, en plus
    # de config.yaml -- GRATUIT ici en requetes HTTP (catalogue entier deja
    # recupere en un seul appel par boutique, cf. watchlist_saas.py),
    # contrairement a main.py (eBay/Vinted/Leboncoin, plafonne la-bas).
    cartes_saas = cartes_watchlist_saas(
        os.environ.get("SUPABASE_URL", ""), os.environ.get("SUPABASE_SERVICE_ROLE_KEY", ""))
    if cartes_saas:
        print(f"{len(cartes_saas)} carte(s) supplementaire(s) des watchlists utilisateur (SaaS) ajoutee(s)")
        cartes = cartes + cartes_saas
    print(f"{len(cartes)} criteres de recherche charges depuis config.yaml (121 cartes, avec variantes alias)")
    print(f"{len(boutiques)} boutique(s) a scanner : {', '.join(boutiques)}")
    print(f"Telegram : {'configure' if token else 'NON configure (TELEGRAM_BOT_TOKEN absent -- envoi desactive)'}\n")

    cotes = charger_cotes()
    regles = charger_regles()

    # Memoire stock : Supabase si les secrets sont configures (prod, cf.
    # memoire_supabase.py -- ne DOIT jamais silencieusement repartir d'une
    # memoire vide sur une panne reseau), repli sur le fichier local sinon
    # (dev/test sans secrets).
    supabase_url = os.environ.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    memoire_via_supabase = bool(supabase_url and supabase_key)
    if memoire_via_supabase:
        memoire_stock = charger_memoire_supabase(CLE_MEMOIRE_STOCK, supabase_url, supabase_key)
        if memoire_stock is None:
            print("[scan_boutique] Supabase injoignable : mémoire stock illisible, "
                  "cycle ABANDONNÉ (évite de rejouer une alerte pour chaque produit déjà en stock).")
            sys.exit(1)
    else:
        memoire_stock = charger_memoire()  # repli fichier local : data/stock_boutiques_tcg.json

    resume = scanner_plusieurs_boutiques(boutiques, cartes, memoire_stock, cotes, regles)

    # SaaS (saas/) : fait correspondre les deals boutiques deja valides
    # ci-dessus aux watchlists personnalisees des utilisateurs, enregistre
    # les alertes et notifie (push/email) -- meme pipeline que main.py pour
    # eBay/Vinted. Entierement additif et non-bloquant.
    secrets_saas = {
        "SUPABASE_URL": os.environ.get("SUPABASE_URL", ""),
        "SUPABASE_SERVICE_ROLE_KEY": os.environ.get("SUPABASE_SERVICE_ROLE_KEY", ""),
        "VAPID_PRIVATE_KEY": os.environ.get("VAPID_PRIVATE_KEY", ""),
        "VAPID_CLAIM_EMAIL": os.environ.get("VAPID_CLAIM_EMAIL", ""),
        "RESEND_API_KEY": os.environ.get("RESEND_API_KEY", ""),
        "RESEND_FROM_EMAIL": os.environ.get("RESEND_FROM_EMAIL", ""),
    }
    notifier_deals_boutique_saas(secrets_saas, resume["deals"])

    # Envoi Telegram REEL (une fois le cycle complet termine, meme pattern
    # que main.py qui envoie une fois tous les deals collectes). Chaque
    # fonction gere son propre canal/format et ne fait rien si la liste est vide.
    envoyer_telegram_bonnes_affaires(resume["deals"], TELEGRAM_CHAT_ID, token, cle_anthropic)
    # V57 (18/08/2026, audit externe) : sauvegarde APRES la tentative
    # d'envoi -- envoyer_telegram_retours_stock() commite desormais l'etat
    # "retour en stock" dans memoire_stock elle-meme, uniquement pour les
    # evenements effectivement envoyes avec succes. Sauvegarder avant
    # aurait fige la transition en memoire meme pour un envoi qui echoue,
    # la rendant indetectable au cycle suivant (perte definitive).
    envoyer_telegram_retours_stock(resume["evenements_stock"], TELEGRAM_CHAT_ID, token, memoire_stock)

    if memoire_via_supabase:
        if not sauvegarder_memoire_supabase(memoire_stock, CLE_MEMOIRE_STOCK, supabase_url, supabase_key):
            print("[scan_boutique] ATTENTION : échec de sauvegarde de la mémoire stock sur Supabase "
                  "-- l'état de ce cycle est perdu, les transitions détectées ce cycle-ci pourront se rejouer au prochain.")
    else:
        sauvegarder_memoire(memoire_stock)

    print(f"\n{'=' * 70}")
    print("RESUME DU CYCLE")
    print("=" * 70)
    print(f"Boutiques OK      : {len(resume['boutiques_ok'])}/{len(boutiques)}")
    print(f"Boutiques en echec: {len(resume['boutiques_echec'])}/{len(boutiques)}")
    for e in resume["boutiques_echec"]:
        print(f"  - {e['domaine']} : {e['raison']}")
    print(f"Bonnes affaires detectees : {len(resume['deals'])}")
    for d in resume["deals"]:
        print(f"  🔥 {d['nom']} — {d['boutique']} — {d['prix']:.2f}€ (cote {d['cote']:.2f}€, -{d['decote_pct']}%)")
    print(f"Retours en stock detectes : {len(resume['evenements_stock'])}")
    for ev in resume["evenements_stock"]:
        print(f"  📦 {ev['nom']} — {ev['boutique']} — {ev['prix']:.2f}€")
    print(f"Duree totale du cycle : {resume['duree_secondes']:.1f}s ({resume['duree_secondes'] / 60:.1f} min)")
