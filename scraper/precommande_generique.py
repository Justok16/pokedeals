"""
Detection GENERIQUE de precommandes Pokemon TCG (produit non liste a l'avance),
pour PokePrecoms -- distinct de precommandes_watchlist.py (qui suit une liste
FIXE de produits connus a l'avance pour le radar historique PokeDeals).

Contrairement a precommandes_watchlist.py (mots-cles edition+type propres a
CHAQUE produit surveille), ce module determine SI un produit scanne est une
precommande Pokemon TCG scellee candidate a une alerte, sans connaitre le
produit a l'avance -- destine a etre appele sur le CATALOGUE ENTIER d'une
boutique (comme cartes_watchlist_saas() le fait deja pour les cartes), pas
sur une liste de produits cibles.

4 conditions, toutes requises (cf. discussion avec Justok, 23/08/2026) :
1. Mention explicite "pokemon" dans le titre -- meme garde-fou anti-franchise
   que decouverte_boutiques.py (un nom de domaine ou une categorie evocatrice
   ne suffit jamais, seul le contenu reel compte).
2. Mention explicite "precommande" (FR UNIQUEMENT, pas d'anglais "pre-order"/
   "preorder" -- demande explicite de Justok) -- ecarte l'immense majorite du
   catalogue (produits deja en vente normale).
3. Un mot-cle de TYPE de produit scelle (ETB, coffret, display...) -- liste
   volontairement incomplete, comme NOMS_SET_QUALIFICATIF_AMBIGU/
   MOTS_ETAT_REFUSE ailleurs dans ce projet -- a enrichir au fil des cas reels
   constates (faux positifs/negatifs), jamais par detection automatique.
4. Aucune autre franchise TCG mentionnee (Yu-Gi-Oh, Magic, Lorcana...) --
   securite supplementaire, meme si la condition 1 (mention Pokemon) filtre
   deja l'essentiel des cas evidents.

La verification du STOCK (en_stock) n'est PAS la responsabilite de ce module
(donnee brute deja fournie par les connecteurs Shopify/PrestaShop/WooCommerce,
cf. radar_precommandes.py -- ConnecteurShopify expose deja `available` par
variant) -- a appliquer par l'appelant AVANT de generer une alerte (demande
explicite : "faire en sorte qu'il y ait bien du stock, sinon inutile").
"""
from __future__ import annotations

import re
import unicodedata


def _normaliser(texte: str) -> str:
    """Minuscule, accents retires, ponctuation reduite a un espace -- meme
    principe que precommandes_watchlist._normaliser (compare un texte de
    page, accents/casse/typographie variables, aux mots-cles ci-dessous,
    deja ecrits sans accents)."""
    sans_accents = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", sans_accents.lower())


MOT_CLE_POKEMON = "pokemon"
MOT_CLE_PRECOMMANDE = "precommande"

# Volontairement incomplete -- a enrichir au fil des cas reels constates
# (meme limite assumee que NOMS_SET_QUALIFICATIF_AMBIGU/MOTS_ETAT_REFUSE).
MOTS_CLES_TYPE_PRODUIT_SCELLE = frozenset({
    "etb", "dresseur d'elite", "dresseur elite", "elite trainer box",
    "display", "coffret", "boite", "box", "triple pack", "collection",
    "starter deck", "deck de demarrage", "tin", "boite metal",
    "duo pack", "premium collection", "ultra premium collection", "upc",
    "booster box", "bundle",
})

# Idem : volontairement incomplete.
FRANCHISES_EXCLUES = frozenset({
    "yu-gi-oh", "yugioh", "yu gi oh", "magic", "mtg", "lorcana",
    "disney lorcana", "one piece", "dragon ball", "digimon", "naruto",
    "star wars unlimited", "final fantasy tcg",
})


# Categories exposees au filtre du dashboard PokePrecoms (justok16/pokeprecoms,
# app/dashboard/page.tsx) -- ajoute le 23/08/2026 a la demande de Justok.
# Liste volontairement FERMEE (contrairement a MOTS_CLES_TYPE_PRODUIT_SCELLE,
# qui ne fait qu'accepter/rejeter) : un produit qui ne matche AUCUN mot-cle
# ci-dessous tombe dans CATEGORIE_AUTRE plutot que d'etre force dans une
# categorie incorrecte -- le dashboard affiche cette categorie comme un
# onglet a part, jamais masquee.
CATEGORIE_DISPLAYS = "Displays"
CATEGORIE_ETB = "ETB"
CATEGORIE_BOOSTERS_BLISTERS = "Boosters & Blisters"
CATEGORIE_COFFRETS = "Coffrets"
CATEGORIE_POKEBOX_TINS = "Pokébox & Tins"
CATEGORIE_AUTRE = "Autres"

# Ordre de verification volontaire : du plus specifique au plus generique,
# pour eviter qu'un mot-cle generique ("box" dans "coffret"/"booster box")
# ne masque une categorie plus precise presente dans le meme titre (ex. "ETB"
# doit l'emporter sur "coffret" si les deux mots apparaissent). Chaque
# categorie a sa propre liste, volontairement incomplete comme
# MOTS_CLES_TYPE_PRODUIT_SCELLE -- a enrichir au fil des cas reels constates.
_CATEGORIES_PAR_PRIORITE = (
    (CATEGORIE_ETB, frozenset({"etb", "dresseur d'elite", "dresseur elite", "elite trainer box"})),
    (CATEGORIE_POKEBOX_TINS, frozenset({"tin", "boite metal", "pokebox", "poke box"})),
    (CATEGORIE_DISPLAYS, frozenset({"display"})),
    (CATEGORIE_BOOSTERS_BLISTERS, frozenset({"booster", "blister", "sachet"})),
    (CATEGORIE_COFFRETS, frozenset({
        "coffret", "collection", "premium collection", "ultra premium collection",
        "upc", "duo pack", "triple pack", "starter deck", "deck de demarrage", "bundle",
        "boite", "box",
    })),
)


def determiner_categorie_produit(titre: str, description: str = "") -> str:
    """Classe un produit deja retenu comme candidat (cf.
    produit_est_candidat_precommande) dans l'une des categories du filtre
    dashboard PokePrecoms. CATEGORIE_AUTRE si aucun mot-cle ne matche --
    jamais une exception, jamais une categorie devinee au hasard."""
    texte_norm = _normaliser(f"{titre} {description}")
    for categorie, mots_cles in _CATEGORIES_PAR_PRIORITE:
        if any(_normaliser(mot) in texte_norm for mot in mots_cles):
            return categorie
    return CATEGORIE_AUTRE


def produit_est_candidat_precommande(titre: str, description: str = "") -> tuple[bool, str]:
    """Applique les 4 conditions au texte d'un produit (titre + description
    optionnelle). Retourne (True, raison) si retenu comme candidat serieux
    a une alerte de precommande Pokemon TCG generique, (False, raison)
    sinon -- la raison sert au logging/debug, jamais affichee telle quelle
    dans une alerte."""
    texte_norm = _normaliser(f"{titre} {description}")

    if MOT_CLE_POKEMON not in texte_norm:
        return False, "aucune mention explicite de Pokemon"

    franchise_trouvee = next(
        (f for f in FRANCHISES_EXCLUES if _normaliser(f) in texte_norm), None
    )
    if franchise_trouvee:
        return False, f"autre franchise TCG mentionnee ({franchise_trouvee})"

    if MOT_CLE_PRECOMMANDE not in texte_norm:
        return False, "aucune mention explicite de precommande"

    if not any(_normaliser(mot) in texte_norm for mot in MOTS_CLES_TYPE_PRODUIT_SCELLE):
        return False, "aucun mot-cle de type de produit scelle"

    return True, "pokemon + precommande + type de produit scelle confirmes, aucune autre franchise"
