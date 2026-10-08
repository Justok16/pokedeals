"""
Orchestrateur du radar de precommandes (cf. precommandes_watchlist.py /
alerte_precommande.py / radar_precommandes.py) -- fonctionnalite
INDEPENDANTE des 3 orchestrateurs existants (scan_boutique.py /
scan_boutique_prestashop.py / scan_boutique_woocommerce.py), qu'elle ne
modifie ni n'appelle. Concu pour tourner comme une ETAPE SUPPLEMENTAIRE au
sein des memes workflows GitHub Actions existants (meme cadence par
plateforme), sans creer de nouveau workflow separe.

Usage :
  python scan_precommandes.py shopify [boutique1 boutique2 ...]
  python scan_precommandes.py prestashop [boutique1 ...]
  python scan_precommandes.py woocommerce [boutique1 ...]
Sans boutique(s) en argument : scanne toutes les boutiques actives de la
plateforme donnee (sitemap + replis confondus).

S'arrete automatiquement de chercher un produit une fois sa date de sortie
passee (cf. precommandes_watchlist.produits_actifs) -- si TOUS les produits
surveilles sont perimes, le script se termine immediatement sans rien
scanner (radar desactive de lui-meme).
"""

import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alerte_precommande import (
    charger_memoire,
    detecter_nouvelles_precommandes,
    envoyer_telegram_precommandes,
    marquer_boutique_balayee,
    sauvegarder_memoire,
)
from memoire_supabase import charger_memoire_supabase, sauvegarder_memoire_supabase
from parallelisme import PARALLELISME_MAX, PARALLELISME_PAR_DEFAUT, lire_parallelisme
from notifications_perso import memoriser_si_telegram_perso_coupe, token_telegram_perso
from precommandes_watchlist import produits_actifs

# cf. scan_boutique.py pour le detail de ce correctif (31/08/2026) : sans
# ceci, les log.info()/log.warning() (ex. memoire_supabase.py) restaient
# invisibles dans les logs GitHub Actions.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
from radar_precommandes import (
    scanner_auchan,
    scanner_leclerc,
    scanner_prestashop_repli_html,
    scanner_prestashop_sitemap,
    scanner_shopify,
    scanner_woocommerce_api_rest,
    scanner_woocommerce_repli_html,
    scanner_woocommerce_sitemap,
)

DELAI_ENTRE_BOUTIQUES = 2.5
TELEGRAM_CHAT_ID = "1245330032"

# Un fichier memoire PAR PLATEFORME (meme principe que
# stock_boutiques_tcg{,_prestashop,_woocommerce}.json pour alerte_stock.py) :
# les 3 workflows GitHub Actions tournent en PARALLELE toutes les 30 min --
# un fichier unique partage entre les 3 risquerait un vrai conflit de
# contenu JSON (pas juste un conflit git resolu par rebase) si deux
# workflows le modifient au meme moment.
FICHIER_MEMOIRE_PAR_PLATEFORME = {
    "shopify": Path(__file__).parent / "data" / "precommandes_anniversaire_shopify.json",
    "prestashop": Path(__file__).parent / "data" / "precommandes_anniversaire_prestashop.json",
    "woocommerce": Path(__file__).parent / "data" / "precommandes_anniversaire_woocommerce.json",
    "leclerc": Path(__file__).parent / "data" / "precommandes_anniversaire_leclerc.json",
    "auchan": Path(__file__).parent / "data" / "precommandes_anniversaire_auchan.json",
}
# Cles Supabase equivalentes (cf. memoire_supabase.py) -- migration du
# 25/08/2026, meme principe que stock_boutiques_tcg* pour alerte_stock.py.
CLE_MEMOIRE_PAR_PLATEFORME = {
    "shopify": "precommandes_anniversaire_shopify",
    "prestashop": "precommandes_anniversaire_prestashop",
    "woocommerce": "precommandes_anniversaire_woocommerce",
    "leclerc": "precommandes_anniversaire_leclerc",
    "auchan": "precommandes_anniversaire_auchan",
}


# Perimetre COMPLEMENT (04/10/2026) : boutiques de boutiques_complement.py,
# scannees par leur propre workflow avec leur propre memoire (suffixe
# ci-dessous) -- jamais en meme temps que le perimetre principal, dont la
# memoire Supabase est partagee par plateforme (risque d'ecrasement mutuel
# si deux workflows ecrivaient la meme cle).
SUFFIXE_MEMOIRE_COMPLEMENT = "_complement"


def _boutiques_et_replis_complement(plateforme: str) -> tuple[list[str], dict[str, str]]:
    # Annuaire verifie (boutiques_complement.py) + certificats HTTPS
    # (boutiques_complement_ct.py), dedoublonnes en gardant l'ordre.
    import boutiques_complement as bc
    import boutiques_complement_ct as ct

    def union(*listes):
        return list(dict.fromkeys(d for liste in listes for d in liste))

    if plateforme == "shopify":
        return union(bc.BOUTIQUES_COMPLEMENT_SHOPIFY, ct.BOUTIQUES_COMPLEMENT_CT_SHOPIFY), {}
    if plateforme == "prestashop":
        repli = union(bc.BOUTIQUES_COMPLEMENT_PRESTASHOP_REPLI_HTML, ct.BOUTIQUES_COMPLEMENT_CT_PRESTASHOP_REPLI_HTML)
        sitemap = union(bc.BOUTIQUES_COMPLEMENT_PRESTASHOP_SITEMAP, ct.BOUTIQUES_COMPLEMENT_CT_PRESTASHOP_SITEMAP)
        return union(sitemap, repli), {d: "html" for d in repli}
    if plateforme == "woocommerce":
        return union(bc.BOUTIQUES_COMPLEMENT_WOOCOMMERCE_SITEMAP, ct.BOUTIQUES_COMPLEMENT_CT_WOOCOMMERCE_SITEMAP), {}
    if plateforme == "leclerc":
        return ["e.leclerc"], {}
    if plateforme == "auchan":
        return ["auchan.fr"], {}
    raise ValueError(f"Plateforme inconnue : {plateforme!r} (attendu: shopify/prestashop/woocommerce)")


def _boutiques_et_replis(plateforme: str, complement: bool = False) -> tuple[list[str], dict[str, str]]:
    """Retourne (liste des boutiques actives, {domaine: mode_repli}) pour
    la plateforme donnee -- mode_repli vaut "html", "api_rest", ou absent
    du dict pour les boutiques en sitemap standard."""
    if complement:
        return _boutiques_et_replis_complement(plateforme)
    if plateforme == "leclerc":   # 08/10/2026 : une seule "boutique", cf. connecteur_leclerc.py
        return ["e.leclerc"], {}
    if plateforme == "auchan":    # 08/10/2026 : idem, cf. connecteur_auchan.py
        return ["auchan.fr"], {}
    if plateforme == "shopify":
        from boutiques_decouvertes import BOUTIQUES_SHOPIFY_AUTO, BOUTIQUES_SHOPIFY_AUTO_PRECOMMANDE_SEULEMENT
        from boutiques_shopify import BOUTIQUES_SHOPIFY, BOUTIQUES_SHOPIFY_PRECOMMANDE_SEULEMENT
        # BOUTIQUES_SHOPIFY_PRECOMMANDE_SEULEMENT : boutiques 100% scelle,
        # exclues du scan cartes mais pertinentes ici (cf. boutiques_shopify.py).
        # BOUTIQUES_SHOPIFY_AUTO* : trouvees par decouverte_boutiques.py.
        return (list(BOUTIQUES_SHOPIFY) + list(BOUTIQUES_SHOPIFY_PRECOMMANDE_SEULEMENT)
                + list(BOUTIQUES_SHOPIFY_AUTO) + list(BOUTIQUES_SHOPIFY_AUTO_PRECOMMANDE_SEULEMENT)), {}

    if plateforme == "prestashop":
        from boutiques_prestashop import BOUTIQUES_PRESTASHOP_REPLI_HTML, BOUTIQUES_PRESTASHOP_SITEMAP
        boutiques = list(BOUTIQUES_PRESTASHOP_SITEMAP) + list(BOUTIQUES_PRESTASHOP_REPLI_HTML)
        modes = {d: "html" for d in BOUTIQUES_PRESTASHOP_REPLI_HTML}
        return boutiques, modes

    if plateforme == "woocommerce":
        from boutiques_decouvertes import BOUTIQUES_WOOCOMMERCE_AUTO, BOUTIQUES_WOOCOMMERCE_AUTO_PRECOMMANDE_SEULEMENT
        from boutiques_woocommerce import (
            BOUTIQUES_WOOCOMMERCE_PRECOMMANDE_SEULEMENT,
            BOUTIQUES_WOOCOMMERCE_REPLI_API_REST,
            BOUTIQUES_WOOCOMMERCE_SITEMAP,
        )
        boutiques = (list(BOUTIQUES_WOOCOMMERCE_SITEMAP) + list(BOUTIQUES_WOOCOMMERCE_REPLI_API_REST)
                     + list(BOUTIQUES_WOOCOMMERCE_PRECOMMANDE_SEULEMENT)
                     + list(BOUTIQUES_WOOCOMMERCE_AUTO) + list(BOUTIQUES_WOOCOMMERCE_AUTO_PRECOMMANDE_SEULEMENT))
        modes = {d: "api_rest" for d in BOUTIQUES_WOOCOMMERCE_REPLI_API_REST}
        return boutiques, modes

    raise ValueError(f"Plateforme inconnue : {plateforme!r} (attendu: shopify/prestashop/woocommerce)")


def scanner_une_boutique(plateforme: str, domaine: str, mode_repli: str | None, produits: list) -> list[dict]:
    if plateforme == "shopify":
        return scanner_shopify(domaine, produits)
    if plateforme == "prestashop":
        if mode_repli == "html":
            return scanner_prestashop_repli_html(domaine, produits)
        return scanner_prestashop_sitemap(domaine, produits)
    if plateforme == "woocommerce":
        if mode_repli == "api_rest":
            return scanner_woocommerce_api_rest(domaine, produits)
        if mode_repli == "html":
            return scanner_woocommerce_repli_html(domaine, produits)
        return scanner_woocommerce_sitemap(domaine, produits)
    if plateforme == "leclerc":
        return scanner_leclerc(domaine, produits)
    if plateforme == "auchan":
        return scanner_auchan(domaine, produits)
    raise ValueError(plateforme)


# Lecture des catalogues EN PARALLELE (06/10/2026). Un cycle Shopify lisait ses
# 54 boutiques l'une apres l'autre (~8 min) ; pour un restock qui s'epuise en
# quelques minutes, c'est trop lent. La lecture est du pur reseau : chaque
# boutique a son propre connecteur et sa propre session, et aucune ecriture en
# memoire n'a lieu pendant la lecture. Le traitement (detection des alertes,
# memoire, marqueurs de balayage) reste SEQUENTIEL et dans l'ordre d'origine
# (resultat identique a l'ancien comportement). Une meme boutique n'est jamais
# interrogee deux fois en meme temps ; seules des boutiques differentes se
# chevauchent. RADAR_PARALLELISME=1 retablit le comportement sequentiel.
def _parallelisme() -> int:
    return lire_parallelisme("RADAR_PARALLELISME", PARALLELISME_PAR_DEFAUT, PARALLELISME_MAX)


def _lire_catalogues(plateforme: str, boutiques: list[str], modes: dict[str, str], produits: list,
                     parallelisme: int) -> list[tuple[list[dict] | None, Exception | None]]:
    """Resultats alignes sur `boutiques` : (candidats, None) ou (None, exception).
    Reseau uniquement : ne touche a aucune memoire."""
    def une(domaine: str):
        try:
            return scanner_une_boutique(plateforme, domaine, modes.get(domaine), produits), None
        except Exception as e:  # noqa: BLE001 -- une boutique en echec ne doit jamais arreter le cycle
            return None, e

    if parallelisme <= 1:
        resultats = []
        for i, domaine in enumerate(boutiques):
            resultats.append(une(domaine))
            if i < len(boutiques) - 1:
                time.sleep(DELAI_ENTRE_BOUTIQUES)
        return resultats
    with ThreadPoolExecutor(max_workers=parallelisme) as pool:
        return list(pool.map(une, boutiques))


def scanner_plusieurs_boutiques(plateforme: str, boutiques: list[str], modes: dict[str, str], produits: list, memoire: dict) -> dict:
    debut = time.monotonic()
    tous_les_evenements: list[dict] = []
    boutiques_ok: list[str] = []
    boutiques_echec: list[dict] = []

    lectures = _lire_catalogues(plateforme, boutiques, modes, produits, _parallelisme())

    for i, (domaine, (candidats, erreur)) in enumerate(zip(boutiques, lectures)):
        try:
            if erreur is not None:
                raise erreur
            evenements = detecter_nouvelles_precommandes(domaine, candidats, memoire)
            tous_les_evenements.extend(evenements)
            marquer_boutique_balayee(
                domaine, [p.nom for p in produits if p.alerte_disponibilite], memoire,
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
            )
            boutiques_ok.append(domaine)
            print(f"[{i + 1}/{len(boutiques)}] {domaine} : OK — {len(candidats)} candidat(s), {len(evenements)} nouvelle(s) alerte(s)")
        except Exception as e:  # noqa: BLE001 -- une boutique en echec ne doit jamais arreter le cycle
            raison = f"{type(e).__name__}: {e}"
            boutiques_echec.append({"domaine": domaine, "raison": raison})
            print(f"[{i + 1}/{len(boutiques)}] {domaine} : ECHEC — {raison}")

    duree = time.monotonic() - debut
    return {
        "evenements": tous_les_evenements,
        "boutiques_ok": boutiques_ok,
        "boutiques_echec": boutiques_echec,
        "duree_secondes": duree,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("shopify", "prestashop", "woocommerce", "leclerc", "auchan"):
        print("Usage : python scan_precommandes.py {shopify|prestashop|woocommerce|leclerc|auchan} [boutique1 boutique2 ...]")
        sys.exit(1)

    plateforme = sys.argv[1]
    complement = os.environ.get("RADAR_PERIMETRE", "") == "complement"
    boutiques_defaut, modes = _boutiques_et_replis(plateforme, complement)
    boutiques = sys.argv[2:] if len(sys.argv) > 2 else boutiques_defaut

    produits = produits_actifs()
    if not produits:
        print("Aucun produit surveille actif (toutes les dates de sortie sont passees) -- rien a scanner.")
        sys.exit(0)

    # 19/09/2026 : token vide (no-op silencieux en aval) si Justok a coupe
    # ses notifications perso -- cf. notifications_perso.py.
    token = token_telegram_perso()

    print(f"{len(produits)} produit(s) surveille(s) actif(s) :")
    for p in produits:
        sortie = p.date_sortie.isoformat() if p.date_sortie else "date inconnue/reportee"
        print(f"  - {p.nom} (sortie {sortie})")
    print(f"{len(boutiques)} boutique(s) {plateforme} a scanner" + (" (perimetre COMPLEMENT)" if complement else ""))
    # 08/10/2026 : l'ancien libelle ("NON configure ... envoi desactive")
    # laissait croire que les alertes des 30 ans etaient coupees, alors
    # qu'elles partent avec TELEGRAM_BOT_TOKEN directement (cf. plus bas).
    token_direct = bool(os.environ.get("TELEGRAM_BOT_TOKEN"))
    print(f"Telegram (alertes perso) : {'actif' if token else 'coupe (config.yaml) ou token absent'}")
    print(f"Telegram (disponibilite produits suivis) : "
          f"{'actif' if token_direct else 'INACTIF -- TELEGRAM_BOT_TOKEN absent'}\n")

    supabase_url = os.environ.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    memoire_via_supabase = bool(supabase_url and supabase_key)
    cle_memoire = CLE_MEMOIRE_PAR_PLATEFORME[plateforme] + (SUFFIXE_MEMOIRE_COMPLEMENT if complement else "")
    fichier_memoire = FICHIER_MEMOIRE_PAR_PLATEFORME[plateforme]
    if complement:
        fichier_memoire = fichier_memoire.with_name(fichier_memoire.stem + SUFFIXE_MEMOIRE_COMPLEMENT + ".json")
    if memoire_via_supabase:
        memoire = charger_memoire_supabase(cle_memoire, supabase_url, supabase_key)
        if memoire is None:
            print("[scan_precommandes] Supabase injoignable : mémoire illisible, "
                  "cycle ABANDONNÉ (évite de rejouer une alerte pour chaque précommande déjà connue).")
            sys.exit(1)
    else:
        memoire = charger_memoire(fichier_memoire)

    resume = scanner_plusieurs_boutiques(plateforme, boutiques, modes, produits, memoire)
    # V57 (18/08/2026, audit externe) : sauvegarde APRES la tentative
    # d'envoi Telegram (pas avant) -- envoyer_telegram_precommandes()
    # commite desormais l'etat des evenements alertes dans `memoire`
    # elle-meme, uniquement pour ceux effectivement envoyes avec succes.
    # Sauvegarder avant aurait fige "deja alerte" en memoire meme pour un
    # envoi qui echoue, perdant l'evenement definitivement (plus jamais
    # redetecte au cycle suivant).
    # 04/10/2026 (demande explicite de Justok : alertes Telegram pour le
    # suivi des produits des 30 ans) : les evenements des produits en suivi
    # de disponibilite partent MEME si notifications.telegram est coupe dans
    # config.yaml (19/09/2026) -- cet interrupteur reste actif pour tout le
    # reste (autres produits du radar, deals, stock, prix bas...). Pour
    # couper aussi ces alertes : retirer alerte_disponibilite=True des
    # produits concernes dans precommandes_watchlist.py.
    evenements_dispo = [e for e in resume["evenements"] if e.get("alerte_disponibilite")]
    autres_evenements = [e for e in resume["evenements"] if not e.get("alerte_disponibilite")]
    memoriser_si_telegram_perso_coupe(autres_evenements, memoire)
    envoyer_telegram_precommandes(autres_evenements, TELEGRAM_CHAT_ID, token, memoire)
    envoyer_telegram_precommandes(
        evenements_dispo, TELEGRAM_CHAT_ID, os.environ.get("TELEGRAM_BOT_TOKEN", ""), memoire)
    if memoire_via_supabase:
        if not sauvegarder_memoire_supabase(memoire, cle_memoire, supabase_url, supabase_key):
            print("[scan_precommandes] ATTENTION : échec de sauvegarde de la mémoire sur Supabase "
                  "-- l'état de ce cycle est perdu, les événements détectés ce cycle-ci pourront se rejouer au prochain.")
    else:
        sauvegarder_memoire(memoire, fichier_memoire)

    print(f"\n{'=' * 70}")
    print("RESUME DU CYCLE PRECOMMANDES")
    print("=" * 70)
    print(f"Boutiques OK      : {len(resume['boutiques_ok'])}/{len(boutiques)}")
    print(f"Boutiques en echec: {len(resume['boutiques_echec'])}/{len(boutiques)}")
    for e in resume["boutiques_echec"]:
        print(f"  - {e['domaine']} : {e['raison']}")
    print(f"Nouvelles alertes precommande : {len(resume['evenements'])}")
    for e in resume["evenements"]:
        niveau = "🟢 forte" if e["confiance"] == "forte" else "🟡 moyenne"
        print(f"  🎉 [{niveau}] {e['nom_produit']} — {e['domaine']} — {e['titre']}")
    print(f"Duree totale du cycle : {resume['duree_secondes']:.1f}s ({resume['duree_secondes'] / 60:.1f} min)")
