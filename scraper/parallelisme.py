"""Reglage du parallelisme de lecture des boutiques (06/10/2026).

Les scans lisent des dizaines de catalogues : en sequentiel (une boutique apres
l'autre) un cycle dure ~8 min. La lecture est du pur reseau (un connecteur et une
session par boutique) ; seules des boutiques DIFFERENTES se chevauchent, jamais
la meme deux fois. Le traitement (matching, alertes, memoire) reste sequentiel.

Chaque scan lit son nombre de lecteurs dans une variable d'environnement
(1 = ancien comportement sequentiel). Valeur invalide ou absente -> defaut ;
toujours bornee entre 1 et `plafond` pour ne jamais surcharger les boutiques.
"""

import os

PARALLELISME_PAR_DEFAUT = 4
PARALLELISME_MAX = 8


def lire_parallelisme(nom_variable: str, defaut: int = PARALLELISME_PAR_DEFAUT,
                      plafond: int = PARALLELISME_MAX) -> int:
    try:
        n = int(os.environ.get(nom_variable, defaut))
    except ValueError:
        n = defaut
    return max(1, min(n, plafond))
