"""
Decouverte de boutiques de TOUTES extensions (.com, .net, .shop, .fr...) par
les journaux de transparence des certificats HTTPS (crt.sh) -- troisieme
source de decouverte, comble la limite de decouverte_boutiques.py (AFNIC :
uniquement les nouveaux .fr) et de decouverte_annuaires.py (uniquement les
boutiques deja referencees par un annuaire).

Tout site HTTPS a un certificat public : chercher les noms de domaine
contenant "pokemon", "pikachu"... revele des boutiques existantes comme
nouvelles, quelle que soit l'extension.

SOURCE NON VERIFIEE -> garde-fous STRICTS (cf. legitimite.py), tous requis :
  1. domaine absent des listes d'arnaques (Pokescam + PokeGourou) ;
  2. anciennete : premier certificat vu il y a >= 60 jours (un faux site
     fraichement cree est ecarte, re-evalue chaque semaine) ;
  3. produits FRANCAIS : .fr/.be/.ch/.lu, page d'accueil en francais, ou >= 3 produits
     du catalogue en francais (un site etranger vendant du francais est accepte) ;
  4. plateforme exploitable (Shopify/WooCommerce/PrestaShop) ET catalogue
     Pokemon net (memes seuils que decouverte_boutiques.verifier_candidat) ;
  5. HTTPS valide + mentions legales avec SIRET/SIREN.
Sinon : rien n'est ajoute (les cas limites sont juste rapportes).

crt.sh est un service communautaire souvent instable (502/404) : quelques
tentatives espacees par mot-cle, puis on passe -- une panne ne casse jamais
le cycle et ne retire jamais rien.
"""

import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from connecteur_shopify import HEADERS_HTML, TIMEOUT
from decouverte_annuaires import classer_plateforme, domaines_deja_scannes
from decouverte_boutiques import verifier_candidat
from legitimite import charger_liste_noire, est_legitime, normaliser_domaine, verifier_legitimite
from memoire_supabase import charger_memoire_supabase, sauvegarder_memoire_supabase
from notifications_perso import token_telegram_perso
from telegram_utils import echapper_html

sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)

FICHIER_CT = Path(__file__).parent / "boutiques_complement_ct.py"
CLE_MEMOIRE = "decouverte_certificats_memoire"
# crt.sh plafonne chaque reponse a ~1000 certificats : un mot trop courant
# ("pokemon") ne ramene qu'un echantillon, surtout des sites officiels ou
# etrangers (mesure 04/10/2026 : 38 domaines distincts, aucun francophone).
# Les mots composes francais ciblent beaucoup mieux les boutiques.
MOTS_CLES_CT = [
    "cartepokemon", "cartespokemon", "pokemoncarte", "pokemoncartes", "boutiquepokemon",
    "pokemon-fr", "jcc-pokemon", "pokemon-tcg", "pokemontcg", "pokestore", "pokeshop",
    "displaypoke", "pokedisplay", "pokemon", "pikachu", "dracaufeu",
]
BUDGET_CRTSH_SECONDES = 480   # au-dela, on arrete d'interroger crt.sh (service instable)
AGE_MIN_JOURS = 60
RECONTROLE_REJETS_JOURS = 30
MAX_CANDIDATS_PAR_CYCLE = 80
SEUIL_MIN_LISTE_NOIRE = 50
DELAI_ENTRE_BOUTIQUES = 1.0
TENTATIVES_CRTSH = 4
PAUSE_ENTRE_TENTATIVES = 20

CLES_LISTES = ("shopify", "prestashop_sitemap", "prestashop_repli_html", "woocommerce_sitemap")
NOMS_VARIABLES = {
    "shopify": "BOUTIQUES_COMPLEMENT_CT_SHOPIFY",
    "prestashop_sitemap": "BOUTIQUES_COMPLEMENT_CT_PRESTASHOP_SITEMAP",
    "prestashop_repli_html": "BOUTIQUES_COMPLEMENT_CT_PRESTASHOP_REPLI_HTML",
    "woocommerce_sitemap": "BOUTIQUES_COMPLEMENT_CT_WOOCOMMERCE_SITEMAP",
}

# Domaines officiels / sans rapport avec une boutique.
DOMAINES_IGNORES = {"pokemon.com", "pokemon.fr", "pokemon.co.jp", "pokemoncenter.com", "pokemongo.com", "nintendo.com"}
_SECOND_NIVEAUX = {"co", "com", "org", "net", "gov", "ac"}


def domaine_enregistrable(nom: str) -> str | None:
    """`shop.exemple.co.uk` -> `exemple.co.uk` ; ignore adresses e-mail,
    IP et noms invalides."""
    nom = nom.strip().lower().lstrip("*.")
    if not nom or "@" in nom or " " in nom or not re.fullmatch(r"[a-z0-9.\-]+", nom):
        return None
    labels = nom.split(".")
    if len(labels) < 2 or labels[-1].isdigit():
        return None
    if len(labels) >= 3 and len(labels[-1]) == 2 and labels[-2] in _SECOND_NIVEAUX:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


def interroger_crtsh(mot: str, session=None, tentatives: int = TENTATIVES_CRTSH,
                     pause: float = PAUSE_ENTRE_TENTATIVES) -> list[dict] | None:
    """Entrees JSON crt.sh pour un mot-cle, ou None si le service reste
    indisponible apres `tentatives` essais."""
    s = session or requests
    for essai in range(tentatives):
        try:
            r = s.get("https://crt.sh/", params={"q": mot, "output": "json"}, headers=HEADERS_HTML, timeout=60)
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list):
                    return data
        except (requests.exceptions.RequestException, ValueError):
            pass
        if essai < tentatives - 1:
            time.sleep(pause)
    return None


def candidats_depuis_entrees(entrees: list[dict], mot: str) -> dict[str, datetime]:
    """{domaine enregistrable contenant `mot`: date du plus ancien certificat}."""
    premiers: dict[str, datetime] = {}
    for e in entrees:
        try:
            debut = datetime.fromisoformat(e["not_before"]).replace(tzinfo=timezone.utc)
        except (KeyError, ValueError, TypeError):
            continue
        for nom in str(e.get("name_value", "")).split("\n"):
            d = domaine_enregistrable(nom)
            if d and mot in d.split(".")[0] and d not in DOMAINES_IGNORES:
                if d not in premiers or debut < premiers[d]:
                    premiers[d] = debut
    return premiers


MARQUEURS_PRODUIT_FRANCAIS = ("francais", "français", "anniversaire", "coffret", "dresseur", "booster", "display")


def vend_des_produits_francais(domaine: str, session=None) -> bool:
    """Un site etranger (.com, .ch, .de...) est accepte s'il vend des
    produits en FRANCAIS : au moins 3 titres de son catalogue Shopify avec un
    marqueur francais (Justok, 04/10/2026 : "des produits francais sur des
    sites etrangers" -- le critere porte sur le PRODUIT, plus sur la
    nationalite du site). Catalogue non lisible -> repli sur la langue de la
    page d'accueil."""
    s = session or requests
    try:
        r = s.get(f"https://{domaine}/products.json?limit=250", headers=HEADERS_HTML, timeout=TIMEOUT)
        if r.status_code == 200:
            titres = [str(p.get("title", "")).lower() for p in r.json().get("products", [])]
            if sum(any(m in t for m in MARQUEURS_PRODUIT_FRANCAIS) for t in titres) >= 3:
                return True
    except (requests.exceptions.RequestException, ValueError, AttributeError):
        pass
    return False


def site_en_francais(domaine: str, session=None) -> bool:
    if domaine.endswith((".fr", ".be", ".ch", ".lu")):
        return True
    if vend_des_produits_francais(domaine, session):
        return True
    s = session or requests
    try:
        r = s.get(f"https://{domaine}/", headers=HEADERS_HTML, timeout=TIMEOUT)
    except requests.exceptions.RequestException:
        return False
    return r.status_code == 200 and bool(re.search(r"<html[^>]*\blang=[\"']fr", r.text[:5000], re.IGNORECASE))


def evaluer_candidat(domaine: str, premier_certificat: datetime, liste_noire: set[str], maintenant: datetime,
                     classer=classer_plateforme, verifier=verifier_candidat, legitimite=verifier_legitimite,
                     francais=site_en_francais) -> tuple[str, str | None, str]:
    """Retourne (verdict, plateforme, raison). verdict : "ajout", "rejet" ou
    "observation" (trop recent -- a reevaluer)."""
    if domaine in liste_noire:
        return "rejet", None, "signale comme arnaque"
    if maintenant - premier_certificat < timedelta(days=AGE_MIN_JOURS):
        return "observation", None, f"premier certificat il y a moins de {AGE_MIN_JOURS} jours"
    if not francais(domaine):
        return "rejet", None, "aucun produit en francais"
    plateforme = classer(domaine)
    if plateforme is None:
        return "rejet", None, "plateforme non supportee"
    rapport = verifier(domaine)
    if rapport.get("verdict") not in ("singles", "scelle"):
        return "rejet", plateforme, "catalogue Pokemon insuffisant"
    legit = legitimite(domaine)
    if not est_legitime(legit):
        return "rejet", plateforme, legit.get("raison") or "legitimite non prouvee"
    return "ajout", plateforme, "ok"


def charger_listes_ct() -> dict[str, list[str]]:
    vide = {cle: [] for cle in CLES_LISTES}
    if not FICHIER_CT.exists():
        return vide
    namespace: dict = {}
    exec(FICHIER_CT.read_text(encoding="utf-8"), namespace)  # noqa: S102 -- fichier interne auto-genere
    return {cle: list(namespace.get(nom, [])) for cle, nom in NOMS_VARIABLES.items()}


def ecrire_listes_ct(listes: dict[str, list[str]]) -> None:
    jour = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    blocs = [f"{NOMS_VARIABLES[cle]} = [\n" + "".join(f"    {d!r},\n" for d in sorted(set(listes[cle]))) + "]\n"
             for cle in CLES_LISTES]
    entete = (
        '"""\nBoutiques COMPLEMENTAIRES trouvees par les certificats HTTPS (crt.sh), scannees par\n'
        "scan_complement.yml au meme titre que boutiques_complement.py.\n\n"
        "FICHIER AUTO-GENERE par decouverte_certificats.py (garde-fous stricts : liste noire,\n"
        "anciennete, marche francais, catalogue Pokemon, HTTPS + SIRET/TVA) -- ne pas editer a la main.\n\n"
        f"Derniere mise a jour : {jour}\n" '"""\n\n'
    )
    tmp = FICHIER_CT.with_suffix(".py.tmp")
    tmp.write_text(entete + "\n".join(blocs), encoding="utf-8")
    tmp.replace(FICHIER_CT)


def envoyer_rapport_telegram(ajouts, retraits, observation, token: str, chat_id: str) -> None:
    if not token or not chat_id or not (ajouts or retraits):
        return
    lignes = ["\U0001f50e <b>Certificats HTTPS -- nouvelles boutiques</b>", ""]
    if ajouts:
        lignes.append(f"<b>{len(ajouts)} boutique(s) ajoutee(s) (liste noire, anciennete, SIRET controles) :</b>")
        lignes += [f"✅ {echapper_html(d)} ({p})" for d, p in ajouts]
    if retraits:
        lignes.append("<b>Retirees :</b>")
        lignes += [f"⛔ {echapper_html(d)} ({echapper_html(r)})" for d, r in retraits]
    if observation:
        lignes.append(f"👀 {len(observation)} domaine(s) trop recents, en observation.")
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      json={"chat_id": chat_id, "text": "\n".join(lignes), "parse_mode": "HTML"}, timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        print(f"[telegram] echec envoi rapport certificats : {e}", file=sys.stderr)


def main() -> int:
    supabase_url = os.environ.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not (supabase_url and supabase_key):
        print("Supabase non configure : memoire indisponible -- aucune modification.")
        return 0
    memoire = charger_memoire_supabase(CLE_MEMOIRE, supabase_url, supabase_key)
    if memoire is None:
        print("Supabase injoignable : cycle abandonne (evite de re-verifier des domaines deja jugés).")
        return 0
    verifies = memoire.setdefault("domaines_verifies", {})

    liste_noire = charger_liste_noire()
    if len(liste_noire) < SEUIL_MIN_LISTE_NOIRE:
        print(f"Listes d'arnaques indisponibles ({len(liste_noire)}) -- aucune modification.")
        return 0

    candidats: dict[str, datetime] = {}
    sources_ok = 0
    debut_crtsh = time.monotonic()
    for mot in MOTS_CLES_CT:
        if time.monotonic() - debut_crtsh > BUDGET_CRTSH_SECONDES:
            print("Budget de temps crt.sh atteint -- mots-cles restants ignores ce cycle.")
            break
        entrees = interroger_crtsh(mot)
        if entrees is None:
            print(f"crt.sh indisponible pour '{mot}' -- ignore.")
            continue
        sources_ok += 1
        for d, debut in candidats_depuis_entrees(entrees, mot).items():
            if d not in candidats or debut < candidats[d]:
                candidats[d] = debut
    print(f"{sources_ok}/{len(MOTS_CLES_CT)} mots-cles interroges, {len(candidats)} domaine(s) candidat(s).")

    maintenant = datetime.now(timezone.utc)
    listes = charger_listes_ct()
    connus = domaines_deja_scannes() | {d for v in listes.values() for d in v}
    try:
        from decouverte_annuaires import charger_listes_complement
        connus |= {d for v in charger_listes_complement().values() for d in v}
    except Exception:  # noqa: BLE001 -- liste optionnelle
        pass

    # Retraits : une boutique CT devenue arnaque signalee.
    retraits = []
    for cle in CLES_LISTES:
        for d in list(listes[cle]):
            if d in liste_noire:
                listes[cle].remove(d)
                retraits.append((d, "signalee comme arnaque"))

    a_verifier = []
    for d in sorted(candidats):
        if d in connus:
            continue
        precedent = verifies.get(d)
        if precedent and precedent.get("verdict") == "rejet":
            derniere = datetime.fromisoformat(precedent["date"])
            if maintenant - derniere < timedelta(days=RECONTROLE_REJETS_JOURS):
                continue
        a_verifier.append(d)
    a_verifier = a_verifier[:MAX_CANDIDATS_PAR_CYCLE]
    print(f"{len(a_verifier)} domaine(s) a evaluer ce cycle.")

    ajouts, observation = [], []
    for i, d in enumerate(a_verifier):
        verdict, plateforme, raison = evaluer_candidat(d, candidats[d], liste_noire, maintenant)
        print(f"[{i + 1}/{len(a_verifier)}] {d} : {verdict} ({raison})")
        if verdict == "ajout":
            listes[plateforme].append(d)
            ajouts.append((d, plateforme))
            verifies[d] = {"verdict": "ajout", "date": maintenant.isoformat(timespec="seconds")}
        elif verdict == "observation":
            observation.append(d)
        else:
            verifies[d] = {"verdict": "rejet", "raison": raison, "date": maintenant.isoformat(timespec="seconds")}
        time.sleep(DELAI_ENTRE_BOUTIQUES)

    if ajouts or retraits:
        ecrire_listes_ct(listes)
    if not sauvegarder_memoire_supabase(memoire, CLE_MEMOIRE, supabase_url, supabase_key):
        print("ATTENTION : echec de sauvegarde de la memoire Supabase -- l'etat de ce cycle est perdu.")
    envoyer_rapport_telegram(ajouts, retraits, observation, token_telegram_perso().strip(),
                             os.environ.get("TELEGRAM_CHAT_ID", "1245330032").strip())
    print(f"\nTermine : {len(ajouts)} ajout(s), {len(retraits)} retrait(s), {len(observation)} en observation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
