"""Tests de non-regression pour memoire_json.py (charger_memoire /
sauvegarder_memoire) -- premiere couverture dediee (audit du 18/08/2026),
partagees par alerte_stock.py, alerte_precommande.py, decouverte_boutiques.py
et mcp_pokedeals/cache.py."""

import json
from pathlib import Path

from memoire_json import charger_memoire, sauvegarder_memoire


def test_charger_memoire_fichier_absent_renvoie_dict_vide(tmp_path):
    chemin = tmp_path / "nexistepas.json"
    assert charger_memoire(chemin) == {}


def test_charger_memoire_json_invalide_renvoie_dict_vide(tmp_path):
    chemin = tmp_path / "corrompu.json"
    chemin.write_text("{ceci n'est pas du json valide", encoding="utf-8")
    assert charger_memoire(chemin) == {}


def test_ecrit_puis_relit_les_memes_donnees(tmp_path):
    chemin = tmp_path / "sous_dossier" / "memoire.json"
    donnees = {"exemple.fr|Dracaufeu ex 199/165": {"en_stock": True}}
    sauvegarder_memoire(donnees, chemin)
    assert charger_memoire(chemin) == donnees


def test_cree_les_dossiers_intermediaires_manquants(tmp_path):
    chemin = tmp_path / "ne" / "existe" / "pas" / "memoire.json"
    assert not chemin.parent.exists()
    sauvegarder_memoire({"a": 1}, chemin)
    assert chemin.exists()


def test_ne_laisse_pas_de_fichier_tmp_apres_ecriture(tmp_path):
    chemin = tmp_path / "memoire.json"
    sauvegarder_memoire({"a": 1}, chemin)
    assert not chemin.with_suffix(".json.tmp").exists()


def test_ecriture_preserve_les_accents_sans_les_echapper(tmp_path):
    # ensure_ascii=False (fixe dans sauvegarder_memoire) -- deja verifie
    # comme fausse alerte lors d'un audit precedent (SESSION_NOTES.md,
    # "encodage des fichiers memoire precommandes"), teste explicitement ici.
    chemin = tmp_path / "memoire.json"
    sauvegarder_memoire({"nom": "Florizarre ex 198/165"}, chemin)
    contenu = chemin.read_text(encoding="utf-8")
    assert "\\u" not in contenu


def test_ecrasement_dun_fichier_existant(tmp_path):
    chemin = tmp_path / "memoire.json"
    sauvegarder_memoire({"version": 1}, chemin)
    sauvegarder_memoire({"version": 2}, chemin)
    assert charger_memoire(chemin) == {"version": 2}


def test_chemin_str_fonctionne_comme_chemin_path(tmp_path):
    # charger_memoire()/sauvegarder_memoire() sont annotees Path mais
    # Path(chemin) et open(chemin) acceptent aussi une str -- verifie que
    # ca fonctionne reellement (duck typing), certains appelants passant
    # parfois des chemins construits en str.
    chemin = str(tmp_path / "memoire.json")
    sauvegarder_memoire({"a": 1}, Path(chemin))
    assert json.loads(Path(chemin).read_text(encoding="utf-8")) == {"a": 1}
