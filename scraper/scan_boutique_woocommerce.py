"""
Orchestrateur WooCommerce -- meme structure que scan_boutique.py (Shopify)
et scan_boutique_prestashop.py : un seul appel sitemap + un seul passage de
matching par boutique, dont le resultat alimente les DEUX logiques d'alerte
independantes deja generiques (bonne_affaire_shopify.py / alerte_stock.py).

Meme resilience : delai de politesse entre boutiques, une boutique en echec
est loguee et sautee (ne bloque pas les suivantes).

Fichier de memoire SEPARE des deux autres plateformes -- chacune a son
propre fichier, pas de collision possible meme en cas d'execution parallele.
"""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alerte_stock import charger_memoire, detecter_retours_en_stock, envoyer_telegram_retours_stock, sauvegarder_memoire
from bonne_affaire_shopify import charger_cotes, charger_regles, detecter_bonnes_affaires, envoyer_telegram_bonnes_affaires
from connecteur_woocommerce import ConnecteurWooCommerce
from watchlist_shopify import CarteWatchlist

DELAI_ENTRE_BOUTIQUES = 2.5  # secondes -- meme politesse que les 2 autres scans

TELEGRAM_CHAT_ID = "1245330032"

FICHIER_MEMOIRE = Path(__file__).parent / "data" / "stock_boutiques_tcg_woocommerce.json"


def scanner_boutique_complet(
    domaine: str,
    cartes: list[CarteWatchlist],
    memoire_stock: dict,
    cotes: dict,
    regles: dict,
    repli_api_rest: bool = False,
) -> tuple[list[dict], list[dict]]:
    """Scanne UNE boutique WooCommerce et retourne
    (deals_bonne_affaire, evenements_retour_stock).

    `repli_api_rest=True` : boutique dont la recherche visible est pilotee
    par JS/AJAX (widget de theme), sans sitemap exploitable -- utilise
    l'API REST WooCommerce "Store API" (rechercher_via_api_rest) au lieu du
    sitemap XML. Meme structures de retour, aucune modification requise
    cote bonne_affaire_shopify.py / alerte_stock.py.

    Ne catch AUCUNE exception ici -- c'est la responsabilite de l'appelant
    (scanner_plusieurs_boutiques) de faire en sorte qu'un echec sur cette
    boutique ne bloque pas les suivantes.
    """
    cartes_par_critere = {carte.cle_recherche: carte for carte in cartes}
    criteres = list(cartes_par_critere.keys())

    connecteur = ConnecteurWooCommerce(domaine)
    if repli_api_rest:
        resultats_par_critere = connecteur.rechercher_via_api_rest(criteres)
    else:
        urls_produits = connecteur.recuperer_toutes_les_urls_produits()                    # 1 seul appel sitemap
        resultats_par_critere = connecteur.rechercher_dans_catalogue(urls_produits, criteres)  # 1 seul passage

    deals = detecter_bonnes_affaires(resultats_par_critere, cartes_par_critere, cotes, regles)
    evenements_stock = detecter_retours_en_stock(domaine, resultats_par_critere, cartes_par_critere, memoire_stock)

    return deals, evenements_stock


def scanner_plusieurs_boutiques(
    boutiques: list[str],
    cartes: list[CarteWatchlist],
    memoire_stock: dict,
    cotes: dict,
    regles: dict,
    boutiques_repli_api_rest: set[str] | None = None,
) -> dict:
    boutiques_repli_api_rest = boutiques_repli_api_rest or set()
    debut = time.monotonic()
    tous_les_deals: list[dict] = []
    tous_les_evenements: list[dict] = []
    boutiques_ok: list[str] = []
    boutiques_echec: list[dict] = []

    for i, domaine in enumerate(boutiques):
        try:
            repli_api_rest = domaine in boutiques_repli_api_rest
            deals, evenements = scanner_boutique_complet(domaine, cartes, memoire_stock, cotes, regles, repli_api_rest)
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
    from boutiques_decouvertes import BOUTIQUES_WOOCOMMERCE_AUTO
    from boutiques_woocommerce import BOUTIQUES_WOOCOMMERCE_REPLI_API_REST, BOUTIQUES_WOOCOMMERCE_SITEMAP
    from watchlist_shopify import charger_watchlist_config

    # Sans argument : boutiques curees a la main + boutiques ajoutees
    # automatiquement par decouverte_boutiques.py (radar AFNIC). En
    # production, la production passe LOT_A/LOT_B explicitement (cf.
    # scan_woocommerce.yml) -- BOUTIQUES_WOOCOMMERCE_AUTO y est scannee
    # via une etape dediee separee, pas via ce defaut.
    boutiques = (sys.argv[1:] if len(sys.argv) > 1
                 else BOUTIQUES_WOOCOMMERCE_SITEMAP + BOUTIQUES_WOOCOMMERCE_REPLI_API_REST + BOUTIQUES_WOOCOMMERCE_AUTO)
    boutiques_repli_api_rest = set(boutiques) & set(BOUTIQUES_WOOCOMMERCE_REPLI_API_REST)

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    cle_anthropic = os.environ.get("ANTHROPIC_API_KEY", "")

    cartes = charger_watchlist_config()
    print(f"{len(cartes)} criteres de recherche charges depuis config.yaml (121 cartes, avec variantes alias)")
    print(f"{len(boutiques)} boutique(s) a scanner : {', '.join(boutiques)}")
    print(f"Telegram : {'configure' if token else 'NON configure (TELEGRAM_BOT_TOKEN absent -- envoi desactive)'}\n")

    cotes = charger_cotes()
    regles = charger_regles()

    memoire_stock = charger_memoire(FICHIER_MEMOIRE)

    resume = scanner_plusieurs_boutiques(boutiques, cartes, memoire_stock, cotes, regles, boutiques_repli_api_rest)

    envoyer_telegram_bonnes_affaires(resume["deals"], TELEGRAM_CHAT_ID, token, cle_anthropic)
    # V57 (18/08/2026, audit externe) : sauvegarde APRES la tentative
    # d'envoi -- cf. scan_boutique.py pour le detail complet.
    envoyer_telegram_retours_stock(resume["evenements_stock"], TELEGRAM_CHAT_ID, token, memoire_stock)

    sauvegarder_memoire(memoire_stock, FICHIER_MEMOIRE)

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
