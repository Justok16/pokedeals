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
    "francaise", "francais", "france", "vf",
    "neuve", "neuf", "etat", "envoi", "envoie", "livraison", "expedition",
    "vends", "vendue", "achat", "acheteur", "merci", "bonjour",
    "rapide", "soignee", "parfait", "jouee",
    "prix ferme", "port compris", "port offert", "main propre",
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
    return an