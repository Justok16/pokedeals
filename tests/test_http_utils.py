"""Tests de non-regression pour http_utils.py (extrait de main.py le
17/08/2026) -- retry sur 429 et propagation d'erreur reseau apres echec
de toutes les tentatives."""

from unittest.mock import patch

import requests

import http_utils


def test_user_agent_pioche_dans_la_liste():
    for _ in range(20):
        assert http_utils.user_agent() in http_utils.USER_AGENTS


def test_requete_avec_retry_renvoie_directement_si_succes():
    reponse_ok = type("R", (), {"status_code": 200})()
    appel = lambda url, **kw: reponse_ok  # noqa: E731
    r = http_utils.requete_avec_retry(appel, "https://x", tentatives=3)
    assert r is reponse_ok


def test_requete_avec_retry_reessaie_sur_429_puis_reussit():
    reponses = [
        type("R", (), {"status_code": 429})(),
        type("R", (), {"status_code": 200})(),
    ]
    appel = lambda url, **kw: reponses.pop(0)  # noqa: E731
    with patch("http_utils.time.sleep"):
        r = http_utils.requete_avec_retry(appel, "https://x", tentatives=3)
    assert r.status_code == 200


def test_requete_avec_retry_propage_lerreur_apres_toutes_les_tentatives():
    def appel(url, **kw):
        raise requests.exceptions.ConnectionError("panne")
    with patch("http_utils.time.sleep"):
        try:
            http_utils.requete_avec_retry(appel, "https://x", tentatives=2)
            assert False, "aurait du lever"
        except requests.exceptions.ConnectionError:
            pass
