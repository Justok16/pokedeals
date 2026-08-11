"""
Chargement/sauvegarde generique d'un fichier memoire JSON (dict simple).

Partage par alerte_stock.py et alerte_precommande.py -- fonctions
identiques dupliquees dans les 2 avant factorisation ici le 11/08/2026
(audit de sante du projet).
"""

import json
from pathlib import Path


def charger_memoire(chemin: Path) -> dict:
    if not chemin.exists():
        return {}
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def sauvegarder_memoire(memoire: dict, chemin: Path) -> None:
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(memoire, f, indent=2, ensure_ascii=False)
