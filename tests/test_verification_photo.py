"""Tests de non-regression pour verification_photo.py -- systeme
OPTIONNEL et NON BLOQUANT (cf. module docstring). Verifie surtout que
toute situation ambigue/en echec renvoie (None, raison), jamais une
fausse confirmation ni un faux rejet."""

from unittest.mock import Mock, patch

import requests

from verification_photo import _interpreter_reponse, verifier_photo_annonce


def test_pas_de_cle_api_ne_declenche_aucun_appel_reseau():
    with patch("verification_photo.requests.get") as get_mock, \
         patch("verification_photo.requests.post") as post_mock:
        verdict, raison = verifier_photo_annonce("https://x/photo.jpg", "Dracaufeu ex 199/165", "fr", "")
    assert verdict is None
    assert "ANTHROPIC_API_KEY" in raison
    get_mock.assert_not_called()
    post_mock.assert_not_called()


def test_pas_dimage_ne_declenche_aucun_appel_reseau():
    with patch("verification_photo.requests.get") as get_mock, \
         patch("verification_photo.requests.post") as post_mock:
        verdict, raison = verifier_photo_annonce("", "Dracaufeu ex 199/165", "fr", "sk-ant-xxx")
    assert verdict is None
    get_mock.assert_not_called()
    post_mock.assert_not_called()


def _reponse_image_ok():
    r = Mock()
    r.status_code = 200
    r.content = b"donnees-image"
    r.headers = {"Content-Type": "image/jpeg"}
    r.raise_for_status = Mock()
    return r


def _reponse_api(texte: str):
    r = Mock()
    r.status_code = 200
    r.raise_for_status = Mock()
    r.json.return_value = {"content": [{"type": "text", "text": texte}]}
    return r


def test_verdict_coherent_bien_parse():
    with patch("verification_photo.requests.get", return_value=_reponse_image_ok()), \
         patch("verification_photo.requests.post", return_value=_reponse_api("COHERENT")):
        verdict, raison = verifier_photo_annonce("https://x/photo.jpg", "Dracaufeu ex 199/165", "fr", "sk-ant-xxx")
    assert verdict == "coherent"
    assert raison == ""


def test_verdict_incoherent_bien_parse_avec_raison():
    with patch("verification_photo.requests.get", return_value=_reponse_image_ok()), \
         patch("verification_photo.requests.post", return_value=_reponse_api("INCOHERENT: carte coréenne visible sur la photo")):
        verdict, raison = verifier_photo_annonce("https://x/photo.jpg", "Dracaufeu ex 199/165", "fr", "sk-ant-xxx")
    assert verdict == "incoherent"
    assert "coréenne" in raison


def test_verdict_incertain_traite_comme_non_concluant():
    with patch("verification_photo.requests.get", return_value=_reponse_image_ok()), \
         patch("verification_photo.requests.post", return_value=_reponse_api("INCERTAIN: photo floue")):
        verdict, raison = verifier_photo_annonce("https://x/photo.jpg", "Dracaufeu ex 199/165", "fr", "sk-ant-xxx")
    assert verdict is None
    assert "floue" in raison


def test_reponse_hors_format_traitee_comme_non_concluante():
    with patch("verification_photo.requests.get", return_value=_reponse_image_ok()), \
         patch("verification_photo.requests.post", return_value=_reponse_api("Je pense que oui, probablement.")):
        verdict, raison = verifier_photo_annonce("https://x/photo.jpg", "Dracaufeu ex 199/165", "fr", "sk-ant-xxx")
    assert verdict is None


def test_image_inaccessible_ne_plante_pas():
    with patch("verification_photo.requests.get", side_effect=requests.exceptions.ConnectionError("coupé")):
        verdict, raison = verifier_photo_annonce("https://x/photo.jpg", "Dracaufeu ex 199/165", "fr", "sk-ant-xxx")
    assert verdict is None
    assert "inaccessible" in raison


def test_erreur_api_ne_plante_pas():
    with patch("verification_photo.requests.get", return_value=_reponse_image_ok()), \
         patch("verification_photo.requests.post", side_effect=requests.exceptions.Timeout("trop long")):
        verdict, raison = verifier_photo_annonce("https://x/photo.jpg", "Dracaufeu ex 199/165", "fr", "sk-ant-xxx")
    assert verdict is None
    assert "erreur" in raison.lower()


def test_interpreter_reponse_directement():
    assert _interpreter_reponse("COHERENT") == ("coherent", "")
    assert _interpreter_reponse("coherent") == ("coherent", "")  # insensible a la casse
    assert _interpreter_reponse("INCOHERENT: mauvais pokemon")[0] == "incoherent"
    assert _interpreter_reponse("")[0] is None
    assert _interpreter_reponse(None)[0] is None
