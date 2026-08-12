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

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alerte_precommande import (
    charger_memoire,
    detecter_nouvelles_precommandes,
    envoyer_telegram_precommandes,
    sauvegarder_memoire,
)
from precommandes_watchlist import produits_actifs
from radar_precommandes import (
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
}


def _boutiques_et_replis(plateforme: str) -> tuple[list[str], dict[str, str]]:
    """Retourne (liste des boutiques actives, {domaine: mode_repli}) pour
    la plateforme donnee -- mode_repli vaut "html", "api_rest", ou absent
    du dict pour les boutiques en sitemap standard."""
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
    raise ValueError(plateforme)


def scanner_plusieurs_boutiques(plateforme: str, boutiques: list[str], modes: dict[str, str], produits: list, memoire: dict) -> dict:
    debut = time.monotonic()
    tous_les_evenements: list[dict] = []
    boutiques_ok: list[str] = []
    boutiques_echec: list[dict] = []

    for i, domaine in enumerate(boutiques):
        try:
            candidats = scanner_une_boutique(plateforme, domaine, modes.get(domaine), produits)
            evenements = detecter_nouvelles_precommandes(domaine, candidats, memoire)
            tous_les_evenements.extend(evenements)
            boutiques_ok.append(domaine)
            print(f"[{i + 1}/{len(boutiques)}] {domaine} : OK — {len(candidats)} candidat(s), {len(evenements)} nouvelle(s) alerte(s)")
        except Exception as e:  # noqa: BLE001 -- une boutique en echec ne doit jamais arreter le cycle
            raison = f"{type(e).__name__}: {e}"
            boutiques_echec.append({"domaine": domaine, "raison": raison})
            print(f"[{i + 1}/{len(boutiques)}] {domaine} : ECHEC — {raison}")

        if i < len(boutiques) - 1:
            time.sleep(DELAI_ENTRE_BOUTIQUES)

    duree = time.monotonic() - debut
    return {
        "evenements": tous_les_evenements,
        "boutiques_ok": boutiques_ok,
        "boutiques_echec": boutiques_echec,
        "duree_secondes": duree,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("shopify", "prestashop", "woocommerce"):
        print("Usage : python scan_precommandes.py {shopify|prestashop|woocommerce} [boutique1 boutique2 ...]")
        sys.exit(1)

    plateforme = sys.argv[1]
    boutiques_defaut, modes = _boutiques_et_replis(plateforme)
    boutiques = sys.argv[2:] if len(sys.argv) > 2 else boutiques_defaut

    produits = produits_actifs()
    if not produits:
        print("Aucun produit surveille actif (toutes les dates de sortie sont passees) -- rien a scanner.")
        sys.exit(0)

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")

    print(f"{len(produits)} produit(s) surveille(s) actif(s) :")
    for p in produits:
        print(f"  - {p.nom} (sortie {p.date_sortie.isoformat()})")
    print(f"{len(boutiques)} boutique(s) {plateforme} a scanner")
    print(f"Telegram : {'configure' if token else 'NON configure (TELEGRAM_BOT_TOKEN absent -- envoi desactive)'}\n")

    fichier_memoire = FICHIER_MEMOIRE_PAR_PLATEFORME[plateforme]
    memoire = charger_memoire(fichier_memoire)
    resume = scanner_plusieurs_boutiques(plateforme, boutiques, modes, produits, memoire)
    sauvegarder_memoire(memoire, fichier_memoire)

    envoyer_telegram_precommandes(resume["evenements"], TELEGRAM_CHAT_ID, token)

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
