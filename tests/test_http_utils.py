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


def test_requete_avec_retry_reessaie_sur_503_puis_reussit():
    # Audit externe du 17/08/2026 : un 5xx (erreur serveur temporaire,
    # frequent sur eBay/Vinted/Cardtrader) doit aussi declencher un retry,
    # pas seulement le 429.
    reponses = [
        type("R", (), {"status_code": 503})(),
        type("R", (), {"status_code": 200})(),
    ]
    appel = lambda url, **kw: reponses.pop(0)  # noqa: E731
    with patch("http_utils.time.sleep"):
        r = http_utils.requete_avec_retry(appel, "https://x", tentatives=3)
    assert r.status_code == 200


def test_requete_avec_retry_reessaie_sur_408_puis_reussit():
    reponses = [
        type("R", (), {"status_code": 408})(),
        type("R", (), {"status_code": 200})(),
    ]
    appel = lambda url, **kw: reponses.pop(0)  # noqa: E731
    with patch("http_utils.time.sleep"):
        r = http_utils.requete_avec_retry(appel, "https://x", tentatives=3)
    assert r.status_code == 200


def test_requete_avec_retry_ne_reessaie_pas_sur_une_vraie_erreur_client():
    # Un 404/403 (hors 408/429) ne se corrige pas en reessayant -- doit
    # etre retourne immediatement, sans consommer de tentative pour rien.
    appels = []

    def appel(url, **kw):
        appels.append(1)
        return type("R", (), {"status_code": 404})()

    r = http_utils.requete_avec_retry(appel, "https://x", tentatives=3)
    assert r.status_code == 404
    assert len(appels) == 1


def test_requete_avec_retry_propage_lerreur_apres_toutes_les_tentatives():
    def appel(url, **kw):
        raise requests.exceptions.ConnectionError("panne")
    with patch("http_utils.time.sleep"):
        try:
            http_utils.requete_avec_retry(appel, "https://x", tentatives=2)
            assert False, "aurait du lever"
        except requests.exceptions.ConnectionError:
            pass
