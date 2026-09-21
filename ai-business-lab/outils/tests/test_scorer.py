"""Tests du moteur de classement.

Ce qui est teste ici, ce n'est pas une opinion strategique mais le fait que
le calcul soit juste et qu'une donnee fausse casse au lieu de passer.
"""

import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import scorer  # noqa: E402


@pytest.fixture
def criteres():
    return scorer.charger_criteres()


@pytest.fixture
def concepts():
    return scorer.charger_concepts()


def test_les_donnees_reelles_se_chargent(criteres, concepts):
    assert len(criteres) >= 10
    assert len(concepts) >= 10


def test_chaque_concept_est_valide(criteres, concepts):
    # Garde-fou principal : un critere oublie dans concepts.yaml fausserait
    # le classement a la baisse sans aucun signal visible.
    for concept in concepts:
        scorer.valider(concept, criteres)


def test_score_maximal_vaut_cent(criteres):
    parfait = scorer.Concept(
        id="TEST", nom="parfait", cluster="", resume="",
        notes={c.nom: scorer.NOTE_MAX for c in criteres},
    )
    assert scorer.score(parfait, criteres) == 100.0


def test_score_minimal_vaut_zero(criteres):
    nul = scorer.Concept(
        id="TEST", nom="nul", cluster="", resume="",
        notes={c.nom: 0 for c in criteres},
    )
    assert scorer.score(nul, criteres) == 0.0


def test_note_hors_bornes_refusee(criteres):
    triche = scorer.Concept(
        id="TRICHE", nom="triche", cluster="", resume="",
        notes={c.nom: (7 if i == 0 else 3) for i, c in enumerate(criteres)},
    )
    with pytest.raises(scorer.ErreurDonnees):
        scorer.score(triche, criteres)


def test_critere_manquant_refuse(criteres):
    incomplet = scorer.Concept(
        id="INCOMPLET", nom="incomplet", cluster="", resume="",
        notes={c.nom: 3 for c in criteres[:-1]},
    )
    with pytest.raises(scorer.ErreurDonnees):
        scorer.score(incomplet, criteres)


def test_le_poids_change_le_classement(concepts, tmp_path):
    """Le classement doit reellement dependre des poids, pas seulement des notes.

    Si ce test echoue, c'est que la grille de poids est decorative.
    """
    base = scorer.charger_criteres()
    ordre_initial = [c.id for c, *_ in scorer.classement(concepts, base)]

    # Grille alternative : tout le poids sur la faisabilite immediate.
    alternative = [
        scorer.Critere(nom=c.nom, poids=(10.0 if c.nom in scorer.AXE_FAISABILITE else 0.1), sens=c.sens)
        for c in base
    ]
    ordre_alternatif = [c.id for c, *_ in scorer.classement(concepts, alternative)]
    assert ordre_initial != ordre_alternatif


def test_identifiants_uniques(concepts):
    identifiants = [c.id for c in concepts]
    assert len(identifiants) == len(set(identifiants))


def test_rendus_markdown_et_csv(concepts, criteres):
    lignes = scorer.classement(concepts, criteres)
    assert scorer.rendu_markdown(lignes).startswith("| # | ID |")
    assert scorer.rendu_csv(lignes).splitlines()[0].startswith("rang,id")


def test_le_fichier_concepts_est_du_yaml_valide():
    brut = yaml.safe_load((scorer.FICHIER_CONCEPTS).read_text(encoding="utf-8"))
    assert "concepts" in brut
