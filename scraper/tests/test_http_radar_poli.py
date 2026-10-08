from types import SimpleNamespace
from unittest.mock import Mock, patch

import requests

import http_radar_poli as poli


def test_depart_espace_entre_sessions_et_ua_non_usurpe(monkeypatch):
    poli._derniers_departs.clear()
    horloge = [10.0]
    departs = []
    monkeypatch.setattr(poli.time, "monotonic", lambda: horloge[0])
    monkeypatch.setattr(poli.time, "sleep", lambda duree: horloge.__setitem__(0, horloge[0] + duree))

    def envoyer(self, request, **kwargs):
        departs.append((horloge[0], request.headers["User-Agent"], request.headers["Accept"]))
        return requests.Response()

    with patch.object(requests.Session, "send", envoyer):
        for _ in range(3):
            poli.SessionRadarPolie().get("https://exemple.fr/p.json",
                                       headers={"User-Agent": "Chrome", "Accept": "application/json"})
    assert [d[0] for d in departs] == [10.0, 11.0, 12.0]
    assert all(d[1] == poli.USER_AGENT and d[2] == "application/json" for d in departs)


def test_session_unique_remplacement_idempotent_et_doublure_preservee():
    c = SimpleNamespace(session=requests.Session())
    poli.rendre_poli(c)
    session = c.session
    assert isinstance(session, poli.SessionRadarPolie)
    assert poli.rendre_poli(c).session is session
    faux = SimpleNamespace(session=Mock())
    assert poli.rendre_poli(faux).session is faux.session
