"""Tests de non-regression pour les coupe-circuits Vinted/Leboncoin
(main.py/connecteur_leboncoin.py, 03/09/2026, audit) -- meme principe que
le coupe-circuit 429 eBay (V61, tests/test_circuit_ebay.py) : apres N
echecs REELS consecutifs (pas un 0 resultat legitime, ni un blocage
403/429 Leboncoin deja documente comme un comportement anti-bot ROUTINE),
on arrete d'appeler la plateforme pour le reste du cycle."""

from unittest.mock import Mock, patch

import requests

import connecteur_leboncoin as lbc
import main


def setup_function():
    # Chaque test repart d'un etat propre -- _stats_fiabilite/_circuit_vinted/
    # _circuit_leboncoin sont des dicts module-level partages (meme risque
    # que _ebay_circuit, cf. tests/test_circuit_ebay.py).
    main._reinitialiser_stats_fiabilite()
    main._reinitialiser_circuits_vinted_leboncoin()


def _session_ok():
    s = Mock()
    return s


def _reponse_vinted_ok(items=None):
    r = Mock()
    r.status_code = 200
    r.raise_for_status.side_effect = None
    r.json.return_value = {"items": items or []}
    return r


# ------------------- Vinted -------------------

def test_vinted_moins_de_3_echecs_ne_declenche_rien(monkeypatch):
    monkeypatch.setattr(main, "_get_vinted_session", _session_ok)
    with patch("main.requete_avec_retry", side_effect=requests.exceptions.ConnectionError("panne")):
        main.vinted_rechercher("Dracaufeu ex 199/165", "fr")
        main.vinted_rechercher("Pikachu 173/165", "fr")
    assert main._circuit_vinted["abandonne"] is False


def test_vinted_3_echecs_consecutifs_declenche_le_coupe_circuit(monkeypatch):
    monkeypatch.setattr(main, "_get_vinted_session", _session_ok)
    with patch("main.requete_avec_retry", side_effect=requests.exceptions.ConnectionError("panne")):
        for nom in ("Dracaufeu ex 199/165", "Pikachu 173/165", "Mew 193/165"):
            main.vinted_rechercher(nom, "fr")
    assert main._circuit_vinted["abandonne"] is True


def test_vinted_session_indisponible_compte_aussi_comme_un_echec(monkeypatch):
    # _get_vinted_session() peut renvoyer None (pas d'exception levee) --
    # doit alimenter le coupe-circuit exactement comme une exception reseau.
    monkeypatch.setattr(main, "_get_vinted_session", lambda: None)
    for nom in ("Dracaufeu ex 199/165", "Pikachu 173/165", "Mew 193/165"):
        main.vinted_rechercher(nom, "fr")
    assert main._circuit_vinted["abandonne"] is True


def test_vinted_un_succes_entre_deux_echecs_remet_le_compteur_a_zero(monkeypatch):
    monkeypatch.setattr(main, "_get_vinted_session", _session_ok)
    sequence = [
        requests.exceptions.ConnectionError("panne"),
        _reponse_vinted_ok(),
        requests.exceptions.ConnectionError("panne"),
        requests.exceptions.ConnectionError("panne"),
    ]
    with patch("main.requete_avec_retry", side_effect=sequence):
        for nom in ("Dracaufeu ex 199/165", "Pikachu 173/165", "Mew 193/165", "Evoli 167/131"):
            main.vinted_rechercher(nom, "fr")
    # 4 appels : echec, OK (reset), echec, echec -- jamais 3 D'AFFILEE
    assert main._circuit_vinted["abandonne"] is False


def test_vinted_une_fois_declenche_ne_fait_plus_aucun_appel_reseau():
    main._circuit_vinted["abandonne"] = True
    with patch("main.requete_avec_retry") as appel_mock:
        resultat = main.vinted_rechercher("Dracaufeu ex 199/165", "fr")
    assert resultat == []
    appel_mock.assert_not_called()
    # Ne doit meme pas incrementer _stats_fiabilite (aucune tentative reelle).
    assert main._stats_fiabilite["vinted_appels"] == 0


def test_vinted_recherche_reussie_renvoie_bien_les_annonces(monkeypatch):
    monkeypatch.setattr(main, "_get_vinted_session", _session_ok)
    items = [{"id": 1, "title": "Dracaufeu 199/165", "price": {"amount": "10.0"}, "url": "https://vinted.fr/x"}]
    with patch("main.requete_avec_retry", return_value=_reponse_vinted_ok(items)):
        resultat = main.vinted_rechercher("Dracaufeu ex 199/165", "fr")
    assert len(resultat) == 1
    assert main._circuit_vinted["abandonne"] is False


# ------------------- Leboncoin -------------------

def _reponse_lbc_ok(ads=None):
    r = Mock()
    r.status_code = 200
    r.raise_for_status.side_effect = None
    r.json.return_value = {"ads": ads or []}
    return r


def _reponse_lbc_bloquee(code):
    r = Mock()
    r.status_code = code
    return r


def test_lbc_moins_de_3_echecs_ne_declenche_rien():
    with patch.object(lbc, "requete_avec_retry", side_effect=ConnectionError("panne")):
        lbc.lbc_rechercher("Dracaufeu ex 199/165", "fr")
        lbc.lbc_rechercher("Pikachu 173/165", "fr")
    assert lbc._circuit_leboncoin["abandonne"] is False


def test_lbc_3_echecs_consecutifs_declenche_le_coupe_circuit():
    with patch.object(lbc, "requete_avec_retry", side_effect=ConnectionError("panne")):
        for nom in ("Dracaufeu ex 199/165", "Pikachu 173/165", "Mew 193/165"):
            lbc.lbc_rechercher(nom, "fr")
    assert lbc._circuit_leboncoin["abandonne"] is True


def test_lbc_blocage_403_429_ne_declenche_jamais_le_coupe_circuit():
    # Blocage anti-bot ROUTINE (deja documente) -- ne doit JAMAIS compter
    # comme un echec du coupe-circuit, sous peine de le declencher a
    # chaque cycle des que Leboncoin bloque normalement (comportement
    # attendu, pas une panne).
    with patch.object(lbc, "requete_avec_retry", return_value=_reponse_lbc_bloquee(403)):
        for _ in range(10):
            lbc.lbc_rechercher("Dracaufeu ex 199/165", "fr")
    assert lbc._circuit_leboncoin["abandonne"] is False
    with patch.object(lbc, "requete_avec_retry", return_value=_reponse_lbc_bloquee(429)):
        for _ in range(10):
            lbc.lbc_rechercher("Dracaufeu ex 199/165", "fr")
    assert lbc._circuit_leboncoin["abandonne"] is False


def test_lbc_un_succes_entre_deux_echecs_remet_le_compteur_a_zero():
    sequence = [
        ConnectionError("panne"),
        _reponse_lbc_ok(),
        ConnectionError("panne"),
        ConnectionError("panne"),
    ]
    with patch.object(lbc, "requete_avec_retry", side_effect=sequence):
        for nom in ("Dracaufeu ex 199/165", "Pikachu 173/165", "Mew 193/165", "Evoli 167/131"):
            lbc.lbc_rechercher(nom, "fr")
    assert lbc._circuit_leboncoin["abandonne"] is False


def test_lbc_une_fois_declenche_ne_fait_plus_aucun_appel_reseau():
    lbc._circuit_leboncoin["abandonne"] = True
    with patch.object(lbc, "requete_avec_retry") as appel_mock:
        resultat = lbc.lbc_rechercher("Dracaufeu ex 199/165", "fr")
    assert resultat == []
    appel_mock.assert_not_called()
    assert lbc._stats_fiabilite["leboncoin_appels"] == 0


def test_lbc_recherche_reussie_renvoie_bien_les_annonces():
    ads = [{"list_id": "1", "subject": "Dracaufeu 199/165", "price": [10.0], "url": "https://leboncoin.fr/x"}]
    with patch.object(lbc, "requete_avec_retry", return_value=_reponse_lbc_ok(ads)):
        resultat = lbc.lbc_rechercher("Dracaufeu ex 199/165", "fr")
    assert len(resultat) == 1
    assert lbc._circuit_leboncoin["abandonne"] is False


# ------------------- reinitialisation -------------------

def test_reinitialiser_circuits_vinted_leboncoin_remet_tout_a_zero():
    main._circuit_vinted["echecs_consecutifs"] = 5
    main._circuit_vinted["abandonne"] = True
    lbc._circuit_leboncoin["echecs_consecutifs"] = 5
    lbc._circuit_leboncoin["abandonne"] = True
    main._reinitialiser_circuits_vinted_leboncoin()
    assert main._circuit_vinted == {"echecs_consecutifs": 0, "abandonne": False}
    assert lbc._circuit_leboncoin == {"echecs_consecutifs": 0, "abandonne": False}


# ------------------- verifier_circuits_vinted_leboncoin (alerte Telegram) -------------------

def test_verifier_circuits_silencieux_si_rien_de_declenche():
    assert main.verifier_circuits_vinted_leboncoin({}) == []


def test_verifier_circuits_alerte_si_vinted_declenche():
    main._circuit_vinted["abandonne"] = True
    main._circuit_vinted["echecs_consecutifs"] = 3
    alertes = main.verifier_circuits_vinted_leboncoin({})
    assert len(alertes) == 1
    assert "Vinted" in alertes[0]


def test_verifier_circuits_alerte_si_leboncoin_declenche():
    lbc._circuit_leboncoin["abandonne"] = True
    lbc._circuit_leboncoin["echecs_consecutifs"] = 3
    alertes = main.verifier_circuits_vinted_leboncoin({})
    assert len(alertes) == 1
    assert "Leboncoin" in alertes[0]


def test_verifier_circuits_alerte_double_si_les_deux_sont_declenches():
    main._circuit_vinted["abandonne"] = True
    lbc._circuit_leboncoin["abandonne"] = True
    alertes = main.verifier_circuits_vinted_leboncoin({})
    assert len(alertes) == 2


def test_verifier_circuits_respecte_lanti_spam():
    main._circuit_vinted["abandonne"] = True
    vues = {}
    premiere = main.verifier_circuits_vinted_leboncoin(vues)
    assert len(premiere) == 1
    seconde = main.verifier_circuits_vinted_leboncoin(vues)
    assert seconde == []
