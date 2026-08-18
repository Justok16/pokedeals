"""
Ecriture atomique generique de fichiers JSON pour PokeDeals.

Extrait de main.py le 17/08/2026 lors du decoupage du connecteur
Cardtrader (connecteur_cardtrader.py), qui en a besoin lui aussi -- evite
une duplication entre les deux fichiers plutot que d'en garder une copie
locale a chacun. main.py continue a l'utiliser sous son nom local
historique (`_ecrire_json_atomique`, via un alias d'import) pour ne
toucher aucun de ses appels existants.
"""
import json
import os


def ecrire_json_atomique(chemin: str, donnees, **kwargs) -> None:
    """Ecrit un JSON de facon atomique (fichier temporaire + os.replace)
    pour ne jamais laisser un data/*.json tronque/corrompu si le process
    est tue en plein ecriture (ex. timeout GitHub Actions).

    Audit du 18/08/2026 : os.makedirs(os.path.dirname(chemin)) levait
    FileNotFoundError si `chemin` etait un nom de fichier NU (sans
    composant de dossier, ex. "test.json") -- os.path.dirname() renvoie
    alors "", et os.makedirs("") echoue. Tous les appels reels du projet
    utilisent des chemins deja enracines dans data/ (donc jamais touches
    par ce cas), mais corrige quand meme par prudence (garde-fou gratuit,
    zero risque pour les appels existants)."""
    dossier = os.path.dirname(chemin)
    if dossier:
        os.makedirs(dossier, exist_ok=True)
    tmp = f"{chemin}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(donnees, f, **kwargs)
    os.replace(tmp, chemin)
