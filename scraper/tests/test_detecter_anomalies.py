"""Tests de non-regression pour main.detecter_anomalies() -- premiere
couverture dediee (audit du 18/08/2026).

V58 : `nb_lisse = min(2, len(valeurs) // 2) or 1` retombait a 1 (comparaison
a UN SEUL point, division entiere) pour exactement 3 points d'historique --
c'est precisement le bug que V42 avait corrige (une cote INSTANTANEE peut
sursauter d'un scan a l'autre sans que le marche ait vraiment bouge), mais
reintroduit silencieusement a 3 points. Cet etat a 3 points est traverse par
CHAQUE carte juste apres une purge d'historique (PURGE_VERSION), pas un cas
rare. Corrige par `nb_lisse = min(2, len(valeurs) - 1)`, qui vaut toujours 2
des que la garde `len(entrees) < 3` en amont est passee."""

import main


def _entrees(cotes: list[float]) -> list[dict]:
    return [{"cote": c} for c in cotes]


def test_moins_de_3_points_aucune_alerte():
    main.historique = lambda: {"Dracaufeu ex|jp": _entrees([100.0, 226.0])}
    assert main.detecter_anomalies({}, {}) == []


def test_exactement_3_points_reste_lisse_sur_2_valeurs_pas_1():
    # Avant V58 (bug) : nb_lisse=1 -> ancienne=100, recente=151, +51% ->
    # alerte "FORTE HAUSSE" (seuil par defaut 50%).
    # Apres V58 (fix) : nb_lisse=2 -> ancienne=mean(100,100)=100,
    # recente=mean(100,151)=125.5, +25.5% -> pas d'alerte.
    main.historique = lambda: {"Evoli ex|jp": _entrees([100.0, 100.0, 151.0])}
    assert main.detecter_anomalies({}, {}) == []


def test_exactement_3_points_detecte_quand_meme_une_vraie_grosse_variation():
    # La fenetre a 2 points chevauche a 3 valeurs, mais reste sensible a une
    # variation reellement importante et confirmee sur 2 points recents.
    main.historique = lambda: {"Evoli ex|jp": _entrees([100.0, 100.0, 400.0])}
    alertes = main.detecter_anomalies({}, {})
    assert len(alertes) == 1
    assert "FORTE HAUSSE" in alertes[0]


def test_4_points_comportement_inchange_deux_points_de_chaque_cote():
    main.historique = lambda: {"Pikachu|fr": _entrees([100.0, 100.0, 100.0, 40.0])}
    alertes = main.detecter_anomalies({}, {})
    # ancienne=mean(100,100)=100, recente=mean(100,40)=70, -30% -> alerte chute (seuil 30%)
    assert len(alertes) == 1
    assert "CHUTE" in alertes[0]
