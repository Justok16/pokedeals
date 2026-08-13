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


def _ecrire_json_atomique(chemin: str, donnees, **kwargs) -> None:
    """Ecrit un JSON de facon atomique (fichier temporaire + os.replace) pour
    ne jamais laisser un data/*.json tronque/corrompu si le process est tue
    en plein ecriture (ex. timeout GitHub Actions)."""
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    tmp = f"{chemin}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(donnees, f, **kwargs)
    os.replace(tmp, chemin)


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
# V38 : certains vendeurs écrivent le numéro avec un tiret ou une espace
# au lieu du slash ("199-165", "199 165"). Sans ce filtre de secours, ces
# annonces étaient systématiquement rejetées ("aucun numéro dans le
# titre"), même quand tout le reste du titre était correct. On ne
# l'utilise qu'en repli, après avoir essayé le slash — le slash reste
# prioritaire pour éviter de capturer par erreur une date ou une
# référence interne au vendeur (ex. "025-09").
RE_NUMERO_SEPARATEUR = re.compile(r"\b(\d{1,3})[-\s](\d{2,3})\b")

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
    "jp": ["japonaise", "japonais", "japanese", "japon", "jpn", "jap", "jp",
           # V30 : formes ITALIENNE, ESPAGNOLE, ALLEMANDE et NÉERLANDAISE.
           # Cas vécu : une annonce Vinted titrée « Pokémon Pikachu AR
           # 173/165 – Giapponese – Art Rare » (vendeur italien, carte
           # japonaise) a franchi le filtre FR et failli être comparée à
           # la cote française de 114,42€. Le mot était dans le titre, en
           # clair — on ne le connaissait simplement pas.
           "giapponese", "giapponesi", "giappone",
           "japones", "japonesa", "japonesas",
           "japanisch", "japanische", "japans"],
    "en": ["anglaise", "anglais", "english", "eng",
           "inglese", "ingles", "englisch"],
    "kr": ["coreenne", "coreen", "korean", "korea", "kor", "kr",
           "coreano", "coreana", "koreanisch", "koreaans"],
    "cn": ["chinoise", "chinois", "chinese", "china", "zh", "cn",
           "cinese", "cinesi", "chino", "chinesisch"],
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


# =====================================================================
# V28 : CODES DE SET JAPONAIS = PREUVE QUE LA CARTE N'EST PAS FRANÇAISE
# ---------------------------------------------------------------------
# Cas vécu (fausse alerte Telegram) : une annonce Vinted titrée
# « Pikachu AR sv2a 173/165 — État parfait », photo d'une carte
# CORÉENNE, comparée à la cote FRANÇAISE de 114,42€ -> faux profit
# annoncé de +84,91€.
#
# Pourquoi tous les filtres l'ont laissée passer :
#   - aucun caractère coréen dans le TITRE (seulement sur la photo)
#   - aucun mot de langue ("coréenne", "korean"...)
#   - bon Pokémon, bon numéro 173/165
#   - et le filtre "preuve de français" a trouvé « état » et
#     « parfait »... qui prouvent seulement que le VENDEUR est
#     français, pas que la CARTE l'est. Un vendeur français vend
#     très bien une carte coréenne.
#
# Le vrai signal : « sv2a » est le code de set JAPONAIS de la série
# 151, porté par les versions JP et KR. La version FRANÇAISE ne le
# porte JAMAIS (elle affiche EV3.5, 151, Écarlate & Violet).
# Ce code ne dit pas LAQUELLE des langues asiatiques (JP et KR le
# partagent), mais il exclut le français avec certitude.
#
# Effet double : supprime ces fausses alertes ET nettoie les cotes FR,
# qui absorbaient des cartes japonaises au même numéro (constaté :
# « Bulbizarre AR SFG 9.5 – SV2a 151 (166/165) » à 70€ comptée dans
# le bas-marché de la cote française).
# =====================================================================
SETS_ASIATIQUES = {
    # Écarlate & Violet japonais (sv...)
    "sv1", "sv1a", "sv1s", "sv1v", "sv2", "sv2a", "sv2d", "sv2p",
    "sv3", "sv3a", "sv4", "sv4a", "sv4k", "sv4m", "sv5a", "sv5k", "sv5m",
    "sv6", "sv6a", "sv7", "sv7a", "sv8", "sv8a", "sv9", "sv9a",
    "sv10", "sv11b", "sv11w",
    # Épée & Bouclier japonais (s...)
    "s8b", "s9a", "s10a", "s11", "s12", "s12a",
    # Méga-Évolution japonais (m...)
    "m1l", "m1s", "m2", "m2a", "m3", "m4", "m5", "mc",
    # Promos japonaises
    "s-p",
}


def code_set_asiatique(jetons: list[str]) -> str | None:
    """Renvoie le code de set japonais trouvé dans les jetons, sinon None.

    Comparaison mot à mot : « sv2a » doit être un jeton isolé, pour ne
    pas confondre avec un fragment d'un autre mot.
    """
    for jeton in jetons:
        if jeton in SETS_ASIATIQUES:
            return jeton
    return None


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


def extraire_numero_annonce(titre: str) -> str | None:
    """Comme extraire_numero, mais avec un repli tiret/espace ('199-165',
    '199 165'). Réservé aux TITRES D'ANNONCES (eBay/Vinted) : le nom de la
    carte dans config.yaml doit rester sur le format strict X/Y, sinon un
    tiret dans "Méga-Dracaufeu" pourrait être pris à tort pour un numéro.
    """
    direct = extraire_numero(titre)
    if direct:
        return direct
    m = RE_NUMERO_SEPARATEUR.search(titre or "")
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


# =====================================================================
# V26 : PREUVE POSITIVE DE FRANÇAIS (annonces Vinted uniquement)
# ---------------------------------------------------------------------
# Sur eBay, _localisation_incoherente écarte déjà TOUTE annonce non
# localisée en France quand la carte recherchée est française —
# italiennes comprises. Rien à ajouter de ce côté.
#
# Vinted, lui, ne fournit aucun pays exploitable. Le filtre habituel
# exige le nom FRANÇAIS du Pokémon, ce qui suffit pour Dracaufeu : un
# vendeur italien n'écrit jamais « Dracaufeu ». Mais le nom ne prouve
# RIEN pour les Pokémon qui s'écrivent pareil dans toutes les langues :
# Mew, Pikachu, Mewtwo, Lucario, Gardevoir, Darkrai, Morpeko, Latias,
# Lugia, Zoroark. Un titre « Mew ex 205/165 » est compatible avec les
# versions FR, JP, KR, IT, EN, DE et ES à la fois — elles portent toutes
# le même numéro. C'est exactement là que les italiennes passaient.
#
# Le danger n'est PAS d'alerter sur une carte qui n'existe pas en
# français : c'est de comparer une italienne à 40€ à la COTE FRANÇAISE
# de 40€, alors que l'italienne en vaut 25.
# =====================================================================
MARQUEURS_FRANCAIS = (
    "francaise", "francais", "france",
    # V39 : retrait de "etat", "envoi", "envoie", "livraison", "expedition",
    # "merci", "bonjour", "rapide", "soignee", "jouee" et des formules de
    # prix ("prix ferme", "port compris"...). Même raisonnement que pour
    # "vf"/"parfait" retirés à la session précédente : ces mots prouvent
    # que le VENDEUR écrit en français, pas que la CARTE l'est. Un vendeur
    # français vend très bien une carte japonaise ou coréenne en écrivant
    # "état parfait, envoi rapide, merci". Ne restent que les mots qui
    # décrivent explicitement la nationalité de la carte elle-même.
    "neuve", "neuf",
)


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


def preuve_francais(texte: str) -> bool:
    """Un mot typiquement français figure-t-il dans l'annonce ?"""
    t = normaliser(texte)
    jetons = t.split()
    return any(_marqueur_present(m, t, jetons) for m in MARQUEURS_FRANCAIS)


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
    # V39 : neutraliser "non gradée" / "ungraded" AVANT le test des mots
    # exclus. La correction faite dans _etat_ok() ne suffisait pas : cette
    # fonction-ci a sa PROPRE liste (EXCLUSIONS, qui contient aussi "gradee"
    # et "graded") et elle est testée plus tôt dans le pipeline. Une annonce
    # « Dracaufeu ex 199/165 non gradée » était donc encore rejetée ici,
    # avant même d'atteindre le correctif de la session précédente.
    for negation in ("non gradee", "non-gradee", "pas gradee",
                     "ungraded", "not graded", "no grading", "sans grading"):
        t = t.replace(negation, "")
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
        # V28 : un code de set JAPONAIS (sv2a, m2a, s8b...) dans le titre
        # prouve que la carte n'est pas française — même si le vendeur, lui,
        # écrit en français. Signal factuel, pas du vocabulaire.
        code_jp = code_set_asiatique(jetons_langue)
        if code_jp:
            return False, (f"carte étrangère : code de set japonais "
                           f"'{code_jp}' (une carte FR n'en porte jamais)")
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
    numero_annonce = extraire_numero_annonce(titre)
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
            # matcher le "v" de "vmax"). Le nom PRINCIPAL du Pokémon aussi :
            # sans ça, "mew" est considéré présent dans "mewtwo" (sous-
            # chaîne), et une carte sans numéro pourrait valider une
            # annonce d'un AUTRE Pokémon au nom proche. Les autres mots
            # (noms de sets composés, etc.) restent en sous-chaîne, plus
            # tolérants et sans ce risque de confusion entre Pokémon.
            if mot in TYPES_CARTE or mot == pokemon:
                if mot not in jetons_titre:
                    return False, f"'{mot}' absent du titre (mot entier requis)"
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

# =====================================================================
# V44 : SUIVI DE L'ANCIENNETÉ DES ANNONCES (pour repérer les prix qui
# ne se vendent jamais).
# ---------------------------------------------------------------------
# seen.json ne suffit pas pour ça : il ne mémorise QUE les annonces qui
# ont failli devenir un deal. Or le problème vient justement des annonces
# qui composent le calcul de la cote SANS jamais devenir un deal — une
# annonce à 300€ qui traîne sans se vendre gonfle la cote, mais n'est
# jamais "vue" au sens actuel du programme.
# On crée donc un suivi séparé : première date à laquelle chaque
# annonce a été VUE dans le calcul de cote (pas seulement testée pour
# une alerte). Une annonce qui reste identique sur plusieurs jours
# n'est probablement jamais vendue à ce prix.
# =====================================================================
FICHIER_ANCIENNETE = os.path.join(RACINE, "data", "anciennete_annonces.json")
ANCIENNETE_RETENTION_JOURS = 45  # un peu plus que seen.json, pour garder assez d'historique

_anciennete: dict | None = None


def _charger_anciennete() -> dict:
    if not os.path.exists(FICHIER_ANCIENNETE):
        return {}
    try:
        with open(FICHIER_ANCIENNETE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def anciennete() -> dict:
    global _anciennete
    if _anciennete is None:
        _anciennete = _charger_anciennete()
    return _anciennete


def sauvegarder_anciennete() -> None:
    donnees = anciennete()
    limite = time.time() - ANCIENNETE_RETENTION_JOURS * 86400
    donnees = {k: v for k, v in donnees.items() if v.get("premiere_vue", 0) > limite}
    _ecrire_json_atomique(FICHIER_ANCIENNETE, donnees, ensure_ascii=False, indent=1)


def jours_en_ligne(annonce_id: str) -> float:
    """Nombre de jours depuis la première fois que cette annonce a été vue
    dans un calcul de cote. Enregistre aussi la première apparition si
    c'est la première fois qu'on la voit. Retourne 0.0 pour une annonce
    toute nouvelle (aucun signal d'ancienneté, ni bon ni mauvais)."""
    donnees = anciennete()
    maintenant = time.time()
    entree = donnees.get(annonce_id)
    if entree is None:
        donnees[annonce_id] = {"premiere_vue": maintenant}
        return 0.0
    return (maintenant - entree["premiere_vue"]) / 86400


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
        # gonfle une cote. V44 : on garde aussi l'id, pour le suivi
        # d'ancienneté (annonces qui traînent sans se vendre).
        retenues = [(a["prix"], a.get("titre", "")[:70], a.get("plateforme", ""), a.get("id", ""))
                    for a in annonces
                    if a["prix"] > 0
                    and not _localisation_incoherente(a, langue)
                    and annonce_pertinente(a.get("titre", ""), nom_carte, langue, alias, a.get("plateforme", ""))[0]]
        retenues.sort()
        prix = [p for p, _, _, _ in retenues]
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
    coef = float(cfg_cote.get("coefficient_marche", 1.0))
    cote = round(reference * coef, 2)

    # V23 : MÉTHODE ALTERNATIVE — moyenne des N annonces les moins chères.
    # Motif : les prix eBay sont des prix DEMANDÉS. La médiane capture le
    # milieu des espoirs de vendeurs, pas le prix auquel une carte part
    # réellement. Mesuré sur 3 cartes vérifiées à la main contre Cardmarket,
    # la médiane eBay dépasse la tendance Cardmarket d'un facteur 1,8 à 2,5.
    # La moyenne du bas de marché (même méthode que pour Cardtrader) s'en
    # approche nettement mieux — et se réajuste seule quand le marché bouge.
    nb_bas = int(cfg_cote.get("nb_prix_bas", 5))
    seuil_jours = float(cfg_cote.get("seuil_jours_stagnant", 10))
    if nom_carte and retenues:
        # V44 : une annonce en ligne depuis plus de `seuil_jours_stagnant`
        # jours ne se vend probablement pas à ce prix — elle gonfle le
        # panier bas-marché sans refléter un vrai prix de vente. On
        # l'écarte du panier tant que des annonces plus fraîches
        # suffisent ; sinon on la garde (mieux qu'aucune cote).
        candidats = sorted(nettoyes)
        fraiches = [p for p, _, _, aid in retenues
                   if p in candidats and jours_en_ligne(aid) < seuil_jours]
        fraiches.sort()
        bas_marche = fraiches[:max(1, nb_bas)] if len(fraiches) >= max(1, nb_bas) else candidats[:max(1, nb_bas)]
    else:
        bas_marche = sorted(nettoyes)[:max(1, nb_bas)]
    cote_basse = round((sum(bas_marche) / len(bas_marche)) * coef, 2)

    mode_cote = str(cfg_cote.get("methode", "mediane")).lower()
    if mode_cote == "bas_marche":
        cote_retenue = cote_basse
    else:
        cote_retenue = cote

    # V20 diagnostic : détail des annonces qui composent la cote (visible dans
    # les logs GitHub). Permet de repérer une annonce anormalement chère qui
    # gonfle la médiane. À retirer une fois le diagnostic terminé.
    if nom_carte and retenues:
        rejetes_iqr = [p for p in prix if p not in nettoyes]
        log.info("    [cote %s] médiane=%.2f€ | bas-marché(%d)=%.2f€ | ×%.2f -> RETENUE %.2f€"
                 " | %d annonces%s",
                 nom_carte, reference, len(bas_marche), cote_basse / coef if coef else cote_basse,
                 coef, cote_retenue, len(nettoyes),
                 f" ({len(rejetes_iqr)} écartées IQR : {rejetes_iqr})" if rejetes_iqr else "")
        for p, titre, plat, aid in retenues:
            marque = " ← ÉCARTÉE(IQR)" if p not in nettoyes else ""
            if p in bas_marche and not marque:
                marque = " ← bas-marché"
            elif not marque and p in candidats and jours_en_ligne(aid) >= seuil_jours:
                marque = f" ← stagnante ({jours_en_ligne(aid):.0f}j, exclue du panier)"
            log.info("        %.2f€  [%s] %s%s", p, plat, titre, marque)

    return cote_retenue, len(nettoyes)


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
        _ecrire_json_atomique(CT_CACHE_FICHIER, {"sig": _ct_signature_code(), **_ct_cache}, ensure_ascii=False)
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
    # V47 : m2/m3/m4 pointaient tous vers le mot-clé generique "mega", qui
    # ne matche QUE l'expansion ME01 "Mega Evolution" -- les vrais noms
    # anglais de ME02/ME03/ME04 (confirmes via TCGdex) ne contiennent pas
    # "mega" du tout, donc la recherche echouait silencieusement pour
    # toute carte de ces 3 sets (constate identiquement en JP et KR :
    # Meowth ex 114 m3, Froakie 086 m4, Mega Charizard X ex m2, Piplup
    # 085 m2, Oricorio ex 111 m2 -- aucun blueprint trouve dans aucune
    # langue avant ce correctif).
    "m1l": ["mega evolution"], "m2": ["phantasmal"], "m2a": ["dream"],
    "m3": ["perfect order"], "m4": ["chaos rising"], "m5": ["abyss"], "mc": ["start deck"],
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
    """Identifiant d'une carte indépendant de sa langue."""
    return normaliser(str(carte.get("nom", "")))


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
    ent = _ct_cache["blueprints"].get(cle) or {}
    cm_id = ent.get("cm_id")
    if not cm_id:
        return None

    prix = _cm_prix_par_id.get(str(cm_id))
    if prix:
        log.info("    [Cardmarket] '%s' (cardmarket_id=%s) : tendance officielle %.2f€",
                 carte["nom"], cm_id, prix)
    return prix


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
        _ecrire_json_atomique(API_CACHE_FICHIER, _api_prix_cache, ensure_ascii=False)
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
PURGE_VERSION = 20  # V26 : les clés d'historique intègrent la langue (fuite KR<-JP)
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
    # On réécrit le tag de version à chaque sauvegarde.
    a_ecrire = {"_purge_version": PURGE_VERSION}
    a_ecrire.update(h)
    _ecrire_json_atomique(FICHIER_COTES, a_ecrire, ensure_ascii=False, indent=1)


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
        # V46 : avant, rien n'était loggé si 0 email trouvé ou 0 annonce
        # extraite -> impossible de savoir depuis les logs GitHub Actions si
        # le canal Leboncoin est bloqué (aucune alerte Leboncoin reçue côté
        # Gmail) ou cassé côté code (mise en page LBC changée, regex à jour
        # mais extraction vide). Les trois cas sont maintenant distingués.
        if annonces:
            log.info("Alertes email LBC : %d annonce(s) extraite(s) de %d email(s)", len(annonces), len(ids))
        elif ids:
            log.warning("Alertes email LBC : %d email(s) non lu(s) de Leboncoin trouvé(s) mais AUCUNE annonce "
                        "extraite (mise en page Leboncoin changée ?)", len(ids))
        else:
            log.info("Alertes email LBC : aucun email non lu de Leboncoin trouvé dans %s", adresse)
    except Exception as e:  # noqa: BLE001
        log.warning("Alertes email LBC en erreur (non bloquant) : %s", e)
    return annonces


# =====================================================================
# V26 : CLÉS D'HISTORIQUE PAR LANGUE
# ---------------------------------------------------------------------
# LE NOM SEUL NE SUFFIT PAS. Une même carte figure dans la watchlist
# sous le MÊME nom dans plusieurs langues (« Charizard ex 201/165 sv2a »
# existe en JP et en KR). Avec le nom pour seule clé, la passe KR
# relisait la cote JAPONAISE enregistrée quelques secondes plus tôt et
# l'affichait comme sa propre cote — avec 0 annonce derrière. Une
# annonce coréenne était donc comparée à un prix japonais : fausse
# alerte garantie dès qu'un écart de marché existe entre les deux
# langues (et le coréen se vend moins cher que le japonais).
# =====================================================================

def cle_cote(nom_carte: str, langue: str = "fr") -> str:
    """Clé d'historique d'une cote : nom + langue."""
    return f"{nom_carte}|{str(langue or 'fr').lower()}"


def cote_lissee(nom_carte: str, langue: str = "fr") -> float | None:
    """Médiane des cotes des 7 derniers jours (l'historique est déjà purgé
    par version au chargement, donc plus besoin de borne de déploiement)."""
    entrees = historique().get(cle_cote(nom_carte, langue), [])
    limite = time.time() - VALIDITE_JOURS * 86400
    valeurs = [e["cote"] for e in entrees if e.get("ts", 0) >= limite]
    if not valeurs:
        return None
    return round(statistics.median(valeurs), 2)


def enregistrer_cote(nom_carte: str, cote: float, langue: str = "fr") -> None:
    h = historique()
    cle = cle_cote(nom_carte, langue)
    entrees = h.get(cle, [])
    entrees.append({"cote": cote, "ts": time.time()})
    h[cle] = entrees[-HISTORIQUE_MAX:]


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
    langue = carte.get("langue", "fr")
    cote_instant, nb_pertinentes = calculer_cote(
        annonces_ebay, cfg["cote"], carte["nom"],
        langue, carte.get("alias", ""))
    if cote_instant:
        enregistrer_cote(carte["nom"], cote_instant, langue)

    # 3) Cote lissée (médiane des derniers passages, MÊME LANGUE uniquement)
    cote = cote_lissee(carte["nom"], langue)
    if cote is None:
        cote = cote_instant
    if cote is None:
        log.info("Cote introuvable pour '%s' (%d annonce(s) pertinente(s), minimum %s requis)",
                 carte.get("nom"), nb_pertinentes, cfg["cote"].get("minimum_annonces", 8))
        return None, 0
    # V26 : dire clairement quand la cote vient de la MÉMOIRE et non du scan
    # du jour. Une cote « confiance : 0 annonces » n'est plus un mystère.
    if cote_instant is None:
        log.info("    [cote %s (%s)] aucune annonce eBay ce scan -> cote MÉMORISÉE "
                 "de %.2f€ réutilisée (moins de %s jours)",
                 carte["nom"], str(langue).upper(), cote, VALIDITE_JOURS)
    return cote, nb_pertinentes


def _etat_ok(texte: str, acceptes: list[str], refuses: list[str]) -> bool:
    t = (texte or "").lower()
    # V36 : NÉGATIONS. "Non gradée" / "ungraded" / "pas gradée" sont des
    # informations RASSURANTES (le vendeur précise que ce n'est PAS gradé),
    # mais elles contiennent littéralement le mot "gradée" — donc rejetées
    # à tort par erreur depuis le début. Cas vécu : "Non gradée Carte
    # Pokémon FR DRACAUFEU EX..." à 310€ (79€ sous la cote) écartée pour
    # "état refusé (gradée)" alors que la carte n'est justement PAS gradée.
    # On neutralise ces négations avant de chercher les mots interdits.
    for negation in ("non gradée", "non gradee", "non-gradée", "non-gradee",
                     "pas gradée", "pas gradee", "ungraded", "not graded",
                     "no grading", "sans grading"):
        t = t.replace(negation, "")
    if any(mot in t for mot in refuses):
        return False
    # V39 : nettoyage de code. etats_acceptes ne fait volontairement
    # RIEN filtrer — l'intention (documentée depuis le début) est
    # "accepter tout sauf les états explicitement refusés", beaucoup de
    # vendeurs n'indiquant pas l'état dans le titre. L'ancien code avait
    # deux branches qui renvoyaient toutes les deux True, ce qui donnait
    # l'impression trompeuse qu'un vrai filtre existait. etats_acceptes
    # dans config.yaml reste donc décoratif : garder la liste n'a pas
    # d'effet, seule etats_refuses agit.
    return True


def evaluate(annonce: dict, cote: float | None, cfg: dict, confiance: int = 0, marge_achat: float | None = None) -> tuple[dict | None, str]:
    """Évalue une annonce. Retourne (deal, status)."""
    r = cfg["regles"]

    # V45 : SEUIL DE PRIX FIXE, indépendant de la cote. Certaines cartes ont
    # un prix d'achat cible fixé à la main (ex. "je veux Plumeline à 15€ ou
    # moins, peu importe la cote calculée"). Défini par carte dans
    # config.yaml via "prix_max_fixe". Compare le PRIX SEUL (hors port),
    # comme demandé — pas le total.
    prix_fixe = annonce.get("prix_max_fixe")
    if prix_fixe:
        pertinent, raison = annonce_pertinente(
            annonce.get("titre", ""), annonce.get("carte", ""),
            annonce.get("langue", "fr"), annonce.get("alias", ""), annonce.get("plateforme", ""))
        if not pertinent:
            return None, raison
        if _localisation_incoherente(annonce, annonce.get("langue", "fr")):
            return None, "annonce localisée à l'étranger"
        if not _etat_ok(annonce.get("etat_texte", ""), cfg["etats_acceptes"], cfg["etats_refuses"]):
            return None, "état refusé (abîmée / gradée / jouée)"
        prix = float(annonce.get("prix", 0))
        if prix <= 0 or prix > float(prix_fixe):
            return None, f"prix ({prix:.2f}€) au-dessus du seuil fixe ({float(prix_fixe):.2f}€)"
        deal = {
            **annonce,
            "cote": float(prix_fixe),
            "total": round(prix + float(annonce.get("port", 0)), 2),
            "decote_pct": 0.0,
            "prix_revente_conseille": 0.0,
            "profit_net_estime": 0.0,
            "confiance": 100,  # 100 = seuil fixe manuel
        }
        return deal, "DEAL (seuil fixe)"

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
    # V36 : le plafond de port n'a plus de sens en chiffre FIXE quand la
    # watchlist va des cartes à 15€ (port à 6€ = 40% du prix, déjà limite)
    # V40 : plafond basé sur la COTE, pas sur le prix de l'annonce. Le
    # prix payé varie (c'est justement ce qu'on négocie), mais le vrai
    # risque du port reste proportionnel à la VALEUR RÉELLE de la carte.
    # V41 : passage de 5% à 7%. À 5%, une carte à ~160€ de cote (comme
    # Florizarre) plafonnait le port à 8€, alors que les ports réels
    # tournaient autour de 10-11€ sur cette gamme de prix -> 30 annonces
    # rejetées sur un seul scan pour ce seul motif.
    base_port = cote if (cote and cote > 0) else prix
    port_max = max(float(r["frais_port_max"]), base_port * 0.07)
    if str(annonce.get("plateforme", "")).startswith("eBay ("):
        port_max = max(float(r.get("frais_port_max_international", 10.0)), base_port * 0.07)
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
        # nb d'annonces eBay derrière la cote.
        # Valeurs spéciales : 99 = cote manuelle (config.yaml),
        #                     98 = cote fournie par Cardtrader (V27).
        "confiance": confiance,
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


def _echapper_url_html(url: str) -> str:
    """Échappe uniquement le '&' dans une URL pour usage en attribut HTML
    (href="..."). Les '<', '>' et '"' sont volontairement laissés intacts
    dans le chemin/la requête d'une URL normale, mais '&' doit être encodé
    en &amp; dans du HTML, sinon Telegram peut refuser le message si l'URL
    contient plusieurs paramètres (ex. '?item=1&category=2')."""
    return str(url).replace("&", "&amp;")


def _texte_telegram(d: dict) -> str:
    # V46 : ligne Cardmarket, purement informative -- n'existe QUE quand
    # main() a pu la calculer en toute confiance (cf. commentaire V46 dans
    # main(), juste après les GARDE-FOU 4/5). N'influence jamais "cote" ni
    # aucune décision : simple info affichée en plus pour vérification
    # visuelle rapide avant achat.
    ligne_cardmarket = ""
    if d.get("cardmarket_prix") is not None:
        ligne_cardmarket = f"\n🇪🇺 Cardmarket (tendance) : {d['cardmarket_prix']:.2f}€"

    # V45 : message dédié pour un deal sur seuil de prix fixe (confiance
    # 100). Pas de cote/décote/profit à afficher, ça n'a pas de sens ici.
    if d.get("confiance") == 100:
        return (
            f"🎯 <b>{_echapper_html(d['titre'])}</b>\n"
            f"🛒 {_echapper_html(d['plateforme'])} — <b>{d['prix']:.2f}€</b> "
            f"(seuil fixé : {d['cote']:.2f}€, port non compté)"
            f"{ligne_cardmarket}\n"
            f"👉 <a href=\"{_echapper_url_html(d['url'])}\">Voir l'annonce</a>"
        )
    # V37 : AVERTISSEMENT sur les écarts extrêmes. Une décote de plus de 30%
    # sous la cote est un vrai signal d'alerte, PAS une bonne nouvelle plus
    # grande : le programme lit uniquement le TEXTE de l'annonce, jamais la
    # photo. Cas vécu : une annonce titrée entièrement en français (drapeau
    # 🇫🇷, "EV3.5", "Écarlate et Violet") pointait en réalité vers une carte
    # CORÉENNE sur la photo — le vendeur avait mis la mauvaise image. Aucun
    # filtre textuel ne peut détecter ça. Un écart de prix trop généreux est
    # souvent le seul indice indirect qu'il faut vérifier la photo avant
    # d'acheter.
    avertissement = ""
    if d.get("decote_pct", 0) and float(d["decote_pct"]) >= 30:
        avertissement = (
            "\n⚠️ <b>Écart important avec la cote — vérifie la photo avant "
            "d'acheter</b> (le titre peut être juste, mais l'image parfois "
            "ne correspond pas à la carte annoncée).")
    return (
        f"🔥 <b>{_echapper_html(d['titre'])}</b>\n"
        f"🛒 {_echapper_html(d['plateforme'])} — <b>{d['prix']:.2f}€</b> + {d['port']:.2f}€ port = <b>{d['total']:.2f}€</b>\n"
        f"📊 Cote : {d['cote']:.2f}€ (<b>-{d['decote_pct']}%</b>)"
        f"{ligne_cardmarket}\n"
        f"💶 Revente conseillée : {d['prix_revente_conseille']:.2f}€\n"
        f"✅ Profit net estimé : <b>+{d['profit_net_estime']:.2f}€</b>"
        f"{avertissement}\n"
        f"👉 <a href=\"{_echapper_url_html(d['url'])}\">Voir l'annonce</a>"
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

def calculer_tendance_cote(nom_carte: str, langue: str = "fr") -> str:
    """Compare la cote actuelle avec celle d'hier pour déterminer la tendance."""
    h = historique()
    cle = cle_cote(nom_carte, langue)
    if cle not in h or len(h[cle]) < 2:
        return "="  # pas assez de données

    cotes = [e["cote"] for e in h[cle]]
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
        nb_lisse = min(2, len(valeurs) // 2) or 1
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
        a["prix_max_fixe"] = carte.get("prix_max_fixe")
    return annonces, annonces_ebay


def main() -> int:
    debut = time.time()
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
            if envoyer_telegram(nouveaux_deals, cfg["telegram"], secrets["TELEGRAM_BOT_TOKEN"]):
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
