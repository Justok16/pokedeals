"""Tests de non-regression pour notifications_historique.py (extrait de
main.py le 16/08/2026) : formatage des messages Telegram et branchement de
la verification photo (verification_photo.py) -- ne s'active que lorsqu'une
cle API et une image sont disponibles, jamais bloquant."""

from unittest.mock import patch

from notifications_historique import _texte_telegram, envoyer_telegram


def _deal(**kwargs) -> dict:
    base = dict(
        titre="Dracaufeu ex 199/165", plateforme="eBay", prix=50.0, port=3.0,
        total=53.0, cote=100.0, decote_pct=47.0, prix_revente_conseille=120.0,
        profit_net_estime=40.0, confiance=0, url="https://ebay.fr/x",
    )
    base.update(kwargs)
    return base


def test_texte_telegram_sans_verification_est_inchange():
    texte = _texte_telegram(_deal())
    assert "Vérification IA" not in texte


def test_texte_telegram_verdict_coherent():
    texte = _texte_telegram(_deal(), ("coherent", ""))
    assert "cohérente" in texte


def test_texte_telegram_verdict_incoherent():
    texte = _texte_telegram(_deal(), ("incoherent", "carte japonaise sur la photo"))
    assert "INCOHÉRENTE" in texte
    assert "carte japonaise sur la photo" in texte


def test_texte_telegram_verdict_non_concluant_naffiche_rien():
    texte = _texte_telegram(_deal(), (None, "image inaccessible"))
    assert "Vérification IA" not in texte


def test_envoyer_telegram_sans_cle_api_nappelle_jamais_la_verification():
    deal = _deal(image_url="https://ebay.fr/photo.jpg")
    with patch("notifications_historique.verifier_photo_annonce") as verif_mock, \
         patch("notifications_historique.requests.post") as post_mock:
        post_mock.return_value.status_code = 200
        envoyer_telegram([deal], {"chat_id": "123"}, "token-telegram", anthropic_api_key="")
    verif_mock.assert_not_called()


def test_envoyer_telegram_sans_image_nappelle_jamais_la_verification():
    deal = _deal()  # pas d'image_url
    with patch("notifications_historique.verifier_photo_annonce") as verif_mock, \
         patch("notifications_historique.requests.post") as post_mock:
        post_mock.return_value.status_code = 200
        envoyer_telegram([deal], {"chat_id": "123"}, "token-telegram", anthropic_api_key="sk-ant-xxx")
    verif_mock.assert_not_called()


def test_envoyer_telegram_avec_cle_et_image_appelle_la_verification():
    deal = _deal(image_url="https://ebay.fr/photo.jpg", carte="Dracaufeu ex 199/165", langue="fr")
    with patch("notifications_historique.verifier_photo_annonce", return_value=("coherent", "")) as verif_mock, \
         patch("notifications_historique.requests.post") as post_mock:
        post_mock.return_value.status_code = 200
        envoyer_telegram([deal], {"chat_id": "123"}, "token-telegram", anthropic_api_key="sk-ant-xxx")
    verif_mock.assert_called_once_with("https://ebay.fr/photo.jpg", "Dracaufeu ex 199/165", "fr", "sk-ant-xxx")
    # Le texte envoye a Telegram doit refleter le verdict de la verification.
    texte_envoye = post_mock.call_args.kwargs["json"]["text"]
    assert "cohérente" in texte_envoye
