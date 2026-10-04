"""
Decouverte AUTOMATIQUE de boutiques a partir d'un annuaire de boutiques
VERIFIEES A LA MAIN (Pokescam : SIRET actif, mentions legales, adresse,
avis independants) -- seconde source de decouverte, complementaire de
decouverte_boutiques.py (qui ne voit que les nouveaux domaines .fr via
l'AFNIC).

Pipeline hebdomadaire (cf. decouverte_annuaires.yml) :
  1. Telecharger l'annuaire des boutiques verifiees et les listes
     d'arnaques (Pokescam + PokeGourou, cf. legitimite.py).
  2. Pour chaque boutique de l'annuaire pas encore scannee :
       - sur liste noire d'arnaques   -> conflit, JAMAIS ajoutee, signalee ;
       - HTTPS invalide / injoignable -> ignoree ce cycle ;
       - plateforme reconnue (Shopify / WooCommerce / PrestaShop) ->
         ajoutee a boutiques_complement.py ;
       - sinon (plateforme maison, JavaScript, anti-robot) -> rangee dans
         A_CONNECTEUR_DEDIE (informatif).
  3. Retirer de boutiques_complement.py toute boutique devenue arnaque
     signalee ou sortie de l'annuaire (l'annuaire retire les sites qui ne
     respectent plus ses criteres).
  4. Reecrire boutiques_complement.py (atomique) + rapport Telegram si
     changement.

Garde-fous : si l'annuaire ou les listes d'arnaques sont indisponibles /
suspectement petites, AUCUNE modification (jamais d'ajout a l'aveugle ni de
retrait massif sur une erreur reseau).
"""

import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from connecteur_shopify import HEADERS, HEADERS_HTML, TIMEOUT
from legitimite import charger_liste_noire, normaliser_domaine, verifier_legitimite
from notifications_perso import token_telegram_perso
from telegram_utils import echapper_html

sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)

URL_ANNUAIRE_POKESCAM = "https://pokescam.com/sites-fiables/"
FICHIER_COMPLEMENT = Path(__file__).parent / "boutiques_complement.py"
SEUIL_MIN_ANNUAIRE = 30       # en dessous : page cassee / format change -> on ne touche a rien
SEUIL_MIN_LISTE_NOIRE = 50    # idem pour les listes d'arnaques
DELAI_ENTRE_BOUTIQUES = 1.0

# Domaines a ne JAMAIS (re)ajouter, meme s'ils sont dans l'annuaire --
# decision humaine, meme principe que DOMAINES_REJETES_MANUELLEMENT dans
# decouverte_boutiques.py.
DOMAINES_REFUSES: set[str] = set()

# Grandes enseignes / places de marche deja couvertes par un connecteur
# dedie ou hors perimetre (ex: philibertnet.com -> connecteur_philibert.py).
DOMAINES_DEJA_COUVERTS_AUTREMENT = {"philibertnet.com"}

_RE_BOUTIQUE_ANNUAIRE = re.compile(r"Visiter\s+([a-z0-9][a-z0-9.\-]*\.[a-z]{2,})", re.IGNORECASE)

CLES_LISTES = (
    "shopify", "prestashop_sitemap", "prestashop_repli_html", "woocommerce_sitemap", "a_connecteur_dedie",
)
NOMS_VARIABLES = {
    "shopify": "BOUTIQUES_COMPLEMENT_SHOPIFY",
    "prestashop_sitemap": "BOUTIQUES_COMPLEMENT_PRESTASHOP_SITEMAP",
    "prestashop_repli_html": "BOUTIQUES_COMPLEMENT_PRESTASHOP_REPLI_HTML",
    "woocommerce_sitemap": "BOUTIQUES_COMPLEMENT_WOOCOMMERCE_SITEMAP",
    "a_connecteur_dedie": "BOUTIQUES_COMPLEMENT_A_CONNECTEUR_DEDIE",
}


def extraire_boutiques_annuaire(html: str) -> set[str]:
    return {normaliser_domaine(m) for m in _RE_BOUTIQUE_ANNUAIRE.findall(html)}


def classer_plateforme(domaine: str, session=None) -> str | None:
    """Plateforme exploitable par un connecteur existant, ou None."""
    s = session or requests
    base = f"https://{domaine}"
    try:
        r = s.get(f"{base}/products.json?limit=5", headers=HEADERS, timeout=TIMEOUT)
        if r.status_code == 200 and isinstance(r.json().get("products"), list):
            return "shopify"
    except (requests.exceptions.RequestException, ValueError):
        pass
    try:
        r = s.get(f"{base}/product-sitemap.xml", headers=HEADERS_HTML, timeout=TIMEOUT)
        if r.status_code == 200 and "<loc>" in r.text:
            return "woocommerce_sitemap"
    except requests.exceptions.RequestException:
        pass
    try:
        from connecteur_prestashop_sitemap import ConnecteurPrestaShopSitemap
        if ConnecteurPrestaShopSitemap(domaine).recuperer_toutes_les_urls_produits():
            return "prestashop_sitemap"
        accueil = s.get(f"{base}/", headers=HEADERS_HTML, timeout=TIMEOUT)
        if accueil.status_code == 200 and "prestashop" in accueil.text[:200000].lower():
            return "prestashop_repli_html"
    except requests.exceptions.RequestException:
        pass
    return None


def charger_listes_complement() -> dict[str, list[str]]:
    vide = {cle: [] for cle in CLES_LISTES}
    if not FICHIER_COMPLEMENT.exists():
        return vide
    namespace: dict = {}
    exec(FICHIER_COMPLEMENT.read_text(encoding="utf-8"), namespace)  # noqa: S102 -- fichier interne auto-genere
    return {cle: list(namespace.get(nom, [])) for cle, nom in NOMS_VARIABLES.items()}


def ecrire_listes_complement(listes: dict[str, list[str]]) -> None:
    """Reecrit le fichier en entier (atomique : il est importe par
    scan_precommandes.py, un .py tronque casserait le prochain scan)."""
    jour = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    blocs = []
    for cle in CLES_LISTES:
        corps = "".join(f"    {d!r},\n" for d in sorted(set(listes[cle])))
        blocs.append(f"{NOMS_VARIABLES[cle]} = [\n{corps}]\n")
    entete = (
        '"""\nBoutiques COMPLEMENTAIRES du radar de precommandes/disponibilite (cf.\n'
        "scan_precommandes.py, mode RADAR_PERIMETRE=complement), scannees par leur\n"
        "propre workflow (scan_complement.yml).\n\n"
        "FICHIER AUTO-GENERE par decouverte_annuaires.py (annuaire Pokescam des\n"
        "boutiques verifiees a la main + controles de legitimite, cf. legitimite.py)\n"
        "-- ne pas editer a la main : il est reecrit a chaque execution. Pour retirer\n"
        "une boutique durablement, l'ajouter a DOMAINES_REFUSES dans\n"
        "decouverte_annuaires.py.\n\n"
        f"Derniere mise a jour : {jour}\n" '"""\n\n'
    )
    contenu = entete + "\n".join(blocs)
    tmp = FICHIER_COMPLEMENT.with_suffix(".py.tmp")
    tmp.write_text(contenu, encoding="utf-8")
    tmp.replace(FICHIER_COMPLEMENT)


def domaines_deja_scannes() -> set[str]:
    """Union de TOUTES les listes de boutiques du projet (principales,
    decouvertes, complement) -- une boutique deja scannee ailleurs n'est
    jamais ajoutee en double."""
    import boutiques_decouvertes as bd
    import boutiques_prestashop as bp
    import boutiques_shopify as bs
    import boutiques_woocommerce as bw
    connus: set[str] = set()
    try:
        import boutiques_complement_ct as ct  # boutiques trouvees par certificats : jamais en double
        modules_ct = (ct,)
    except ImportError:
        modules_ct = ()
    for module in (bs, bp, bw, bd) + modules_ct:
        for nom, valeur in vars(module).items():
            if nom.isupper() and isinstance(valeur, (list, tuple, set, dict)):
                for d in (valeur.keys() if isinstance(valeur, dict) else valeur):
                    if isinstance(d, str) and "." in d:
                        connus.add(normaliser_domaine(d))
    return connus


def calculer_changements(annuaire: set[str], liste_noire: set[str], listes: dict[str, list[str]],
                         connus_ailleurs: set[str], classer=classer_plateforme,
                         legitimite=verifier_legitimite, pause=DELAI_ENTRE_BOUTIQUES):
    """Retourne (listes_mises_a_jour, ajouts, retraits, conflits, ignores).
    Fonction pure (reseau injecte) pour pouvoir la tester."""
    listes = {cle: list(v) for cle, v in listes.items()}
    deja_dans_complement = {d for v in listes.values() for d in v}
    ajouts: list[tuple[str, str]] = []
    retraits: list[tuple[str, str]] = []
    conflits: list[str] = []
    ignores: list[tuple[str, str]] = []

    # 3. retraits : arnaque signalee, ou sortie de l'annuaire
    for cle in CLES_LISTES:
        for d in list(listes[cle]):
            if d in liste_noire:
                listes[cle].remove(d)
                retraits.append((d, "signalee comme arnaque"))
            elif d not in annuaire or d in DOMAINES_REFUSES:
                listes[cle].remove(d)
                retraits.append((d, "sortie de l'annuaire des boutiques verifiees"))

    # 2. ajouts
    candidats = sorted(
        d for d in annuaire
        if d not in deja_dans_complement and d not in connus_ailleurs
        and d not in DOMAINES_REFUSES and d not in DOMAINES_DEJA_COUVERTS_AUTREMENT
    )
    for i, d in enumerate(candidats):
        if d in liste_noire:
            conflits.append(d)
            continue
        rapport = legitimite(d)
        if not rapport["https_ok"]:
            ignores.append((d, rapport["raison"]))
            continue
        plateforme = classer(d) or "a_connecteur_dedie"
        listes[plateforme].append(d)
        ajouts.append((d, plateforme))
        if i < len(candidats) - 1:
            pause and time.sleep(pause)
    return listes, ajouts, retraits, conflits, ignores


def envoyer_rapport_telegram(ajouts, retraits, conflits, token: str, chat_id: str) -> None:
    if not token or not chat_id or not (ajouts or retraits or conflits):
        return
    lignes = ["\U0001f50e <b>Annuaire boutiques verifiees -- mise a jour</b>", ""]
    scannees = [(d, p) for d, p in ajouts if p != "a_connecteur_dedie"]
    dediees = [d for d, p in ajouts if p == "a_connecteur_dedie"]
    if scannees:
        lignes.append(f"<b>{len(scannees)} boutique(s) ajoutee(s) au radar :</b>")
        lignes += [f"✅ {echapper_html(d)} ({p})" for d, p in scannees]
    if dediees:
        lignes.append(f"ℹ️ {len(dediees)} verifiee(s), sans connecteur compatible : " + ", ".join(echapper_html(d) for d in dediees))
    if retraits:
        lignes.append("<b>Retirees du radar :</b>")
        lignes += [f"⛔ {echapper_html(d)} ({echapper_html(r)})" for d, r in retraits]
    if conflits:
        lignes.append("⚠️ Dans l'annuaire ET signalees comme arnaque (non ajoutees) : " + ", ".join(echapper_html(d) for d in conflits))
    try:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": "\n".join(lignes), "parse_mode": "HTML"}, timeout=TIMEOUT,
        )
    except requests.exceptions.RequestException as e:
        print(f"[telegram] echec envoi rapport annuaires : {e}", file=sys.stderr)


def main() -> int:
    try:
        r = requests.get(URL_ANNUAIRE_POKESCAM, headers=HEADERS_HTML, timeout=TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Annuaire indisponible ({e}) -- aucune modification.")
        return 0
    annuaire = extraire_boutiques_annuaire(r.text)
    if len(annuaire) < SEUIL_MIN_ANNUAIRE:
        print(f"Annuaire suspect ({len(annuaire)} boutiques < {SEUIL_MIN_ANNUAIRE}) -- aucune modification.")
        return 0
    liste_noire = charger_liste_noire()
    if len(liste_noire) < SEUIL_MIN_LISTE_NOIRE:
        print(f"Listes d'arnaques indisponibles ({len(liste_noire)} < {SEUIL_MIN_LISTE_NOIRE}) -- aucune modification.")
        return 0
    print(f"{len(annuaire)} boutiques verifiees dans l'annuaire, {len(liste_noire)} arnaques connues.")

    listes = charger_listes_complement()
    nouvelles, ajouts, retraits, conflits, ignores = calculer_changements(
        annuaire, liste_noire, listes, domaines_deja_scannes())
    for d, p in ajouts:
        print(f"+ {d} ({p})")
    for d, raison in retraits:
        print(f"- {d} ({raison})")
    for d in conflits:
        print(f"! {d} : dans l'annuaire ET sur une liste d'arnaques -- non ajoutee")
    for d, raison in ignores:
        print(f"~ {d} ignoree ce cycle : {raison}")

    if ajouts or retraits:
        ecrire_listes_complement(nouvelles)
    envoyer_rapport_telegram(ajouts, retraits, conflits, token_telegram_perso().strip(),
                             os.environ.get("TELEGRAM_CHAT_ID", "1245330032").strip())
    print(f"\nTermine : {len(ajouts)} ajout(s), {len(retraits)} retrait(s), {len(conflits)} conflit(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
