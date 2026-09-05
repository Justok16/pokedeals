"""Tests de non-regression pour extraire_nom_et_numero() (watchlist_shopify.py)
-- aucune couverture existante avant ce fichier, malgre son usage direct sur
du texte libre saisi par les utilisateurs du SaaS (dashboard "Ajouter une
carte", cf. watchlist_saas.py)."""

from watchlist_shopify import extraire_nom_et_numero


def test_format_config_yaml_standard():
    assert extraire_nom_et_numero("Charmander 168/165 sv2a") == ("Charmander", "168/165", None)


def test_qualificatif_ex_detecte():
    assert extraire_nom_et_numero("Plumeline ex 024") == ("Plumeline", "024", "ex")


def test_prefixe_team_rocket_ignore():
    assert extraire_nom_et_numero("Team Rocket's Mewtwo ex 237 m2a") == (
        "Mewtwo", "237", "ex"
    )


def test_set_151_ecrit_apres_le_numero_ne_remplace_pas_le_vrai_numero():
    """Bug reel signale par Justok (23/08/2026) : un utilisateur SaaS a
    saisi "Carapuce (MEW 170) 151 - Squirtle" (170 = vrai numero de la
    carte dans le set "151"/sv2a, "MEW" = code de set anglophone, "151" =
    nom populaire du set, PAS le numero). Avant correctif (ajout de
    "151"/"mew" a CODES_SET_CONNUS), la regle "dernier token avec un
    chiffre = numero" capturait a tort "151" (le nom du set) au lieu de
    "170" (le vrai numero), et "MEW" restait dans le nom de recherche
    -- mauvaise carte alertee en production."""
    assert extraire_nom_et_numero("Carapuce (MEW 170) 151 - Squirtle") == (
        "Carapuce", "170", None
    )


def test_set_151_seul_sans_parentheses():
    assert extraire_nom_et_numero("Dracaufeu ex 006 151") == ("Dracaufeu", "006", "ex")


def test_mention_gradation_nest_pas_capturee_dans_le_nom():
    """Bug reel trouve lors d'un audit externe multi-IA (05/09/2026) sur un
    vrai compte utilisateur SaaS : "Metagross PSA 10 m2a 245/193" -- le
    numero (245/193) apparait APRES "PSA 10", donc la boucle de collecte du
    nom atteignait "psa" (ni terminateur ni code de set connu a l'epoque)
    avant tout token contenant un chiffre, et le capturait dans le nom de
    recherche ("Metagross PSA" au lieu de "Metagross"), degradant toute
    recherche eBay/Vinted/boutiques pour cette carte. "psa"/"cgc"/"bgs"/
    "ccc"/"gradee"/"graded"/"grade" ajoutes a MOTS_TERMINATEURS."""
    assert extraire_nom_et_numero("Metagross PSA 10 m2a 245/193") == (
        "Metagross", "245/193", None
    )
