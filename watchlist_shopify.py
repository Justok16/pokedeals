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
