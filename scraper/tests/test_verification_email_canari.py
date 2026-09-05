"""Tests de non-regression pour verification_email_canari.py -- canari de
livraison email de bout en bout (ajoute le 04/09/2026 suite au bug Resend
sandbox : appel API "reussi" mais livraison silencieusement restreinte au
seul proprietaire du compte). Reutilise notifications_saas._envoyer_email
(pas de reimplementation), donc mocke ce point d'entree plutot que
requests.post directement -- verifie que le canari appelle le VRAI chemin
de code de production."""

from unittest.mock import patch

from verification_email_canari import main, verifier_livraison

_ENV_BASE = {
    "SENDGRID_API_KEY": "SG.xxx",
    "SENDGRID_FROM_EMAIL": "noreply@pokedeals.app",
    "EMAIL_CANARI_DESTINATAIRE": "canari@example.com",
    "TELEGRAM_BOT_TOKEN": "tg-tok",
    "SUPABASE_URL": "https://x.supabase.co",
    "SUPABASE_SERVICE_ROLE_KEY": "cle",
}


# ------------------- verifier_livraison -------------------

def test_verifier_livraison_secrets_absents_retourne_none():
    assert verifier_livraison("", "noreply@pokedeals.app", "canari@example.com") is None
    assert verifier_livraison("SG.xxx", "", "canari@example.com") is None
    assert verifier_livraison("SG.xxx", "noreply@pokedeals.app", "") is None


def test_verifier_livraison_appelle_envoyer_email_de_notifications_saas():
    with patch("verification_email_canari._envoyer_email", return_value=True) as send_mock:
        result = verifier_livraison("SG.xxx", "noreply@pokedeals.app", "canari@example.com")
    assert result is True
    args, kwargs = send_mock.call_args
    assert args[0] == "SG.xxx"
    assert args[1] == "noreply@pokedeals.app"
    assert args[2] == "canari@example.com"
    # Ajoute le 05/09/2026 (webhook SendGrid) : permet de distinguer un
    # evenement de livraison du canari de ceux des vrais utilisateurs.
    assert kwargs["custom_args"] == {"produit": "pokedeals", "type_notification": "canari"}


def test_verifier_livraison_echec_est_propage():
    with patch("verification_email_canari._envoyer_email", return_value=False):
        result = verifier_livraison("SG.xxx", "noreply@pokedeals.app", "canari@example.com")
    assert result is False


# ------------------- main (orchestration + anti-spam) -------------------

def test_main_sans_secrets_ne_declenche_aucun_appel():
    with patch.dict("os.environ", {}, clear=True), \
         patch("verification_email_canari._envoyer_email") as send_mock, \
         patch("verification_email_canari.envoyer_telegram") as tg_mock:
        main()
    send_mock.assert_not_called()
    tg_mock.assert_not_called()


def test_main_echec_alerte_et_persiste_letat():
    with patch.dict("os.environ", _ENV_BASE, clear=True), \
         patch("verification_email_canari.charger_memoire_supabase", return_value={}), \
         patch("verification_email_canari._envoyer_email", return_value=False), \
         patch("verification_email_canari.envoyer_telegram", return_value=True) as tg_mock, \
         patch("verification_email_canari.sauvegarder_memoire_supabase", return_value=True) as save_mock:
        main()
    tg_mock.assert_called_once()
    assert "n'a PAS pu être envoyé" in tg_mock.call_args[0][0]
    save_mock.assert_called_once()
    assert save_mock.call_args[0][0]["echec"] is True


def test_main_echec_deja_alerte_ne_re_notifie_pas():
    with patch.dict("os.environ", _ENV_BASE, clear=True), \
         patch("verification_email_canari.charger_memoire_supabase", return_value={"echec": True}), \
         patch("verification_email_canari._envoyer_email", return_value=False), \
         patch("verification_email_canari.envoyer_telegram") as tg_mock, \
         patch("verification_email_canari.sauvegarder_memoire_supabase") as save_mock:
        main()
    tg_mock.assert_not_called()
    save_mock.assert_not_called()


def test_main_retour_au_vert_envoie_resolution_et_reinitialise_letat():
    with patch.dict("os.environ", _ENV_BASE, clear=True), \
         patch("verification_email_canari.charger_memoire_supabase", return_value={"echec": True}), \
         patch("verification_email_canari._envoyer_email", return_value=True), \
         patch("verification_email_canari.envoyer_telegram", return_value=True) as tg_mock, \
         patch("verification_email_canari.sauvegarder_memoire_supabase", return_value=True) as save_mock:
        main()
    tg_mock.assert_called_once()
    assert "revenue au vert" in tg_mock.call_args[0][0]
    assert save_mock.call_args[0][0]["echec"] is False


def test_main_succes_sans_alerte_prealable_ne_declenche_rien():
    with patch.dict("os.environ", _ENV_BASE, clear=True), \
         patch("verification_email_canari.charger_memoire_supabase", return_value={}), \
         patch("verification_email_canari._envoyer_email", return_value=True), \
         patch("verification_email_canari.envoyer_telegram") as tg_mock, \
         patch("verification_email_canari.sauvegarder_memoire_supabase") as save_mock:
        main()
    tg_mock.assert_not_called()
    save_mock.assert_not_called()


def test_main_supabase_injoignable_continue_avec_etat_vide():
    with patch.dict("os.environ", _ENV_BASE, clear=True), \
         patch("verification_email_canari.charger_memoire_supabase", return_value=None), \
         patch("verification_email_canari._envoyer_email", return_value=False), \
         patch("verification_email_canari.envoyer_telegram", return_value=True) as tg_mock, \
         patch("verification_email_canari.sauvegarder_memoire_supabase", return_value=True):
        main()
    tg_mock.assert_called_once()
