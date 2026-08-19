"""Tests de non-regression pour le filtre qualificatif symetrique
(watchlist_shopify.py) -- 3 bugs reels distincts corriges sur ce meme
mecanisme, cf. SESSION_NOTES.md."""

from watchlist_shopify import detecter_qualificatif_titre, qualificatif_present_dans_titre


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


# ------------------- qualificatif_present_dans_titre (verification POSITIVE) -------------------
# Audit externe du 18/08/2026 : la verification positive ("carte.qualificatif
# attendu -- est-il present ?") cherchait auparavant \bex\b sur le TITRE
# ENTIER, sans le fenetrage deja applique a la verification negative
# ci-dessus. Ces tests couvrent le nouveau comportement.

def test_qualificatif_attendu_present_pres_du_numero():
    titre = "Dracaufeu ex 199/165 - Edition Speciale"
    assert qualificatif_present_dans_titre(titre, "ex", numero="199/165") is True


def test_qualificatif_attendu_absent():
    titre = "Dracaufeu 199/165 - Edition Speciale"
    assert qualificatif_present_dans_titre(titre, "ex", numero="199/165") is False


def test_qualificatif_v_ne_matche_pas_evoli_par_substring():
    # Meme piege que detecter_qualificatif_titre : "v" nu matcherait "Evoli".
    titre = "Evoli 210 - Set Standard"
    assert qualificatif_present_dans_titre(titre, "v", numero="210") is False


def test_qualificatif_attendu_reste_detecte_meme_depuis_un_nom_de_set_ambigu():
    # Cas cle de l'audit : contrairement a detecter_qualificatif_titre (qui
    # renvoie None des qu'un nom de set ambigu comme "MEGA Dream ex" est
    # present, pour eviter un FAUX REJET d'une carte SANS qualificatif),
    # qualificatif_present_dans_titre ne doit PAS avoir ce court-circuit --
    # sinon une VRAIE carte "ex" issue de ce meme set (ex: Team Rocket's
    # Mewtwo ex, m2a "MEGA Dream ex", deja suivie dans la watchlist) serait
    # rejetee a tort pour "qualificatif manquant".
    titre = "Team Rocket's Mewtwo ex 237/193 — MEGA Dream ex"
    assert qualificatif_present_dans_titre(titre, "ex", numero="237/193") is True
