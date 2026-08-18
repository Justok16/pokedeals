"""Tests de non-regression pour notifications_historique.py (extrait de
main.py le 16/08/2026) : formatage des messages Telegram et branchement de
la verification photo (verification_photo.py) -- ne s'active que lorsqu'une
cle API et une image sont disponibles, jamais bloquant."""

from unittest.mock import patch

from notifications_historique import _echapper_url_html, _texte_telegram, envoyer_telegram


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


def test_echapper_url_html_echappe_le_guillemet_double():
    # V59 (audit du 18/08/2026) : cette fonction n'est utilisee QUE dans un
    # attribut href="..." -- un guillemet non echappe fermerait
    # prematurement l'attribut et casserait le HTML du message (rejet
    # Telegram, erreur 400). Copie locale de telegram_utils.echapper_url_html
    # (deliberement dupliquee, cf. docstring du module).
    resultat = _echapper_url_html('https://ex.fr/p?x="onmouseover=alert(1)')
    assert '"' not in resultat
    assert "&quot;" in resultat


def test_texte_telegram_url_avec_guillemet_produit_un_href_valide():
    texte = _texte_telegram(_deal(url='https://ebay.fr/x?y="><b>'))
    assert texte.count('href="') == 1
    # Le href doit rester correctement delimite par exactement 2 guillemets.
    debut = texte.index('href="')
    fin = texte.index('">', debut)
    assert '"' not in texte[debut + len('href="'):fin]


def test_texte_telegram_verdict_incoherent():
    # V51 : le verdict n'est plus affiché en majuscules comme un fait
    # confirmé (cf. faux positif reel Mega-Dracaufeu X/Y, 17/08/2026) --
    # le message hedge desormais explicitement ("peut se tromper").
    texte = _texte_telegram(_deal(), ("incoherent", "carte japonaise sur la photo"))
    assert "incohérente" in texte
    assert "peut se tromper" in texte
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


def test_envoyer_telegram_verdict_incoherent_nempeche_jamais_lenvoi():
    # Cas reel (17/08/2026, cf. SESSION_NOTES.md V51) : un faux positif de
    # verification photo NE DOIT JAMAIS empecher l'envoi d'un vrai deal --
    # le systeme est concu comme purement informatif, jamais bloquant.
    deal = _deal(image_url="https://ebay.fr/photo.jpg", carte="Dracaufeu ex 199/165", langue="fr")
    with patch("notifications_historique.verifier_photo_annonce",
               return_value=("incoherent", "carte differente sur la photo")), \
         patch("notifications_historique.requests.post") as post_mock:
        post_mock.return_value.status_code = 200
        resultat = envoyer_telegram([deal], {"chat_id": "123"}, "token-telegram", anthropic_api_key="sk-ant-xxx")
    post_mock.assert_called_once()
    assert resultat is True
