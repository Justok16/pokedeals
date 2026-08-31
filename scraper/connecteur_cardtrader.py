"""
Connecteur Cardtrader (place de marche pour cartes Pokemon) pour PokeDeals.

Extrait de main.py le 17/08/2026 (troisieme module du decoupage progressif
de main.py, cf. SESSION_NOTES.md) : integration Cardtrader utilisee pour
affiner/verifier la cote calculee a partir des annonces eBay -- recherche
de la carte chez Cardtrader (blueprint_id), recuperation de son prix de
marche, et garde-fous de coherence (cartes gradees, prix aberrants entre
langues). Inclut aussi la calibration automatique eBay -> marche reel
(_calibration_*), etroitement couplee au meme mecanisme.

Deux points de couplage restants avec main.py, geres explicitement :
- `CT_NOMS_EN` (table FR->EN) est reimportee par `_nom_neutre_entre_langues()`,
  restee dans main.py (elle-meme depend d'une dependance vers l'avant
  historique, cf. filtre_annonces.py).
- `_ct_cache` est un dict REASSIGNE (pas seulement mute) par
  `_ct_charger_cache()` -- main.py ne doit donc jamais faire
  `from connecteur_cardtrader import _ct_cache` (la liaison se figerait
  sur l'ancien objet), mais toujours passer par
  `connecteur_cardtrader._ct_cache` (acces qualifie, toujours a jour).
  Seul `cardmarket_prix()` (reste dans main.py) en a besoin.
"""
from __future__ import annotations

import hashlib
import inspect
import json
import logging
import os
import re
import statistics
import time

import requests

from filtre_annonces import mots_requis, normaliser
from json_utils import ecrire_json_atomique

log = logging.getLogger("pokedeals.connecteur_cardtrader")
RACINE = os.path.dirname(os.path.abspath(__file__))

# =====================================================================
# V22 : COTES CARDTRADER (marché européen, prix RÉELS par langue)
# ---------------------------------------------------------------------
# Pourquoi Cardtrader plutôt que Cardmarket : l'API Cardmarket est
# fermée aux nouvelles inscriptions ET interdit explicitement la
# récupération quotidienne de prix. Cardtrader est un marché européen
# comparable (en EUR), avec une API gratuite (token perso) qui expose
# les VRAIES annonces filtrables par langue (fr/jp/kr) — exactement ce
# qui manquait à TCGdex (qui mélangeait les versions linguistiques).
#
# Cote = MOYENNE DES N PRIX LES PLUS BAS (choix de l'utilisateur) :
# plus robuste qu'un prix unique (erreur de saisie, carte abîmée) et
# plus proche du prix de vente réel que la tendance du marché.
# =====================================================================
CT_BASE = "https://api.cardtrader.com/api/v2"
CT_JEU_POKEMON = 5           # id du jeu Pokémon chez Cardtrader
CT_CACHE_FICHIER = os.path.join(RACINE, "data", "cardtrader.json")
CT_CACHE_PRIX_DUREE = 20 * 3600      # prix trouvé : 1 rafraîchissement/jour
CT_CACHE_ECHEC_DUREE = 2 * 3600      # échec : on retente au bout de 2 h
CT_CACHE_VERSION = 6                 # V33 : purge forcée pour vérifier cardmarket_id
CT_CACHE_BLUEPRINT_DUREE = 30 * 86400  # blueprint_id : quasi permanent
# Correspondance langue interne -> code langue Cardtrader
CT_LANGUES = {"fr": "fr", "jp": "jp", "kr": "kr", "en": "en"}
_ct_cache: dict = {"blueprints": {}, "prix": {}, "expansions": []}


def _ct_signature_code() -> str:
    """Empreinte du code de recherche Cardtrader. Si ce code change, le
    cache est automatiquement purgé : les échecs enregistrés par une
    version précédente ne peuvent plus masquer une correction (piège
    rencontré plusieurs fois pendant la mise au point)."""
    try:
        src = (inspect.getsource(_ct_numero_de)
               + inspect.getsource(_ct_trouver_blueprint)
               + inspect.getsource(cardtrader_prix)   # V25 : le filtre des
               # gradées vit ici ; sans cette ligne, une correction du filtre
               # ne purgeait pas le cache et le bot relisait les prix erronés.
               + str(sorted(CT_NOMS_EN.items())))
        return hashlib.md5(src.encode("utf-8")).hexdigest()[:12]
    except Exception:  # noqa: BLE001
        return str(CT_CACHE_VERSION)


def _ct_charger_cache() -> None:
    global _ct_cache
    try:
        with open(CT_CACHE_FICHIER, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            # Purge si le code de recherche a changé depuis l'écriture.
            if data.get("sig") != _ct_signature_code():
                log.info("Cache Cardtrader réinitialisé (code modifié) : repart propre")
                _ct_cache = {"blueprints": {}, "prix": {}}
                return
            _ct_cache = {"blueprints": data.get("blueprints", {}),
                         "prix": data.get("prix", {})}
    except (OSError, ValueError):
        pass


def _ct_sauver_cache() -> None:
    try:
        ecrire_json_atomique(CT_CACHE_FICHIER, {"sig": _ct_signature_code(), **_ct_cache}, ensure_ascii=False)
    except OSError as e:
        log.warning("Cache Cardtrader non sauvegardé : %s", e)


def _ct_entete(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Accept": "application/json"}


# Noms FR -> EN des Pokémon suivis (Cardtrader catalogue en anglais).
# Complète les alias de config.yaml : évite d'avoir à saisir un alias
# pour chaque carte française. Ajouter ici tout nouveau Pokémon FR.
CT_NOMS_EN = {
    "dracaufeu": "Charizard", "tortank": "Blastoise", "florizarre": "Venusaur",
    "salameche": "Charmander", "salamèche": "Charmander",
    "bulbizarre": "Bulbasaur", "herbizarre": "Ivysaur",
    "carapuce": "Squirtle", "carabaffe": "Wartortle",
    "gardevoir": "Gardevoir", "lucario": "Lucario", "latias": "Latias",
    "dracolosse": "Dragonite", "ectoplasma": "Gengar",
    "amphinobi": "Greninja", "grenousse": "Froakie",
    "miaouss": "Meowth", "psykokwak": "Psyduck", "poissirene": "Goldeen",
    "tiplouf": "Piplup", "plumeline": "Oricorio", "melofee": "Clefairy",
    "mélofée": "Clefairy", "evoli": "Eevee", "évoli": "Eevee",
    "morpeko": "Morpeko", "pikachu": "Pikachu", "mew": "Mew",
    "mewtwo": "Mewtwo", "darkrai": "Darkrai", "lugia": "Lugia",
    "zoroark": "Zoroark", "alakazam": "Alakazam",
}


# Dénominateur de la carte -> mots-clés du nom de set chez Cardtrader.
# Sert à cibler la bonne expansion (l'API plafonne à 50 résultats sur une
# recherche par nom, donc on interroge le set entier puis on filtre).
CT_SETS = {
    "165": ["151"],                              # Pokémon 151 (sv2a / EV3.5)
    "132": ["mega evolution", "megaevolution"],  # Méga-Évolution (ME01)
    "094": ["phantasmal", "flames"],             # Flammes Fantasmagoriques (ME02)
    "217": ["ascendant", "transcend"],           # Héros Ascendants/Transcendants
    "086": ["chaos"],                            # Chaos Ascendant (ME04)
    "081": ["abyss"],                            # Abyss Eye (M5)
    "131": ["prismatic"],                        # Évolutions Prismatiques
    "167": ["twilight", "masquerade"],           # Mascarade Crépusculaire
    "193": ["dream"],                            # MEGA Dream ex (m2a)
    "063": ["mega", "gardevoir"],
    "172": ["paradigm", "trigger"],
    # V47 : "098" pointait vers "Lost Origin" -- mauvais set pour l'unique
    # carte de la watchlist utilisant ce denominateur ("Lugia V 110/098",
    # confirme JP "Paradigm Trigger" via Cardmarket, cf. session du
    # 13/08/2026). Corrige : aucune autre carte n'utilise ce denominateur.
    "098": ["paradigm", "trigger"],
}


# Code de set japonais présent dans le nom -> mots-clés Cardtrader.
# Beaucoup de cartes JP/KR n'ont pas de dénominateur (« Mew ex 195 sv2a »)
# mais portent leur code de set, ce qui suffit à cibler l'expansion.
CT_SETS_JP = {
    "sv2a": ["151"], "sv8a": ["terastal"], "sv5a": ["crimson"],
    "sv9": ["battle partners"], "s8b": ["vmax climax"], "s12": ["paradigm"],
    # V47 (premiere passe) : m2/m3/m4 pointaient tous vers le mot-cle
    # generique "mega", qui ne matche QUE l'expansion ME01 "Mega Evolution"
    # -- constate identiquement en JP et KR (Meowth ex 114 m3, Froakie 086
    # m4, Mega Charizard X ex m2, Piplup 085 m2, Oricorio ex 111 m2 :
    # aucun blueprint trouve dans aucune langue avant correctif).
    #
    # V47 (correction) : la premiere passe avait mappe m2/m3/m4 vers les
    # noms INTERNATIONAUX ME02/ME03/ME04 (Phantasmal Flames/Perfect Order/
    # Chaos Rising) par similitude de code -- ERREUR reperee en creusant
    # suite a une question de Justok sur l'automatisation de Piplup/
    # Tiplouf : "m2" (code JP, catalogue via /ja/sets sur TCGdex) est en
    # realite le set JAPONAIS EXCLUSIF "M2 : インフェルノX" ("Inferno X",
    # deja identifie par Justok des le debut de la session), SANS AUCUN
    # RAPPORT avec "ME02 Phantasmal Flames" -- deux sets differents malgre
    # la similitude du code. Meme suspicion pour m3 ("M3 : ムニキスゼロ")
    # et m4 ("M4 : ニンジャスピナー"), confirmee par TCGdex : series "M"
    # (ポケモンカードゲーム MEGA, exclusive JP) totalement distincte de la
    # serie "ME" (internationale). m5 ("M5 : アビスアイ" = Abyss Eye) avait
    # ete laisse INCHANGE lors de la premiere passe et s'est avere juste
    # (confirme par un blueprint Cardtrader deja trouve en prod avec succes,
    # ex. Goldeen 084 m5 -> 4,72€) -- meme methode appliquee ici : mot-cle
    # anglais phonetique du nom JP reel, pas le nom international ME0x.
    "m1l": ["mega evolution"], "m2": ["inferno"], "m2a": ["dream"],
    # m3 "ムニキスゼロ" : VERIFIE le 13/08/2026 -- le set existe bien chez
    # Cardtrader sous le nom officiel "Nihil Zero"
    # (cardtrader.com/en/games/pokemon/expansions/nihil-zero/categories),
    # avec des annonces reelles incluant "Meowth ex ... Nihil Zero"
    # (exactement la carte JP 114 m3 suivie ici). Mot-cle resserre de
    # "zero" seul a "nihil zero" -- toujours suffisant et plus precis,
    # moins de risque de faux positif sur un autre set contenant "zero".
    "m3": ["nihil zero"],
    "m4": ["ninja spinner"],  # "ニンジャスピナー", transliteration phonetique directe
    "m5": ["abyss"], "mc": ["start deck"],
}


def _ct_indices_set(nom: str, denom: str) -> list:
    """Mots-clés permettant d'identifier l'expansion Cardtrader d'une carte,
    à partir de son dénominateur (.../165) ou de son code de set JP (sv2a).
    Le dénominateur est testé avec ET sans zéros initiaux (094 <-> 94)."""
    if denom:
        for variante in (denom, denom.lstrip("0"), denom.zfill(3)):
            if variante in CT_SETS:
                return CT_SETS[variante]
    n = normaliser(nom)
    for code, indices in CT_SETS_JP.items():
        if re.search(rf"\b{re.escape(code)}\b", n):
            return indices
    return []


def _ct_numero_de(bp: dict) -> str:
    """Extrait le numéro de collection d'un blueprint Cardtrader.

    V22.4 : l'endpoint /blueprints ne renvoie PAS de champ numérique
    dédié (constaté en production : les seuls champs sont back_image,
    category_id, expansion_id, game_id, id, image, meta_name, name,
    slug). Le numéro se trouve donc dans le NOM ou le SLUG, sous des
    formes variées : « Charizard ex (199/165) », « Pikachu 173/165 »,
    « charizard-ex-199-165 », « ... #199 ».
    """
    props = bp.get("fixed_properties") or {}
    editable = bp.get("editable_properties") or {}
    for src in (props, editable, bp):
        if isinstance(src, dict):
            for champ in ("collector_number", "card_number", "number",
                          "collectors_number", "cardnumber"):
                v = src.get(champ)
                if v not in (None, "", []):
                    return str(v)

    # Champs textuels réellement présents dans la réponse.
    # ATTENTION : le slug commence par l'ID Cardtrader
    # (« 110706-pikachu-48-162-breakthrough ») — on le retire d'abord,
    # sinon on prend l'ID pour le numéro de carte.
    for champ in ("name", "meta_name", "slug"):
        texte = str(bp.get(champ) or "")
        if not texte:
            continue
        if champ == "slug":
            texte = re.sub(r"^\d+-", "", texte)
        # « 199/165 », « 48-162 » -> 199 / 48
        mm = re.search(r"\b0*(\d{1,3})\s*[/-]\s*0*(\d{2,3})\b", texte)
        if mm:
            return mm.group(1)
        # « #199 » ou « (199) »
        mm = re.search(r"[#(]\s*0*(\d{1,3})\b", texte)
        if mm:
            return mm.group(1)
        # « ... 199 » en fin de nom
        mm = re.search(r"\b0*(\d{1,3})\s*$", texte.strip())
        if mm:
            return mm.group(1)
    return ""


def _ct_expansions(token: str) -> list:
    """Liste (mise en cache) des expansions Pokémon de Cardtrader."""
    if _ct_cache.get("expansions"):
        return _ct_cache["expansions"]
    try:
        rep = requests.get(f"{CT_BASE}/expansions", timeout=25,
                           headers=_ct_entete(token))
        if rep.status_code == 200 and isinstance(rep.json(), list):
            exps = [e for e in rep.json() if e.get("game_id") == CT_JEU_POKEMON]
            _ct_cache["expansions"] = exps
            log.info("    [Cardtrader] %d expansions Pokémon chargées", len(exps))
            return exps
        log.info("    [Cardtrader] /expansions : HTTP %s", rep.status_code)
    except Exception as e:  # noqa: BLE001
        log.info("    [Cardtrader] /expansions : erreur (%s)", e)
    return []


def _ct_expansions_recentes(token: str, combien: int) -> list:
    """Les `combien` expansions Pokémon les plus RÉCENTES.

    V24 : sert de repli quand le set d'une carte n'est pas déductible de
    son nom (promos, numéros nus : « Morpeko ex 117 », « Poissirene 087 »).
    Cardtrader ne renvoyant pas de date de sortie exploitable, on trie par
    identifiant décroissant — les id sont attribués chronologiquement, donc
    les plus grands correspondent aux sorties les plus récentes. C'est une
    approximation, mais elle colle au besoin : la watchlist ne suit que des
    séries récentes.
    """
    exps = _ct_expansions(token)
    if not exps:
        return []
    return sorted(exps, key=lambda e: int(e.get("id") or 0), reverse=True)[:combien]


def _ct_blueprints_du_set(expansion_id: int, token: str) -> list:
    """Catalogue d'une expansion, mis en cache pour toute la session.
    Évite de re-télécharger le même set pour chaque carte non résolue."""
    cle = str(expansion_id)
    cache = _ct_cache.setdefault("sets", {})
    if cle in cache:
        return cache[cle]
    try:
        rep = requests.get(f"{CT_BASE}/blueprints/export", timeout=30,
                           headers=_ct_entete(token),
                           params={"expansion_id": expansion_id})
        bps = rep.json() if rep.status_code == 200 else []
        if not isinstance(bps, list):
            bps = []
    except Exception:  # noqa: BLE001
        bps = []
    cache[cle] = bps
    return bps


def _ct_trouver_blueprint(carte: dict, token: str) -> int | None:
    """Trouve l'identifiant Cardtrader (blueprint_id) d'une carte.

    V22.6 : la recherche par NOM est inutilisable (l'API plafonne à 50
    résultats, or un Pokémon populaire a des centaines de cartes — celle
    cherchée n'y figure jamais). On passe donc par le SET : on récupère
    tous les blueprints de l'expansion, puis on filtre sur le numéro
    exact. Le nom du set est déduit du dénominateur de la carte
    (ex. .../165 -> Pokémon 151) via CT_SETS.
    """
    cle = f"{carte.get('langue','fr')}|{carte['nom']}"
    ent = _ct_cache["blueprints"].get(cle)
    if ent:
        age = time.time() - ent.get("ts", 0)
        duree = CT_CACHE_BLUEPRINT_DUREE if ent.get("id") else CT_CACHE_ECHEC_DUREE
        if age < duree:
            return ent.get("id")

    nom = str(carte["nom"])
    m_xy = re.search(r"\b0*(\d+)\s*/\s*0*(\d+)\b", nom)
    m_seul = re.search(r"\b0*(\d+)\b", nom)
    numero = m_xy.group(1) if m_xy else (m_seul.group(1) if m_seul else "")
    denom = m_xy.group(2) if m_xy else ""
    if not numero:
        log.info("    [Cardtrader] '%s' : pas de numéro exploitable", nom)
        _ct_cache["blueprints"][cle] = {"id": None, "ts": time.time()}
        return None

    # Nom anglais du Pokémon (Cardtrader catalogue en anglais)
    mots = [w for w in mots_requis(nom) if w not in ("mega", "ex")]
    principal = mots[0] if mots else nom
    nom_en = CT_NOMS_EN.get(normaliser(principal), principal).lower()

    # Expansions candidates : celles dont le nom correspond au set déduit
    exps = _ct_expansions(token)
    if not exps:
        _ct_cache["blueprints"][cle] = {"id": None, "ts": time.time()}
        return None
    indices = _ct_indices_set(nom, denom)
    candidats_exp = [e for e in exps
                     if any(ind in normaliser(str(e.get("name", ""))) for ind in indices)] if indices else []

    # V24 : REPLI. Si le set n'est pas déductible du nom (promo, numéro nu),
    # on cherche dans les N expansions les plus RÉCENTES. La watchlist ne
    # suivant que des séries récentes, c'est suffisant — et entièrement
    # automatique (aucune saisie de set à maintenir).
    repli = False
    if not candidats_exp:
        nb_recents = int(_ct_cfg.get("sets_recents", 0))
        if nb_recents > 0:
            candidats_exp = _ct_expansions_recentes(token, nb_recents)
            repli = True

    blueprint_id = None
    nom_exp_trouve = ""   # V31 : extension retenue, pour diagnostic
    cm_id_trouve = None   # V33 : identifiant Cardmarket, pour le prix officiel
    diag = f"set inconnu pour /{denom}" if not candidats_exp else ""
    # Sans repli on teste peu de sets (la déduction est fiable) ; avec repli
    # on ratisse plus large, mais les catalogues sont mis en cache.
    for exp in candidats_exp[:(len(candidats_exp) if repli else 4)]:
        try:
            bps = _ct_blueprints_du_set(exp.get("id"), token)
            if not bps:
                diag = f"export {exp.get('name')} : vide ou indisponible"
                continue
            for bp in bps:
                if _ct_numero_de(bp).lstrip("0") != str(int(numero)):
                    continue
                if nom_en and nom_en not in normaliser(str(bp.get("name", ""))):
                    continue
                blueprint_id = bp.get("id")
                nom_exp_trouve = str(exp.get("name", ""))
                cm_id_trouve = bp.get("cardmarket_id")
                log.info("    [Cardtrader] '%s' -> blueprint %s (%s / %s, #%s)%s "
                         "| cardmarket_id=%s",
                         nom, blueprint_id, str(bp.get("name", ""))[:30],
                         nom_exp_trouve[:22], numero,
                         "  [via sets récents]" if repli else "", cm_id_trouve)
                break
            if blueprint_id:
                break
            diag = (f"{len(bps)} cartes dans '{exp.get('name')}' mais aucune "
                    f"'{nom_en}' #{numero}")
        except Exception as e:  # noqa: BLE001
            log.info("    [Cardtrader] '%s' : erreur export (%s)", nom, e)
            return None

    if blueprint_id is None:
        log.info("    [Cardtrader] '%s' introuvable — %s", nom, diag)

    # V31 : on mémorise AUSSI l'extension retenue. Sans elle, un
    # « blueprint trouvé mais 0 annonce en fr » est indiagnosticable : on ne
    # sait pas si Cardtrader n'a vraiment aucune carte française, ou si le
    # bot a visé la mauvaise extension. Cas suspecté : CT_SETS["165"] vaut
    # ["151"], ce qui matche l'extension JAPONAISE sv2a « 151 » aussi bien
    # que l'internationale — et une extension japonaise n'a évidemment
    # aucune impression française.
    _ct_cache["blueprints"][cle] = {"id": blueprint_id, "exp": nom_exp_trouve,
                                    "cm_id": cm_id_trouve,
                                    "ts": time.time()}
    return blueprint_id


# V23 : CALIBRATION AUTOMATIQUE eBay -> marché réel.
# Sur les cartes où l'on dispose des DEUX sources (cote eBay ET prix
# Cardtrader), on mesure le rapport réel. Le rapport MÉDIAN de toutes ces
# paires donne un coefficient correcteur qui suit le marché tout seul —
# contrairement à une cote saisie à la main, qui vieillit en silence.
_calibration_paires: list[float] = []


def _calibration_ajouter(cote_ebay: float, prix_ct: float) -> None:
    """Enregistre une paire (cote eBay, prix Cardtrader) pour la calibration."""
    if cote_ebay and prix_ct and cote_ebay > 0 and prix_ct > 0:
        rapport = prix_ct / cote_ebay
        # On ignore les rapports absurdes (mauvaise correspondance de carte) :
        # une vraie divergence de marché reste dans une fourchette raisonnable.
        if 0.2 <= rapport <= 2.0:
            _calibration_paires.append(rapport)


def _calibration_coefficient() -> float | None:
    """Coefficient correcteur médian, ou None si trop peu de mesures."""
    if len(_calibration_paires) < 5:
        return None
    return round(statistics.median(_calibration_paires), 3)


# V24 : configuration Cardtrader accessible aux fonctions internes
# (renseignée au démarrage depuis config.yaml).
_ct_cfg: dict = {}

# V24 : prix Cardtrader déjà obtenus, par carte « dénudée » de sa langue.
# Sert de garde-fou pour les cartes SANS cote eBay : une même carte ne peut
# pas valoir 100x plus dans une langue que dans une autre. Cas vécu : Mew ex
# 208 sv2a coté 51€ en JP mais 5020€ en KR (annonces aberrantes, cohérentes
# entre elles, donc invisibles pour les autres garde-fous).
_ct_prix_par_carte: dict = {}


def _ct_cle_carte(carte: dict) -> str:
    """Identifiant d'une carte indépendant de sa langue.

    Utilise l'ALIAS quand il existe (meme convention que main.py:1562 pour
    le regroupement des cotes) -- bug reel corrige le 31/08/2026 : deux
    entrees config.yaml pour la MEME carte physique dans des langues
    differentes (ex. "Plumeline ex 024" FR et "Oricorio ex 111 m2" JP,
    lie par `alias: "Plumeline"`) ont des `nom` totalement differents.
    Avant ce correctif, `_ct_cle_carte` se basait uniquement sur `nom` :
    les deux entrees ne se rencontraient donc JAMAIS dans
    `_ct_prix_par_carte`, rendant ce garde-fou totalement inoperant pour
    exactement le cas qu'il est cense proteger (deduit d'un prix marche
    affiche a 1.08€ pour Plumeline ex alors que la carte se vend
    reellement ~30€, signale par Justok)."""
    return normaliser(str(carte.get("alias") or carte.get("nom", "")))


def _ct_incoherent_entre_langues(carte: dict, prix: float, facteur: float) -> tuple[bool, str]:
    """La même carte dans une autre langue donne-t-elle un prix radicalement
    différent ? Retourne (suspect, explication)."""
    cle = _ct_cle_carte(carte)
    connus = _ct_prix_par_carte.get(cle, {})
    for lg, p in connus.items():
        if lg == carte.get("langue") or not p:
            continue
        if prix > p * facteur or prix < p / facteur:
            return True, f"{prix:.2f}€ contre {p:.2f}€ en {lg.upper()}"
    return False, ""


def _ct_memoriser_prix(carte: dict, prix: float) -> None:
    _ct_prix_par_carte.setdefault(_ct_cle_carte(carte), {})[carte.get("langue", "fr")] = prix


def cardtrader_prix(carte: dict, token: str, nb_bas: int = 5,
                    min_annonces: int = 3) -> float | None:
    """Cote Cardtrader d'une carte = moyenne des `nb_bas` annonces les
    MOINS CHÈRES dans la langue de la carte (port exclu, EUR).
    Retourne None si carte introuvable, pas d'annonce, ou erreur."""
    if not token:
        return None
    langue_ct = CT_LANGUES.get(carte.get("langue", "fr"))
    if not langue_ct:
        return None

    cle = f"{carte.get('langue','fr')}|{carte['nom']}"
    ent = _ct_cache["prix"].get(cle)
    if ent:
        age = time.time() - ent.get("ts", 0)
        # V22.2 : un SUCCÈS est gardé ~1 jour ; un ÉCHEC seulement 1 h.
        # Sinon un scan raté fige toutes les cartes en "None" pendant 20 h
        # et masque complètement le diagnostic (cas vécu en V22.1).
        duree = CT_CACHE_PRIX_DUREE if ent.get("prix") is not None else CT_CACHE_ECHEC_DUREE
        if age < duree:
            return ent.get("prix")

    blueprint_id = _ct_trouver_blueprint(carte, token)
    if not blueprint_id:
        _ct_cache["prix"][cle] = {"prix": None, "ts": time.time()}
        return None  # (déjà logué par _ct_trouver_blueprint)

    prix_final = None
    try:
        rep = requests.get(f"{CT_BASE}/marketplace/products", timeout=20,
                           headers=_ct_entete(token),
                           params={"blueprint_id": blueprint_id,
                                   "language": langue_ct})
        if rep.status_code == 200:
            data = rep.json()
            # La réponse est un dict {blueprint_id: [produits]} ou une liste
            produits = []
            if isinstance(data, dict):
                for v in data.values():
                    if isinstance(v, list):
                        produits.extend(v)
            elif isinstance(data, list):
                produits = data
            prix = []
            gradees = 0
            for p in produits:
                # Prix en centimes chez Cardtrader (cents + currency)
                pr = p.get("price") or {}
                cents = pr.get("cents")
                devise = (pr.get("currency") or "EUR").upper()
                if not cents or devise != "EUR":
                    continue
                # V24.1 GARDE-FOU 1 : écarter les cartes GRADÉES (PSA...),
                # dont les prix (souvent x5-x20) polluent la moyenne.
                # ATTENTION au piège corrigé ici : Cardtrader expose un champ
                # `graded` valant "false" sur les annonces NORMALES. Chercher
                # la chaîne "grad" dans le texte des propriétés écartait donc
                # TOUTES les annonces (« graded=false » contient « grad »).
                # Cas vécu : Mega Dragonite JP, 7 annonces saines écartées ->
                # prix gonflé à 316€ contre 265€ de tendance Cardmarket.
                # On lit désormais la VALEUR du champ, et on ne cherche les
                # sigles de gradeurs que dans la description libre.
                props = p.get("properties_hash") or {}
                est_gradee = False
                for champ in ("graded", "is_graded", "grading"):
                    v = props.get(champ)
                    if isinstance(v, bool):
                        est_gradee = est_gradee or v
                    elif isinstance(v, str) and v.strip().lower() not in ("", "false", "no", "none", "0"):
                        est_gradee = True
                # Sigles de gradeurs dans la description libre uniquement.
                description = str(p.get("description") or "").lower()
                if any(g in description for g in (" psa", "psa ", "psa10", "bgs", "cgc",
                                                  " pca", "pca ", "gradee", "graded",
                                                  "gem mint", "slab")):
                    est_gradee = True
                if est_gradee:
                    gradees += 1
                    continue
                val = float(cents) / 100.0
                if val > 0:
                    prix.append(val)
            if prix:
                prix.sort()
                # V22.7 GARDE-FOU 2 : ne garder que le "groupe bas" cohérent.
                # Une annonce à 5000€ à côté d'annonces à 50€ (gradée non
                # étiquetée, erreur de saisie) ne doit pas entrer dans la
                # moyenne : on écarte tout prix > 3x le moins cher (+5€ de
                # tolérance pour les petites cartes).
                base = prix[0]
                groupe = [p for p in prix if p <= base * 3 + 5]
                # V22.7 GARDE-FOU 3 : un marché d'1 annonce n'est pas un
                # marché. En dessous de min_annonces, pas de cote Cardtrader
                # (le bot garde la cote eBay).
                if len(groupe) < max(1, min_annonces):
                    log.info("    [Cardtrader] '%s' (%s) : seulement %d annonce(s) "
                             "cohérente(s) (< %d requises) -> ignoré",
                             carte["nom"], carte.get("langue", "fr"),
                             len(groupe), min_annonces)
                else:
                    retenus = groupe[:max(1, nb_bas)]
                    prix_final = round(sum(retenus) / len(retenus), 2)
                    ecartees = len(prix) - len(groupe)
                    if ecartees or gradees:
                        log.info("    [Cardtrader] '%s' : %d annonce(s) aberrante(s) "
                                 "et %d gradée(s) écartée(s)",
                                 carte["nom"], ecartees, gradees)
            else:
                # V31 : on affiche l'EXTENSION retenue. « 0 produit brut » sur
                # un marché européen est invraisemblable pour une carte
                # française courante : si l'extension affichée est japonaise,
                # le bot cherche la version FR dans un set qui n'en a pas.
                exp_diag = (_ct_cache["blueprints"]
                            .get(cle, {}).get("exp") or "extension inconnue")
                log.info("    [Cardtrader] '%s' (%s) : blueprint %s dans '%s' "
                         "mais 0 annonce en '%s' (%d produits bruts, %d gradées)",
                         carte["nom"], carte.get("langue", "fr"), blueprint_id,
                         exp_diag[:34], langue_ct, len(produits), gradees)
        elif rep.status_code == 429:
            log.info("    [Cardtrader] quota atteint (429), on réessaiera")
            return None
        else:
            log.info("    [Cardtrader] prix bp=%s : HTTP %s", blueprint_id, rep.status_code)
    except Exception as e:  # noqa: BLE001
        log.info("    [Cardtrader] erreur prix '%s' : %s", carte["nom"], e)
        return None

    _ct_cache["prix"][cle] = {"prix": prix_final, "ts": time.time()}
    return prix_final
