"""PokéDeals — bot d'arbitrage de cartes Pokémon (fichier unique).

TOUT le programme est dans ce seul fichier : plus de dossier modules.
Il lit config.yaml, scanne eBay/Vinted/Leboncoin, calcule les cotes,
filtre les faux positifs et envoie les alertes Telegram (+ email si activé).
"""
from __future__ import annotations

import base64
import csv
import json
import logging
import os
import random
import re
import smtplib
import statistics
import sys
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from zoneinfo import ZoneInfo

import requests
import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("pokedeals")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
]


def user_agent() -> str:
    return random.choice(USER_AGENTS)


def requete_avec_retry(methode, url, tentatives: int = 3, **kwargs):
    """Requête HTTP avec 3 tentatives et attente progressive."""
    derniere_erreur = None
    r = None
    for i in range(tentatives):
        try:
            r = methode(url, **kwargs)
            if r.status_code == 429:
                attente = (2 ** (i + 1)) + random.uniform(0, 2)
                log.info("429 reçu, pause de %.1fs", attente)
                time.sleep(attente)
                continue
            return r
        except requests.RequestException as e:
            derniere_erreur = e
            time.sleep((2 ** i) + random.uniform(0, 1))
    if derniere_erreur:
        raise derniere_erreur
    return r


# ------------------- Normalisation de texte -------------------

def normaliser(texte: str) -> str:
    """minuscules + sans accents + sans tirets (méga-dracaufeu -> mega dracaufeu)."""
    t = unicodedata.normalize("NFD", (texte or "").lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return t.replace("-", " ").replace("_", " ")


# ------------------- Filtres de pertinence -------------------

RE_NUMERO = re.compile(r"(\d{1,3})\s*/\s*(\d{2,3})")

# 1) L'annonce doit contenir AU MOINS UN de ces indices de "vraie carte"
INDICES_CARTE = [
    "carte", "card", "carta", "karte",       # carte en FR/EN/IT-ES/DE
    "tcg", "holo", "reverse", "full art", "fa ",
    "promo", "alt ", "alternative", "secrete", "secret",
    " ar", "ar ", "sar", "sir", "mhr", "chr",
    " ex", "ex ", " gx", "gx ", "vstar", "vmax", " nm", "nm ",
    "near mint", "mint", "psa", "pca",       # (psa/pca restent exclus ensuite,
]                                             #  mais prouvent que c'est une carte)

# 2) Mots qui signalent que ce N'EST PAS une carte à l'unité non gradée
EXCLUSIONS = [
    # Lots & produits scellés
    "lot de", "lot ", " lots", "x5", "x10", "x20", "x50", "x100",
    "display", "booster", "coffret", "etb", "elite trainer", "tin ",
    "blister", "tripack", "bundle", "collection complete", "set complet",
    "classeur", "album", "a choisir", "au choix",
    # Contrefaçons & produits dérivés de cartes
    "proxy", "proxies", "fake", "replique", "custom", "metal", "jumbo",
    "oversize", "gold plated", "plastifiee", "sticker", "autocollant",
    # Cartes gradées
    "psa", "pca", "bgs", "cgc", "gradee", "graded", "grade 8", "grade 9", "grade 10",
    # Vêtements & accessoires
    "t shirt", "tee shirt", "tshirt", "pull", "sweat", "hoodie", "veste",
    "casquette", "bonnet", "pyjama", "chaussette", "chausson", "basket",
    "deguisement", "costume", "sac ", "sacoche", "cartable", "trousse",
    # Jouets & objets
    "peluche", "figurine", "funko", "pop!", "jouet", "lego", "puzzle",
    "piece", "medaille", "mug", "tasse", "gourde", "porte cle", "porte cles",
    "coque", "poster", "tapis", "protege", "sleeve", "toploader",
    "jeu video", "nintendo switch", "game boy", "ds ", "3ds",
    "livre", "manga", "dvd", "blu ray",
]

# Petits mots à ignorer quand on extrait le nom du Pokémon
MOTS_VIDES = {"carte", "pokemon", "ex", "gx", "v", "vstar", "vmax", "de", "n",
              "la", "le", "et", "mega", "team", "rocket", "jp", "fr", "sv2a",
              "sir", "sar", "ar", "mhr"}


def extraire_numero(texte: str) -> str | None:
    m = RE_NUMERO.search(texte or "")
    return f"{int(m.group(1))}/{int(m.group(2))}" if m else None


def nom_pokemon(nom_carte: str) -> str | None:
    """Extrait le nom du Pokémon depuis le nom de la watchlist.
    'Méga-Dracolosse ex 290/217' -> 'dracolosse'
    'Zoroark de N ex héros transcendants' -> 'zoroark'
    """
    for mot in normaliser(nom_carte).split():
        if len(mot) >= 4 and mot not in MOTS_VIDES and not any(c.isdigit() for c in mot):
            return mot
    return None


def annonce_pertinente(titre: str, nom_carte: str) -> tuple[bool, str]:
    """Filtre strict : (pertinent, raison)."""
    t = normaliser(titre)
    if not t.strip():
        return False, "titre vide"

    # 1) Exclusions d'abord (vêtements, lots, scellé, gradées, objets...)
    for mot in EXCLUSIONS:
        if mot in t:
            return False, f"exclue ('{mot.strip()}')"

    # 2) Doit ressembler à une carte
    if not any(ind in f" {t} " for ind in INDICES_CARTE):
        return False, "pas une carte (aucun indice carte/holo/promo...)"

    # 3) Le nom du Pokémon recherché doit apparaître dans le titre
    pokemon = nom_pokemon(nom_carte)
    if pokemon and pokemon not in t:
        return False, f"pokemon absent du titre ('{pokemon}')"

    # 4) Numéro exact si précisé dans la watchlist
    numero_voulu = extraire_numero(nom_carte)
    if numero_voulu:
        numero_annonce = extraire_numero(titre)
        if numero_annonce and numero_annonce != numero_voulu:
            return False, f"mauvais numéro ({numero_annonce} ≠ {numero_voulu})"

    return True, "ok"


RACINE = os.path.dirname(os.path.abspath(__file__))


def charger_config(chemin: str | None = None) -> dict:
    chemin = chemin or os.path.join(RACINE, "config.yaml")
    with open(chemin, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # Valeurs par défaut de sécurité
    cfg.setdefault("regles", {})
    r = cfg["regles"]
    r.setdefault("frais_port_max", 6.0)
    r.setdefault("marge_achat", 0.10)
    r.setdefault("marge_revente", 0.10)
    r.setdefault("frais_revente_estimes", 0.13)
    r.setdefault("cote_min", 5.0)
    r.setdefault("prix_max", 0)  # 0 = illimité

    cfg.setdefault("watchlist", [])
    cfg.setdefault("etats_acceptes", [])
    cfg.setdefault("etats_refuses", [])
    cfg.setdefault("cote", {"coefficient_marche": 0.92, "minimum_annonces": 4})
    cfg.setdefault("plateformes", {"ebay": True, "vinted": True, "leboncoin": True})

    if not cfg["watchlist"]:
        raise ValueError("La watchlist est vide : ajoute des cartes dans config.yaml")

    return cfg


def secrets_env() -> dict:
    """Secrets injectés par GitHub Actions (jamais écrits dans le code)."""
    return {
        "EBAY_CLIENT_ID": os.environ.get("EBAY_CLIENT_ID", ""),
        "EBAY_CLIENT_SECRET": os.environ.get("EBAY_CLIENT_SECRET", ""),
        "GMAIL_APP_PASSWORD": os.environ.get("GMAIL_APP_PASSWORD", ""),
        "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", ""),
    }


RACINE = os.path.dirname(os.path.abspath(__file__))
FICHIER_SEEN = os.path.join(RACINE, "data", "seen.json")
RETENTION_JOURS = 30


def charger_vues() -> dict:
    if not os.path.exists(FICHIER_SEEN):
        return {}
    try:
        with open(FICHIER_SEEN, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def sauvegarder_vues(vues: dict) -> None:
    # Nettoyage des entrées trop anciennes
    limite = time.time() - RETENTION_JOURS * 86400
    vues = {k: v for k, v in vues.items() if v.get("ts", 0) > limite}
    os.makedirs(os.path.dirname(FICHIER_SEEN), exist_ok=True)
    with open(FICHIER_SEEN, "w", encoding="utf-8") as f:
        json.dump(vues, f, ensure_ascii=False, indent=1)


def deja_vue(vues: dict, annonce_id: str) -> bool:
    return annonce_id in vues


def marquer(vues: dict, annonce_id: str) -> None:
    vues[annonce_id] = {"ts": time.time()}


TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"
BROWSE_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"
MARKETPLACE = "EBAY_FR"

_token_cache = {"token": None, "expire": 0}


def _obtenir_token(client_id: str, client_secret: str) -> str | None:
    if _token_cache["token"] and time.time() < _token_cache["expire"] - 60:
        return _token_cache["token"]
    if not client_id or not client_secret:
        log.warning("Identifiants eBay manquants (secrets GitHub non configurés)")
        return None
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    try:
        r = requests.post(
            TOKEN_URL,
            headers={
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "client_credentials",
                "scope": "https://api.ebay.com/oauth/api_scope",
            },
            timeout=20,
        )
        r.raise_for_status()
        data = r.json()
        _token_cache["token"] = data["access_token"]
        _token_cache["expire"] = time.time() + int(data.get("expires_in", 7200))
        return _token_cache["token"]
    except Exception as e:  # noqa: BLE001
        log.error("Échec d'authentification eBay : %s", e)
        return None


def ebay_rechercher(nom_carte: str, langue: str, secrets: dict, limite: int = 40) -> list[dict]:
    """Retourne les annonces eBay FR en achat immédiat pour une carte."""
    token = _obtenir_token(secrets["EBAY_CLIENT_ID"], secrets["EBAY_CLIENT_SECRET"])
    if not token:
        return []

    requete = f"carte pokemon {nom_carte}"
    if langue == "jp":
        requete += " japonaise"

    try:
        r = requete_avec_retry(
            requests.get,
            BROWSE_URL,
            headers={
                "Authorization": f"Bearer {token}",
                "X-EBAY-C-MARKETPLACE-ID": MARKETPLACE,
            },
            params={
                "q": requete,
                "limit": str(limite),
                "filter": "buyingOptions:{FIXED_PRICE},itemLocationCountry:FR,priceCurrency:EUR",
            },
            timeout=25,
        )
        r.raise_for_status()
        items = r.json().get("itemSummaries", []) or []
    except Exception as e:  # noqa: BLE001
        log.error("Recherche eBay '%s' échouée : %s", nom_carte, e)
        return []

    annonces = []
    for it in items:
        try:
            prix = float(it["price"]["value"])
        except (KeyError, ValueError, TypeError):
            continue
        port = 0.0
        opts = it.get("shippingOptions") or []
        if opts:
            try:
                port = float(opts[0]["shippingCost"]["value"])
            except (KeyError, ValueError, TypeError):
                port = 0.0
        annonces.append(
            {
                "plateforme": "eBay",
                "id": f"ebay-{it.get('itemId', '')}",
                "titre": it.get("title", ""),
                "prix": prix,
                "port": port,
                "url": it.get("itemWebUrl", ""),
                "etat_texte": (it.get("condition") or "") + " " + it.get("title", ""),
            }
        )
    return annonces


def calculer_cote(annonces: list[dict], cfg_cote: dict) -> float | None:
    """Cote = médiane des prix (hors port) des annonces actives × coefficient."""
    prix = sorted(a["prix"] for a in annonces if a["prix"] > 0)
    if len(prix) < int(cfg_cote.get("minimum_annonces", 4)):
        return None
    # On écarte les 15% extrêmes de chaque côté (annonces fantaisistes)
    k = max(1, int(len(prix) * 0.15))
    tronque = prix[k:-k] if len(prix) > 2 * k else prix
    mediane = statistics.median(tronque)
    return round(mediane * float(cfg_cote.get("coefficient_marche", 0.92)), 2)


VINTED_BASE = "https://www.vinted.fr"
VINTED_SEARCH = VINTED_BASE + "/api/v2/catalog/items"

_vinted_session: requests.Session | None = None

VINTED_HEADERS = {
    "User-Agent": user_agent(),
    "Accept": "application/json",
    "Accept-Language": "fr-FR,fr;q=0.9",
}


def _get_vinted_session() -> requests.Session | None:
    global _vinted_session
    if _vinted_session is not None:
        return _vinted_session
    s = requests.Session()
    s.headers.update(VINTED_HEADERS)
    try:
        # Première visite pour récupérer les cookies nécessaires
        s.get(VINTED_BASE, timeout=20)
        _vinted_session = s
        return s
    except Exception as e:  # noqa: BLE001
        log.error("Impossible d'initialiser la session Vinted : %s", e)
        return None


def vinted_rechercher(nom_carte: str, langue: str, limite: int = 30, prix_plafond: float | None = None) -> list[dict]:
    s = _get_vinted_session()
    if s is None:
        return []
    requete = f"carte pokemon {nom_carte}"
    if langue == "jp":
        requete += " japonaise"
    params = {
        "search_text": requete,
        "per_page": str(limite),
        "order": "newest_first",
        "currency": "EUR",
    }
    # Optimisation : si la cote est connue, on demande à Vinted de ne
    # renvoyer QUE les annonces sous le seuil d'achat (moins de bruit,
    # réponses plus rapides, plus d'annonces utiles par page).
    if prix_plafond and prix_plafond > 0:
        params["price_to"] = str(prix_plafond)
    try:
        r = requete_avec_retry(s.get, VINTED_SEARCH, params=params, timeout=25)
        if r.status_code == 401:
            # Cookies expirés : on retente une fois avec une session neuve
            global _vinted_session
            _vinted_session = None
            s = _get_vinted_session()
            if s is None:
                return []
            r = requete_avec_retry(s.get, VINTED_SEARCH, params=params, timeout=25)
        r.raise_for_status()
        items = r.json().get("items", []) or []
    except Exception as e:  # noqa: BLE001
        log.warning("Recherche Vinted '%s' échouée : %s", nom_carte, e)
        return []

    annonces = []
    for it in items:
        try:
            prix = float(it["price"]["amount"])
        except (KeyError, ValueError, TypeError):
            continue
        annonces.append(
            {
                "plateforme": "Vinted",
                "id": f"vinted-{it.get('id', '')}",
                "titre": it.get("title", ""),
                "prix": prix,
                # Port Vinted : ~3-5€ pour une carte en lettre suivie
                "port": 3.5,
                "url": it.get("url") or f"{VINTED_BASE}/items/{it.get('id', '')}",
                "etat_texte": (it.get("status") or "") + " " + it.get("title", ""),
            }
        )
    return annonces


LBC_API = "https://api.leboncoin.fr/finder/search"

LBC_HEADERS = {
    "User-Agent": user_agent(),
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Origin": "https://www.leboncoin.fr",
    "Referer": "https://www.leboncoin.fr/",
}


def lbc_rechercher(nom_carte: str, langue: str, limite: int = 30) -> list[dict]:
    requete = f"carte pokemon {nom_carte}"
    if langue == "jp":
        requete += " japonaise"
    payload = {
        "filters": {
            "category": {"id": "41"},  # Jeux & Jouets
            "keywords": {"text": requete},
        },
        "limit": limite,
        "sort_by": "time",
        "sort_order": "desc",
    }
    try:
        r = requete_avec_retry(requests.post, LBC_API, json=payload, headers=LBC_HEADERS, timeout=25)
        if r.status_code in (403, 429):
            log.info("Leboncoin a bloqué la requête (%s) — plateforme ignorée ce tour-ci", r.status_code)
            return []
        r.raise_for_status()
        ads = r.json().get("ads", []) or []
    except Exception as e:  # noqa: BLE001
        log.info("Leboncoin indisponible (%s) — on continue sans", e)
        return []

    annonces = []
    for ad in ads:
        prix_liste = ad.get("price") or []
        if not prix_liste:
            continue
        try:
            prix = float(prix_liste[0])
        except (ValueError, TypeError):
            continue
        annonces.append(
            {
                "plateforme": "Leboncoin",
                "id": f"lbc-{ad.get('list_id', '')}",
                "titre": ad.get("subject", ""),
                "prix": prix,
                "port": 4.0,  # estimation lettre suivie / Mondial Relay
                "url": ad.get("url", ""),
                "etat_texte": (ad.get("subject") or "") + " " + (ad.get("body") or ""),
            }
        )
    return annonces


RACINE = os.path.dirname(os.path.abspath(__file__))
FICHIER_COTES = os.path.join(RACINE, "data", "cotes.json")
HISTORIQUE_MAX = 5          # nombre de cotes conservées par carte
VALIDITE_JOURS = 7          # une cote de plus de 7 jours est ignorée


def _charger_historique() -> dict:
    if not os.path.exists(FICHIER_COTES):
        return {}
    try:
        with open(FICHIER_COTES, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def sauvegarder_historique() -> None:
    h = historique()
    os.makedirs(os.path.dirname(FICHIER_COTES), exist_ok=True)
    with open(FICHIER_COTES, "w", encoding="utf-8") as f:
        json.dump(h, f, ensure_ascii=False, indent=1)


_historique = None


def historique() -> dict:
    global _historique
    if _historique is None:
        _historique = _charger_historique()
    return _historique


def cote_lissee(nom_carte: str) -> float | None:
    """Médiane des cotes récentes enregistrées pour cette carte."""
    entrees = historique().get(nom_carte, [])
    limite = time.time() - VALIDITE_JOURS * 86400
    valeurs = [e["cote"] for e in entrees if e.get("ts", 0) > limite]
    if not valeurs:
        return None
    return round(statistics.median(valeurs), 2)


def enregistrer_cote(nom_carte: str, cote: float) -> None:
    h = historique()
    entrees = h.get(nom_carte, [])
    entrees.append({"cote": cote, "ts": time.time()})
    h[nom_carte] = entrees[-HISTORIQUE_MAX:]


def obtenir_cote(carte: dict, annonces_ebay: list[dict], cfg: dict) -> tuple[float | None, int]:
    """Retourne (cote, confiance) où confiance = nb d'annonces eBay utilisées."""
    # 1) Cote manuelle prioritaire
    cote_manuelle = carte.get("cote")
    if cote_manuelle:
        try:
            return float(cote_manuelle), 99
        except (ValueError, TypeError):
            log.warning("Cote manuelle invalide pour %s", carte.get("nom"))

    # 2) Cote du jour depuis eBay, ajoutée à l'historique
    cote_instant = calculer_cote(annonces_ebay, cfg["cote"])
    if cote_instant:
        enregistrer_cote(carte["nom"], cote_instant)

    # 3) Cote lissée (médiane des derniers passages)
    cote = cote_lissee(carte["nom"])
    if cote is None:
        cote = cote_instant
    if cote is None:
        log.info("Cote introuvable pour '%s' (pas assez d'annonces eBay)", carte.get("nom"))
        return None, 0
    return cote, len(annonces_ebay)


def _etat_ok(texte: str, acceptes: list[str], refuses: list[str]) -> bool:
    t = (texte or "").lower()
    if any(mot in t for mot in refuses):
        return False
    # Si aucun mot-clé d'état n'est présent, on laisse passer :
    # beaucoup de vendeurs n'indiquent pas l'état dans le titre.
    if not any(mot in t for mot in acceptes):
        return True
    return True




def evaluate(annonce: dict, cote: float | None, cfg: dict, confiance: int = 0, marge_achat: float | None = None) -> tuple[dict | None, str]:
    """Évalue une annonce. Retourne (deal, status)."""
    r = cfg["regles"]

    if cote is None or cote <= 0:
        return None, "cote indisponible"
    if cote < r.get("cote_min", 5.0):
        return None, f"cote trop faible ({cote:.2f}€ < {r.get('cote_min', 5.0):.2f}€)"

    # Filtre anti-faux-positifs : lots, produits scellés, proxys, mauvaise version...
    pertinent, raison = annonce_pertinente(annonce.get("titre", ""), annonce.get("carte", ""))
    if not pertinent:
        return None, raison

    prix = float(annonce.get("prix", 0))
    port = float(annonce.get("port", 0))
    total = prix + port

    prix_max = float(r.get("prix_max", 0) or 0)
    if prix_max > 0 and total > prix_max:
        return None, f"au-dessus du budget ({total:.2f}€)"
    if port > r["frais_port_max"]:
        return None, f"port trop cher ({port:.2f}€ > {r['frais_port_max']:.2f}€)"
    if not _etat_ok(annonce.get("etat_texte", ""), cfg["etats_acceptes"], cfg["etats_refuses"]):
        return None, "état refusé (abîmée / gradée / jouée)"

    # --- Achat : total net au moins 10% sous la cote ---
    # Marge par carte (override), sinon marge globale
    marge = marge_achat if marge_achat is not None else r["marge_achat"]
    seuil_achat = cote * (1 - marge)
    if total > seuil_achat:
        return None, f"pas assez sous la cote ({total:.2f}€ > seuil {seuil_achat:.2f}€)"

    # --- Revente : au moins 10% net au-dessus de la cote, frais déduits ---
    prix_revente = cote * (1 + r["marge_revente"]) / (1 - r["frais_revente_estimes"])
    profit_net = cote * (1 + r["marge_revente"]) - total
    if profit_net <= 0:
        return None, "profit net nul ou négatif"

    deal = {
        **annonce,
        "cote": round(cote, 2),
        "total": round(total, 2),
        "decote_pct": round((1 - total / cote) * 100, 1),
        "prix_revente_conseille": round(prix_revente, 2),
        "profit_net_estime": round(profit_net, 2),
        "confiance": confiance,  # nb d'annonces eBay derrière la cote (99 = cote manuelle)
    }
    return deal, "DEAL"


def envoyer_telegram_texte(textes: list[str], cfg_tg: dict, token: str) -> bool:
    """Envoie des messages Telegram libres (récap quotidien, anomalies...)."""

    if not textes:
        return True
    if not token or not str(cfg_tg.get("chat_id", "")).strip():
        log.error("Telegram non configuré : message non envoyé")
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    ok = True
    for txt in textes:
        try:
            r = requests.post(
                url,
                json={"chat_id": str(cfg_tg["chat_id"]), "text": txt, "parse_mode": "HTML"},
                timeout=20,
            )
            if r.status_code != 200:
                log.error("Telegram a refusé le message (%s)", r.status_code)
                ok = False
        except Exception as e:  # noqa: BLE001
            log.error("Échec message Telegram : %s", e)
            ok = False
    return ok


def _texte_vente(v: dict) -> str:
    return (
        f"💰 <b>C'EST LE MOMENT DE VENDRE !</b>\n"
        f"🎴 <b>{v['nom']}</b>\n"
        f"🛒 Acheté : {v['prix_achat']:.2f}€\n"
        f"📈 Cote actuelle : <b>{v['cote']:.2f}€</b> (x{v['multiple']})\n"
        f"✅ Gain net estimé après frais : <b>+{v['gain_net_estime']:.2f}€</b>"
    )


def envoyer_telegram_ventes(ventes: list[dict], cfg_tg: dict, token: str) -> bool:
    """Alertes de revente (stock ayant atteint l'objectif) sur Telegram."""

    if not ventes:
        return True
    if not token or not str(cfg_tg.get("chat_id", "")).strip():
        log.error("Telegram non configuré : alerte de vente non envoyée")
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    ok = True
    for v in ventes:
        try:
            r = requests.post(
                url,
                json={"chat_id": str(cfg_tg["chat_id"]), "text": _texte_vente(v), "parse_mode": "HTML"},
                timeout=20,
            )
            if r.status_code != 200:
                log.error("Telegram a refusé l'alerte vente (%s)", r.status_code)
                ok = False
        except Exception as e:  # noqa: BLE001
            log.error("Échec alerte vente Telegram : %s", e)
            ok = False
    return ok


def _texte_telegram(d: dict) -> str:
    return (
        f"🔥 <b>{d['titre']}</b>\n"
        f"🛒 {d['plateforme']} — <b>{d['prix']:.2f}€</b> + {d['port']:.2f}€ port = <b>{d['total']:.2f}€</b>\n"
        f"📊 Cote : {d['cote']:.2f}€ (<b>-{d['decote_pct']}%</b>)\n"
        f"💶 Revente conseillée : {d['prix_revente_conseille']:.2f}€\n"
        f"✅ Profit net estimé : <b>+{d['profit_net_estime']:.2f}€</b>\n"
        f"👉 <a href=\"{d['url']}\">Voir l'annonce</a>"
    )


def envoyer_telegram(deals: list[dict], cfg_tg: dict, token: str) -> bool:
    """Envoie une notification Telegram par deal (instantané)."""

    if not deals:
        return True
    if not token:
        log.error("TELEGRAM_BOT_TOKEN manquant : notification Telegram impossible")
        return False
    chat_id = str(cfg_tg.get("chat_id", "")).strip()
    if not chat_id:
        log.error("telegram.chat_id manquant dans config.yaml")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    ok = True
    for d in deals:
        try:
            r = requests.post(
                url,
                json={
                    "chat_id": chat_id,
                    "text": _texte_telegram(d),
                    "parse_mode": "HTML",
                    "disable_web_page_preview": False,
                },
                timeout=20,
            )
            if r.status_code != 200:
                log.error("Telegram a refusé le message (%s) : %s", r.status_code, r.text[:200])
                ok = False
        except Exception as e:  # noqa: BLE001
            log.error("Échec envoi Telegram : %s", e)
            ok = False
    if ok:
        log.info("Telegram : %d notification(s) envoyée(s)", len(deals))
    return ok


def _html_deal(d: dict) -> str:
    return f"""
    <div style="border:1px solid #ddd;border-radius:8px;padding:14px;margin:10px 0;font-family:Arial">
      <h3 style="margin:0 0 6px">🔥 {d['titre']}</h3>
      <p style="margin:4px 0">
        <b>Plateforme :</b> {d['plateforme']}<br>
        <b>Prix :</b> {d['prix']:.2f}€ + {d['port']:.2f}€ de port = <b>{d['total']:.2f}€</b><br>
        <b>Cote estimée :</b> {d['cote']:.2f}€ &nbsp;(<b style="color:green">-{d['decote_pct']}%</b>)<br>
        <b>Prix de revente conseillé :</b> {d['prix_revente_conseille']:.2f}€<br>
        <b>Profit net estimé :</b> <b style="color:green">+{d['profit_net_estime']:.2f}€</b>
      </p>
      <a href="{d['url']}" style="display:inline-block;background:#1a73e8;color:#fff;
         padding:8px 16px;border-radius:6px;text-decoration:none">Voir l'annonce ➜</a>
    </div>"""


def envoyer_alertes(deals: list[dict], cfg_email: dict, mot_de_passe: str) -> bool:
    if not deals:
        return True
    if not mot_de_passe:
        log.error("GMAIL_APP_PASSWORD manquant : impossible d'envoyer le mail")
        return False

    corps = "".join(_html_deal(d) for d in deals)
    html = f"""<html><body style="font-family:Arial">
      <h2>💰 PokéDeals — {len(deals)} affaire(s) détectée(s)</h2>
      {corps}
      <p style="color:#888;font-size:12px">Vérifie toujours les photos et la description
      avant d'acheter : le bot ne voit que le texte de l'annonce.</p>
    </body></html>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🔥 PokéDeals : {len(deals)} bonne(s) affaire(s) !"
    msg["From"] = cfg_email["expediteur"]
    msg["To"] = cfg_email["destinataire"]
    msg.attach(MIMEText(html, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as srv:
            srv.login(cfg_email["expediteur"], mot_de_passe)
            srv.send_message(msg)
        log.info("Email envoyé (%d deals)", len(deals))
        return True
    except Exception as e:  # noqa: BLE001
        log.error("Échec de l'envoi du mail : %s", e)
        return False


RAPPEL_JOURS = 7  # ne pas re-alerter la même carte avant 7 jours


def verifier_stock(cfg: dict, secrets: dict, vues: dict) -> list[dict]:
    """Retourne la liste des alertes de vente à envoyer."""
    achats = cfg.get("mes_achats") or []
    if not achats:
        return []

    multiplicateur = float(cfg["regles"].get("multiplicateur_revente", 2.0))
    frais = float(cfg["regles"].get("frais_revente_estimes", 0.13))
    alertes = []

    for achat in achats:
        nom = achat.get("nom")
        prix_achat = achat.get("prix_achat")
        if not nom or not prix_achat:
            log.warning("Entrée mes_achats incomplète ignorée : %s", achat)
            continue
        prix_achat = float(prix_achat)

        # Cote actuelle : manuelle si fournie, sinon eBay (recherche + lissage)
        annonces_ebay = []
        if not achat.get("cote"):
            annonces_ebay = ebay_rechercher(nom, achat.get("langue", "fr"), secrets)
        cote, _ = obtenir_cote(achat, annonces_ebay, cfg)
        if not cote:
            log.info("Stock '%s' : cote introuvable, on réessaiera au prochain scan", nom)
            continue

        seuil = prix_achat * multiplicateur
        if cote < seuil:
            log.info("Stock '%s' : cote %.2f€ / objectif %.2f€ (x%.1f de %.2f€)",
                     nom, cote, seuil, multiplicateur, prix_achat)
            continue

        # Anti-spam : une alerte par carte par semaine maximum
        cle = f"vente-{nom}"
        derniere = vues.get(cle, {}).get("ts", 0)
        if time.time() - derniere < RAPPEL_JOURS * 86400:
            continue
        vues[cle] = {"ts": time.time()}

        gain_net = cote * (1 - frais) - prix_achat
        alertes.append(
            {
                "nom": nom,
                "prix_achat": round(prix_achat, 2),
                "cote": round(cote, 2),
                "multiple": round(cote / prix_achat, 2),
                "gain_net_estime": round(gain_net, 2),
            }
        )
        log.info("  💰 ALERTE VENTE : %s — cote %.2f€ = x%.2f ton prix d'achat",
                 nom, cote, cote / prix_achat)

    return alertes


RACINE = os.path.dirname(os.path.abspath(__file__))
FICHIER_STATS = os.path.join(RACINE, "data", "stats.json")
FICHIER_CSV = os.path.join(RACINE, "data", "deals.csv")
PARIS = ZoneInfo("Europe/Paris")

COLONNES_CSV = ["date", "carte", "plateforme", "titre", "prix", "port", "total",
                "cote", "decote_pct", "prix_revente_conseille", "profit_net_estime", "url"]


# ------------------------- STATS QUOTIDIENNES -------------------------

def _charger_stats() -> dict:
    if not os.path.exists(FICHIER_STATS):
        return {}
    try:
        with open(FICHIER_STATS, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def enregistrer_scan(nb_annonces: int, deals: list[dict]) -> None:
    """Ajoute les chiffres du scan courant aux stats du jour (garde 30 jours)."""
    stats = _charger_stats()
    jour = datetime.now(PARIS).strftime("%Y-%m-%d")
    s = stats.get(jour, {"scans": 0, "annonces": 0, "deals": 0, "profit_potentiel": 0.0})
    s["scans"] += 1
    s["annonces"] += nb_annonces
    s["deals"] += len(deals)
    s["profit_potentiel"] = round(s["profit_potentiel"] + sum(d["profit_net_estime"] for d in deals), 2)
    stats[jour] = s
    stats = dict(sorted(stats.items())[-30:])  # 30 derniers jours
    os.makedirs(os.path.dirname(FICHIER_STATS), exist_ok=True)
    with open(FICHIER_STATS, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=1)


# ------------------------------ CSV -----------------------------------

def exporter_csv(deals: list[dict]) -> None:
    """Ajoute chaque deal détecté à data/deals.csv (créé au premier deal)."""
    if not deals:
        return
    nouveau = not os.path.exists(FICHIER_CSV)
    os.makedirs(os.path.dirname(FICHIER_CSV), exist_ok=True)
    with open(FICHIER_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        if nouveau:
            w.writerow(COLONNES_CSV)
        maintenant = datetime.now(PARIS).strftime("%Y-%m-%d %H:%M")
        for d in deals:
            w.writerow([maintenant, d.get("carte", ""), d["plateforme"], d["titre"],
                        d["prix"], d["port"], d["total"], d["cote"], d["decote_pct"],
                        d["prix_revente_conseille"], d["profit_net_estime"], d["url"]])
    log.info("CSV : %d deal(s) ajouté(s) à data/deals.csv", len(deals))


# --------------------------- ANOMALIES --------------------------------

def detecter_anomalies(cfg: dict, vues: dict) -> list[str]:
    """Compare la cote la plus récente à la plus ancienne de l'historique.

    Retourne une liste de messages Telegram (HTML) à envoyer.
    """
    seuil_chute = float(cfg.get("anomalies", {}).get("seuil_chute", 0.30))
    seuil_hausse = float(cfg.get("anomalies", {}).get("seuil_hausse", 0.50))
    messages = []

    for nom, entrees in historique().items():
        if len(entrees) < 3:
            continue  # pas assez de recul
        ancienne, recente = entrees[0]["cote"], entrees[-1]["cote"]
        if ancienne <= 0:
            continue
        variation = (recente - ancienne) / ancienne

        alerte = None
        if variation <= -seuil_chute:
            alerte = (f"⚠️ <b>COTE EN CHUTE</b> : {nom}\n"
                      f"📉 {ancienne:.2f}€ → {recente:.2f}€ ({variation * 100:+.0f}%)\n"
                      f"Prudence : possible vague de contrefaçons ou réimpression. "
                      f"Vérifie avant d'acheter, et si tu l'as en stock, envisage de vendre.")
        elif variation >= seuil_hausse:
            alerte = (f"🚀 <b>COTE EN FORTE HAUSSE</b> : {nom}\n"
                      f"📈 {ancienne:.2f}€ → {recente:.2f}€ ({variation * 100:+.0f}%)\n"
                      f"La carte devient recherchée : priorité aux alertes d'achat sur celle-ci.")
        if not alerte:
            continue

        # Anti-spam : une alerte anomalie par carte toutes les 48h
        cle = f"anomalie-{nom}"
        if time.time() - vues.get(cle, {}).get("ts", 0) < 48 * 3600:
            continue
        vues[cle] = {"ts": time.time()}
        messages.append(alerte)
        log.info("Anomalie détectée sur '%s' : %+.0f%%", nom, variation * 100)

    return messages


# ------------------------ RÉCAPITULATIF 21H ----------------------------

def recap_du_jour(cfg: dict, vues: dict) -> str | None:
    """Retourne le message de récap si on est dans la fenêtre d'envoi (sinon None)."""
    heure_cible = int(cfg.get("rapport", {}).get("heure", 21))
    if not cfg.get("rapport", {}).get("actif", True):
        return None

    maintenant = datetime.now(PARIS)
    if maintenant.hour != heure_cible:
        return None

    jour = maintenant.strftime("%Y-%m-%d")
    cle = f"rapport-{jour}"
    if cle in vues:  # déjà envoyé aujourd'hui
        return None
    vues[cle] = {"ts": time.time()}

    s = _charger_stats().get(jour, {"scans": 0, "annonces": 0, "deals": 0, "profit_potentiel": 0.0})
    
    # Profit cumulé sur les 30 derniers jours
    tous_stats = _charger_stats()
    profit_cumule = sum(st.get("profit_potentiel", 0) for st in tous_stats.values())

    # État du stock
    lignes_stock = []
    multiplicateur = float(cfg["regles"].get("multiplicateur_revente", 2.0))
    for achat in (cfg.get("mes_achats") or []):
        nom, prix = achat.get("nom"), achat.get("prix_achat")
        if not nom or not prix:
            continue
        cote = achat.get("cote") or cote_lissee(nom)
        if cote:
            progression = float(cote) / (float(prix) * multiplicateur) * 100
            lignes_stock.append(f"  • {nom} : cote {float(cote):.0f}€ ({min(progression, 999):.0f}% de l'objectif)")

    msg = (f"📊 <b>PokéDeals — Récap du {maintenant.strftime('%d/%m/%Y')}</b>\n"
           f"🔍 {s['scans']} scans, {s['annonces']} annonces analysées\n"
           f"🔥 {s['deals']} deal(s) détecté(s)"
           + (f" — profit du jour : <b>{s['profit_potentiel']:.0f}€</b>" if s["deals"] else "")
           + f"\n💎 <b>Profit cumulé (30j) : {profit_cumule:.0f}€</b>\n")
    if lignes_stock:
        msg += "📦 <b>Ton stock :</b>\n" + "\n".join(lignes_stock) + "\n"
    msg += "📈 Historique complet des deals : fichier <code>data/deals.csv</code> sur ton dépôt GitHub."
    return msg




def collecter(carte: dict, cfg: dict, secrets: dict) -> tuple[list[dict], list[dict]]:
    """Interroge les 3 plateformes en parallèle. Retourne (annonces, annonces_ebay)."""
    nom, langue = carte["nom"], carte.get("langue", "fr")
    plateformes = cfg["plateformes"]

    # Plafond de prix envoyé à Vinted pour réduire le bruit :
    # cote lissée connue -> on ne demande que les annonces sous le seuil d'achat
    prix_plafond = None
    cote_connue = carte.get("cote") or cote_lissee(nom)
    if cote_connue:
        prix_plafond = round(float(cote_connue) * (1 - cfg["regles"]["marge_achat"]), 2)

    taches = {}
    with ThreadPoolExecutor(max_workers=3) as pool:
        if plateformes.get("ebay"):
            taches["ebay"] = pool.submit(ebay_rechercher, nom, langue, secrets)
        if plateformes.get("vinted"):
            taches["vinted"] = pool.submit(vinted_rechercher, nom, langue, 30, prix_plafond)
        if plateformes.get("leboncoin"):
            taches["leboncoin"] = pool.submit(lbc_rechercher, nom, langue)

    resultats = {}
    for cle, fut in taches.items():
        try:
            resultats[cle] = fut.result(timeout=60)
        except Exception as e:  # noqa: BLE001
            log.warning("Plateforme %s en erreur pour '%s' : %s", cle, nom, e)
            resultats[cle] = []

    annonces_ebay = resultats.get("ebay", [])
    annonces = annonces_ebay + resultats.get("vinted", []) + resultats.get("leboncoin", [])
    # On attache le nom de la carte à chaque annonce (utile aux filtres)
    for a in annonces:
        a["carte"] = nom
    return annonces, annonces_ebay




def grouper_deals_par_scan(deals_list: list) -> list:
    """Groupe les deals par scan, max 10 par message (anti-spam)."""
    if not deals_list:
        return []
    # Trier par profit décroissant
    deals_tries = sorted(deals_list, key=lambda d: d["profit_net_estime"], reverse=True)
    # Grouper par tranches de 10
    groupes = []
    for i in range(0, len(deals_tries), 10):
        groupes.append(deals_tries[i:i+10])
    return groupes


def main() -> int:
    debut = time.time()
    cfg = charger_config()
    secrets = secrets_env()
    vues = charger_vues()

    nouveaux_deals: list[dict] = []
    total_annonces = 0

    for carte in cfg["watchlist"]:
        nom = carte["nom"]
        log.info("=== %s (%s) ===", nom, carte.get("langue", "fr").upper())

        annonces, annonces_ebay = collecter(carte, cfg, secrets)
        total_annonces += len(annonces)

        cote, confiance = obtenir_cote(carte, annonces_ebay, cfg)
        if cote:
            log.info("Cote retenue : %.2f€ (confiance : %s annonces) — %d annonces analysées",
                     cote, confiance, len(annonces))

        for annonce in annonces:
            marge_carte = carte.get("marge_achat")  # override par carte si présent
            deal, status = evaluate(annonce, cote, cfg, confiance, marge_carte)
            if deal is None:
                continue
            if deja_vue(vues, deal["id"]):
                continue
            log.info("  ✓ DEAL : %s à %.2f€ (cote %.2f€)", deal["titre"][:60], deal["total"], cote)
            nouveaux_deals.append(deal)
            marquer(vues, deal["id"])

        # Pause aléatoire courte entre les cartes (la parallélisation
        # compense largement : le scan reste ~3x plus rapide qu'avant)
        time.sleep(random.uniform(1.5, 3.5))

    # --- Suivi du stock : alertes de REVENTE (cote >= 2x prix d'achat) ---
    alertes_vente = verifier_stock(cfg, secrets, vues)

    # Tri : les affaires les plus rentables en premier
    nouveaux_deals.sort(key=lambda d: d["profit_net_estime"], reverse=True)

    log.info("Analyse terminée en %.0fs : %d annonces, %d nouveau(x) deal(s), %d alerte(s) de vente",
             time.time() - debut, total_annonces, len(nouveaux_deals), len(alertes_vente))

    notif = cfg.get("notifications", {"telegram": True, "email": True})
    if nouveaux_deals:
        if notif.get("telegram") and "telegram" in cfg:
            envoyer_telegram(nouveaux_deals, cfg["telegram"], secrets["TELEGRAM_BOT_TOKEN"])
        if notif.get("email") and "email" in cfg:
            envoyer_alertes(nouveaux_deals, cfg["email"], secrets["GMAIL_APP_PASSWORD"])
    if alertes_vente and notif.get("telegram") and "telegram" in cfg:
        envoyer_telegram_ventes(alertes_vente, cfg["telegram"], secrets["TELEGRAM_BOT_TOKEN"])

    # --- Stats du jour + export CSV de l'historique des deals ---
    enregistrer_scan(total_annonces, nouveaux_deals)
    exporter_csv(nouveaux_deals)

    # --- Détection d'anomalies de cote (chute >=30% / hausse >=50%) ---
    anomalies = detecter_anomalies(cfg, vues)
    if anomalies and notif.get("telegram") and "telegram" in cfg:
        envoyer_telegram_texte(anomalies, cfg["telegram"], secrets["TELEGRAM_BOT_TOKEN"])

    # --- Récapitulatif quotidien (envoyé une fois, vers 21h heure de Paris) ---
    recap = recap_du_jour(cfg, vues)
    if recap and notif.get("telegram") and "telegram" in cfg:
        envoyer_telegram_texte([recap], cfg["telegram"], secrets["TELEGRAM_BOT_TOKEN"])

    sauvegarder_vues(vues)
    sauvegarder_historique()
    return 0


if __name__ == "__main__":
    sys.exit(main())
