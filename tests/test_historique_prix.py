"""Tests de la logique de tendance de prix (historique_prix.py) -- purement
locaux, aucun appel reseau (PokemonPriceTracker n'est jamais interroge ici)."""

from unittest.mock import patch

import requests

from historique_prix import MIN_POINTS_POUR_SIGNAL, analyser_tendance, taux_change_vers_eur, _texte_telegram_tendance
from watchlist_tendance import CARTES_TENDANCE


def _points(prix: list[float], debut_jour: int = 1) -> list[dict]:
    return [
        {"date": f"2026-07-{debut_jour + i:02d}", "prix_pokemonpricetracker": p, "cote_pokedeals": None}
        for i, p in enumerate(prix)
    ]


def test_pas_assez_de_points_pas_de_signal():
    points = _points([100.0] * (MIN_POINTS_POUR_SIGNAL - 1))
    resultat = analyser_tendance(points)
    assert resultat["signal"] == "pas_assez_de_donnees"


def test_baisse_de_prix_declenche_bon_moment_achat():
    points = _points([100.0] * 19) + _points([85.0], debut_jour=32)
    resultat = analyser_tendance(points)
    assert resultat["signal"] == "bon_moment_achat"
    assert resultat["ecart_pct"] < -10.0


def test_hausse_de_prix_declenche_prix_eleve():
    points = _points([100.0] * 19) + _points([130.0], debut_jour=32)
    resultat = analyser_tendance(points)
    assert resultat["signal"] == "prix_eleve"
    assert resultat["ecart_pct"] > 10.0


def test_prix_stable_ne_declenche_aucun_signal_extreme():
    points = _points([100.0, 101.0, 99.0] * 7)
    resultat = analyser_tendance(points)
    assert resultat["signal"] == "stable"


def test_repli_sur_cote_pokedeals_si_pokemonpricetracker_absent():
    points = [
        {"date": f"2026-07-{i:02d}", "prix_pokemonpricetracker": None, "cote_pokedeals": 50.0}
        for i in range(1, 20)
    ]
    resultat = analyser_tendance(points)
    assert resultat["signal"] == "stable"
    assert resultat["prix_actuel"] == 50.0


def test_points_sans_aucun_prix_sont_ignores():
    points = [{"date": "2026-07-01", "prix_pokemonpricetracker": None, "cote_pokedeals": None}] * 20
    resultat = analyser_tendance(points)
    assert resultat["signal"] == "pas_assez_de_donnees"
    assert resultat["nb_points"] == 0


def test_taux_change_eur_vers_eur_est_toujours_1_sans_reseau():
    # Pas de mock necessaire : le passthrough EUR->EUR ne doit jamais appeler le reseau.
    assert taux_change_vers_eur("EUR") == 1.0


def test_taux_change_retourne_none_si_les_2_sources_echouent():
    with patch("historique_prix.requests.get", side_effect=requests.exceptions.ConnectionError("coupe")):
        assert taux_change_vers_eur("CHF") is None


def test_texte_telegram_affiche_conversion_euro_quand_taux_disponible():
    tendance = {"signal": "stable", "prix_actuel": 10.0, "devise": "USD", "date_actuelle": "2026-08-13",
                "moyenne_recente": 10.0, "ecart_pct": 0.0, "nb_points_fenetre": 14, "nb_points_total": 14}
    with patch("historique_prix.taux_change_vers_eur", return_value=0.9):
        texte = _texte_telegram_tendance(CARTES_TENDANCE[0], tendance)
    assert "9.00€" in texte
    assert "10.00 USD" in texte


def test_texte_telegram_ne_plante_pas_si_taux_indisponible():
    tendance = {"signal": "stable", "prix_actuel": 10.0, "devise": "USD", "date_actuelle": "2026-08-13",
                "moyenne_recente": 10.0, "ecart_pct": 0.0, "nb_points_fenetre": 14, "nb_points_total": 14}
    with patch("historique_prix.taux_change_vers_eur", return_value=None):
        texte = _texte_telegram_tendance(CARTES_TENDANCE[0], tendance)
    assert "conversion € indisponible" in texte
    assert "10.00 USD" in texte
