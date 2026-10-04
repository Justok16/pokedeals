"""
Controles de LEGITIMITE d'une boutique candidate, avant tout ajout
automatique a la liste des boutiques scannees (qui declenche de vraies
alertes d'achat sur Telegram).

Trois garde-fous, objectifs et automatisables :
  1. liste noire : domaines signales comme arnaques par deux annuaires
     communautaires (Pokescam, PokeGourou) ;
  2. HTTPS valide (certificat verifie par `requests`, jamais desactive) ;
  3. mentions legales : lien vers une page mentions legales / CGV et
     presence d'un numero SIRET/SIREN/RCS sur cette page (obligation legale
     pour tout e-commercant francais -- les faux sites l'omettent ou
     recopient celui d'un autre).

Ces controles ne PROUVENT pas qu'une boutique est honnete : ils eliminent
les cas evidents. Les boutiques issues d'un annuaire verifie a la main
(Pokescam) passent en plus par la verification humaine de cet annuaire.
"""

import re
import time
from urllib.parse import urljoin

import requests

from connecteur_shopify import HEADERS_HTML, TIMEOUT

URL_ARNAQUES_POKESCAM = "https://pokescam.com/arnaques/"
URL_ARNAQUES_POKEGOUROU = (
    "https://pokegourou.com/conseils-pour-collectionner/"
    "liste-des-sites-darnaques-pokemon-contrefacons-et-scam/"
)

# Pokescam : une carte par arnaque, domaine en texte du lien de la fiche
# (la page contient aussi un encart "sites fiables" -- a NE PAS lire : un
# parsing trop large de tout le texte classait a tort des boutiques
# verifiees comme arnaques).
_RE_ARNAQUE_POKESCAM = re.compile(
    r'class="pap-sc-name"[^>]*>\s*([^<\s]+)\s*<', re.IGNORECASE)
# PokeGourou : lignes "domaine.tld — Arnaque confirmee" (ou statut vide).
_RE_ARNAQUE_POKEGOUROU = re.compile(
    r"^\s*([a-z0-9][a-z0-9.\-]*\.[a-z]{2,})\s+[—–-]\s", re.IGNORECASE | re.MULTILINE)

_RE_SIRET = re.compile(r"\b(?:siret|siren|r\.?c\.?s\.?)\b[^0-9]{0,40}((?:\d[ .]?){9,14})", re.IGNORECASE)
_RE_LIEN_LEGAL = re.compile(
    r'href=["\']([^"\']*(?:mention|legal|cgv|conditions-g|cgu|politique-de-confidentialit)[^"\']*)["\']',
    re.IGNORECASE,
)


def normaliser_domaine(domaine: str) -> str:
    d = domaine.strip().lower()
    d = re.sub(r"^https?://", "", d).split("/")[0]
    return d.removeprefix("www.")


def extraire_arnaques_pokescam(html: str) -> set[str]:
    return {normaliser_domaine(m) for m in _RE_ARNAQUE_POKESCAM.findall(html)}


def extraire_arnaques_pokegourou(html: str) -> set[str]:
    texte = re.sub(r"<[^>]+>", "\n", html)
    return {normaliser_domaine(m) for m in _RE_ARNAQUE_POKEGOUROU.findall(texte)}


def charger_liste_noire(session: requests.Session | None = None) -> set[str]:
    """Union des domaines signales par les deux annuaires d'arnaques. Un
    echec de telechargement d'une source ne vide pas l'autre ; si les DEUX
    echouent, retourne un ensemble vide (l'appelant le sait via
    `liste_noire_disponible`, pour ne pas ajouter a l'aveugle)."""
    s = session or requests
    noire: set[str] = set()
    for url, extraire in ((URL_ARNAQUES_POKESCAM, extraire_arnaques_pokescam),
                          (URL_ARNAQUES_POKEGOUROU, extraire_arnaques_pokegourou)):
        try:
            r = s.get(url, headers=HEADERS_HTML, timeout=TIMEOUT)
            if r.status_code == 200:
                noire |= extraire(r.text)
        except requests.exceptions.RequestException:
            continue
        time.sleep(0.5)
    return noire


def extraire_siret(texte: str) -> str | None:
    """Premier numero SIRET (14 chiffres) ou SIREN (9 chiffres) plausible."""
    for m in _RE_SIRET.finditer(re.sub(r"<[^>]+>", " ", texte)):
        chiffres = re.sub(r"\D", "", m.group(1))
        if len(chiffres) in (9, 14):
            return chiffres
    return None


def verifier_legitimite(domaine: str, session: requests.Session | None = None) -> dict:
    """Retourne {https_ok, mentions_legales, siret, raison}. Ne leve jamais.
    `https_ok` est False sur certificat invalide / site injoignable."""
    s = session or requests
    base = f"https://{normaliser_domaine(domaine)}/"
    resultat = {"https_ok": False, "mentions_legales": False, "siret": None, "raison": ""}
    try:
        accueil = s.get(base, headers=HEADERS_HTML, timeout=TIMEOUT)
    except requests.exceptions.SSLError:
        resultat["raison"] = "certificat HTTPS invalide"
        return resultat
    except requests.exceptions.RequestException as e:
        resultat["raison"] = f"injoignable ({type(e).__name__})"
        return resultat
    if accueil.status_code >= 400:
        resultat["raison"] = f"accueil HTTP {accueil.status_code}"
        return resultat
    resultat["https_ok"] = True

    siret = extraire_siret(accueil.text)
    liens = []
    for href in _RE_LIEN_LEGAL.findall(accueil.text):
        url = urljoin(base, href)
        if url not in liens:
            liens.append(url)
    resultat["mentions_legales"] = bool(liens)
    for url in liens[:3]:
        if siret:
            break
        try:
            page = s.get(url, headers=HEADERS_HTML, timeout=TIMEOUT)
        except requests.exceptions.RequestException:
            continue
        if page.status_code == 200:
            siret = extraire_siret(page.text)
        time.sleep(0.5)
    resultat["siret"] = siret
    if not resultat["mentions_legales"]:
        resultat["raison"] = "aucune page mentions legales/CGV trouvee"
    elif not siret:
        resultat["raison"] = "aucun SIRET/SIREN trouve dans les mentions legales"
    return resultat


def est_legitime(rapport: dict) -> bool:
    return bool(rapport.get("https_ok") and rapport.get("mentions_legales") and rapport.get("siret"))
