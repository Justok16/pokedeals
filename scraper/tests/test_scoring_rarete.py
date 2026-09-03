"""Tests de non-regression pour scoring_rarete.py -- notamment le cablage
de nb_annonces_ebay sur moteur_cote.derniere_nb_annonces() (03/09/2026,
audit) qui remplace l'ancien stub statique a None."""

from unittest.mock import patch

from scoring_rarete import charger_depuis_pokedeals
from watchlist_shopify import CarteWatchlist


def _carte(nom_config="Dracaufeu ex 199/165", langue="fr"):
    return CarteWatchlist(
        nom_recherche="Dracaufeu",
        numero="199/165",
        langue=langue,
        nom_config=nom_config,
    )


def test_charger_depuis_pokedeals_cable_nb_annonces_ebay():
    with patch("scoring_rarete.charger_watchlist_config", return_value=[_carte()]), \
         patch("scoring_rarete.moteur_cote.cote_lissee", return_value=123.45), \
         patch("scoring_rarete.moteur_cote.derniere_nb_annonces", return_value=8) as dna_mock:
        cartes = charger_depuis_pokedeals()
    assert len(cartes) == 1
    assert cartes[0]["nb_annonces_ebay"] == 8
    assert cartes[0]["cote_bas_marche"] == 123.45
    dna_mock.assert_called_once_with("Dracaufeu ex 199/165", "fr")


def test_charger_depuis_pokedeals_nb_annonces_ebay_none_si_jamais_enregistre():
    with patch("scoring_rarete.charger_watchlist_config", return_value=[_carte()]), \
         patch("scoring_rarete.moteur_cote.cote_lissee", return_value=None), \
         patch("scoring_rarete.moteur_cote.derniere_nb_annonces", return_value=None):
        cartes = charger_depuis_pokedeals()
    assert cartes[0]["nb_annonces_ebay"] is None


def test_charger_depuis_pokedeals_autres_champs_encore_a_none():
    # Champs sans source restent volontairement a None (cf. docstring du module).
    with patch("scoring_rarete.charger_watchlist_config", return_value=[_carte()]), \
         patch("scoring_rarete.moteur_cote.cote_lissee", return_value=None), \
         patch("scoring_rarete.moteur_cote.derniere_nb_annonces", return_value=None):
        cartes = charger_depuis_pokedeals()
    assert cartes[0]["nb_annonces_cardtrader"] is None
    assert cartes[0]["set"] is None
    assert cartes[0]["rarete"] is None
