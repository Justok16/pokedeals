"""Tests de non-regression pour verification_photo.py -- systeme
OPTIONNEL et NON BLOQUANT (cf. module docstring). Verifie surtout que
toute situation ambigue/en echec renvoie (None, raison), jamais une
fausse confirmation ni un faux rejet.

_url_photo_autorisee() (garde-fou SSRF, ajoute le 17/08/2026 suite a un
audit externe -- cf. SESSION_NOTES.md) fait une vraie resolution DNS :
les URLs de test ci-dessous ("https://x/photo.jpg") ne sont pas des
hotes reels, donc la plupart des tests patchent _url_photo_autorisee
pour se concentrer sur le comportement qu'ils testent reellement (pas
la validation d'URL, testee separement plus bas)."""

import socket
from unittest.mock import Mock, patch

import pytest
import requests

from verification_photo import _interpreter_reponse, _url_photo_autorisee, verifier_photo_annonce


@pytest.fixture(autouse=True)
def _url_photo_toujours_autorisee(request):
    """La plupart des tests de ce fichier ne testent pas la validation
    d'URL elle-meme (couverte par test_url_photo_autorisee_*) -- on evite
    donc une vraie resolution DNS sur des hotes de test factices."""
    if "sans_autopatch_url" in request.keywords:
        yield
        return
    with patch("verification_photo._url_photo_autorisee", return_value=True):
        yield


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


def _reponse_image_ok(contenu: bytes = b"donnees-image"):
    r = Mock()
    r.status_code = 200
    r.headers = {"Content-Type": "image/jpeg"}
    r.raise_for_status = Mock()
    r.iter_content = Mock(return_value=[contenu])
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


# ------------------- _url_photo_autorisee (garde-fou SSRF, V51) -------------------
# Ces tests desactivent l'autopatch de la fixture ci-dessus pour tester la
# vraie logique de validation d'URL.

@pytest.mark.sans_autopatch_url
def test_url_photo_refuse_un_schema_non_http():
    assert _url_photo_autorisee("file:///etc/passwd") is False
    assert _url_photo_autorisee("ftp://exemple.fr/photo.jpg") is False


@pytest.mark.sans_autopatch_url
def test_url_photo_refuse_une_ip_privee_ou_loopback(monkeypatch):
    def fausse_resolution(hote, port):
        adresses = {
            "169.254.169.254": "169.254.169.254",  # metadonnees cloud
            "localhost": "127.0.0.1",
            "interne.local": "10.0.0.5",
        }
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (adresses[hote], 0))]
    monkeypatch.setattr(socket, "getaddrinfo", fausse_resolution)
    assert _url_photo_autorisee("http://169.254.169.254/latest/meta-data/") is False
    assert _url_photo_autorisee("http://localhost/photo.jpg") is False
    assert _url_photo_autorisee("http://interne.local/photo.jpg") is False


@pytest.mark.sans_autopatch_url
def test_url_photo_autorise_une_ip_publique(monkeypatch):
    def fausse_resolution(hote, port):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 0))]
    monkeypatch.setattr(socket, "getaddrinfo", fausse_resolution)
    assert _url_photo_autorisee("https://exemple-boutique.fr/photo.jpg") is True


@pytest.mark.sans_autopatch_url
def test_url_photo_refuse_hote_introuvable(monkeypatch):
    def resolution_echouee(hote, port):
        raise socket.gaierror("hote introuvable")
    monkeypatch.setattr(socket, "getaddrinfo", resolution_echouee)
    assert _url_photo_autorisee("https://domaine-inexistant-xyz.invalid/photo.jpg") is False


@pytest.mark.sans_autopatch_url
def test_verifier_photo_annonce_bloque_avant_tout_appel_reseau_si_url_privee(monkeypatch):
    def fausse_resolution(hote, port):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 0))]
    monkeypatch.setattr(socket, "getaddrinfo", fausse_resolution)
    with patch("verification_photo.requests.get") as get_mock, \
         patch("verification_photo.requests.post") as post_mock:
        verdict, raison = verifier_photo_annonce(
            "http://localhost/photo.jpg", "Dracaufeu ex 199/165", "fr", "sk-ant-xxx")
    assert verdict is None
    get_mock.assert_not_called()
    post_mock.assert_not_called()


def test_telecharger_image_abandonne_si_trop_volumineuse():
    from verification_photo import _telecharger_image, TAILLE_IMAGE_MAX
    gros_morceau = b"x" * (TAILLE_IMAGE_MAX + 1)
    reponse = _reponse_image_ok()
    reponse.iter_content = Mock(return_value=[gros_morceau])
    with patch("verification_photo.requests.get", return_value=reponse):
        assert _telecharger_image("https://x/photo.jpg") is None
