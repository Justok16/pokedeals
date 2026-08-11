"""Tests de non-regression pour le filtre qualificatif symetrique
(watchlist_shopify.py) -- 3 bugs reels distincts corriges sur ce meme
mecanisme, cf. SESSION_NOTES.md."""

from watchlist_shopify import detecter_qualificatif_titre


def test_qualificatif_present_est_detecte():
    assert detecter_qualificatif_titre("Bulbizarre ex 166/165 - Edition Speciale") == "ex"


def test_pas_de_qualificatif_ne_detecte_rien():
    assert detecter_qualificatif_titre("Bulbizarre 166/165") is None


def test_pas_de_faux_positif_sur_evoli_a_cause_du_v_de_qualificatif():
    # "v" en substring nu matcherait "Evoli" -- doit etre borne par \b...\b.
    assert detecter_qualificatif_titre("Evoli 210 - Set Standard") is None


def test_nom_de_coffret_ambigu_mega_dream_nexclut_pas_a_tort():
    # Bug reel corrige (2026-08-10) : le coffret JP "MEGA Dream ex" contient
    # lui-meme le mot "ex" dans son propre nom -- une carte de BASE
    # (Psykokwak, non-ex) vendue dans ce coffret ne doit pas etre rejetee a
    # tort pour "qualificatif inattendu".
    titre = "Psykokwak 199/193 - MEGA Dream ex Booster Box"
    assert detecter_qualificatif_titre(titre, numero="199") is None


def test_nom_de_coffret_ambigu_vmax_climax_nexclut_pas_a_tort():
    titre = "Evoli 210 - VMAX Climax Booster Box"
    assert detecter_qualificatif_titre(titre, numero="210") is None
