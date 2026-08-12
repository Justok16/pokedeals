"""Tests de la logique de tendance de prix (historique_prix.py) -- purement
locaux, aucun appel reseau (PokemonPriceTracker n'est jamais interroge ici)."""

from historique_prix import MIN_POINTS_POUR_SIGNAL, analyser_tendance


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
