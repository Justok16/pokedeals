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
"""
from __future__ import annotations

_stats_fiabilite = {"vinted_appels": 0, "vinted_echecs": 0, "leboncoin_appels": 0, "leboncoin_echecs": 0}
