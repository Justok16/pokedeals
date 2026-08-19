"""Tests de non-regression pour json_utils.ecrire_json_atomique() --
premiere couverture dediee (audit du 18/08/2026), l'un des 2 seuls points
d'ecriture disque du projet (avec memoire_json.py)."""

import json
import os

from json_utils import ecrire_json_atomique


def test_ecrit_puis_relit_les_memes_donnees(tmp_path):
    chemin = str(tmp_path / "data" / "sous_dossier" / "fichier.json")
    ecrire_json_atomique(chemin, {"a": 1, "b": [1, 2, 3]})
    assert json.loads(open(chemin, encoding="utf-8").read()) == {"a": 1, "b": [1, 2, 3]}


def test_cree_les_dossiers_intermediaires_manquants(tmp_path):
    chemin = str(tmp_path / "ne" / "existe" / "pas" / "encore" / "fichier.json")
    assert not os.path.exists(os.path.dirname(chemin))
    ecrire_json_atomique(chemin, {"ok": True})
    assert os.path.exists(chemin)


def test_ne_laisse_pas_de_fichier_tmp_apres_ecriture(tmp_path):
    chemin = str(tmp_path / "fichier.json")
    ecrire_json_atomique(chemin, {"x": 1})
    assert not os.path.exists(chemin + ".tmp")


def test_ecrasement_dun_fichier_existant(tmp_path):
    chemin = str(tmp_path / "fichier.json")
    ecrire_json_atomique(chemin, {"version": 1})
    ecrire_json_atomique(chemin, {"version": 2})
    assert json.loads(open(chemin, encoding="utf-8").read()) == {"version": 2}


def test_kwargs_json_dump_transmis(tmp_path):
    # ensure_ascii=False, indent=... -- deja utilises par tous les vrais
    # appelants (main.py, moteur_cote.py, connecteur_cardtrader.py...).
    chemin = str(tmp_path / "fichier.json")
    ecrire_json_atomique(chemin, {"nom": "carte française"}, ensure_ascii=False, indent=2)
    contenu = open(chemin, encoding="utf-8").read()
    assert "française" in contenu  # pas echappe en ç... grace a ensure_ascii=False
    assert "\n  " in contenu       # indente


def test_nom_de_fichier_nu_sans_dossier_ne_leve_plus(tmp_path, monkeypatch):
    # Audit du 18/08/2026 : os.makedirs(os.path.dirname(chemin)) levait
    # FileNotFoundError pour un chemin sans composant de dossier -- tous
    # les appels reels du projet utilisent des chemins deja enracines
    # dans data/, mais ce cas est corrige par prudence.
    monkeypatch.chdir(tmp_path)
    try:
        ecrire_json_atomique("fichier_nu.json", {"ok": True})
        assert json.loads(open("fichier_nu.json", encoding="utf-8").read()) == {"ok": True}
    finally:
        if os.path.exists("fichier_nu.json"):
            os.remove("fichier_nu.json")
        if os.path.exists("fichier_nu.json.tmp"):
            os.remove("fichier_nu.json.tmp")
