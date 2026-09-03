"""
État partagé pour l'alerte de fiabilité Vinted/Leboncoin (V50, cf.
CLAUDE.md/SESSION_NOTES.md) : compteurs d'appels/échecs par plateforme,
remis à zéro à chaque cycle.

Extrait de main.py le 17/08/2026 en même temps que le connecteur Leboncoin
(connecteur_leboncoin.py) : les deux modules incrémentent ce dict au fil
d'un cycle (vinted_rechercher() reste dans main.py, lbc_rechercher() migre
dans connecteur_leboncoin.py), et main.py le lit ensuite dans
verifier_fiabilite_plateformes(). Seul le dict lui-même vit ici ;
_reinitialiser_stats_fiabilite() et verifier_fiabilite_plateformes()
restent dans main.py (jamais appelés que depuis main()).

Le dict n'est JAMAIS réassigné en bloc (seulement muté clé par clé, `+= 1`
ou `[cle] = 0`) : un simple `from stats_fiabilite import _stats_fiabilite`
dans chaque module suffit donc, pas besoin d'accès qualifié comme pour
_ct_cache dans connecteur_cardtrader.py (cf. SESSION_NOTES.md, piège
_ct_cache).

_circuit_vinted (03/09/2026, audit) : état du coupe-circuit Vinted, même
principe que _ebay_circuit (main.py, V61) mais partagé ici pour la même
raison que _stats_fiabilite -- alimenté par vinted_rechercher() (main.py),
lu par verifier_circuits_vinted_leboncoin()/_reinitialiser_circuits_
vinted_leboncoin() (main.py également). Même garantie de mutation
clé-par-clé (jamais réassigné en bloc), pas d'accès qualifié requis.
_circuit_leboncoin est l'équivalent pour Leboncoin, alimenté depuis
connecteur_leboncoin.py (lbc_rechercher()) mais lu depuis les mêmes
fonctions main.py -- vit ici plutôt que dans main.py pour rester
accessible sans import circulaire depuis connecteur_leboncoin.py (qui ne
peut pas importer main.py, cf. sa docstring).
"""
from __future__ import annotations

_stats_fiabilite = {"vinted_appels": 0, "vinted_echecs": 0, "leboncoin_appels": 0, "leboncoin_echecs": 0}
_circuit_vinted = {"echecs_consecutifs": 0, "abandonne": False}
_circuit_leboncoin = {"echecs_consecutifs": 0, "abandonne": False}
