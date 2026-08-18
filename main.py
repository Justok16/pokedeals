"""PokéDeals — bot d'arbitrage de cartes Pokémon (système historique).

Il lit config.yaml, scanne eBay/Vinted/Leboncoin, calcule les cotes,
filtre les faux positifs et envoie les alertes Telegram (+ email si activé).
Depuis le 16/08/2026, un découpage progressif et prudent en extrait les
fonctions les plus autonomes vers des modules dédiés (cf. SESSION_NOTES.md) :
la normalisation de texte et le filtre de pertinence des annonces vivent
désormais dans filtre_annonces.py, ré-importés ici.

V15 : le NUMÉRO de collection (ex. 199/165) devient OBLIGATOIRE.
- Chaque carte de la watchlist doit inclure son numéro dans son nom
  (ex. "Dracaufeu ex 199/165"). Le numéro part automatiquement dans les
  requêtes eBay/Vinted/Leboncoin.
- Une annonce SANS numéro dans le titre est écartée (cote ET alertes) :
  impossible de distinguer un Dracaufeu commun à 5€ d'une version rare.
- Purge de l'historique des cotes antérieures à V15 (valeurs polluées).

V16 : langues étrangères + eBay international.
- Chaque carte a une langue (fr/jp/en/kr/cn). Une carte non-FR n'est
  retenue que si le titre mentionne sa langue ; une carte FR rejette
  tout titre mentionnant une langue étrangère (les versions JP/KR/CN,
  bien moins chères, ne contaminent plus les cotes françaises).
- Champ optionnel "alias" par carte : nom alternatif du Pokémon
  (ex. nom "Blastoise ex 200/165" + alias "Tortank").
- eBay international : annonces livrables en France, port plafonné
  (regles.ebay_international / frais_port_max_international).

V26 : DEUX CORRECTIONS MAJEURES.
1. Les clés de l'historique des cotes intègrent désormais la LANGUE.
   Avant, une carte présente en JP et en KR sous le même nom partageait
   la même cote : la passe coréenne relisait le prix japonais et
   l'affichait comme sien, avec 0 annonce derrière. Toute annonce KR
   était donc comparée à un prix JP — fausse alerte assurée.
2. Preuve positive de français sur les annonces Vinted. Vinted ne
   fournit aucun pays exploitable : une italienne au titre neutre y
   était indiscernable d'une française et déclenchait des alertes.
"""
from __future__ import annotations

import base64
import csv
import json
import logging
import os
import random
import re
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("pokedeals")

from json_utils import ecrire_json_atomique as _ecrire_json_atomique  # noqa: E402


from http_utils import user_agent, requete_avec_retry  # noqa: E402


# ------------------- Normalisation de texte + filtre de pertinence -------------------
# Extrait dans filtre_annonces.py le 16/08/2026 (premier module du decoupage
# progressif de main.py, cf. SESSION_NOTES.md) : fonctions pures de
# normalisation de texte et de filtrage de pertinence des annonces
# (annonce_pertinente, extraire_numero, mots_requis, preuve_francais...).
from filtre_annonces import (  # noqa: E402
    normaliser,
    SUFFIXES_LANGUE,
    extraire_numero,
    numero_nu_voulu,
    mots_requis,
    preuve_francais,
    annonce_pertinente,
)


# =====================================================================
# V26 : PREUVE POSITIVE DE FRANÇAIS (annonces Vinted uniquement) — suite
# ---------------------------------------------------------------------
# _nom_neutre_entre_langues reste ICI (et non dans filtre_annonces.py) car
# elle depend de CT_NOMS_EN, defini plus bas dans ce fichier (table de
# correspondance FR->EN utilisee par le moteur de cote) -- une dependance
# vers l'avant qui sort du perimetre "texte pur" du module extrait.
# =====================================================================

def _nom_neutre_entre_langues(nom_carte: str) -> bool:
    """Le nom du Pokémon s'écrit-il pareil en français et en anglais ?

    'Dracaufeu ex 199/165' -> False : le nom prouve à lui seul la langue
    'Mew ex 205/165'       -> True  : le nom ne prouve rien

    Un Pokémon absent de CT_NOMS_EN est traité comme NEUTRE : mieux vaut
    exiger une preuve inutile que laisser passer une italienne.
    (CT_NOMS_EN est défini plus bas dans ce fichier ; Python ne résout le
    nom qu'au moment de l'appel, donc l'ordre n'a pas d'importance.)
    """
    mots = [m for m in mots_requis(nom_carte) if m != "mega"]
    if not mots:
        return True
    fr = mots[0]
    en = normaliser(CT_NOMS_EN.get(fr, ""))
    if not en:
        return True
    return en == fr


RACINE = os.path.dirname(os.path.abspath(__file__))


def charger_config(chemin: str | None = None) -> dict:
    chemin = chemin or os.path.join(RACINE, "config.yaml")
    with open(chemin, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # V20 : validation défensive du config. Comme il est édité à la main très
    # souvent, une faute de frappe (valeur en texte, structure cassée) doit
    # produire un message CLAIR plutôt qu'un crash obscur en plein scan.
    if not isinstance(cfg, dict):
        raise ValueError(
            "config.yaml invalide : le fichier ne contient pas une structure "
            "correcte (vérifie l'indentation et qu'il n'est pas vide).")

    # Valeurs par défaut de sécurité
    cfg.setdefault("regles", {})
    r = cfg["regles"]
    if not isinstance(r, dict):
        raise ValueError("config.yaml : la section 'regles' doit être un bloc de clés/valeurs.")
    r.setdefault("frais_port_max", 6.0)
    r.setdefault("marge_achat", 0.10)
    r.setdefault("marge_revente", 0.10)
    r.setdefault("frais_revente_estimes", 0.13)
    r.setdefault("cote_min", 5.0)
    r.setdefault("prix_max", 0)  # 0 = illimité
    r.setdefault("ebay_international", False)
    r.setdefault("frais_port_max_international", 10.0)

    # Toutes les règles numériques doivent être des nombres (pas du texte).
    cles_numeriques = ["frais_port_max", "marge_achat", "marge_revente",
                       "frais_revente_estimes", "cote_min", "prix_max",
                       "frais_port_max_international"]
    for cle in cles_numeriques:
        try:
            r[cle] = float(r[cle])
        except (TypeError, ValueError):
            raise ValueError(
                f"config.yaml : la règle '{cle}' vaut '{r[cle]}' qui n'est pas "
                f"un nombre. Corrige-la (ex. {cle}: 0.30 sans guillemets).")
    # Bornes de bon sens
    if not (0 <= r["marge_achat"] < 1):
        raise ValueError(f"config.yaml : marge_achat doit être entre 0 et 1 (actuel : {r['marge_achat']}).")
    if not (0 <= r["frais_revente_estimes"] < 1):
        raise ValueError(f"config.yaml : frais_revente_estimes doit être entre 0 et 1 (actuel : {r['frais_revente_estimes']}).")

    cfg.setdefault("watchlist", [])
    cfg.setdefault("etats_acceptes", [])
    cfg.setdefault("etats_refuses", [])
    cfg.setdefault("cote", {"coefficient_marche": 0.92, "minimum_annonces": 4})
    cfg.setdefault("plateformes", {"ebay": True, "vinted": True, "leboncoin": True})
    cfg.setdefault("api_cotes", {"actif": False, "mode": "observation"})

    if not isinstance(cfg["watchlist"], list):
        raise ValueError("config.yaml : 'watchlist' doit être une liste de cartes (chaque ligne commençant par '- nom:').")
    if not cfg["watchlist"]:
        raise ValueError("La watchlist est vide : ajoute des cartes dans config.yaml")

    # Chaque carte doit être un dictionnaire avec un 'nom' non vide.
    for i, carte in enumerate(cfg["watchlist"], 1):
        if not isinstance(carte, dict):
            raise ValueError(f"config.yaml : la carte n°{i} de la watchlist est mal formée (il manque peut-être 'nom:').")
        if not str(carte.get("nom", "")).strip():
            raise ValueError(f"config.yaml : la carte n°{i} de la watchlist n'a pas de 'nom'.")

    # V15 : avertir (sans bloquer) si une carte n'a pas de numéro dans son nom.
    # Les versions volontairement sans numéro (SIR) peuvent l'omettre, mais
    # toute carte classique DOIT l'avoir, sinon retour des fausses cotes.
    for carte in cfg["watchlist"]:
        if not extraire_numero(carte.get("nom", "")):
            log.warning("⚠️ '%s' n'a pas de numéro (ex. 199/165) dans config.yaml : "
                        "filtrage V15 dégradé pour cette carte", carte.get("nom"))

    return cfg


def secrets_env() -> dict:
    """Secrets injectés par GitHub Actions (jamais écrits dans le code)."""
    return {
        "EBAY_CLIENT_ID": os.environ.get("EBAY_CLIENT_ID", ""),
        "EBAY_CLIENT_SECRET": os.environ.get("EBAY_CLIENT_SECRET", ""),
        "GMAIL_APP_PASSWORD": os.environ.get("GMAIL_APP_PASSWORD", ""),
        "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", ""),
        "CARDTRADER_TOKEN": os.environ.get("CARDTRADER_TOKEN", ""),
        # Optionnel : active la verification photo (cf. verification_photo.py).
        # Absent -> comportement inchange (avertissement generique existant).
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", ""),
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
    _ecrire_json_atomique(FICHIER_SEEN, vues, ensure_ascii=False, indent=1)


def deja_vue(vues: dict, annonce_id: str) -> bool:
    return annonce_id in vues


def marquer(vues: dict, annonce_id: str) -> None:
    vues[annonce_id] = {"ts": time.time()}


# V46 : mutualise le mécanisme "anti-spam" (une alerte par clé, pas plus
# souvent que `duree_secondes`) qui était copié-collé à l'identique à trois
# endroits (verifier_stock, detecter_anomalies, et l'alerte d'écart entre
# langues) avec le même bug potentiel si on oubliait de marquer après coup.
# Réutilise `vues` (déjà persisté dans data/seen.json) comme stockage : les
# clés d'anti-spam ("vente-...", "anomalie-...", "ecart-langues-...") vivent
# à côté des identifiants d'annonces, distinguées par leur préfixe.
def anti_spam(vues: dict, cle: str, duree_secondes: float) -> bool:
    """True si une alerte peut partir pour `cle` (silence écoulé) — et marque
    alors `cle` comme envoyée maintenant. False si on est encore dans la
    période de silence (rien n'est marqué, on pourra ré-essayer plus tard)."""
    if time.time() - vues.get(cle, {}).get("ts", 0) < duree_secondes:
        return False
    vues[cle] = {"ts": time.time()}
    return True


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


def ebay_rechercher(nom_carte: str, langue: str, secrets: dict, limite: int = 40,
                    cfg_regles: dict | None = None, alias: str = "") -> list[dict]:
    """Retourne les annonces eBay en achat immédiat pour une carte.

    V15 : le numéro de collection contenu dans `nom_carte` (ex. 199/165)
    part tel quel dans la requête eBay.
    V16 : si regles.ebay_international est actif, on cherche tout ce qui
    est LIVRABLE en France (port <= frais_port_max_international) au lieu
    de se limiter aux annonces situées en France.
    V17.5 : si un `alias` est fourni (nom alternatif du Pokémon, ex.
    "Tortank" pour "Blastoise"), on lance AUSSI une recherche eBay sur
    l'alias et on fusionne. Sans ça, une annonce titrée uniquement avec
    l'alias (« carte Tortank ex 202 japonaise ») n'était jamais remontée,
    car la requête ne portait que sur le nom principal.
    """
    token = _obtenir_token(secrets["EBAY_CLIENT_ID"], secrets["EBAY_CLIENT_SECRET"])
    if not token:
        return []

    regles = cfg_regles or {}
    international = bool(regles.get("ebay_international"))
    port_max_intl = float(regles.get("frais_port_max_international", 10.0))

    filtre = "buyingOptions:{FIXED_PRICE},priceCurrency:EUR"
    filtre += ",deliveryCountry:FR" if international else ",itemLocationCountry:FR"
    suffixe = SUFFIXES_LANGUE.get(langue, "")

    def _une_recherche(terme: str) -> list[dict]:
        """Interroge eBay pour un terme et renvoie les annonces brutes."""
        requete = f"carte pokemon {terme}{suffixe}"
        try:
            r = requete_avec_retry(
                requests.get,
                BROWSE_URL,
                headers={
                    "Authorization": f"Bearer {token}",
                    "X-EBAY-C-MARKETPLACE-ID": MARKETPLACE,
                },
                params={"q": requete, "limit": str(limite), "filter": filtre},
                timeout=25,
            )
            r.raise_for_status()
            return r.json().get("itemSummaries", []) or []
        except Exception as e:  # noqa: BLE001
            log.error("Recherche eBay '%s' échouée : %s", terme, e)
            return []

    # Recherche sur le nom principal, + sur l'alias si fourni.
    # On construit le nom recherché pour l'alias en remplaçant le Pokémon
    # dans le nom de carte (on garde numéro/type) : "Blastoise ex 202" +
    # alias "Tortank" -> on cherche aussi "Tortank ex 202".
    items = _une_recherche(nom_carte)
    alias_norm = normaliser(alias) if alias else ""
    if alias and alias_norm not in normaliser(nom_carte):
        terme_alias = nom_carte
        pokemon_principal = next((m for m in mots_requis(nom_carte) if m != "mega"), None)
        if pokemon_principal:
            # remplace le nom du Pokémon (insensible à la casse) par l'alias.
            # On échappe le motif (re.escape) et le remplacement (\\ -> \\\\)
            # au cas où un nom/alias contiendrait un caractère spécial regex.
            remplacement = alias.replace("\\", "\\\\")
            terme_alias = re.sub(re.escape(pokemon_principal), remplacement,
                                 nom_carte, flags=re.IGNORECASE)
        if terme_alias == nom_carte:  # rien remplacé : on préfixe l'alias
            terme_alias = f"{alias} {nom_carte}"
        items = items + _une_recherche(terme_alias)

    annonces = []
    vus_ids = set()
    for it in items:
        item_id = it.get("itemId", "")
        if item_id and item_id in vus_ids:
            continue  # annonce déjà captée par l'autre recherche
        if item_id:
            vus_ids.add(item_id)
        try:
            prix = float(it["price"]["value"])
        except (KeyError, ValueError, TypeError):
            continue
        # Sécurité : ne jamais mélanger des devises dans les cotes
        if (it.get("price", {}).get("currency") or "EUR") != "EUR":
            continue
        # V39 : port = None tant qu'on ne sait pas. AVANT, port valait 0.0
        # par défaut, donc une annonce FRANÇAISE sans "shippingOptions"
        # disponible dans la réponse eBay était traitée comme "port
        # gratuit" — alors que le vrai port pouvait être de 15-20€ sur une
        # carte chère. Le garde-fou "port inconnu -> prudence" n'existait
        # jusqu'ici que pour les annonces ÉTRANGÈRES (international) ; les
        # annonces françaises n'avaient aucune protection équivalente.
        # On prend aussi le port LE PLUS BAS parmi toutes les options
        # proposées (pas seulement la première, qui n'est pas forcément
        # la moins chère).
        port = None
        opts = it.get("shippingOptions") or []
        for option in opts:
            try:
                cout = float(option["shippingCost"]["value"])
            except (KeyError, ValueError, TypeError):
                continue
            port = cout if port is None else min(port, cout)
        pays = ((it.get("itemLocation") or {}).get("country") or "FR").upper()
        if pays != "FR":
            if not international:
                continue
            if port is None:
                continue  # port inconnu depuis l'étranger : prudence
            if port > port_max_intl:
                continue
        elif port is None:
            # V39 : port inconnu pour une annonce FRANÇAISE -> on l'écarte
            # aussi, plutôt que de supposer 0€. Mieux vaut rater une
            # annonce que de comparer un faux "total" à la cote.
            continue
        annonces.append(
            {
                "plateforme": "eBay" if pays == "FR" else f"eBay ({pays})",
                "id": f"ebay-{item_id}",
                "titre": it.get("title", ""),
                "prix": prix,
                "port": port,
                "url": it.get("itemWebUrl", ""),
                "etat_texte": (it.get("condition") or "") + " " + it.get("title", ""),
                "image_url": (it.get("image") or {}).get("imageUrl", ""),
            }
        )
    return annonces


# ------------------- Suivi d'anciennete -------------------
# Extrait dans moteur_cote.py le 17/08/2026, avec le reste du moteur de
# cote (cf. import plus bas, juste avant le moteur de cote proprement dit).
# calculer_cote() n'est jamais appelee directement par main.py (seulement
# par obtenir_cote(), restee dans moteur_cote.py) : pas reimportee ici.
from moteur_cote import sauvegarder_anciennete  # noqa: E402


# =====================================================================
# V21 : COTES CARDMARKET AUTOMATIQUES via l'API TCGdex (gratuite)
# ---------------------------------------------------------------------
# Problème résolu : les cotes eBay reflètent les prix DEMANDÉS (les
# annonces au juste prix partent vite, les surcotées s'accumulent), ce
# qui gonfle la médiane sur les cartes peu liquides. TCGdex republie les
# prix tendance Cardmarket — la vraie référence du marché — pour les
# cartes occidentales ET japonaises.
# Mode "observation" : les prix API sont seulement AFFICHÉS dans les
# logs, à côté des cotes eBay, pour vérification humaine. Mode "actif" :
# ils REMPLACENT la cote (sauf cote manuelle, toujours prioritaire).
# Les cartes coréennes ne sont pas cotées par Cardmarket : elles restent
# sur le système eBay quoi qu'il arrive.
# =====================================================================
# ------------------- Connecteur Cardtrader -------------------
# Extrait dans connecteur_cardtrader.py le 17/08/2026 (troisieme module du
# decoupage progressif de main.py, cf. SESSION_NOTES.md) : integration
# Cardtrader (recherche de blueprint, prix de marche, garde-fous de
# coherence, calibration eBay -> marche reel).
from connecteur_cardtrader import (  # noqa: E402
    CT_NOMS_EN,
    _ct_charger_cache,
    _ct_sauver_cache,
    _ct_trouver_blueprint,
    _ct_incoherent_entre_langues,
    _ct_memoriser_prix,
    _calibration_ajouter,
    _calibration_coefficient,
    _calibration_paires,
    _ct_cfg,
    cardtrader_prix,
)
import connecteur_cardtrader  # noqa: E402  -- acces qualifie a _ct_cache (cf. cardmarket_prix, plus bas)


# =====================================================================
# V33 : PRIX CARDMARKET OFFICIELS (fichier public, gratuit, légal)
# ---------------------------------------------------------------------
# Cardmarket publie lui-même, une fois par jour, un fichier contenant le
# prix ("trend" = tendance) de TOUTES ses cartes. Ce fichier est officiel
# et gratuit — pas de scan du site, pas de risque de blocage.
# Chaque carte y est identifiée par un numéro (idProduct) plutôt que par
# un nom. C'est justement ce numéro que Cardtrader connaît déjà sous le
# nom "cardmarket_id" dans chaque blueprint (vérifié en production le
# 26/07/2026 : Bulbizarre 166/165 FR -> cardmarket_id 271439, qui
# correspond bien à une entrée du fichier de prix).
#
# On télécharge ce fichier UNE FOIS par jour (pas à chaque scan) et on le
# garde en mémoire. Cette étape se contente de le charger ; il n'est pas
# encore utilisé dans le calcul des cotes.
# =====================================================================
CM_PRICEGUIDE_URL = "https://downloads.s3.cardmarket.com/productCatalog/priceGuide/price_guide_6.json"
CM_CACHE_FICHIER = os.path.join(RACINE, "data", "cardmarket_prix.json")
CM_CACHE_DUREE = 20 * 3600  # ~1 fois par jour
_cm_prix_par_id: dict = {}   # idProduct -> tendance (trend)
_cm_charge_le: float = 0.0


def _cm_charger_guide_prix() -> None:
    """Charge en mémoire le fichier de prix Cardmarket (idProduct -> trend),
    en le retéléchargeant seulement si le cache local a plus de 20h."""
    global _cm_prix_par_id, _cm_charge_le
    if _cm_prix_par_id and (time.time() - _cm_charge_le) < CM_CACHE_DUREE:
        return  # déjà chargé récemment, rien à faire

    # 1) Cache disque : évite de re-télécharger si le fichier local est frais
    if os.path.exists(CM_CACHE_FICHIER):
        age = time.time() - os.path.getmtime(CM_CACHE_FICHIER)
        if age < CM_CACHE_DUREE:
            try:
                with open(CM_CACHE_FICHIER, "r", encoding="utf-8") as f:
                    _cm_prix_par_id = json.load(f)
                _cm_charge_le = time.time()
                log.info("[Cardmarket] guide des prix chargé depuis le cache "
                         "local (%d cartes)", len(_cm_prix_par_id))
                return
            except (OSError, ValueError):
                pass  # cache corrompu : on retélécharge

    # 2) Téléchargement du fichier officiel
    try:
        r = requests.get(CM_PRICEGUIDE_URL, timeout=60)
        r.raise_for_status()
        data = r.json()
        guides = data.get("priceGuides", [])
        _cm_prix_par_id = {
            str(g["idProduct"]): g.get("trend")
            for g in guides if g.get("idProduct") and g.get("trend")
        }
        _cm_charge_le = time.time()
        log.info("[Cardmarket] guide des prix téléchargé : %d cartes avec prix "
                 "(sur %d au total)", len(_cm_prix_par_id), len(guides))
        _ecrire_json_atomique(CM_CACHE_FICHIER, _cm_prix_par_id)
    except Exception as e:  # noqa: BLE001
        log.warning("[Cardmarket] échec du téléchargement du guide des prix : %s", e)


def cardmarket_prix(carte: dict, token: str) -> float | None:
    """Prix Cardmarket officiel ("trend") d'une carte, via son cardmarket_id.

    Le cardmarket_id est déjà connu grâce à _ct_trouver_blueprint (V33) :
    Cardtrader le fournit directement dans chaque blueprint. On le
    retrouve donc dans le cache blueprint, sans appel réseau
    supplémentaire, puis on cherche son prix dans le guide des prix
    Cardmarket téléchargé une fois par jour.
    Retourne None si la carte n'a pas de cardmarket_id connu, ou si son
    prix n'est pas dans le guide.
    """
    _cm_charger_guide_prix()  # ne re-télécharge que si le cache a expiré
    if not _cm_prix_par_id:
        return None  # guide indisponible (échec réseau) : pas bloquant

    # Le cardmarket_id est trouvé UNIQUEMENT lors de la résolution du
    # blueprint (_ct_trouver_blueprint). On appelle cette fonction pour
    # être sûr qu'il est en cache — elle ne refait aucun travail si c'est
    # déjà le cas (voir la vérification d'âge en tout début de fonction).
    _ct_trouver_blueprint(carte, token)

    cle = f"{carte.get('langue','fr')}|{carte['nom']}"
    # Acces qualifie (connecteur_cardtrader._ct_cache), pas un import direct
    # du nom : _ct_charger_cache() REASSIGNE ce dict (pas juste .update()),
    # un `from connecteur_cardtrader import _ct_cache` figerait la liaison
    # sur l'ancien objet et lirait un cache perime en permanence.
    ent = connecteur_cardtrader._ct_cache["blueprints"].get(cle) or {}
    cm_id = ent.get("cm_id")
    if not cm_id:
        return None

    prix = _cm_prix_par_id.get(str(cm_id))
    if prix:
        log.info("    [Cardmarket] '%s' (cardmarket_id=%s) : tendance officielle %.2f€",
                 carte["nom"], cm_id, prix)
    return prix


# ------------------- Connecteur TCGdex -------------------
# Extrait dans connecteur_tcgdex.py le 17/08/2026 (quatrieme module du
# decoupage progressif de main.py, cf. SESSION_NOTES.md) : integration
# TCGdex (repli quand Cardtrader n'a rien, republie les prix tendance
# Cardmarket).
from connecteur_tcgdex import (  # noqa: E402
    _api_charger_cache,
    _api_sauver_cache,
    api_prix_carte,
)

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


# V50 (17/08/2026) : compteurs de FIABILITÉ Vinted/Leboncoin, remis à zéro
# à chaque cycle (cf. main()). Un "échec" ici = une vraie exception/erreur
# réseau dans le bloc try/except de la fonction -- jamais un 0 résultat
# légitime, ni un blocage 403/429 Leboncoin (déjà documenté comme un
# comportement anti-bot ROUTINE, pas une panne). Objectif : détecter qu'un
# connecteur est CASSÉ (ex. Vinted change son API/ses cookies) avant que ça
# ne passe inaperçu pendant des jours -- cf. verifier_fiabilite_plateformes()
# plus bas, appelée une fois par cycle dans main().
from stats_fiabilite import _stats_fiabilite  # noqa: E402


def _reinitialiser_stats_fiabilite() -> None:
    for cle in _stats_fiabilite:
        _stats_fiabilite[cle] = 0


def vinted_rechercher(nom_carte: str, langue: str, limite: int = 30, prix_plafond: float | None = None) -> list[dict]:
    _stats_fiabilite["vinted_appels"] += 1
    s = _get_vinted_session()
    if s is None:
        _stats_fiabilite["vinted_echecs"] += 1
        return []
    requete = f"carte pokemon {nom_carte}"
    requete += SUFFIXES_LANGUE.get(langue, "")
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
        _stats_fiabilite["vinted_echecs"] += 1
        return []

    annonces = []
    for it in items:
        try:
            prix = float(it["price"]["amount"])
        except (KeyError, ValueError, TypeError):
            continue
        # V15 : frais de protection acheteur Vinted = 0,7€ fixe + 5% du prix
        frais_protection = 0.7 + (prix * 0.05)
        port_total = 3.5 + frais_protection
        # V18 : le titre court Vinted ("Bulbizarre AR 166/165") ne mentionne
        # souvent PAS la langue ; c'est la DESCRIPTION qui dit "édition 151
        # Jap". On concatène donc titre + description pour que le filtre de
        # langue voie ces indices et rejette les cartes japonaises vendues
        # sous une carte française du même numéro.
        titre_court = it.get("title", "")
        description = it.get("description", "") or ""
        texte_complet = f"{titre_court} {description}".strip()
        annonces.append(
            {
                "plateforme": "Vinted",
                "id": f"vinted-{it.get('id', '')}",
                "titre": texte_complet,
                "prix": prix,
                # Port Vinted (~3.5€) + frais de protection acheteur (0.7€ + 5%)
                "port": round(port_total, 2),
                "url": it.get("url") or f"{VINTED_BASE}/items/{it.get('id', '')}",
                "etat_texte": (it.get("status") or "") + " " + texte_complet,
                "image_url": (it.get("photo") or {}).get("url", ""),
            }
        )
    return annonces


VINTED_ITEM = VINTED_BASE + "/api/v2/items/"


def vinted_description(item_id: str) -> str | None:
    """Description complète d'une annonce Vinted.

    V25 : l'endpoint de RECHERCHE (/catalog/items) ne renvoie pas la
    description — seulement le titre. Or sur Vinted le titre est souvent
    neutre (« Bulbizarre AR 166/165 ») alors que la description trahit la
    langue (« Extension SV2a — Carte Japonaise »). On va donc chercher la
    description sur la fiche détaillée, mais UNIQUEMENT pour les annonces
    qui s'apprêtent à déclencher une alerte.

    V29 : la fonction distingue désormais DEUX situations que l'ancienne
    version confondait, avec des conséquences opposées :
      - None : la fiche n'a PAS pu être lue (réseau, 429, session
        expirée, annonce supprimée). On ne sait rien -> l'appelant doit
        s'abstenir d'alerter et réessayer au prochain scan.
      - ""   : la fiche a bien été lue, le vendeur n'a simplement rien
        écrit. Information exploitable.
    Avant, les deux renvoyaient "" : un simple incident réseau faisait
    donc passer une carte japonaise pour une carte française (cas vécu :
    Bulbizarre AR 166/165 japonais alerté contre la cote FR de 109,58€).
    """
    s = _get_vinted_session()
    if s is None or not item_id:
        log.info("    [Vinted] fiche %s illisible : pas de session", item_id)
        return None
    try:
        r = requete_avec_retry(s.get, VINTED_ITEM + str(item_id), timeout=20)
        # V30 : cookies expirés (401) ou blocage temporaire (403) -> on
        # refait UNE tentative avec une session neuve, exactement comme le
        # fait déjà vinted_rechercher. Sans ça, une session périmée rendait
        # TOUTES les fiches illisibles, donc plus aucune alerte Vinted du
        # tout — et en silence.
        if r.status_code in (401, 403):
            global _vinted_session
            log.info("    [Vinted] fiche %s : HTTP %s, on renouvelle la session",
                     item_id, r.status_code)
            _vinted_session = None
            s = _get_vinted_session()
            if s is None:
                return None
            r = requete_avec_retry(s.get, VINTED_ITEM + str(item_id), timeout=20)
        if r.status_code != 200:
            # V30 : on journalise le CODE. Sans lui, impossible de savoir si
            # l'échec vient d'une session périmée, d'un blocage anti-bot ou
            # d'une annonce supprimée — et donc impossible de le corriger.
            log.info("    [Vinted] fiche %s illisible : HTTP %s", item_id, r.status_code)
            return None
        item = (r.json() or {}).get("item") or {}
        # V26 TEMPORAIRE (à retirer après 1 scan) : lister les champs
        # disponibles. Si la fiche expose un pays / une locale du vendeur,
        # on remplacera la détection par vocabulaire par un vrai filtre
        # de localisation, comme sur eBay.
        log.info("    [Vinted debug] champs disponibles : %s", sorted(item.keys()))
        return str(item.get("description") or "")
    except Exception as e:  # noqa: BLE001 — ne doit jamais casser le scan
        log.info("    [Vinted] fiche %s illisible : %s (%s)",
                 item_id, type(e).__name__, str(e)[:80])
        return None


# ------------------- Connecteur Leboncoin -------------------
# Extrait dans connecteur_leboncoin.py le 17/08/2026 (sixieme module du
# decoupage progressif de main.py, cf. SESSION_NOTES.md) : recherche API
# + extraction des annonces depuis les emails d'alerte Leboncoin.
from connecteur_leboncoin import (  # noqa: E402
    lbc_rechercher,
    lbc_relever_alertes_email,
)


# ------------------- Moteur de cote -------------------
# Extrait dans moteur_cote.py le 17/08/2026 (septieme module du decoupage
# progressif de main.py, cf. SESSION_NOTES.md) : calcul de la cote, cote
# lissee, persistance de l'historique, et evaluation d'une annonce contre
# la cote (evaluate). Recolle avec le suivi d'anciennete (plus haut dans
# main.py, cf. import juste avant _localisation_incoherente) et
# calculer_tendance_cote (utilisee par exporter_csv, plus bas).
from moteur_cote import (  # noqa: E402
    historique,
    sauvegarder_historique,
    cote_lissee,
    enregistrer_cote,
    obtenir_cote,
    evaluate,
    calculer_tendance_cote,
)


# ------------------- Notifications (Telegram + email) -------------------
# Extrait dans notifications_historique.py le 16/08/2026 (deuxieme module du
# decoupage progressif de main.py, cf. SESSION_NOTES.md) : formatage et envoi
# des messages Telegram/email (deals, ventes, messages libres).
from notifications_historique import (  # noqa: E402
    envoyer_telegram_texte,
    envoyer_telegram_ventes,
    envoyer_telegram,
    envoyer_alertes,
)




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
            annonces_ebay = ebay_rechercher(nom, achat.get("langue", "fr"), secrets, 40, cfg["regles"], achat.get("alias", ""))
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
        if not anti_spam(vues, f"vente-{nom}", RAPPEL_JOURS * 86400):
            continue

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
                "cote", "tendance_cote", "decote_pct", "prix_revente_conseille", "profit_net_estime",
                "vendeur_nom", "vendeur_note", "url"]


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
    _ecrire_json_atomique(FICHIER_STATS, stats, ensure_ascii=False, indent=1)


# ------------------------------ CSV -----------------------------------
# calculer_tendance_cote() vit desormais dans moteur_cote.py (reimportee
# plus haut avec le reste du moteur de cote) -- utilisee ici par exporter_csv().

def _proteger_csv(valeur) -> str:
    """Préfixe d'une apostrophe les valeurs commençant par =, +, -, @ : ces
    caractères sont interprétés comme le début d'une FORMULE par Excel et
    LibreOffice quand le CSV est ouvert. Un titre d'annonce vient d'un
    vendeur inconnu ; sans cette protection, un titre du genre
    "=HYPERLINK(...)" pourrait s'exécuter comme une formule à l'ouverture."""
    texte = str(valeur)
    return f"'{texte}" if texte.startswith(("=", "+", "-", "@")) else texte


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
            tendance = calculer_tendance_cote(d.get("carte", ""), d.get("langue", "fr"))
            w.writerow([maintenant, d.get("carte", ""), d["plateforme"], _proteger_csv(d["titre"]),
                        d["prix"], d["port"], d["total"], d["cote"], tendance, d["decote_pct"],
                        d["prix_revente_conseille"], d["profit_net_estime"],
                        _proteger_csv(d.get("vendeur_nom", "?")), f"{d.get('vendeur_pct', 100):.0f}%",
                        _proteger_csv(d["url"])])
    log.info("CSV : %d deal(s) ajouté(s) à data/deals.csv", len(deals))


# --------------------------- ANOMALIES --------------------------------

def detecter_anomalies(cfg: dict, vues: dict) -> list[str]:
    """Compare une moyenne RÉCENTE à une moyenne ANCIENNE de l'historique.

    Retourne une liste de messages Telegram (HTML) à envoyer.

    V42 : AVANT, la comparaison se faisait entre UN SEUL point ancien et
    UN SEUL point récent (entrees[0] et entrees[-1]). Une cote INSTANTANÉE
    peut sursauter d'un scan à l'autre sans que le vrai marché ait bougé —
    cas vécu : Evoli 188/167 est passée de 127,78€ à 226,59€ en un seul
    scan simplement parce que l'annonce à 80€ qui faisait partie du "bas
    du marché" a disparu (vendue), et deux annonces à prix DEMANDÉS jamais
    vendus (299,99€, 332,95€) ont dû la remplacer dans le calcul. Une
    alerte "+77%" est alors partie alors que la cote LISSÉE (celle qui
    sert réellement aux achats) n'avait quasiment pas bougé (127,78€
    inchangée). On compare désormais la moyenne des 2 valeurs les plus
    anciennes à la moyenne des 2 plus récentes : un sursaut isolé pèse
    deux fois moins et ne suffit plus, à lui seul, à déclencher l'alerte.
    """
    seuil_chute = float(cfg.get("anomalies", {}).get("seuil_chute", 0.30))
    seuil_hausse = float(cfg.get("anomalies", {}).get("seuil_hausse", 0.50))
    messages = []

    for cle, entrees in historique().items():
        if len(entrees) < 3:
            continue  # pas assez de recul
        # V26 : la clé vaut « Nom|langue » — on l'affiche proprement.
        nom_seul, _, lg = cle.partition("|")
        nom = f"{nom_seul} ({lg.upper()})" if lg else nom_seul
        valeurs = [e["cote"] for e in entrees]
        # V58 : `len(valeurs) // 2` retombe à 1 pour exactement 3 points
        # (division entière), ce qui redonne la comparaison À UN SEUL POINT
        # que V42 visait justement à éliminer — et cet état à 3 points est
        # celui que traverse CHAQUE carte juste après une purge
        # (PURGE_VERSION), donc pas un cas rare. `len(valeurs) - 1` reste
        # toujours ≥ 2 dès que la garde `len(entrees) < 3` ci-dessus est
        # passée, donc nb_lisse vaut systématiquement 2 (les 2 fenêtres se
        # chevauchent sur 1 point à 3 valeurs, ce qui amortit encore plus
        # la variation détectée — jamais un problème pour un détecteur
        # d'anomalies dont le but est d'éviter les faux positifs).
        nb_lisse = min(2, len(valeurs) - 1)
        ancienne = statistics.mean(valeurs[:nb_lisse])
        recente = statistics.mean(valeurs[-nb_lisse:])
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
        if not anti_spam(vues, f"anomalie-{cle}", 48 * 3600):
            continue
        messages.append(alerte)
        log.info("Anomalie détectée sur '%s' : %+.0f%%", nom, variation * 100)

    return messages


# V46 : au-delà de ce nombre de jours, une cote manuelle (champ `cote:` dans
# la watchlist) déclenche un rappel de revérification (voir fonction
# ci-dessous). Une cote manuelle fige un prix relevé à la main un jour donné
# ; sans rappel, elle peut devenir fausse en silence pendant des mois si
# personne n'y repense (cas vécu : 4 cotes manuelles datant de fin juillet
# 2026, jamais revérifiées depuis leur ajout).
COTE_MANUELLE_MAX_JOURS = 30


def verifier_cotes_manuelles_perimees(cfg: dict, vues: dict) -> list[str]:
    """Rappelle de revérifier les cotes manuelles trop anciennes.

    Une carte de la watchlist avec `cote: XX` ET `cote_date: "AAAA-MM-JJ"`
    déclenche un rappel Telegram si `cote_date` a plus de
    COTE_MANUELLE_MAX_JOURS jours. Sans `cote_date`, aucune vérification
    n'est possible (comportement inchangé) : le champ est optionnel, mais
    c'est lui qui active le rappel.
    """
    messages = []
    for carte in cfg.get("watchlist", []):
        cote = carte.get("cote")
        date_txt = carte.get("cote_date")
        if not cote or not date_txt:
            continue
        try:
            date_maj = datetime.strptime(str(date_txt), "%Y-%m-%d")
        except ValueError:
            log.warning("cote_date invalide pour %s : %r (attendu AAAA-MM-JJ)",
                        carte.get("nom"), date_txt)
            continue
        age_jours = (datetime.now(PARIS).date() - date_maj.date()).days
        if age_jours < COTE_MANUELLE_MAX_JOURS:
            continue
        nom = carte.get("nom", "?")
        langue = carte.get("langue", "fr")
        # Anti-spam : un seul rappel par carte par semaine tant qu'elle
        # n'est pas mise à jour dans config.yaml.
        if not anti_spam(vues, f"cote-perimee-{nom}|{langue}", 7 * 86400):
            continue
        messages.append(
            f"🗓️ <b>COTE MANUELLE À REVÉRIFIER</b> : {nom} ({langue.upper()})\n"
            f"Figée à {cote}€ le {date_txt} ({age_jours} jours). Revérifie le "
            f"prix réel (Cardmarket...) et mets à jour `cote_date` dans "
            f"config.yaml — ou retire la ligne `cote:` pour repasser au "
            f"calcul automatique.")
        log.info("Cote manuelle périmée : %s (%s, %d jours)", nom, langue.upper(), age_jours)

    return messages


# V50 : au-delà de ce nombre d'appels sur un cycle, un taux d'échec élevé
# devient un signal fiable (pas un hasard sur un tout petit échantillon --
# ex. un run de test manuel sur 2-3 cartes où Vinted a un pépin ponctuel).
SEUIL_MIN_APPELS_FIABILITE = 5
# 80% d'échecs RÉELS (pas de 0 résultat) sur un cycle entier : un connecteur
# qui fonctionne encore correctement échoue occasionnellement (réseau,
# timeout ponctuel), jamais presque systématiquement.
SEUIL_TAUX_ECHEC_FIABILITE = 0.8


# Anti-spam : pokedeals.yml tourne toutes les 15 min -- sans ça, une
# plateforme cassée déclencherait une alerte à CHAQUE cycle, en continu,
# jusqu'à la correction. Une alerte toutes les 6h reste largement assez
# réactif pour agir, sans noyer Justok de messages identiques.
DELAI_ANTI_SPAM_FIABILITE = 6 * 3600


def verifier_fiabilite_plateformes(vues: dict) -> list[str]:
    """Alerte si Vinted et/ou Leboncoin échouent de façon quasi systématique
    sur CE cycle -- signe probable d'un connecteur CASSÉ (ex. Vinted change
    son format d'API ou son mécanisme de cookies), à distinguer d'un échec
    isolé (réseau, timeout ponctuel) déjà toléré partout ailleurs dans le
    programme sans alerte. S'appuie sur _stats_fiabilite, alimenté par
    vinted_rechercher()/lbc_rechercher() au fil du cycle (cf. plus haut) --
    à appeler une fois, après la boucle complète sur la watchlist."""
    alertes = []
    for plateforme, cle_appels, cle_echecs in (
        ("Vinted", "vinted_appels", "vinted_echecs"),
        ("Leboncoin", "leboncoin_appels", "leboncoin_echecs"),
    ):
        appels = _stats_fiabilite[cle_appels]
        echecs = _stats_fiabilite[cle_echecs]
        if appels < SEUIL_MIN_APPELS_FIABILITE:
            continue
        taux = echecs / appels
        if taux < SEUIL_TAUX_ECHEC_FIABILITE:
            continue
        if not anti_spam(vues, f"fiabilite-{plateforme.lower()}", DELAI_ANTI_SPAM_FIABILITE):
            continue
        alertes.append(
            f"🚨 <b>{plateforme} semble cassé</b>\n"
            f"{echecs}/{appels} recherches en échec sur ce cycle ({taux * 100:.0f}%). "
            f"Vérifie si l'API a changé côté {plateforme} (format de réponse, "
            f"cookies/session, blocage anti-bot renforcé...).")
        log.warning("Fiabilité %s dégradée : %d/%d échecs (%.0f%%)",
                    plateforme, echecs, appels, taux * 100)
    return alertes


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
        cote = achat.get("cote") or cote_lissee(nom, achat.get("langue", "fr"))
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
    cote_connue = carte.get("cote") or cote_lissee(nom, langue)
    if cote_connue:
        prix_plafond = round(float(cote_connue) * (1 - cfg["regles"]["marge_achat"]), 2)

    # V49 (audit du 16/08/2026) : `with ThreadPoolExecutor(...) as pool:`
    # appelle shutdown(wait=True) a la SORTIE du bloc -- donc AVANT meme
    # d'atteindre la boucle .result(timeout=60) ci-dessous, qui attendait
    # deja (sans limite) la fin des 3 taches. Le "timeout=60" ne servait
    # donc a rien en pratique : un retry Vinted avec backoff (jusqu'a 3
    # tentatives de 25s + pauses progressives) peut a lui seul depasser 90s,
    # bloquant collecter() bien au-dela de la limite apparente. Pool géré
    # manuellement + shutdown(wait=False) : la tache lente continue en
    # arriere-plan jusqu'a son propre timeout HTTP interne, mais ne bloque
    # plus le scan des cartes suivantes.
    taches = {}
    pool = ThreadPoolExecutor(max_workers=3)
    try:
        if plateformes.get("ebay"):
            taches["ebay"] = pool.submit(ebay_rechercher, nom, langue, secrets, 40, cfg["regles"], carte.get("alias", ""))
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
    finally:
        pool.shutdown(wait=False, cancel_futures=True)

    annonces_ebay = resultats.get("ebay", [])
    annonces = annonces_ebay + resultats.get("vinted", []) + resultats.get("leboncoin", [])
    # On attache la carte, sa langue et son alias à chaque annonce (filtres)
    for a in annonces:
        a["carte"] = nom
        a["langue"] = langue
        a["alias"] = carte.get("alias", "")
        a["prix_max_fixe"] = carte.get("prix_max_fixe")
    return annonces, annonces_ebay


def main() -> int:
    debut = time.time()
    _reinitialiser_stats_fiabilite()  # V50 : un cycle frais, un compteur frais
    cfg = charger_config()
    _ct_charger_cache()  # V22 : cache Cardtrader (blueprints + prix du jour)
    _api_charger_cache()  # V47 : cache TCGdex (repli quand Cardtrader n'a rien)
    secrets = secrets_env()
    _cfg_api = cfg.get("api_cotes", {})
    _ct_cfg.update(_cfg_api)  # V24 : accessible aux fonctions de recherche
    if _cfg_api.get("actif"):
        log.info("Cardtrader : ACTIF (mode %s) — token %s",
                 _cfg_api.get("mode", "observation"),
                 "présent ✓" if secrets.get("CARDTRADER_TOKEN") else "ABSENT ✗ (secret GitHub manquant)")
    else:
        log.info("Cardtrader : désactivé (api_cotes.actif = false dans config.yaml)")
    vues = charger_vues()

    nouveaux_deals: list[dict] = []
    total_annonces = 0
    # V34 : mémorise la cote de chaque carte, groupée par "nom sans langue",
    # pour repérer en fin de scan les cas où une même carte a des cotes très
    # différentes selon la langue (JP/KR/FR...) — signe possible d'un
    # mélange de langue quelque part dans le calcul.
    cotes_par_carte: dict[str, list[tuple[str, float]]] = {}
    # V39 : identifiants des deals trouvés, marqués "vus" seulement après
    # un envoi de notification réussi (voir plus bas).
    deals_a_marquer: list[str] = []

    for carte in cfg["watchlist"]:
        nom = carte["nom"]
        log.info("=== %s (%s) ===", nom, carte.get("langue", "fr").upper())

        annonces, annonces_ebay = collecter(carte, cfg, secrets)
        total_annonces += len(annonces)

        cote, confiance = obtenir_cote(carte, annonces_ebay, cfg)
        cote_avant_correction = cote  # V47 : pour détecter un ajustement Cardtrader/TCGdex ci-dessous
        prix_cm_affiche = None  # V46 : prix Cardmarket affiché sur Telegram (info seule, jamais utilisé pour decider)

        # V22 : cote Cardtrader (marché européen, prix réels par langue).
        # mode "observation" = affiché seulement ; "actif" = remplace la cote.
        cfg_api = cfg.get("api_cotes", {})
        if cfg_api.get("actif"):
            nb_bas = int(cfg_api.get("nb_prix_bas", 5))
            min_ann = int(cfg_api.get("min_annonces", 3))
            if carte.get("langue") == "kr":
                # V47 : le coréen n'a AUCUN repli TCGdex possible (Cardmarket
                # ne cote pas le coréen) -- c'est la SEULE langue où
                # Cardtrader est le dernier rempart avant une cote eBay non
                # vérifiée. Seuil abaissé pour ces cartes uniquement (marché
                # coréen structurellement plus mince) : un peu de signal réel
                # Cardtrader, même sur 1-2 annonces, protège mieux qu'aucune
                # vérification croisée -- les GARDE-FOU 2 (élimination des
                # prix aberrants) et 4 (écart ×5 vs eBay) restent actifs et
                # limitent le risque d'une annonce isolée erronée.
                min_ann = int(cfg_api.get("min_annonces_kr", 1))
            prix_ct = cardtrader_prix(carte, secrets.get("CARDTRADER_TOKEN", ""), nb_bas, min_ann)
            if prix_ct is not None:
                # V22.7 GARDE-FOU 4 : vérification croisée avec la cote eBay.
                # Si les deux existent et s'écartent d'un facteur 5+, l'une
                # des deux est fausse (mauvaise correspondance de carte,
                # cf. Méga-Dracaufeu X trouvé à 3€ contre 1199€ eBay) : on
                # n'utilise PAS le prix Cardtrader et on le signale.
                suspect = bool(cote) and (prix_ct > cote * 5 or prix_ct < cote / 5)
                motif = f"cote eBay {cote:.2f}€" if suspect else ""
                # V24 GARDE-FOU 5 : cohérence ENTRE LANGUES. Indispensable
                # pour les cartes SANS cote eBay, que le garde-fou 4 ne peut
                # pas protéger (cf. Mew ex 208 sv2a : 51€ en JP, 5020€ en KR
                # alors qu'il s'achète à moins de 30€ sur Cardmarket).
                if not suspect:
                    facteur_lg = float(cfg_api.get("facteur_langues", 5))
                    suspect, motif = _ct_incoherent_entre_langues(carte, prix_ct, facteur_lg)
                if suspect:
                    log.warning("    [Cardtrader ⚠️] %s : prix %.2f€ INCOHÉRENT (%s) "
                                "-> Cardtrader ignoré pour cette carte",
                                nom, prix_ct, motif)
                else:
                    _ct_memoriser_prix(carte, prix_ct)
                    log.info("    [Cardtrader %s] %s ≈ %.2f€  (moyenne des %d plus bas)  —  cote eBay : %s",
                             carte.get("langue", "fr").upper(), nom, prix_ct, nb_bas,
                             f"{cote:.2f}€" if cote else "aucune")
                    # V23 : mémoriser l'écart pour calibrer les cartes que
                    # Cardtrader ne couvre pas.
                    _calibration_ajouter(cote or 0, prix_ct)

                    # V46 : prix Cardmarket calculé ICI (avant le if/elif de
                    # mode), pas seulement en mode "plus_bas" -- pour pouvoir
                    # l'AFFICHER dans le message Telegram quel que soit le
                    # mode actif, sans jamais influencer la cote retenue.
                    # Sûr par construction : on n'atteint ce point QUE si le
                    # prix Cardtrader vient de passer le GARDE-FOU 4 (cross-
                    # check eBay) ET le GARDE-FOU 5 (cohérence de langue)
                    # ci-dessus -- donc seulement quand on est déjà confiant
                    # que c'est la bonne carte, dans la bonne langue. Si l'un
                    # des deux avait échoué, "suspect" serait True et ce code
                    # ne serait jamais exécuté (cf. branche if suspect: ci-dessus).
                    prix_cm_affiche = cardmarket_prix(carte, secrets.get("CARDTRADER_TOKEN", ""))

                    # V27 : APPLICATION du prix Cardtrader selon le mode.
                    #   observation : le prix est seulement affiché
                    #   secours     : utilisé UNIQUEMENT si eBay n'a rien
                    #   actif       : remplace systématiquement la cote eBay
                    #   plus_bas    : V32 — on garde le prix le PLUS BAS entre
                    #     eBay et Cardtrader. Motif : les prix eBay sont des
                    #     prix DEMANDÉS, pas des prix payés. Une carte peut
                    #     rester affichée à 130€ pendant des mois sans se
                    #     vendre pendant que le vrai marché est à 70€. Prendre
                    #     le plus bas des deux sources se rapproche davantage
                    #     du prix réel qu'une seule source.
                    #     Sécurité : si les deux prix sont trop différents
                    #     (l'un fait plus du double de l'autre), c'est le
                    #     signe d'une erreur (mauvaise carte, gradée non
                    #     détectée...) -> on garde alors le PLUS HAUT des deux,
                    #     par prudence, plutôt que de foncer sur un prix qui
                    #     pourrait être une erreur.
                    #
                    # La cote MANUELLE (config.yaml) reste prioritaire dans
                    # tous les cas.
                    mode_ct = str(cfg_api.get("mode", "observation")).lower()
                    if carte.get("cote"):
                        pass  # cote manuelle : on ne touche à rien
                    elif mode_ct == "plus_bas":
                        # V33 : Cardmarket rejoint la comparaison comme
                        # troisième source. C'est la SEULE des trois qui
                        # donne un prix de VENTE réel plutôt qu'un prix
                        # demandé (vérifié : Bulbizarre 166/165 FR, eBay
                        # demandait 88€, Cardmarket vend réellement 65€).
                        # V46 : déjà calculé plus haut (prix_cm_affiche),
                        # réutilisé ici sous son ancien nom local pour ne
                        # rien changer à la logique de comparaison suivante.
                        prix_cm = prix_cm_affiche

                        candidats = [("eBay", cote)] if cote is not None else []
                        candidats.append(("Cardtrader", prix_ct))
                        if prix_cm is not None:
                            candidats.append(("Cardmarket", prix_cm))

                        valeurs = [v for _, v in candidats]
                        grand, petit = max(valeurs), min(valeurs)

                        if len(valeurs) >= 2 and grand > petit * 2:
                            # Écart trop important entre au moins deux sources :
                            # on se méfie, on garde la plus HAUTE par prudence
                            # plutôt que de foncer sur un prix qui pourrait
                            # être une erreur.
                            noms = ", ".join(f"{n}={v:.2f}€" for n, v in candidats)
                            log.info("    [Cotes] %s : écart trop important entre "
                                     "sources (%s) -> on garde la PLUS HAUTE (%.2f€)",
                                     nom, noms, grand)
                            cote, confiance = round(grand, 2), 97
                        elif petit != cote:
                            source_retenue = next(n for n, v in candidats if v == petit)
                            log.info("    [Cotes -> RETENU] %s : %s (%.2f€) est la "
                                     "source la plus basse", nom, source_retenue, petit)
                            cote, confiance = round(petit, 2), 98
                        # sinon eBay était déjà le plus bas : on ne touche à rien
                    elif mode_ct == "actif" or (mode_ct == "secours" and cote is None):
                        origine = "eBay muet" if cote is None else f"remplace {cote:.2f}€ eBay"
                        cote, confiance = round(prix_ct, 2), 98
                        log.info("    [Cardtrader -> COTE] %s (%s) : cote fixée à %.2f€ "
                                 "par Cardtrader (mode %s, %s)",
                                 nom, carte.get("langue", "fr").upper(), cote,
                                 mode_ct, origine)
            else:
                # V47 : Cardtrader n'a RIEN pour cette carte (ni annonce
                # marketplace -> prix_ct None, ni cm_id -> cardmarket_prix()
                # inatteignable non plus) : aucun des garde-fous existants ne
                # peut alors corriger une cote eBay isolée. TCGdex (Cardmarket
                # officiel, gratuit, INDÉPENDANT de Cardtrader) sert de repli.
                # Cas réel qui motive ce repli : Evoli ex 167/131, cote eBay
                # à 325,28€ (aucune annonce eBay proche du vrai prix) alors
                # que Cardmarket affichait ~145€ ; Cardtrader n'avait ni
                # marketplace ni cm_id pour cette carte (trop récente).
                mode_ct = str(cfg_api.get("mode", "observation")).lower()
                if mode_ct == "plus_bas" and not carte.get("cote"):
                    prix_tcgdex = api_prix_carte(carte)
                    if prix_tcgdex is not None:
                        prix_cm_affiche = prix_tcgdex
                        if cote is None:
                            cote, confiance = round(prix_tcgdex, 2), 96
                            log.info("    [TCGdex -> COTE] %s : eBay muet, Cardtrader "
                                     "absent -> cote fixée à %.2f€ (Cardmarket via TCGdex)",
                                     nom, cote)
                        else:
                            # V17 documente un biais eBay (prix DEMANDÉS) déjà
                            # mesuré entre 1,8x et 2,5x la tendance Cardmarket
                            # -- un seuil de suspicion à 2x (comme pour les 3
                            # sources Cardtrader/eBay/Cardmarket combinées, où
                            # la redondance rend un écart bas plus fiable)
                            # rejetterait ici l'écart eBay ATTENDU et annulerait
                            # la correction dans le cas même où elle sert le
                            # plus. On tolère donc jusqu'à 3x avant de se méfier.
                            grand, petit = max(cote, prix_tcgdex), min(cote, prix_tcgdex)
                            if grand > petit * 3:
                                log.info("    [Cotes] %s : écart trop important entre eBay "
                                         "(%.2f€) et Cardmarket/TCGdex (%.2f€) -> on garde "
                                         "la PLUS HAUTE par prudence", nom, cote, prix_tcgdex)
                            else:
                                log.info("    [Cotes -> RETENU] %s : Cardmarket/TCGdex "
                                         "(%.2f€) est plus bas que eBay (%.2f€)",
                                         nom, prix_tcgdex, cote)
                                cote, confiance = round(petit, 2), 96
        # V47 : data/cotes.json ne contenait jusqu'ici QUE la cote eBay brute
        # (enregistrée dans obtenir_cote(), avant toute correction Cardtrader/
        # TCGdex ci-dessus) -- alors que le système boutiques TCG (
        # bonne_affaire_shopify.py/alerte_stock.py) lit ce fichier TEL QUEL,
        # sans repasser par cette correction. Une cote corrigée ici restait
        # donc invisible pour les alertes 🔥/📦 des boutiques Shopify/
        # PrestaShop/WooCommerce, qui continuaient de comparer au prix eBay
        # brut (cas réel : Evoli ex 167/131, 325,28€ eBay non corrigé alerté
        # sur cardshunter.fr alors que Cardmarket était à ~145€). On persiste
        # donc la cote FINALEMENT retenue quand elle diffère de la brute.
        if cote and cote != cote_avant_correction:
            enregistrer_cote(nom, cote, carte.get("langue", "fr"))
        if cote:
            log.info("Cote retenue : %.2f€ (confiance : %s annonces) — %d annonces analysées",
                     cote, confiance, len(annonces))
            # V34 correction : on ne doit regrouper que des cartes qui sont
            # VRAIMENT la même carte (juste dans une langue différente), pas
            # toutes les cartes d'un même Pokémon. Sans le numéro, "Mew ex
            # 195" (une carte) et "Mew ex 208" (une AUTRE carte) se
            # retrouvaient comparées comme si c'était la même, ce qui n'a
            # aucun sens : ce sont deux objets différents, pas deux langues
            # du même objet. Le numéro de collection (ex. "223 sv8a") est
            # ce qui identifie une carte de façon unique ; on l'ajoute donc
            # à la clé de regroupement, en plus de l'alias.
            numero_carte = extraire_numero(nom) or numero_nu_voulu(nom) or nom
            cle_regroupement = f"{normaliser(carte.get('alias') or nom)}|{normaliser(str(numero_carte))}"
            cotes_par_carte.setdefault(cle_regroupement, []).append(
                (f"{nom} ({carte.get('langue', 'fr').upper()})", cote))

        for annonce in annonces:
            # V46 : prix Cardmarket transporté jusqu'au deal final pour
            # affichage Telegram (evaluate() fait `deal = {**annonce, ...}`,
            # donc ce champ traverse tel quel jusqu'à _texte_telegram).
            if prix_cm_affiche is not None:
                annonce["cardmarket_prix"] = prix_cm_affiche
            marge_carte = carte.get("marge_achat")  # override par carte si présent
            deal, status = evaluate(annonce, cote, cfg, confiance, marge_carte)
            if deal is None:
                # V35 DIAGNOSTIC TEMPORAIRE : pourquoi une annonce visiblement
                # sous la cote (donc potentiellement une affaire) est écartée.
                if cote and annonce.get("prix", 0) > 0 and annonce["prix"] < cote * 0.85:
                    log.info("    [Diagnostic rejet] %.2f€ '%s' -> %s",
                             annonce["prix"], annonce.get("titre", "")[:50], status)
                    if status.startswith("état refusé"):
                        # V35b : on affiche le texte COMPLET testé (condition
                        # eBay + titre), pas juste le titre, pour voir quel
                        # mot a vraiment déclenché le rejet.
                        log.info("        [Diagnostic état] texte complet testé : %r",
                                 annonce.get("etat_texte", ""))
                continue
            if deja_vue(vues, deal["id"]):
                continue
            # V25 : CONTRÔLE FINAL DE LANGUE sur les annonces Vinted.
            # Le titre seul ne suffit pas (cf. vinted_description) : on va
            # chercher la description de la fiche et on repasse le filtre.
            # Ne concerne que les rares annonces sur le point d'alerter.
            if str(deal.get("id", "")).startswith("vinted-"):
                desc = vinted_description(str(deal["id"]).replace("vinted-", "", 1))

                # V29 : fiche ILLISIBLE -> on n'alerte pas, et on NE marque
                # PAS l'annonce comme vue (elle sera retestée au prochain
                # scan). Le titre Vinted seul ne prouve JAMAIS la langue de
                # la carte : « Bulbizarre AR 166/165 » peut désigner la
                # version française comme la japonaise. Sans la description,
                # on n'a aucun moyen de trancher — le silence est la seule
                # réponse honnête.
                if desc is None:
                    log.info("  ⏸ Vinted : fiche illisible, alerte reportée au "
                             "prochain scan — %s", deal["titre"][:50])
                    continue

                texte_annonce = f"{deal.get('titre', '')} {desc}".strip()
                if desc:
                    ok_lg, motif = annonce_pertinente(
                        texte_annonce, carte["nom"],
                        carte.get("langue", "fr"), carte.get("alias", ""))
                    # On ne rejette QUE sur un motif de LANGUE. Les autres
                    # exclusions (lot, bundle...) ne doivent pas s'appliquer
                    # à la description : un vendeur qui écrit « merci de
                    # privilégier l'achat par lot » vend bien une carte seule,
                    # et son annonce serait écartée à tort.
                    if not ok_lg and ("étrangère" in motif or "langue" in motif):
                        log.info("  ✗ Écarté après lecture de la description : %s (%s)",
                                 deal["titre"][:50], motif)
                        marquer(vues, deal["id"])  # ne pas re-tester à chaque scan
                        continue

                # V26 : preuve positive de français. Cartes FR uniquement —
                # les cartes JP/KR/CN gardent leur filtre habituel.
                if carte.get("langue", "fr") in (None, "", "fr"):
                    neutre = _nom_neutre_entre_langues(carte["nom"])
                    t_norm = normaliser(texte_annonce)
                    mots_fr = [m for m in mots_requis(carte["nom"]) if m != "mega"]
                    nom_fr = mots_fr[0] if mots_fr else ""

                    # (a) Le nom FRANÇAIS doit figurer en toutes lettres.
                    #     Un titre bilingue « Dracaufeu / Charizard » le
                    #     contient : il PASSE — c'est même une preuve de
                    #     français, un vendeur italien n'écrit jamais
                    #     « Dracaufeu ». Ce qu'on écarte ici, c'est
                    #     uniquement l'annonce qui n'a passé le filtre que
                    #     par son ALIAS anglais, sans jamais nommer la
                    #     carte en français.
                    if not neutre and nom_fr and nom_fr not in t_norm:
                        log.info("  ✗ Écarté : nom français '%s' absent de l'annonce "
                                 "(reconnue via l'alias seul) — %s",
                                 nom_fr, deal["titre"][:50])
                        marquer(vues, deal["id"])
                        continue

                    # (b) Nom neutre (Mew, Pikachu, Lucario...) : le nom ne
                    #     prouve rien, on exige un mot français — MAIS
                    #     seulement si on a pu LIRE la description. Une
                    #     description absente (429, session expirée, fiche
                    #     supprimée) est un incident réseau, pas une preuve
                    #     d'annonce étrangère : sans le `desc and`, on
                    #     écarterait de vraies annonces françaises pour une
                    #     panne, et en les marquant vues, définitivement.
                    # V39 : desc=="" (fiche LUE mais vendeur n'a rien écrit)
                    # contournait ce test — "and desc" étant faux sur une
                    # chaîne vide, exactement comme sur None. Or le cas None
                    # est déjà écarté plus haut (continue) : ici, desc ne
                    # peut plus valoir que "" ou du texte réel. On retire
                    # donc "and desc", qui ne protégeait plus rien et
                    # laissait passer sans preuve les annonces où la fiche
                    # est lisible mais simplement vide.
                    if neutre and not preuve_francais(texte_annonce):
                        log.info("  ✗ Écarté : nom de Pokémon identique dans toutes "
                                 "les langues et aucun mot français dans l'annonce "
                                 "— %s", deal["titre"][:50])
                        marquer(vues, deal["id"])
                        continue
            log.info("  ✓ DEAL : %s à %.2f€ (cote %.2f€)", deal["titre"][:60], deal["total"], cote)
            nouveaux_deals.append(deal)
            # V39 : le marquage "vu" est retardé après l'envoi Telegram/email
            # (voir plus bas dans main()). AVANT, l'annonce était marquée vue
            # immédiatement ici — si Telegram tombait en panne ce jour-là
            # (token expiré, quota, erreur réseau...), l'affaire disparaissait
            # définitivement sans jamais avoir été notifiée. On stocke
            # seulement l'identifiant pour l'instant.
            deals_a_marquer.append(deal["id"])

        # Pause aléatoire courte entre les cartes (anti-détection Vinted).
        # V20 : réduite de 1,5-3,5s à 0,6-1,4s — sur 120 cartes, l'ancienne
        # pause représentait ~5 min de pure attente (la moitié du scan !).
        # La pause courte garde la protection anti-bot tout en divisant ce
        # coût par 2,5. eBay (API officielle) n'a pas besoin de pause.
        time.sleep(random.uniform(0.6, 1.4))

    # --- Suivi du stock : alertes de REVENTE (cote >= 2x prix d'achat) ---
    # Annonces reçues par email d'alerte Leboncoin (contourne le blocage DataDome)
    for annonce in lbc_relever_alertes_email(cfg, secrets):
        for carte in cfg["watchlist"]:
            pertinent, _ = annonce_pertinente(annonce["titre"], carte["nom"],
                                              carte.get("langue", "fr"), carte.get("alias", ""))
            if not pertinent:
                continue
            annonce["carte"] = carte["nom"]
            annonce["langue"] = carte.get("langue", "fr")
            annonce["alias"] = carte.get("alias", "")
            cote_carte = carte.get("cote") or cote_lissee(carte["nom"], carte.get("langue", "fr"))
            if not cote_carte:
                break
            deal, _statut = evaluate(annonce, float(cote_carte), cfg, 0, carte.get("marge_achat"))
            if deal and not deja_vue(vues, deal["id"]):
                log.info("  ✓ DEAL (email LBC) : %s à %.2f€ (cote %.2f€)",
                         deal["titre"][:60], deal["total"], float(cote_carte))
                nouveaux_deals.append(deal)
                deals_a_marquer.append(deal["id"])  # V39 : marquage retardé, cf. plus bas
            break

    # V34 : vérification de cohérence entre langues. Pour chaque carte
    # suivie dans plusieurs langues, on compare ses cotes : si l'une est
    # plus du double d'une autre (ex. FR à 200€, JP à 80€), c'est le signe
    # possible d'un mélange de langue quelque part (annonce mal filtrée,
    # mauvais lien Cardtrader...). But : repérer ces cas nous-mêmes plutôt
    # que de laisser une alerte biaisée partir sur Telegram sans prévenir.
    alertes_langues: list[str] = []
    seuil_langues = float(cfg.get("anomalies", {}).get("seuil_ecart_langues", 2.0))
    for cle, entrees in cotes_par_carte.items():
        if len(entrees) < 2:
            continue  # une seule langue suivie : rien à comparer
        valeurs = [v for _, v in entrees]
        grand, petit = max(valeurs), min(valeurs)
        if petit > 0 and grand / petit >= seuil_langues:
            # V46 : anti-spam - une alerte d'écart de langue par carte toutes
            # les 48h maximum (même mécanisme que les anomalies de cote
            # ci-dessus), pour ne pas ré-envoyer la même alerte à chaque scan
            # (toutes les 15 min) tant que l'écart persiste.
            if not anti_spam(vues, f"ecart-langues-{cle}", 48 * 3600):
                continue
            details = ", ".join(f"{n} : {v:.2f}€" for n, v in entrees)
            alertes_langues.append(
                f"⚠️ <b>ÉCART SUSPECT ENTRE LANGUES</b> : {cle}\n{details}\n"
                f"Vérifie qu'aucune annonce d'une langue n'a été comptée "
                f"dans la cote d'une autre avant de te fier à une alerte "
                f"sur cette carte.")
            log.info("[Cohérence langues] écart suspect sur '%s' : %s", cle, details)

    alertes_vente = verifier_stock(cfg, secrets, vues)
    _ct_sauver_cache()  # V22 : persistance du cache Cardtrader
    _api_sauver_cache()  # V47 : persistance du cache TCGdex

    # Tri : les affaires les plus rentables en premier
    nouveaux_deals.sort(key=lambda d: d["profit_net_estime"], reverse=True)

    # V23 : bilan de calibration. Affiche l'écart RÉEL mesuré entre les cotes
    # eBay et les prix Cardtrader sur les cartes couvertes par les deux
    # sources. C'est ce coefficient qui pourra corriger automatiquement les
    # cartes que Cardtrader ne couvre pas (mode observation pour l'instant).
    _coef_mesure = _calibration_coefficient()
    if _coef_mesure is not None:
        log.info("Calibration eBay -> marché réel : coefficient %.3f "
                 "(mesuré sur %d cartes ayant les deux sources). "
                 "Une cote eBay de 100€ vaudrait donc ~%.0f€ au prix réel.",
                 _coef_mesure, len(_calibration_paires), 100 * _coef_mesure)
    elif _calibration_paires:
        log.info("Calibration : seulement %d mesure(s) eBay/Cardtrader "
                 "(5 minimum pour un coefficient fiable)", len(_calibration_paires))

    log.info("Analyse terminée en %.0fs : %d annonces, %d nouveau(x) deal(s), %d alerte(s) de vente",
             time.time() - debut, total_annonces, len(nouveaux_deals), len(alertes_vente))

    notif = cfg.get("notifications", {"telegram": True, "email": True})
    if nouveaux_deals:
        # V39 : on ne marque les deals comme "vus" QUE si au moins une
        # notification est bien partie. Avant, marquer(vues, ...) était
        # appelé dès la détection du deal (voir plus haut), donc un échec
        # Telegram (token expiré, quota, panne réseau) faisait disparaître
        # l'affaire pour toujours, sans jamais avoir prévenu personne.
        notification_reussie = False
        if notif.get("telegram") and "telegram" in cfg:
            if envoyer_telegram(nouveaux_deals, cfg["telegram"], secrets["TELEGRAM_BOT_TOKEN"],
                                secrets.get("ANTHROPIC_API_KEY", "")):
                notification_reussie = True
        if notif.get("email") and "email" in cfg:
            if envoyer_alertes(nouveaux_deals, cfg["email"], secrets["GMAIL_APP_PASSWORD"]):
                notification_reussie = True
        if notification_reussie:
            for annonce_id in deals_a_marquer:
                marquer(vues, annonce_id)
        else:
            log.warning("Aucune notification envoyée avec succès pour %d deal(s) : "
                       "ils resteront visibles au prochain scan (non marqués vus)",
                       len(nouveaux_deals))
    if alertes_vente and notif.get("telegram") and "telegram" in cfg:
        envoyer_telegram_ventes(alertes_vente, cfg["telegram"], secrets["TELEGRAM_BOT_TOKEN"])

    # --- Stats du jour + export CSV de l'historique des deals ---
    enregistrer_scan(total_annonces, nouveaux_deals)
    exporter_csv(nouveaux_deals)

    # --- Détection d'anomalies de cote (chute >=30% / hausse >=50%) ---
    anomalies = detecter_anomalies(cfg, vues)
    if anomalies and notif.get("telegram") and "telegram" in cfg:
        envoyer_telegram_texte(anomalies, cfg["telegram"], secrets["TELEGRAM_BOT_TOKEN"])

    # V34 : alertes d'écart suspect entre langues (voir plus haut dans main).
    if alertes_langues and notif.get("telegram") and "telegram" in cfg:
        envoyer_telegram_texte(alertes_langues, cfg["telegram"], secrets["TELEGRAM_BOT_TOKEN"])

    # V46 : rappel de revérification des cotes manuelles trop anciennes.
    cotes_perimees = verifier_cotes_manuelles_perimees(cfg, vues)
    if cotes_perimees and notif.get("telegram") and "telegram" in cfg:
        envoyer_telegram_texte(cotes_perimees, cfg["telegram"], secrets["TELEGRAM_BOT_TOKEN"])

    # V50 : alerte si Vinted/Leboncoin échouent de façon quasi systématique
    # sur ce cycle (connecteur probablement cassé, cf. verifier_fiabilite_plateformes).
    alertes_fiabilite = verifier_fiabilite_plateformes(vues)
    if alertes_fiabilite and notif.get("telegram") and "telegram" in cfg:
        envoyer_telegram_texte(alertes_fiabilite, cfg["telegram"], secrets["TELEGRAM_BOT_TOKEN"])

    # --- Récapitulatif quotidien (envoyé une fois, vers 21h heure de Paris) ---
    recap = recap_du_jour(cfg, vues)
    if recap and notif.get("telegram") and "telegram" in cfg:
        envoyer_telegram_texte([recap], cfg["telegram"], secrets["TELEGRAM_BOT_TOKEN"])

    sauvegarder_vues(vues)
    sauvegarder_historique()
    sauvegarder_anciennete()
    return 0


if __name__ == "__main__":
    sys.exit(main())
