"""
Cache JSON generique avec expiration (TTL), pour eviter des requetes
inutiles vers les APIs externes.

Reutilise l'ecriture atomique deja existante dans memoire_json.py (racine
du depot, deja utilisee par alerte_stock.py/alerte_precommande.py) -- meme
logique que pour les fichiers data/*.json de PokeDeals, pas de nouveau
mecanisme invente. Le cache du MCP vit dans mcp_pokedeals/.cache/ (jamais
dans data/, pour rester totalement separe des fichiers memoire de
PokeDeals et ne jamais etre embarque par erreur dans un commit -- voir
.gitignore).
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from memoire_json import charger_memoire, sauvegarder_memoire  # noqa: E402


class CacheJSON:
    """Cache cle -> valeur, persiste dans un fichier JSON, avec une duree
    de validite (TTL) en secondes verifiee a la lecture (pas de purge
    automatique des entrees perimees : elles sont juste ignorees, et
    remplacees au prochain `set` sur la meme cle)."""

    def __init__(self, chemin: Path):
        self.chemin = chemin
        self._donnees = charger_memoire(chemin)

    def get(self, cle: str, ttl_secondes: int) -> Any | None:
        entree = self._donnees.get(cle)
        if not entree:
            return None
        age = time.time() - entree.get("ts", 0)
        if age > ttl_secondes:
            return None
        return entree.get("valeur")

    def set(self, cle: str, valeur: Any) -> None:
        self._donnees[cle] = {"valeur": valeur, "ts": time.time()}
        sauvegarder_memoire(self._donnees, self.chemin)
