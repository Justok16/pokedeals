"""
Connecteur TCGdex (API publique gratuite, republie les prix tendance
Cardmarket) pour PokeDeals.

Extrait de main.py le 17/08/2026 (quatrieme module du decoupage
progressif de main.py, cf. SESSION_NOTES.md) : sert de repli quand
Cardtrader n'a rien (cartes/sets qu'il ne couvre pas), en republiant les
prix tendance Cardmarket que TCGdex expose gratuitement, sans les
restrictions d'inscription/scraping de l'API Cardmarket elle-meme.

Extraction plus simple que connecteur_cardtrader.py : aucun couplage
particulier avec main.py au-dela des 3 fonctions publiques reimportees
normalement (deduire_api_id n'est jamais utilisee ailleurs que dans ce
module, aucun dict mutable partage a risque de reassignation).
"""
from __future__ import annotations

import json
import logging
import os
import re
import time

import requests

from json_utils import ecrire_json_atomique

log = logging.getLogger("pokedeals.connecteur_tcgdex")
RACINE = os.path.dirname(os.path.abspath(__file__))

TCGDEX_BASE = "https://api.tcgdex.net/v2"
API_CACHE_FICHIER = os.path.join(RACINE, "data", "api_prix.json")
API_CACHE_DUREE = 20 * 3600  # ≈ 1 rafraîchissement par jour et par carte
_api_prix_cache: dict = {}

# Code de set en fin de nom (sv2a, sv8a, s8b, m1L, m2a, m5, mC, S-P...)
RE_SET_JP = re.compile(r"\b(sv\d+[a-z]*|s\d+[a-z]*|m[A-Za-z0-9]+|S-P)\s*$")


# Correspondances dénominateur -> set TCGdex, confirmées par les cartes de
# la watchlist qui portent déjà leur code de set (ex : Goldeen 084 m5 est
# d'Abyss Eye, donc toute carte jp en x/081 est aussi m5). Prudence : on
# n'ajoute ici QUE des paires vérifiées par les données de l'utilisateur.
_DENOM_VERS_SET = {
    ("jp", 81): "m5",       # Abyss Eye (cf. Goldeen 084 m5)
    ("jp", 193): "m2a",     # Mega Dream ex (cf. Mewtwo 237 m2a)
    ("jp", 172): "s12",     # Paradigm Trigger (cf. commentaire Lugia V S12)
    ("jp", 98): "s12",      # idem
    ("fr", 131): "sv08.5",  # Évolutions Prismatiques (international)
    ("fr", 167): "sv06",    # Mascarade Crépusculaire (international)
}


def deduire_api_id(carte: dict) -> str | None:
    """Construit l'identifiant TCGdex ("set-numéro") depuis le nom de la
    carte. Les noms fournis contiennent déjà set + numéro pour les cartes
    japonaises ; pour les françaises, la Série 151 (x/165) correspond au
    set international sv03.5. Un champ `api_id` dans config.yaml est
    prioritaire sur la déduction (pour corriger un cas particulier).

    V47 : TCGdex exige un numéro local TOUJOURS complété à 3 chiffres
    (ex. "m2-085", jamais "m2-85" -- vérifié en direct : 404 sans le
    padding, 200 avec). Seul le cas SWSH promo (déjà en `:03d`) l'avait
    jusqu'ici -- bug latent sur tous les autres numéros < 100, découvert
    en creusant la cote Piplup 085 m2 (Justok a demandé d'approfondir
    plutôt que de se contenter d'une cote manuelle). Sans ce padding,
    l'appel direct échouait TOUJOURS pour ces cartes et retombait sur la
    recherche générique par numéro seul (_api_recherche_par_numero),
    beaucoup moins fiable (pas de set pour désambiguïser)."""
    if carte.get("api_id"):
        return str(carte["api_id"])
    langue = carte.get("langue", "fr")
    if langue == "kr":
        return None  # Cardmarket ne cote pas les cartes coréennes
    nom = str(carte["nom"])
    if langue == "jp":
        m_set = RE_SET_JP.search(nom)
        m_num = re.search(r"\b0*(\d+)\b", nom)
        if m_set and m_num:
            return f"{m_set.group(1)}-{int(m_num.group(1)):03d}"
        # Pas de code de set : le dénominateur peut identifier le set.
        m_xy = re.search(r"\b0*(\d+)/0*(\d+)\b", nom)
        if m_xy:
            set_id = _DENOM_VERS_SET.get(("jp", int(m_xy.group(2))))
            if set_id:
                return f"{set_id}-{int(m_xy.group(1)):03d}"
        return None
    # Cartes françaises : Série 151 = set international sv03.5
    m151 = re.search(r"\b(\d+)/165\b", nom)
    if m151:
        return f"sv03.5-{int(m151.group(1)):03d}"
    # Promos identifiables : SWSH087 -> swshp ; "promo" SV -> svp
    m_swsh = re.search(r"\bSWSH0*(\d+)\b", nom)
    if m_swsh:
        return f"swshp-SWSH{int(m_swsh.group(1)):03d}"
    if "promo" in nom.lower():
        m_num = re.search(r"\b0*(\d+)\b", nom)
        if m_num:
            return f"svp-{int(m_num.group(1)):03d}"
    # Autres sets FR par dénominateur confirmé
    m_xy = re.search(r"\b0*(\d+)/0*(\d+)\b", nom)
    if m_xy:
        set_id = _DENOM_VERS_SET.get(("fr", int(m_xy.group(2))))
        if set_id:
            return f"{set_id}-{int(m_xy.group(1)):03d}"
    return None


def _api_charger_cache() -> None:
    global _api_prix_cache
    try:
        with open(API_CACHE_FICHIER, "r", encoding="utf-8") as f:
            _api_prix_cache = json.load(f)
    except (OSError, ValueError):
        _api_prix_cache = {}


def _api_sauver_cache() -> None:
    try:
        ecrire_json_atomique(API_CACHE_FICHIER, _api_prix_cache, ensure_ascii=False)
    except OSError as e:
        log.warning("Cache API non sauvegardé : %s", e)


def _api_lire_prix(data: dict) -> float | None:
    """Extrait le prix tendance Cardmarket d'une réponse carte TCGdex."""
    cm = (data.get("pricing") or {}).get("cardmarket") or {}
    for cle in ("trend", "avg30", "avg7", "avg1", "avg", "low"):
        v = cm.get(cle)
        if isinstance(v, (int, float)) and v > 0:
            return float(v)
    return None


def _api_recherche_par_numero(carte: dict) -> tuple[str | None, float | None]:
    """Trouve une carte dans TCGdex par son numéro local (ex. 187/132) SANS
    connaître le set à l'avance. C'est le cœur de l'automatisation : toute
    carte, même d'un set que le code ne connaît pas, est retrouvée tant que
    Cardmarket la cote. Retourne (api_id, prix) ou (None, None).

    On filtre par le numéro local ET le dénominateur = taille du set, pour
    ne pas confondre deux cartes de même numéro dans des sets différents.
    GARDE-FOU : sans dénominateur dans le nom, aucune vérification n'est
    possible -> on refuse tout match plutôt que de prendre le premier
    candidat TCGdex au hasard, tous sets confondus depuis 1999. Cas vécu
    (13/08/2026) : "Mega Charizard X ex 110 m2" (JP, sans dénominateur
    affiché) confondu avec une carte anglaise "Base Set 2" numérotée 110
    par pure coïncidence -> cote à 0,44€ contre 853,83€ de vraies annonces
    Cardtrader ignorées ensuite car jugées "incohérentes" avec cette cote
    fausse. Même logique de prudence pour un set dont la taille officielle
    est inconnue de TCGdex (`total` absent) : pas de vérification possible
    non plus, donc pas de match. La langue française passe par les sets
    internationaux, donc on interroge l'API en anglais (les prix
    Cardmarket sont les mêmes)."""
    nom = str(carte["nom"])
    m_xy = re.search(r"\b0*(\d+)/0*(\d+)\b", nom)
    if not m_xy:
        return None, None
    numero, denom = m_xy.group(1), m_xy.group(2)
    try:
        # L'API permet de filtrer par numéro local : renvoie les cartes
        # candidates (tous sets confondus) qu'on départage par dénominateur.
        rep = requests.get(f"{TCGDEX_BASE}/en/cards",
                           params={"localId": numero}, timeout=15)
        if rep.status_code != 200:
            return None, None
        candidats = rep.json()
        if not isinstance(candidats, list):
            return None, None
        for c in candidats:
            cid = c.get("id")
            if not cid:
                continue
            # Récupère le détail pour vérifier le dénominateur et lire le prix
            det = requests.get(f"{TCGDEX_BASE}/en/cards/{cid}", timeout=15)
            if det.status_code != 200:
                continue
            d = det.json()
            total = ((d.get("set") or {}).get("cardCount") or {}).get("official")
            if not total or str(total) != denom:
                continue  # mauvais set (dénominateur différent ou inconnu)
            prix = _api_lire_prix(d)
            if prix is not None:
                return cid, prix
    except Exception as e:  # noqa: BLE001
        log.info("    [API recherche] %s : %s", nom, e)
    return None, None


def api_prix_carte(carte: dict) -> float | None:
    """Prix tendance Cardmarket (via TCGdex) pour une carte, avec cache.

    Stratégie en 2 temps :
      1. Déduction directe de l'identifiant (rapide, sans requête de
         recherche) quand le set est connu.
      2. Sinon, RECHERCHE automatique par numéro — couvre n'importe quelle
         carte, y compris de sets futurs, sans modifier le code.
    Retourne None si la carte est introuvable/non cotée (cartes coréennes,
    sets non couverts par Cardmarket) ou en cas d'erreur réseau : le bot
    retombe alors sur la cote eBay."""
    if carte.get("langue") == "kr":
        return None  # Cardmarket ne cote pas le coréen : direct sur eBay

    # Clé de cache : l'identifiant déduit, sinon le nom + langue.
    api_id = deduire_api_id(carte)
    cle_cache = api_id or f"?{carte.get('langue','fr')}:{carte['nom']}"
    ent = _api_prix_cache.get(cle_cache)
    if ent and (time.time() - ent.get("ts", 0)) < API_CACHE_DUREE:
        return ent.get("prix")

    prix = None
    try:
        if api_id:
            rep = requests.get(f"{TCGDEX_BASE}/en/cards/{api_id}", timeout=15)
            if rep.status_code == 200:
                prix = _api_lire_prix(rep.json())
            elif rep.status_code == 404:
                # V47 : certains sets JAPONAIS EXCLUSIFS (jamais sortis à
                # l'international : MC = Start Deck 100 Battle Collection,
                # M1S = Mega Symphonia, S12 = Paradigm Trigger...) n'existent
                # QUE côté catalogue japonais de TCGdex ("/ja/"), pas "/en/".
                # Cas vécu : Pikachu ex 764 mC, Clefairy ex 765 mC, Mega
                # Gardevoir ex 087/063 (api_id explicite dans config.yaml,
                # confirmés via Cardmarket par Justok) -- 404 systématique
                # sur "/en/" malgré un api_id juste.
                if carte.get("langue") == "jp":
                    rep_ja = requests.get(f"{TCGDEX_BASE}/ja/cards/{api_id}", timeout=15)
                    if rep_ja.status_code == 200:
                        prix = _api_lire_prix(rep_ja.json())
                if prix is None:
                    # Set déduit erroné : on tente la recherche par numéro.
                    trouve_id, prix = _api_recherche_par_numero(carte)
                    if trouve_id:
                        log.info("    [API] %s : trouvé via recherche -> %s", carte["nom"], trouve_id)
            else:
                log.info("    [API] %s : HTTP %s", api_id, rep.status_code)
        else:
            # Pas de set déductible : recherche directe par numéro.
            trouve_id, prix = _api_recherche_par_numero(carte)
            if trouve_id:
                log.info("    [API] %s : trouvé via recherche -> %s", carte["nom"], trouve_id)
    except Exception as e:  # noqa: BLE001 — l'API ne doit jamais faire échouer le scan
        log.info("    [API] %s : erreur réseau (%s)", carte["nom"], e)
        return None  # erreur réseau : ne pas mettre en cache, on réessaiera

    _api_prix_cache[cle_cache] = {"prix": prix, "ts": time.time()}
    return prix
