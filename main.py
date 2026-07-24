"""PokéDeals — bot d'arbitrage de cartes Pokémon (fichier unique).

TOUT le programme est dans ce seul fichier : plus de dossier modules.
Il lit config.yaml, scanne eBay/Vinted/Leboncoin, calcule les cotes,
filtre les faux positifs et envoie les alertes Telegram (+ email si activé).

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
"""
from __future__ import annotations

import base64
import csv
import hashlib
import inspect
import json
import logging
import os
import random
import re
import imaplib
import smtplib
import statistics
import sys
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import email as email_lib
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
    return t.replace("-", " ").replace("_", " ").replace(".", " ")


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
    # Cartes abîmées (fausseraient la cote vers le bas)
    "abim", "damaged", "played", "poor", "endommag",
    # Vêtements & accessoires
    "t shirt", "tee shirt", "tshirt", "pull", "sweat", "hoodie", "veste",
    "casquette", "bonnet", "pyjama", "chaussette", "chausson", "basket",
    "deguisement", "costume", "sac ", "sacoche", "cartable", "trousse",
    # Jouets & objets
    "peluche", "figurine", "funko", "pop!", "jouet", "lego", "puzzle",
    "piece", "medaille", "mug", "tasse", "gourde", "porte cle", "porte cles",
    "coque", "poster", "tapis", "protege", "sleeve", "toploader",
    # V17 : accessoires de protection/présentation (pas la carte elle-même)
    "vitrine", "affichage", "protection", "presentoir", "support",
    "boitier", "boite de protection", "etui", "pochette", "cadre",
    "magnetique", "acrylique", "screwdown", "top loader", "porte carte",
    "jeu video", "nintendo switch", "game boy", "ds ", "3ds",
    "livre", "manga", "dvd", "blu ray",
]

# Petits mots à ignorer quand on extrait le nom du Pokémon
MOTS_VIDES = {"carte", "pokemon", "ex", "gx", "v", "vstar", "vmax", "de", "n",
              "la", "le", "et", "team", "jp", "fr", "sv2a",
              "sir", "sar", "ar", "mhr"}
# Noms de sets : descriptifs, souvent absents des titres -> jamais exigés
MOTS_SETS = {"heros", "transcendants", "flammes", "fantasmagoriques",
             "equilibre", "parfait", "chaos", "ascendant", "nuit", "noire",
             "serie", "151",
             # V16.1 : descriptifs de rareté/produit (jamais exigés dans un titre)
             "trainer", "gallery", "promo", "alternative", "ultra", "rare",
             "celeste", "prismatiques", "mascarade", "crepusculaire",
             "aventures", "ensemble", "stars", "etincelantes", "de", "lilie"}

# V16 : gestion des langues.
# - Suffixe ajouté aux requêtes eBay/Vinted/Leboncoin selon la langue.
SUFFIXES_LANGUE = {"jp": " japonaise", "en": " anglaise",
                   "kr": " coréenne", "cn": " chinoise"}
# - Marqueurs devant figurer dans le TITRE pour valider la langue.
#   Les marqueurs courts (<= 3 lettres) sont comparés mot à mot pour
#   éviter les faux positifs ("kr" à l'intérieur d'un autre mot, etc.).
MARQUEURS_LANGUE = {
    # NB : les codes de SET (sv2a, m2a...) ne sont PAS des marqueurs de
    # langue — une carte 151 coréenne ou chinoise porte aussi "sv2a". La
    # langue se prouve par un mot de langue, des caractères, ou la
    # localisation eBay, jamais par le code de set.
    "jp": ["japonaise", "japonais", "japanese", "japon", "jpn", "jap", "jp"],
    "en": ["anglaise", "anglais", "english", "eng"],
    "kr": ["coreenne", "coreen", "korean", "korea", "kor", "kr"],
    "cn": ["chinoise", "chinois", "chinese", "china", "zh", "cn"],
    # V20 : langues EUROPÉENNES non désirées. Une carte italienne/allemande/
    # espagnole au même numéro qu'une française vaut souvent moins et créait
    # de faux deals. On les détecte par le mot de langue explicite ET par des
    # mots très caractéristiques présents dans les annonces ou sur la carte.
    "it": ["italienne", "italien", "italian", "italiano", "italia",
           "condizioni", "come da foto", "carta", "fase",
           # V22.8 : mots relevés dans de vraies annonces Vinted italiennes
           # qui avaient un titre parfaitement « neutre » (le piège : seule
           # la description trahissait la langue).
           "comprare", "spedisco", "spedizione", "chiedere", "informazioni",
           "lingua", "espansione", "numero della", "nome della", "carte da",
           "perfette", "ottime", "buone condizioni", "regalo", "prezzo",
           "disponibile", "vendo", "scambio", "grazie", "salve", "ciao"],
    "de": ["allemande", "allemand", "german", "deutsch", "zustand", "karte", "sammlung"],
    "es": ["espagnole", "espagnol", "spanish", "espanol", "espana", "estado", "carta espanola"],
    "pt": ["portugaise", "portugais", "portuguese", "portugues"],
    "nl": ["nederlands", "kaart"],
}
# Langues à REJETER pour une carte française (tout sauf le français).
LANGUES_NON_FR = ("jp", "en", "kr", "cn", "it", "de", "es", "pt", "nl")

# V22.8 : formules signalant une ENCHÈRE DÉGUISÉE. Le vendeur affiche un
# prix dérisoire (1€) et invite à surenchérir en commentaire — le prix
# affiché n'a alors aucun rapport avec le prix de vente réel.
SIGNAUX_ENCHERE = (
    "non comprare", "ne pas acheter", "n achetez pas", "nachetez pas",
    "do not buy", "dont buy", "enchere", "encheres", "asta", "offerta",
    "faire offre", "meilleure offre", "au plus offrant", "plus offrant",
    "chiedere per informazioni", "mp pour prix", "prix en mp",
    "commentaire pour prix", "spedisco energia", "spedisco solo energia",
)
TOUS_MARQUEURS = [m for lst in MARQUEURS_LANGUE.values() for m in lst]


def _marqueur_present(marqueur: str, texte_norm: str, jetons: list[str]) -> bool:
    if len(marqueur) <= 3:
        return marqueur in jetons
    return marqueur in texte_norm


# V18 : détection de caractères asiatiques dans le titre ORIGINAL (avant
# normalisation, qui les supprimerait). Une annonce contenant フシギダネ,
# ピカチュウ, 리자몽, 妙蛙种子... est forcément une carte étrangère, même si
# le reste du titre est en français.
# V19 : on distingue MAINTENANT la langue asiatique (jp / kr / cn), car une
# carte japonaise et sa version coréenne partagent le MÊME numéro. Sans
# cette distinction, une annonce coréenne (moins chère) polluerait la cote
# japonaise et inversement — le même piège que FR/JP.
import unicodedata as _ud


def _script_asiatique(texte: str) -> str | None:
    """Renvoie 'jp', 'kr' ou 'cn' selon les caractères présents, sinon None.
    - Hangul (한글)            -> 'kr' (sans ambiguïté)
    - Hiragana/Katakana (かな) -> 'jp' (sans ambiguïté)
    - Idéogrammes seuls        -> 'cn' (Hanzi ; les kanji japonais isolés sont
      rares dans les titres d'annonces, qui contiennent presque toujours des
      kana ; on tranche donc côté chinois par défaut, la localisation eBay
      restant le signal prioritaire pour lever un éventuel doute).
    """
    a_hangul = a_kana = a_ideo = False
    for ch in texte or "":
        code = ord(ch)
        if 0xAC00 <= code <= 0xD7A3:            # hangul
            a_hangul = True
        elif 0x3040 <= code <= 0x30FF:          # hiragana + katakana
            a_kana = True
        elif (0x4E00 <= code <= 0x9FFF
              or 0x3400 <= code <= 0x4DBF):     # idéogrammes CJK
            a_ideo = True
    if a_hangul:
        return "kr"
    if a_kana:
        return "jp"
    if a_ideo:
        return "cn"
    return None


def extraire_numero(texte: str) -> str | None:
    m = RE_NUMERO.search(texte or "")
    return f"{int(m.group(1))}/{int(m.group(2))}" if m else None


# V17.4 : les cartes Nuit Noire françaises (set PBL) ont un numéro SANS
# dénominateur ("116", "120"...) au lieu du format "X/Y". Sans traitement
# spécial, "Darkrai ex 116" et "Darkrai ex 120" deviennent indiscernables
# (même Pokémon, filtre incapable de distinguer 116 de 120). On extrait donc
# ce numéro nu du NOM de carte, et on l'exige comme un token isolé dans le
# titre, en rejetant tout autre numéro nu du même Pokémon.
RE_NUMERO_NU = re.compile(r"\b(\d{2,3})\b")


def numero_nu_voulu(nom_carte: str) -> str | None:
    """Renvoie le numéro nu (ex '116') si le nom en contient un ET n'a pas
    de numéro au format X/Y. Sinon None."""
    if extraire_numero(nom_carte):
        return None  # déjà un numéro X/Y : géré par la voie normale
    m = RE_NUMERO_NU.search(nom_carte or "")
    return m.group(1) if m else None


def numeros_nus_titre(titre: str) -> list[str]:
    """Tous les numéros nus (2-3 chiffres) présents dans un titre normalisé,
    en excluant ceux qui font partie d'un format X/Y (déjà gérés ailleurs)."""
    t = titre or ""
    # On retire d'abord les 'X/Y' pour ne pas capturer leurs composantes.
    sans_fraction = RE_NUMERO.sub(" ", t)
    return RE_NUMERO_NU.findall(sans_fraction)


def mots_requis(nom_carte: str) -> list[str]:
    """Mots distinctifs de la carte, TOUS exigés dans le titre.
    'Méga-Dracolosse ex 290/217' -> ['mega', 'dracolosse']
    'Zoroark de N ex héros transcendants' -> ['zoroark']
    """
    return [mot for mot in normaliser(nom_carte).split()
            if len(mot) >= 3 and mot not in MOTS_VIDES and mot not in MOTS_SETS
            and not any(c.isdigit() for c in mot)]


# V16.1 : pour une carte SANS numéro (promo, Trainer Gallery), le type de
# carte (vmax / vstar / v / gx / ex) DOIT rester distinctif, sinon une V
# et une VMAX du même Pokémon deviennent indiscernables. On garde donc ces
# marqueurs de rareté que mots_requis() écarte normalement.
TYPES_CARTE = {"vmax", "vstar", "gx", "ex", "v"}


def mots_requis_stricts(nom_carte: str) -> list[str]:
    base = mots_requis(nom_carte)
    for mot in normaliser(nom_carte).split():
        if mot in TYPES_CARTE and mot not in base:
            base.append(mot)
    return base


def _pays_ebay(plateforme: str) -> str | None:
    """Extrait le code pays d'une plateforme 'eBay (JP)' -> 'jp'. None sinon."""
    p = str(plateforme or "")
    if p.startswith("eBay (") and p.endswith(")"):
        code = p[6:-1].strip().lower()
        return code or None
    return None


# Correspondance pays eBay -> langue de la carte
_PAYS_VERS_LANGUE = {"jp": "jp", "kr": "kr", "cn": "cn"}


def annonce_pertinente(titre: str, nom_carte: str, langue: str = "fr", alias: str = "",
                       plateforme: str = "") -> tuple[bool, str]:
    """Filtre strict : (pertinent, raison).

    V18 : `plateforme` permet d'utiliser la localisation eBay comme signal
    de langue. Une annonce "eBay (JP)" au titre 100% français est bien une
    carte japonaise (localisée au Japon) : elle doit être routée vers
    l'entrée japonaise, pas vers l'entrée française.
    """
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

    # 2bis) Cohérence de LANGUE. Une carte coréenne vaut souvent moins que
    #    sa jumelle japonaise (même numéro !) : les mélanger fausserait les
    #    cotes. V19 : on distingue finement jp / kr / cn.
    #    Signaux de langue, par ordre de fiabilité :
    #      1. script du titre (hangul=kr, kana=jp, idéogrammes=cn)
    #      2. localisation eBay (JP/KR/CN)
    #      3. marqueurs texte ("korean", "japonaise"...)
    script = _script_asiatique(titre)              # 'jp'/'kr'/'cn'/None
    pays = _pays_ebay(plateforme)
    langue_du_pays = _PAYS_VERS_LANGUE.get(pays) if pays else None
    titre_a_des_caracteres_asiatiques = script is not None
    origine_asiatique = titre_a_des_caracteres_asiatiques or bool(langue_du_pays)
    jetons_langue = t.split()

    # Quelle(s) langue(s) asiatique(s) l'annonce revendique-t-elle par son texte ?
    langues_marquees = {lg for lg, mots in MARQUEURS_LANGUE.items()
                        if any(_marqueur_present(mm, t, jetons_langue) for mm in mots)}

    if langue in (None, "", "fr"):
        if origine_asiatique or langues_marquees:
            return False, "carte étrangère (caractères/origine) hors recherche FR"
    else:
        # Carte asiatique (jp/kr/cn). Elle doit correspondre à SA langue et
        # rejeter les signaux d'une AUTRE langue asiatique.
        autres = {"jp", "kr", "cn"} - {langue}
        # Signal contradictoire = l'annonce pointe clairement vers une autre langue
        if script in autres:
            return False, f"script {script} ≠ langue {langue}"
        if langue_du_pays in autres:
            return False, f"localisation {langue_du_pays} ≠ langue {langue}"
        if langues_marquees and langue not in langues_marquees and not (script == langue or langue_du_pays == langue):
            return False, f"marqueur {langues_marquees} ≠ langue {langue}"
        # Signal POSITIF requis : au moins un indice confirme la bonne langue
        confirme = (script == langue
                    or langue_du_pays == langue
                    or langue in langues_marquees)
        if not confirme:
            return False, f"langue '{langue}' non confirmée dans le titre"

    # 3) Cohérence Méga : une carte Méga ne pollue pas une recherche non-Méga
    #    et inversement. ATTENTION : "méga" peut aussi venir du NOM DU SET
    #    "Méga-Évolution" (ex. un Bulbizarre de ce set n'est PAS une carte
    #    Méga). On ne compte donc "méga" comme marqueur de carte Méga que
    #    s'il n'est pas immédiatement suivi de "évolution"/"evolution".
    requis = mots_requis(nom_carte)
    jetons = t.split()
    titre_mega = False
    for i, jet in enumerate(jetons):
        if jet in ("mega", "m"):
            suivant = jetons[i + 1] if i + 1 < len(jetons) else ""
            if suivant not in ("evolution", "evolutions"):
                titre_mega = True
                break
    carte_mega = "mega" in requis
    if titre_mega and not carte_mega:
        return False, "carte Méga hors recherche"
    if carte_mega and not titre_mega:
        return False, "'mega' absent du titre"

    # 4) Le nom du Pokémon (mot distinctif principal) doit être présent.
    #    V16 : un alias (ex. Tortank pour Blastoise) est aussi accepté,
    #    car les vendeurs français titrent souvent les cartes étrangères
    #    avec le nom français du Pokémon.
    pokemon = next((m for m in requis if m != "mega"), None)
    noms_acceptes = [pokemon] if pokemon else []
    if alias:
        noms_acceptes += [m for m in normaliser(alias).split() if len(m) >= 3]
    if noms_acceptes and not any(n in t for n in noms_acceptes):
        return False, f"'{pokemon}' (ou alias) absent du titre"

    # 5) Le NUMÉRO de carte est la preuve la plus fiable.
    #    V15 : si la carte recherchée porte un numéro, il est OBLIGATOIRE
    #    dans le titre de l'annonce.
    #    Pourquoi ? Un "Dracaufeu" à 5€ et un "Dracaufeu ex 199/165" à
    #    200€ portent le même nom : sans numéro, impossible de trancher.
    #    Une annonce sans numéro est donc écartée des cotes ET des alertes.
    #    On rate quelques annonces, mais on élimine les fausses cotes —
    #    et une cote fausse coûte bien plus cher qu'une annonce ratée.
    numero_voulu = extraire_numero(nom_carte)
    numero_annonce = extraire_numero(titre)
    if numero_voulu:
        if not numero_annonce:
            return False, "aucun numéro dans le titre (exigé depuis V15)"
        if numero_annonce != numero_voulu:
            return False, f"mauvais numéro ({numero_annonce} != {numero_voulu})"
        # bon numéro + bon pokémon : suffisant, on s'arrête là
    else:
        # Le nom recherché n'a pas de numéro X/Y (ex. versions SIR, promos,
        # TG, ou cartes PBL Nuit Noire à numéro nu). On exige tous les mots
        # distinctifs, EN CONSERVANT le type de carte (vmax/v/ex...) pour ne
        # pas confondre une V et une VMAX du même Pokémon. Le nom principal
        # peut être couvert par l'alias.
        jetons_titre = t.split()
        for mot in mots_requis_stricts(nom_carte):
            if mot == "mega":
                continue
            if mot == pokemon and alias and any(
                    n in t for n in normaliser(alias).split() if len(n) >= 3):
                continue  # nom principal couvert par l'alias
            # Les types de carte se comparent mot à mot ("v" ne doit pas
            # matcher le "v" de "vmax"). Les autres mots : sous-chaîne OK.
            if mot in TYPES_CARTE:
                if mot not in jetons_titre:
                    return False, f"type '{mot}' absent du titre"
            elif mot not in t:
                return False, f"'{mot}' absent du titre"

        # V17.4 : cartes PBL à numéro nu (Nuit Noire FR : "116", "120"...).
        # Le numéro voulu DOIT figurer dans le titre, et aucun AUTRE numéro
        # nu ne doit y figurer (sinon "Darkrai ex 120" matcherait la 116).
        num_nu = numero_nu_voulu(nom_carte)
        if num_nu:
            nus = numeros_nus_titre(titre)
            if num_nu not in nus:
                return False, f"numéro {num_nu} absent du titre"
            autres = [n for n in nus if n != num_nu]
            if autres:
                return False, f"autre numéro présent ({autres[0]} ≠ {num_nu})"
            # Numéro nu exigé et présent : on NE rejette PAS sur numero_annonce
            # (le titre peut aussi contenir un X/Y, ex '116/086' — cohérent).
            return True, "ok"

        # ... et refuser une annonce qui, elle, porte un numéro X/Y : une carte
        # sans numéro (SIR non numérotée) n'est pas une carte numérotée.
        if numero_annonce:
            return False, "annonce numérotée ≠ version sans numéro (SIR)"

    return True, "ok"


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
        port = 0.0
        opts = it.get("shippingOptions") or []
        if opts:
            try:
                port = float(opts[0]["shippingCost"]["value"])
            except (KeyError, ValueError, TypeError):
                port = 0.0
        pays = ((it.get("itemLocation") or {}).get("country") or "FR").upper()
        if pays != "FR":
            if not international:
                continue
            if not opts:
                continue  # port inconnu depuis l'étranger : prudence
            if port > port_max_intl:
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
            }
        )
    return annonces


def _localisation_incoherente(annonce: dict, langue: str) -> bool:
    """V18 : True si l'annonce vient d'un pays incompatible avec la langue
    recherchée. Une carte FRANÇAISE ne se vend pas depuis le Japon : les
    annonces "eBay (JP)", "eBay (KR)", "eBay (CN)" doivent être écartées de
    la cote ET des deals d'une carte FR (sinon la cote est gonflée par des
    cartes japonaises au même numéro, cf. Pikachu 173/165 et Bulbizarre
    166/165 vendus en version JP à des prix bien plus élevés).
    """
    if langue not in (None, "", "fr"):
        return False  # pour une carte JP/KR/CN, l'origine étrangère est normale
    plateforme = str(annonce.get("plateforme", ""))
    # "eBay (JP)", "eBay (DE)"... : tout ce qui n'est pas FR est suspect pour
    # une carte française d'un set (151, Méga) qui existe aussi en asiatique.
    if plateforme.startswith("eBay (") and not plateforme.startswith("eBay (FR"):
        return True
    return False


def calculer_cote(annonces: list[dict], cfg_cote: dict, nom_carte: str = "",
                  langue: str = "fr", alias: str = "") -> tuple[float | None, int]:
    """Cote = médiane des prix des annonces PERTINENTES × coefficient.

    V15 : le filtre `annonce_pertinente` exige le numéro exact de la carte.
    V16 : il vérifie aussi la langue (texte). V18 : on écarte en plus les
    annonces localisées à l'étranger pour une carte FR (eBay JP/KR/CN), qui
    gonflaient la cote avec des versions asiatiques au même numéro.
    Retourne (cote, nb_annonces_utilisées).
    """
    if nom_carte:
        # V20 diagnostic : on garde (prix, titre, plateforme) des annonces
        # retenues pour pouvoir les afficher dans les logs et repérer ce qui
        # gonfle une cote.
        retenues = [(a["prix"], a.get("titre", "")[:70], a.get("plateforme", ""))
                    for a in annonces
                    if a["prix"] > 0
                    and not _localisation_incoherente(a, langue)
                    and annonce_pertinente(a.get("titre", ""), nom_carte, langue, alias, a.get("plateforme", ""))[0]]
        retenues.sort()
        prix = [p for p, _, _ in retenues]
    else:
        retenues = []
        prix = sorted(a["prix"] for a in annonces if a["prix"] > 0)

    if len(prix) < int(cfg_cote.get("minimum_annonces", 8)):
        return None, len(prix)

    # Élimination des valeurs aberrantes (IQR) : vendeurs fantaisistes, erreurs de prix
    if len(prix) >= 4:
        q = statistics.quantiles(prix, n=4)
        iqr = q[2] - q[0]
        bas, haut = q[0] - 1.5 * iqr, q[2] + 1.5 * iqr
        nettoyes = [p for p in prix if bas <= p <= haut] or prix
    else:
        nettoyes = prix

    # V17 : cote = MÉDIANE des prix nettoyés (après filtrage IQR).
    reference = statistics.median(nettoyes)
    cote = round(reference * float(cfg_cote.get("coefficient_marche", 1.0)), 2)

    # V20 diagnostic : détail des annonces qui composent la cote (visible dans
    # les logs GitHub). Permet de repérer une annonce anormalement chère qui
    # gonfle la médiane. À retirer une fois le diagnostic terminé.
    if nom_carte and retenues:
        rejetes_iqr = [p for p in prix if p not in nettoyes]
        log.info("    [cote %s] médiane=%.2f€ ×%.2f = %.2f€ | %d annonces retenues%s",
                 nom_carte, reference, float(cfg_cote.get("coefficient_marche", 1.0)),
                 cote, len(nettoyes),
                 f" ({len(rejetes_iqr)} écartées IQR : {rejetes_iqr})" if rejetes_iqr else "")
        for p, titre, plat in retenues:
            marque = " ← ÉCARTÉE(IQR)" if p not in nettoyes else ""
            log.info("        %.2f€  [%s] %s%s", p, plat, titre, marque)

    return cote, len(nettoyes)


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
CT_CACHE_VERSION = 4                 # incrémenter pour purger le cache
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
        os.makedirs(os.path.dirname(CT_CACHE_FICHIER), exist_ok=True)
        with open(CT_CACHE_FICHIER, "w", encoding="utf-8") as f:
            json.dump({"sig": _ct_signature_code(), **_ct_cache}, f, ensure_ascii=False)
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
    "098": ["lost", "origin"],
}


# Code de set japonais présent dans le nom -> mots-clés Cardtrader.
# Beaucoup de cartes JP/KR n'ont pas de dénominateur (« Mew ex 195 sv2a »)
# mais portent leur code de set, ce qui suffit à cibler l'expansion.
CT_SETS_JP = {
    "sv2a": ["151"], "sv8a": ["terastal"], "sv5a": ["crimson"],
    "sv9": ["battle partners"], "s8b": ["vmax climax"], "s12": ["paradigm"],
    "m1l": ["mega evolution"], "m2": ["mega"], "m2a": ["dream"],
    "m3": ["mega"], "m4": ["mega"], "m5": ["abyss"], "mc": ["start deck"],
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

    blueprint_id = None
    diag = f"set inconnu pour /{denom}" if not candidats_exp else ""
    for exp in candidats_exp[:4]:
        try:
            rep = requests.get(f"{CT_BASE}/blueprints/export", timeout=30,
                               headers=_ct_entete(token),
                               params={"expansion_id": exp.get("id")})
            if rep.status_code != 200:
                diag = f"export {exp.get('name')} : HTTP {rep.status_code}"
                continue
            bps = rep.json()
            if not isinstance(bps, list):
                diag = f"export {exp.get('name')} : réponse inattendue"
                continue
            for bp in bps:
                if _ct_numero_de(bp).lstrip("0") != str(int(numero)):
                    continue
                if nom_en and nom_en not in normaliser(str(bp.get("name", ""))):
                    continue
                blueprint_id = bp.get("id")
                log.info("    [Cardtrader] '%s' -> blueprint %s (%s / %s, #%s)",
                         nom, blueprint_id, str(bp.get("name", ""))[:30],
                         str(exp.get("name", ""))[:22], numero)
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

    _ct_cache["blueprints"][cle] = {"id": blueprint_id, "ts": time.time()}
    return blueprint_id


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
                # V22.7 GARDE-FOU 1 : écarter les cartes GRADÉES (PSA...),
                # dont les prix (souvent x5-x20) polluent la moyenne — cause
                # probable du Mew ex 208 KR affiché à 5020€.
                props = p.get("properties_hash") or {}
                texte_annonce = (str(p.get("description") or "") + " "
                                 + " ".join(f"{k}={v}" for k, v in props.items())).lower()
                if any(g in texte_annonce for g in ("grad", "psa", "bgs", "cgc", "pca")):
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
                log.info("    [Cardtrader] '%s' (%s) : blueprint %s trouvé mais "
                         "0 annonce en '%s' (%d produits bruts, %d gradées)",
                         carte["nom"], carte.get("langue", "fr"), blueprint_id,
                         langue_ct, len(produits), gradees)
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
    prioritaire sur la déduction (pour corriger un cas particulier)."""
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
            return f"{m_set.group(1)}-{int(m_num.group(1))}"
        # Pas de code de set : le dénominateur peut identifier le set.
        m_xy = re.search(r"\b0*(\d+)/0*(\d+)\b", nom)
        if m_xy:
            set_id = _DENOM_VERS_SET.get(("jp", int(m_xy.group(2))))
            if set_id:
                return f"{set_id}-{int(m_xy.group(1))}"
        return None
    # Cartes françaises : Série 151 = set international sv03.5
    m151 = re.search(r"\b(\d+)/165\b", nom)
    if m151:
        return f"sv03.5-{int(m151.group(1))}"
    # Promos identifiables : SWSH087 -> swshp ; "promo" SV -> svp
    m_swsh = re.search(r"\bSWSH0*(\d+)\b", nom)
    if m_swsh:
        return f"swshp-SWSH{int(m_swsh.group(1)):03d}"
    if "promo" in nom.lower():
        m_num = re.search(r"\b0*(\d+)\b", nom)
        if m_num:
            return f"svp-{int(m_num.group(1))}"
    # Autres sets FR par dénominateur confirmé
    m_xy = re.search(r"\b0*(\d+)/0*(\d+)\b", nom)
    if m_xy:
        set_id = _DENOM_VERS_SET.get(("fr", int(m_xy.group(2))))
        if set_id:
            return f"{set_id}-{int(m_xy.group(1))}"
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
        os.makedirs(os.path.dirname(API_CACHE_FICHIER), exist_ok=True)
        with open(API_CACHE_FICHIER, "w", encoding="utf-8") as f:
            json.dump(_api_prix_cache, f, ensure_ascii=False)
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

    On filtre par le numéro local ET (si dispo) le dénominateur = taille du
    set, pour ne pas confondre deux cartes de même numéro dans des sets
    différents. La langue française passe par les sets internationaux, donc
    on interroge l'API en anglais (les prix Cardmarket sont les mêmes)."""
    nom = str(carte["nom"])
    m_xy = re.search(r"\b0*(\d+)/0*(\d+)\b", nom)
    m_seul = re.search(r"\b0*(\d+)\b", nom)
    numero = m_xy.group(1) if m_xy else (m_seul.group(1) if m_seul else None)
    denom = m_xy.group(2) if m_xy else None
    if not numero:
        return None, None
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
            if denom and total and str(total) != denom:
                continue  # mauvais set (dénominateur différent)
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
    requete += SUFFIXES_LANGUE.get(langue, "")
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
# V17.1 : purge par VERSION plutôt que par date.
# La purge par timestamp (DEPLOIEMENT_TS) laissait survivre les cotes
# recalculées le jour même du déploiement (Dracaufeu figé à 432,50€,
# Darkrai 099 à 11,16€...). On passe à un "tag" : si le tag stocké dans
# data/cotes.json ne correspond PAS à PURGE_VERSION ci-dessous, TOUT
# l'historique est jeté au prochain scan. Pour forcer une remise à zéro
# à l'avenir, il suffit d'incrémenter ce numéro.
PURGE_VERSION = 19  # V20 : purge des cotes calculées sur trop peu d'annonces (marché mince)
# Conservé pour compatibilité de lecture des anciens fichiers (non utilisé
# pour la purge elle-même).
DEPLOIEMENT_TS = 1784160000  # 16/07/2026 00:00 UTC


def _charger_historique() -> dict:
    if not os.path.exists(FICHIER_COTES):
        return {}
    try:
        with open(FICHIER_COTES, "r", encoding="utf-8") as f:
            brut = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}
    # Purge par version : si le fichier n'a pas le bon tag, on repart de zéro.
    if not isinstance(brut, dict) or brut.get("_purge_version") != PURGE_VERSION:
        log.info("Historique des cotes réinitialisé (purge V%s) : repart propre", PURGE_VERSION)
        return {}
    # Format valide et à jour : on retire la clé technique et on renvoie les cotes.
    return {nom: entrees for nom, entrees in brut.items() if nom != "_purge_version"}


def sauvegarder_historique() -> None:
    h = historique()
    os.makedirs(os.path.dirname(FICHIER_COTES), exist_ok=True)
    # On réécrit le tag de version à chaque sauvegarde.
    a_ecrire = {"_purge_version": PURGE_VERSION}
    a_ecrire.update(h)
    with open(FICHIER_COTES, "w", encoding="utf-8") as f:
        json.dump(a_ecrire, f, ensure_ascii=False, indent=1)


_historique = None


def historique() -> dict:
    global _historique
    if _historique is None:
        _historique = _charger_historique()
    return _historique


# ====================================================================
# LEBONCOIN VIA ALERTES EMAIL (V11)
# Le scraping direct de Leboncoin est bloqué par DataDome (403 permanent
# depuis les serveurs). Solution officielle et sans risque de ban :
# l'utilisateur crée des "recherches sauvegardées" sur leboncoin.fr, le
# site envoie un email à chaque nouvelle annonce, et le bot lit ces
# emails dans Gmail (IMAP) pour les injecter dans le pipeline normal.
# ====================================================================

RE_LBC_LIEN = re.compile(r'https://www\.leboncoin\.fr/(?:[a-z_]+/)?(?:ad/)?[a-z_]*/?(\d{6,12})[^"\s<>]*')
RE_LBC_PRIX = re.compile(r'(\d{1,3}(?:[\s.\u202f\u00a0]?\d{3})*(?:[,.]\d{2})?)\s*€')


def _html_vers_texte(html: str, separateur: str = " ") -> str:
    """Dégrossit du HTML d'email en texte ; chaque balise devient `separateur`."""
    html = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<[^>]+>', separateur, html)
    html = html.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&#8239;', ' ')
    return re.sub(r'[ \t\r\n]+', ' ', html)


def _prix_depuis_texte(texte: str) -> float | None:
    m = RE_LBC_PRIX.search(texte)
    if not m:
        return None
    brut = m.group(1).replace(' ', '').replace('\u202f', '').replace('\u00a0', '')
    brut = brut.replace('.', '').replace(',', '.') if ',' in brut else brut.replace(' ', '')
    try:
        return float(brut)
    except ValueError:
        return None


def lbc_extraire_annonces_email(html: str) -> list[dict]:
    """Extrait (id, url, titre?, prix?) des emails d'alerte Leboncoin.

    Analyse tolérante : on repère chaque lien d'annonce, puis on cherche un
    titre et un prix dans le texte qui l'entoure. Les emails LBC changent de
    mise en page régulièrement, donc on reste volontairement générique.
    """
    annonces = []
    vus = set()
    for m in RE_LBC_LIEN.finditer(html):
        ad_id = m.group(1)
        if ad_id in vus:
            continue
        vus.add(ad_id)
        # Fenêtre de texte autour du lien pour trouver titre et prix
        debut, fin = max(0, m.start() - 600), min(len(html), m.end() + 600)
        fenetre = html[debut:fin]
        # Le prix d'une annonce LBC suit son lien : on cherche d'abord APRÈS,
        # sinon la fenêtre attraperait le prix de l'annonce précédente.
        prix = _prix_depuis_texte(_html_vers_texte(html[m.end():fin]))
        if prix is None:
            prix = _prix_depuis_texte(_html_vers_texte(fenetre))

        # Titre : d'abord le texte du lien <a ...>...</a> de cette annonce
        titre = ""
        m_a = re.search(r'<a[^>]*' + re.escape(ad_id) + r'[^>]*>(.*?)</a>',
                        fenetre, flags=re.DOTALL | re.IGNORECASE)
        if m_a:
            titre = _html_vers_texte(m_a.group(1)).strip()
        if not (10 <= len(titre) <= 120):
            # Secours : plus long segment de texte plausible autour du lien
            titre = ""
            for morceau in _html_vers_texte(fenetre, separateur="|").split('|'):
                morceau = morceau.strip()
                if 10 <= len(morceau) <= 120 and '€' not in morceau and 'http' not in morceau:
                    if len(morceau) > len(titre):
                        titre = morceau
        annonces.append({
            "id": f"lbc-{ad_id}",
            "url": f"https://www.leboncoin.fr/ad/collection/{ad_id}",
            "titre": titre,
            "prix": prix if prix is not None else 0.0,
            "port": 0.0,
            "plateforme": "Leboncoin (alerte)",
            "etat_texte": "",
            "vendeur_nom": "voir annonce",
            "vendeur_pct": 100,
        })
    return [a for a in annonces if a["prix"] > 0 and a["titre"]]


def lbc_relever_alertes_email(cfg: dict, secrets: dict) -> list[dict]:
    """Lit les emails d'alerte Leboncoin non lus dans Gmail et en extrait les annonces."""
    conf = cfg.get("leboncoin_alertes_email", {})
    if not conf.get("actif"):
        return []
    mdp = secrets.get("GMAIL_APP_PASSWORD", "")
    adresse = cfg.get("email", {}).get("destinataire", "")
    if not mdp or not adresse:
        log.info("Alertes email LBC : GMAIL_APP_PASSWORD ou adresse manquant — ignoré")
        return []

    annonces = []
    try:
        imap = imaplib.IMAP4_SSL(conf.get("imap_hote", "imap.gmail.com"))
        imap.login(adresse, mdp)
        imap.select(conf.get("boite", "INBOX"))
        # Emails NON LUS venant de Leboncoin
        statut, donnees = imap.search(None, '(UNSEEN FROM "leboncoin")')
        ids = donnees[0].split() if statut == "OK" and donnees and donnees[0] else []
        for num in ids[-20:]:  # au plus 20 emails par passage
            statut, msg_data = imap.fetch(num, "(RFC822)")  # fetch marque l'email comme lu
            if statut != "OK":
                continue
            message = email_lib.message_from_bytes(msg_data[0][1])
            html = ""
            for part in message.walk():
                if part.get_content_type() == "text/html":
                    charset = part.get_content_charset() or "utf-8"
                    html += part.get_payload(decode=True).decode(charset, errors="replace")
            if html:
                annonces.extend(lbc_extraire_annonces_email(html))
        imap.logout()
        if annonces:
            log.info("Alertes email LBC : %d annonce(s) extraite(s) de %d email(s)", len(annonces), len(ids))
    except Exception as e:  # noqa: BLE001
        log.warning("Alertes email LBC en erreur (non bloquant) : %s", e)
    return annonces



def cote_lissee(nom_carte: str) -> float | None:
    """Médiane des cotes des 7 derniers jours (l'historique est déjà purgé
    par version au chargement, donc plus besoin de borne de déploiement)."""
    entrees = historique().get(nom_carte, [])
    limite = time.time() - VALIDITE_JOURS * 86400
    valeurs = [e["cote"] for e in entrees if e.get("ts", 0) >= limite]
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

    # 2) Cote du jour depuis eBay (annonces FILTRÉES), ajoutée à l'historique
    cote_instant, nb_pertinentes = calculer_cote(
        annonces_ebay, cfg["cote"], carte["nom"],
        carte.get("langue", "fr"), carte.get("alias", ""))
    if cote_instant:
        enregistrer_cote(carte["nom"], cote_instant)

    # 3) Cote lissée (médiane des derniers passages)
    cote = cote_lissee(carte["nom"])
    if cote is None:
        cote = cote_instant
    if cote is None:
        log.info("Cote introuvable pour '%s' (%d annonce(s) pertinente(s), minimum %s requis)",
                 carte.get("nom"), nb_pertinentes, cfg["cote"].get("minimum_annonces", 8))
        return None, 0
    return cote, nb_pertinentes


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
    # V15 : exige aussi le numéro exact de la carte dans le titre.
    # V16 : exige la cohérence de langue et accepte l'alias du Pokémon.
    pertinent, raison = annonce_pertinente(
        annonce.get("titre", ""), annonce.get("carte", ""),
        annonce.get("langue", "fr"), annonce.get("alias", ""), annonce.get("plateforme", ""))
    if not pertinent:
        return None, raison

    # V18 : une carte FRANÇAISE ne s'achète pas depuis le Japon. On rejette
    # les annonces localisées à l'étranger (eBay JP/KR/CN) qui, au même
    # numéro, sont des versions asiatiques bien plus chères et faussaient
    # les deals (cf. Pikachu 173/165 japonais à 81€ vu comme un deal).
    if _localisation_incoherente(annonce, annonce.get("langue", "fr")):
        return None, "annonce localisée à l'étranger pour une carte FR"

    prix = float(annonce.get("prix", 0))
    port = float(annonce.get("port", 0))
    total = prix + port

    prix_max = float(r.get("prix_max", 0) or 0)
    if prix_max > 0 and total > prix_max:
        return None, f"au-dessus du budget ({total:.2f}€)"
    # V16 : plafond de port spécifique pour les annonces eBay étrangères
    port_max = float(r["frais_port_max"])
    if str(annonce.get("plateforme", "")).startswith("eBay ("):
        port_max = float(r.get("frais_port_max_international", 10.0))
    if port > port_max:
        return None, f"port trop cher ({port:.2f}€ > {port_max:.2f}€)"
    if not _etat_ok(annonce.get("etat_texte", ""), cfg["etats_acceptes"], cfg["etats_refuses"]):
        return None, "état refusé (abîmée / gradée / jouée)"

    # --- Achat : total net au moins 10% sous la cote ---
    # Marge par carte (override), sinon marge globale
    marge = marge_achat if marge_achat is not None else r["marge_achat"]
    seuil_achat = cote * (1 - marge)
    if total > seuil_achat:
        return None, f"pas assez sous la cote ({total:.2f}€ > seuil {seuil_achat:.2f}€)"

    # V22.8 : GARDE-FOU « TROP BEAU POUR ÊTRE VRAI ».
    # Une carte à 340€ affichée 1€ n'est pas une affaire : c'est un prix
    # d'appel pour créer des enchères en commentaire (pratique courante et
    # interdite sur Vinted), un article factice, ou une erreur. Cas vécu :
    # Méga-Lucario Gold 188/132 à 1€ + port, description « Non comprare a
    # 1 € » (= « n'achetez pas à 1 € »). En dessous d'un certain pourcentage
    # de la cote, une annonce est suspecte, pas exceptionnelle.
    seuil_absurde = float(r.get("prix_plancher_ratio", 0.15))
    if cote > 0 and total < cote * seuil_absurde:
        return None, (f"prix d'appel suspect ({total:.2f}€ = {total / cote * 100:.0f}% "
                      f"de la cote {cote:.2f}€, seuil {seuil_absurde * 100:.0f}%)")
    # Signal explicite d'enchère déguisée dans le texte de l'annonce.
    texte_annonce = normaliser(str(annonce.get("titre", "")))
    if any(sig in texte_annonce for sig in SIGNAUX_ENCHERE):
        return None, "annonce d'enchère déguisée (prix d'appel)"

    # --- Revente : au moins 10% net au-dessus de la cote, frais déduits ---
    # Garde-fou : si frais_revente_estimes >= 1 (100%), le dénominateur
    # serait nul ou négatif -> on borne à 0.99 max pour éviter le crash.
    frais_revente = min(float(r["frais_revente_estimes"]), 0.99)
    prix_revente = cote * (1 + r["marge_revente"]) / (1 - frais_revente)
    profit_net = cote * (1 + r["marge_revente"]) - total
    profit_min = float(r.get("profit_min", 0) or 0)
    if profit_net < max(profit_min, 0.01):
        return None, f"profit trop faible ({profit_net:.2f}€ < {profit_min:.2f}€ minimum)"

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


def _echapper_html(texte) -> str:
    """Échappe les caractères spéciaux HTML (< > &) avant insertion dans un
    message Telegram en parse_mode HTML. Sans ça, un titre d'annonce
    contenant '<', '>' ou '&' casse le formatage et Telegram REFUSE le
    message (alerte perdue). On échappe uniquement les 3 caractères
    réservés, dans le bon ordre (& en premier)."""
    s = str(texte)
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _texte_vente(v: dict) -> str:
    return (
        f"💰 <b>C'EST LE MOMENT DE VENDRE !</b>\n"
        f"🎴 <b>{_echapper_html(v['nom'])}</b>\n"
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
        f"🔥 <b>{_echapper_html(d['titre'])}</b>\n"
        f"🛒 {_echapper_html(d['plateforme'])} — <b>{d['prix']:.2f}€</b> + {d['port']:.2f}€ port = <b>{d['total']:.2f}€</b>\n"
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
    os.makedirs(os.path.dirname(FICHIER_STATS), exist_ok=True)
    with open(FICHIER_STATS, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=1)


# ------------------------------ CSV -----------------------------------

def calculer_tendance_cote(nom_carte: str) -> str:
    """Compare la cote actuelle avec celle d'hier pour déterminer la tendance."""
    h = historique()
    if nom_carte not in h or len(h[nom_carte]) < 2:
        return "="  # pas assez de données
    
    cotes = [e["cote"] for e in h[nom_carte]]
    if len(cotes) < 2:
        return "="
    
    cote_aujourd = cotes[-1]
    cote_hier = cotes[0] if len(cotes) >= 2 else cote_aujourd
    
    if cote_aujourd > cote_hier * 1.05:  # +5% = hausse
        return "↗️"
    elif cote_aujourd < cote_hier * 0.95:  # -5% = baisse
        return "↘️"
    else:
        return "="


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
            tendance = calculer_tendance_cote(d.get("carte", ""))
            w.writerow([maintenant, d.get("carte", ""), d["plateforme"], d["titre"],
                        d["prix"], d["port"], d["total"], d["cote"], tendance, d["decote_pct"],
                        d["prix_revente_conseille"], d["profit_net_estime"],
                        d.get("vendeur_nom", "?"), f"{d.get('vendeur_pct', 100):.0f}%", d["url"]])
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

    annonces_ebay = resultats.get("ebay", [])
    annonces = annonces_ebay + resultats.get("vinted", []) + resultats.get("leboncoin", [])
    # On attache la carte, sa langue et son alias à chaque annonce (filtres)
    for a in annonces:
        a["carte"] = nom
        a["langue"] = langue
        a["alias"] = carte.get("alias", "")
    return annonces, annonces_ebay


def main() -> int:
    debut = time.time()
    cfg = charger_config()
    _ct_charger_cache()  # V22 : cache Cardtrader (blueprints + prix du jour)
    secrets = secrets_env()
    _cfg_api = cfg.get("api_cotes", {})
    if _cfg_api.get("actif"):
        log.info("Cardtrader : ACTIF (mode %s) — token %s",
                 _cfg_api.get("mode", "observation"),
                 "présent ✓" if secrets.get("CARDTRADER_TOKEN") else "ABSENT ✗ (secret GitHub manquant)")
    else:
        log.info("Cardtrader : désactivé (api_cotes.actif = false dans config.yaml)")
    vues = charger_vues()

    nouveaux_deals: list[dict] = []
    total_annonces = 0

    for carte in cfg["watchlist"]:
        nom = carte["nom"]
        log.info("=== %s (%s) ===", nom, carte.get("langue", "fr").upper())

        annonces, annonces_ebay = collecter(carte, cfg, secrets)
        total_annonces += len(annonces)

        cote, confiance = obtenir_cote(carte, annonces_ebay, cfg)

        # V22 : cote Cardtrader (marché européen, prix réels par langue).
        # mode "observation" = affiché seulement ; "actif" = remplace la cote.
        cfg_api = cfg.get("api_cotes", {})
        if cfg_api.get("actif"):
            nb_bas = int(cfg_api.get("nb_prix_bas", 5))
            min_ann = int(cfg_api.get("min_annonces", 3))
            prix_ct = cardtrader_prix(carte, secrets.get("CARDTRADER_TOKEN", ""), nb_bas, min_ann)
            if prix_ct is not None:
                # V22.7 GARDE-FOU 4 : vérification croisée avec la cote eBay.
                # Si les deux existent et s'écartent d'un facteur 5+, l'une
                # des deux est fausse (mauvaise correspondance de carte,
                # cf. Méga-Dracaufeu X trouvé à 3€ contre 1199€ eBay) : on
                # n'utilise PAS le prix Cardtrader et on le signale.
                suspect = bool(cote) and (prix_ct > cote * 5 or prix_ct < cote / 5)
                if suspect:
                    log.warning("    [Cardtrader ⚠️] %s : prix %.2f€ INCOHÉRENT avec la cote "
                                "eBay %.2f€ (facteur > 5) -> Cardtrader ignoré pour cette carte",
                                nom, prix_ct, cote)
                else:
                    log.info("    [Cardtrader %s] %s ≈ %.2f€  (moyenne des %d plus bas)  —  cote eBay : %s",
                             carte.get("langue", "fr").upper(), nom, prix_ct, nb_bas,
                             f"{cote:.2f}€" if cote else "aucune")
                    if cfg_api.get("mode") == "actif" and not carte.get("cote"):
                        # Remplace la cote eBay (la cote MANUELLE reste prioritaire).
                        cote, confiance = round(prix_ct, 2), 99
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
            cote_carte = carte.get("cote") or cote_lissee(carte["nom"])
            if not cote_carte:
                break
            deal, _statut = evaluate(annonce, float(cote_carte), cfg, 0, carte.get("marge_achat"))
            if deal and not deja_vue(vues, deal["id"]):
                log.info("  ✓ DEAL (email LBC) : %s à %.2f€ (cote %.2f€)",
                         deal["titre"][:60], deal["total"], float(cote_carte))
                nouveaux_deals.append(deal)
                marquer(vues, deal["id"])
            break

    alertes_vente = verifier_stock(cfg, secrets, vues)
    _ct_sauver_cache()  # V22 : persistance du cache Cardtrader

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
