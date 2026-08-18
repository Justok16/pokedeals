"""
Structures partagees pour representer une carte de la watchlist PokeDeals
(config.yaml) dans le contexte des boutiques Shopify.

Separe deux besoins distincts :
  - nom_recherche / numero : ce qui sert a matcher les titres de produits
    Shopify (cf. connecteur_shopify.py -> ConnecteurShopify.rechercher_dans_catalogue).
  - nom_config / langue : la cle exacte utilisee dans data/cotes.json
    ("<nom_config>|<langue>") pour retrouver la cote connue de la carte,
    necessaire a la logique "bonne affaire".
"""

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from connecteur_shopify import _regex_numero_sans_denominateur

# Chemin relatif au repo (ce fichier vit a la racine, a cote de main.py et
# config.yaml) -- indispensable pour tourner sur le runner GitHub Actions.
CHEMIN_CONFIG_DEFAUT = Path(__file__).parent / "config.yaml"

# Codes de set abreges connus (JP/KR), a NE PAS confondre avec le numero de
# la carte quand celui-ci n'a pas de denominateur. Vus dans config.yaml :
# "Team Rocket's Mewtwo ex 237 m2a" -> numero 237, PAS m2a.
CODES_SET_CONNUS = {
    "sv2a", "sv8a", "sv5a", "sv9", "s8b", "s-p", "m2a", "m1l", "m2", "m3", "m4", "m5", "mc",
}
# Prefixes en tete de "nom" a ignorer avant de commencer la collecte du nom
# de recherche (ex: "Team Rocket's Mewtwo ex 237 m2a" -> ne pas capturer "Team").
PREFIXES_A_IGNORER = {"team", "rocket's", "rocket"}
# Mots qui METTENT FIN a la collecte du nom de recherche (tout ce qui suit
# est un qualificatif -- rarete, forme, promo -- pas le nom du Pokemon).
MOTS_TERMINATEURS = {"ex", "gx", "v", "vmax", "vstar", "promo", "de", "du", "des"}
# Sous-ensemble de MOTS_TERMINATEURS qui distingue reellement des cartes
# DIFFERENTES portant le meme nom+numero (contrairement a "promo"/"de"/"du"/
# "des", qui ne sont pas des mecaniques de jeu). Bug reel corrige : "Plumeline
# ex 024" (config.yaml, MEP Black Star Promos) et "Plumeline 24 Sun & Moon
# REVERSE" (carte plus ancienne, non-ex, sans rapport) partagent le meme
# nom+numero -- sans distinguer le "ex", le mauvais Plumeline (1,50€, en
# stock) a matche a la place du bon (28€, rupture), declenchant une fausse
# alerte via le seuil fixe 15€.
MOTS_QUALIFICATIFS = {"ex", "gx", "v", "vmax", "vstar"}

# Noms de coffret/set connus qui portent EUX-MEMES "ex"/"vmax" dans leur
# propre nom (branding marketing du coffret, pas rarete de la carte).
# Constate lors du test de non-regression sur 81 boutiques (2026-08-10) :
# certains vendeurs dupliquent ce mot juste apres le nom de la carte dans le
# titre (ex: "M2A 199/193 - Psykokwak ex - MEGA Dream ex" pour un Psykokwak
# de BASE, non-ex), rendant la simple proximite au numero insuffisante pour
# distinguer un vrai qualificatif de carte d'un echo du nom du coffret --
# une fenetre de caracteres autour du numero (cf. FENETRE_QUALIFICATIF_TITRE
# ci-dessous) ne suffit PAS a elle seule : dans l'exemple ci-dessus, "ex"
# colle a "Psykokwak" (le nom de la carte) a seulement 13 caracteres du
# numero, une distance indiscernable d'un vrai qualificatif legitime comme
# "Plumeline ex 024". Pas de fix "positionnel" plus robuste connu -- deja
# ecarte (cf. commentaire ci-dessus) car indiscernable du cas legitime a la
# meme distance. Seule parade fiable : cette liste, curee a la main.
#
# >>> ENTRETIEN MANUEL REQUIS : liste volontairement INCOMPLETE, a
# completer au fil des faux positifs constates (meme esprit que
# CODES_SET_CONNUS ci-dessus). Un futur coffret au nom ambigu non
# repertorie ici reproduira le meme faux rejet jusqu'a etre decouvert et
# ajoute -- pas d'alerte automatique en cas d'oubli, verification humaine
# necessaire si un rejet suspect de qualificatif est signale. <<<
NOMS_SET_QUALIFICATIF_AMBIGU = {
    "mega dream",   # coffret JP "MEGA Dream ex" -- ex: Psyduck/Psykokwak 199/193
    "vmax climax",  # set FR/JP "VMAX Climax" (S8b) -- ex: Evoli/Eevee 210
}

# Fenetre de caracteres autour du numero matche dans laquelle chercher un
# qualificatif -- defense en profondeur en complement de
# NOMS_SET_QUALIFICATIF_AMBIGU : les 3 vrais qualificatifs constates lors du
# test de non-regression (Voltali V, Iron Crown ex, Iron Hands ex -- des
# cartes DIFFERENTES matchees a tort via un nom de set contenant "Eevee")
# se trouvent tous a 17 caracteres ou moins du numero ; une fenetre plus
# large limite le risque qu'un mot sans rapport, loin dans un titre a
# rallonge, declenche un rejet.
FENETRE_QUALIFICATIF_TITRE = 40


@dataclass(frozen=True)
class CarteWatchlist:
    nom_recherche: str        # ex: "Dracaufeu" -- pour matcher les titres Shopify
    numero: str | None        # ex: "199/165", "SWSH087", ou None
    langue: str                # "fr" / "jp" / "kr" -- pour la cle cotes.json
    nom_config: str            # nom EXACT tel qu'ecrit dans config.yaml (avec "ex" etc.)
    prix_max_fixe: float | None = None  # override eventuel (cf. config.yaml)
    # "ex"/"gx"/"v"/"vmax"/"vstar" si present dans nom_config, sinon None.
    # Sert a rejeter un match nom+numero qui ne porte PAS ce qualificatif
    # dans son titre (carte homonyme differente) -- cf. bonne_affaire_shopify.py
    # et alerte_stock.py qui appliquent ce filtre.
    qualificatif: str | None = None

    @property
    def cle_recherche(self) -> tuple[str, str | None]:
        """Cle utilisee par ConnecteurShopify (nom, numero)."""
        return (self.nom_recherche, self.numero)

    @property
    def cle_cotes(self) -> str:
        """Cle utilisee dans data/cotes.json."""
        return f"{self.nom_config}|{self.langue}"


def _extraire_nom_et_numero(nom_config: str) -> tuple[str, str | None, str | None]:
    """Extrait (nom_recherche, numero, qualificatif) a partir du champ "nom"
    brut de config.yaml, ex: "Charmander 168/165 sv2a" -> ("Charmander",
    "168/165", None) ; "Plumeline ex 024" -> ("Plumeline", "024", "ex")."""
    tokens = nom_config.split()

    numero = None
    for tok in tokens:
        if re.match(r"^[A-Za-z0-9]*\d+/[A-Za-z0-9]*\d+$", tok):
            numero = tok
            break

    if numero is None:
        candidats = [
            tok.strip(",()") for tok in tokens
            if any(ch.isdigit() for ch in tok) and tok.strip(",()").lower() not in CODES_SET_CONNUS
        ]
        numero = candidats[-1] if candidats else None

    idx = 0
    while idx < len(tokens) and tokens[idx].strip(",()").lower() in PREFIXES_A_IGNORER:
        idx += 1

    premiers_mots = []
    qualificatif = None
    for tok in tokens[idx:]:
        tok_clean = tok.strip(",()")
        tok_lower = tok_clean.lower()
        if tok_lower in MOTS_TERMINATEURS or tok_lower in CODES_SET_CONNUS:
            if tok_lower in MOTS_QUALIFICATIFS:
                qualificatif = tok_lower
            break
        if any(ch.isdigit() for ch in tok_clean):
            break
        premiers_mots.append(tok_clean)

    if premiers_mots:
        nom_recherche = " ".join(premiers_mots)
    else:
        nom_recherche = tokens[idx] if idx < len(tokens) else tokens[0]
    return nom_recherche, numero, qualificatif


def _zone_qualificatif(titre: str, titre_lower: str, numero: str | None) -> str:
    """Retourne la zone de texte (fenetre autour du numero matche si
    fourni, titre entier sinon) dans laquelle chercher un qualificatif --
    reduit le risque qu'un mot sans rapport, loin dans un titre a
    rallonge, soit capture a tort. Partagee par detecter_qualificatif_titre()
    et qualificatif_present_dans_titre() (extraite le 18/08/2026, audit
    externe, pour eviter que les deux dupliquent cette meme logique)."""
    zone = titre_lower
    if numero:
        if "/" in numero:
            correspondance = re.search(re.escape(numero.lower()), titre_lower)
        else:
            correspondance = _regex_numero_sans_denominateur(numero).search(titre)
        if correspondance:
            debut = max(0, correspondance.start() - FENETRE_QUALIFICATIF_TITRE)
            fin = min(len(titre_lower), correspondance.end() + FENETRE_QUALIFICATIF_TITRE)
            zone = titre_lower[debut:fin]
    return zone


def detecter_qualificatif_titre(titre: str, numero: str | None = None) -> str | None:
    """Detecte un qualificatif ("ex"/"gx"/"v"/"vmax"/"vstar") present dans un
    titre de PRODUIT (pas config.yaml), pour la verification SYMETRIQUE du
    filtre qualificatif (cf. bonne_affaire_shopify.py / alerte_stock.py) :
    une carte configuree SANS qualificatif (carte.qualificatif is None) ne
    doit pas matcher un titre qui en porte un -- sinon une carte de base
    ("Bulbizarre 166/165") pourrait matcher a tort une version "ex"/"GX"/"V"
    homonyme (meme nom+numero, carte differente en realite).

    `numero` (carte.numero) restreint la recherche a une FENETRE de
    caracteres autour du numero matche dans le titre, au lieu du titre
    entier -- limite le risque qu'un mot sans rapport, loin dans le titre,
    declenche un rejet. Voir NOMS_SET_QUALIFICATIF_AMBIGU pour la premiere
    ligne de defense (noms de coffret dont le nom contient lui-meme un
    qualificatif) -- COURT-CIRCUIT VOLONTAIRE : specifique a cette
    fonction (verification NEGATIVE), ne pas reprendre tel quel pour une
    verification POSITIVE, cf. qualificatif_present_dans_titre() ci-dessous."""
    titre_lower = titre.lower()

    if any(nom_set in titre_lower for nom_set in NOMS_SET_QUALIFICATIF_AMBIGU):
        return None

    zone = _zone_qualificatif(titre, titre_lower, numero)
    for mot in MOTS_QUALIFICATIFS:
        if re.search(rf"\b{mot}\b", zone):
            return mot
    return None


def qualificatif_present_dans_titre(titre: str, qualificatif: str, numero: str | None = None) -> bool:
    """Verifie qu'un qualificatif ATTENDU (config.yaml, ex: carte.qualificatif
    == "ex") apparait dans la zone proche du numero de la carte dans un
    titre de produit -- audit externe du 18/08/2026 (verifie contre le code
    reel) : le garde-fou positif (bonne_affaire_shopify.py) faisait
    auparavant une recherche `\\bex\\b` sur le titre ENTIER, sans aucune
    protection -- alors que la verification NEGATIVE symetrique
    (detecter_qualificatif_titre) beneficie deja d'un fenetrage. Meme
    fenetre ici (FENETRE_QUALIFICATIF_TITRE, via _zone_qualificatif), MAIS
    volontairement SANS le court-circuit NOMS_SET_QUALIFICATIF_AMBIGU : ce
    court-circuit existe pour eviter un FAUX REJET d'une carte SANS
    qualificatif propre dont le nom de SET en contient un ("MEGA Dream
    ex") -- l'appliquer ici produirait l'effet INVERSE, un FAUX REJET
    d'une carte qui a REELLEMENT ce qualificatif mais vient justement d'un
    set au nom ambigu (ex: "Team Rocket's Mewtwo ex", issu du set
    japonais "MEGA Dream ex", deja suivi dans la watchlist). Le fenetrage
    reste une vraie protection ici : il reduit le risque qu'un mot de
    qualificatif tres eloigne dans un titre a rallonge soit compte a tort
    comme appartenant a CETTE carte."""
    titre_lower = titre.lower()
    zone = _zone_qualificatif(titre, titre_lower, numero)
    return bool(re.search(rf"\b{re.escape(qualificatif)}\b", zone))


def charger_watchlist_config(chemin: Path = CHEMIN_CONFIG_DEFAUT) -> list[CarteWatchlist]:
    """Parse la watchlist reelle de config.yaml (121 cartes) en CarteWatchlist,
    prete pour ConnecteurShopify.

    Pour chaque entree possedant un "alias", genere DEUX CarteWatchlist (nom
    principal + alias) qui partagent le meme nom_config/langue/numero -- les
    boutiques melangent parfois les conventions FR/EN pour une meme carte
    (cf. main.py lignes 581-619, meme logique deja utilisee cote eBay).
    Ces deux variantes seront ensuite consolidees par nom_config lors de la
    detection (une seule alerte/etat de stock par carte, pas par variante).
    """
    with open(chemin, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    cartes: list[CarteWatchlist] = []
    for entree in cfg["watchlist"]:
        nom_config = entree["nom"]
        langue = entree["langue"]
        alias = entree.get("alias")
        prix_max_fixe = entree.get("prix_max_fixe")

        nom_recherche, numero, qualificatif = _extraire_nom_et_numero(nom_config)
        cartes.append(CarteWatchlist(nom_recherche, numero, langue, nom_config, prix_max_fixe, qualificatif))

        if alias and alias.strip().lower() != nom_recherche.strip().lower():
            cartes.append(CarteWatchlist(alias.strip(), numero, langue, nom_config, prix_max_fixe, qualificatif))

    return cartes


# Echantillon de 10 entrees REELLES de config.yaml (watchlist PokeDeals),
# melangeant les 3 formats de numero rencontres (standard avec denominateur,
# JP/KR avec code de set abrege, promo sans denominateur / sans numero).
# Utilise pour les tests de bout en bout (connecteur, alerte stock, bonne affaire).
ECHANTILLON_CONFIG: list[CarteWatchlist] = [
    CarteWatchlist("Dracaufeu", "199/165", "fr", "Dracaufeu ex 199/165"),
    CarteWatchlist("Pikachu", "173/165", "fr", "Pikachu 173/165"),
    CarteWatchlist("Mew", "193/165", "fr", "Mew ex 193/165"),
    CarteWatchlist("Charizard", "201/165", "jp", "Charizard ex 201/165 sv2a"),
    CarteWatchlist("Méga-Dracaufeu Y", "294/217", "fr", "Méga-Dracaufeu Y ex 294/217"),
    CarteWatchlist("Evoli", "SWSH087", "fr", "Evoli VMAX SWSH087"),
    CarteWatchlist("Morpeko", "117", "fr", "Morpeko ex 117"),
    CarteWatchlist("Poissirene", "087", "fr", "Poissirene 087"),
    CarteWatchlist("Pikachu", "764", "jp", "Pikachu ex 764 mC"),
    CarteWatchlist("Evoli", None, "fr", "Evoli Trainer Gallery"),
]
