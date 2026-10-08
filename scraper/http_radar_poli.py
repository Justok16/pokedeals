"""Transport du radar : identite honnete et un depart HTTP/s par hote.

Le verrou couvre les threads du processus, pas des runners distincts.
Les en-tetes Accept des connecteurs sont conserves. Aucun contournement.
"""
import threading
import time
from urllib.parse import urlsplit

import requests

USER_AGENT = "PokeDealsRestock/1.0 (+https://github.com/Justok16/pokedeals; alerts-only)"
_verrou = threading.Lock()
_derniers_departs = {}
_verrous_hotes = {}


class SessionRadarPolie(requests.Session):
    def send(self, request, **kwargs):
        hote = urlsplit(request.url).netloc.lower()
        with _verrou:
            verrou_hote = _verrous_hotes.setdefault(hote, threading.RLock())
        with verrou_hote:
            maintenant = time.monotonic()
            attente = 1.0 - (maintenant - _derniers_departs.get(hote, float("-inf")))
            if attente > 0:
                time.sleep(attente)
            _derniers_departs[hote] = time.monotonic()
            request.headers["User-Agent"] = USER_AGENT
        # Ne pas garder le verrou durant la lecture ; le depart suivant
        # est espace d'au moins 1s, y compris en cas de redirection.
        return super().send(request, **kwargs)


def rendre_poli(connecteur):
    """Remplace la session avant la premiere lecture, jamais les doublures de test."""
    session = getattr(connecteur, "session", None)
    if isinstance(session, requests.Session) and not isinstance(session, SessionRadarPolie):
        session.close()
        connecteur.session = SessionRadarPolie()
    return connecteur
