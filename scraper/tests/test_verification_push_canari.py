"""Tests de non-regression pour verification_push_canari.py -- canari de
livraison push symetrique au canari email (verification_email_canari.py).
Reutilise notifications_saas._envoyer_push/_lister_abonnements_push (pas de
reimplementation), donc mocke ces points d'entree plutot que requests/
pywebpush directement."""

from unittest.mock import patch

from verification_push_canari import main, verifier_livraison

_ENV_BASE = {
    "SUPABASE_URL": "https://x.supabase.co",
    "SUPABASE_SERVICE_ROLE_KEY": "cle",
    "VAPID_PRIVATE_KEY": "priv",
    "VAPID_CLAIM_EMAIL": "a@b.com",
    "PUSH_CANARI_USER_ID": "u1",
    "TELEGRAM_BOT_TOKEN": "tg-tok",
}

_ABONNEMENT = [{"user_id": "u1", "endpoint": "e1", "p256dh": "p", "auth": "a"}]


# ------------------- verifier_livraison -------------------

def test_verifier_livraison_secrets_absents_retourne_none():
    assert verifier_livraison("", "cle", "priv", "a@b.com", "u1") is None
    assert verifier_livraison("https://x.supabase.co", "", "priv", "a@b.com", "u1") is None
    assert verifier_livraison("https://x.supabase.co", "cle", "", "a@b.com", "u1") is None
    assert verifier_livraison("https://x.supabase.co", "cle", "priv", "", "u1") is None
    assert verifier_livraison("https://x.supabase.co", "cle", "priv", "a@b.com", "") is None


def test_verifier_livraison_lecture_abonnements_ratee_retourne_none():
    # Distinct d'un echec de livraison avere -- une panne reseau ce cycle ne
    # doit pas etre traitee comme "le push est casse".
    with patch("verification_push_canari._lister_abonnements_push", return_value=None):
        resultat = verifier_livraison("https://x.supabase.co", "cle", "priv", "a@b.com", "u1")
    assert resultat is None


def test_verifier_livraison_aucun_abonnement_canari_retourne_false():
    # Piege documente dans le module : _envoyer_push() renvoie True aussi
    # bien pour "livre" que pour "abonnement expire, purge" -- sans ce
    # controle explicite, un canari desabonne se traduirait a tort par un
    # succes permanent (aucun test reel n'est plus effectue).
    with patch("verification_push_canari._lister_abonnements_push", return_value=[]), \
         patch("verification_push_canari._envoyer_push") as push_mock:
        resultat = verifier_livraison("https://x.supabase.co", "cle", "priv", "a@b.com", "u1")
    assert resultat is False
    push_mock.assert_not_called()


def test_verifier_livraison_appelle_envoyer_push_de_notifications_saas():
    with patch("verification_push_canari._lister_abonnements_push", return_value=_ABONNEMENT), \
         patch("verification_push_canari._envoyer_push", return_value=True) as push_mock:
        resultat = verifier_livraison("https://x.supabase.co", "cle", "priv", "a@b.com", "u1")
    assert resultat is True
    args, _ = push_mock.call_args
    assert args[0] == "https://x.supabase.co"
    assert args[1] == "cle"
    assert args[2] == "priv"
    assert args[3] == "a@b.com"
    assert args[4] == _ABONNEMENT


def test_verifier_livraison_echec_envoi_est_propage():
    with patch("verification_push_canari._lister_abonnements_push", return_value=_ABONNEMENT), \
         patch("verification_push_canari._envoyer_push", return_value=False):
        resultat = verifier_livraison("https://x.supabase.co", "cle", "priv", "a@b.com", "u1")
    assert resultat is False


# ------------------- main (orchestration + anti-spam) -------------------

def test_main_sans_secrets_ne_declenche_aucun_appel():
    with patch.dict("os.environ", {}, clear=True), \
         patch("verification_push_canari._envoyer_push") as push_mock, \
         patch("verification_push_canari.envoyer_telegram") as tg_mock:
        main()
    push_mock.assert_not_called()
    tg_mock.assert_not_called()


def test_main_echec_alerte_et_persiste_letat():
    with patch.dict("os.environ", _ENV_BASE, clear=True), \
         patch("verification_push_canari.charger_memoire_supabase", return_value={}), \
         patch("verification_push_canari._lister_abonnements_push", return_value=_ABONNEMENT), \
         patch("verification_push_canari._envoyer_push", return_value=False), \
         patch("verification_push_canari.envoyer_telegram", return_value=True) as tg_mock, \
         patch("verification_push_canari.sauvegarder_memoire_supabase", return_value=True) as save_mock:
        main()
    tg_mock.assert_called_once()
    assert "échec" in tg_mock.call_args[0][0].lower() or "échec" in tg_mock.call_args[0][0]
    save_mock.assert_called_once()
    assert save_mock.call_args[0][0]["echec"] is True


def test_main_echec_deja_alerte_ne_re_notifie_pas():
    with patch.dict("os.environ", _ENV_BASE, clear=True), \
         patch("verification_push_canari.charger_memoire_supabase", return_value={"echec": True}), \
         patch("verification_push_canari._lister_abonnements_push", return_value=_ABONNEMENT), \
         patch("verification_push_canari._envoyer_push", return_value=False), \
         patch("verification_push_canari.envoyer_telegram") as tg_mock, \
         patch("verification_push_canari.sauvegarder_memoire_supabase") as save_mock:
        main()
    tg_mock.assert_not_called()
    save_mock.assert_not_called()


def test_main_retour_au_vert_envoie_resolution_et_reinitialise_letat():
    with patch.dict("os.environ", _ENV_BASE, clear=True), \
         patch("verification_push_canari.charger_memoire_supabase", return_value={"echec": True}), \
         patch("verification_push_canari._lister_abonnements_push", return_value=_ABONNEMENT), \
         patch("verification_push_canari._envoyer_push", return_value=True), \
         patch("verification_push_canari.envoyer_telegram", return_value=True) as tg_mock, \
         patch("verification_push_canari.sauvegarder_memoire_supabase", return_value=True) as save_mock:
        main()
    tg_mock.assert_called_once()
    assert "revenue au vert" in tg_mock.call_args[0][0]
    assert save_mock.call_args[0][0]["echec"] is False


def test_main_succes_sans_alerte_prealable_ne_declenche_rien():
    with patch.dict("os.environ", _ENV_BASE, clear=True), \
         patch("verification_push_canari.charger_memoire_supabase", return_value={}), \
         patch("verification_push_canari._lister_abonnements_push", return_value=_ABONNEMENT), \
         patch("verification_push_canari._envoyer_push", return_value=True), \
         patch("verification_push_canari.envoyer_telegram") as tg_mock, \
         patch("verification_push_canari.sauvegarder_memoire_supabase") as save_mock:
        main()
    tg_mock.assert_not_called()
    save_mock.assert_not_called()


def test_main_abonnement_canari_disparu_declenche_une_alerte():
    # Scenario du piege documente : le canari se desabonne (0 abonnement),
    # doit etre traite comme un echec, pas un succes silencieux.
    with patch.dict("os.environ", _ENV_BASE, clear=True), \
         patch("verification_push_canari.charger_memoire_supabase", return_value={}), \
         patch("verification_push_canari._lister_abonnements_push", return_value=[]), \
         patch("verification_push_canari._envoyer_push") as push_mock, \
         patch("verification_push_canari.envoyer_telegram", return_value=True) as tg_mock, \
         patch("verification_push_canari.sauvegarder_memoire_supabase", return_value=True):
        main()
    push_mock.assert_not_called()
    tg_mock.assert_called_once()


def test_main_supabase_injoignable_continue_avec_etat_vide():
    with patch.dict("os.environ", _ENV_BASE, clear=True), \
         patch("verification_push_canari.charger_memoire_supabase", return_value=None), \
         patch("verification_push_canari._lister_abonnements_push", return_value=_ABONNEMENT), \
         patch("verification_push_canari._envoyer_push", return_value=False), \
         patch("verification_push_canari.envoyer_telegram", return_value=True) as tg_mock, \
         patch("verification_push_canari.sauvegarder_memoire_supabase", return_value=True):
        main()
    tg_mock.assert_called_once()


def test_main_lecture_abonnements_ratee_ne_declenche_rien():
    # None (panne reseau ponctuelle) ne doit ni alerter ni modifier l'etat.
    with patch.dict("os.environ", _ENV_BASE, clear=True), \
         patch("verification_push_canari.charger_memoire_supabase", return_value={}), \
         patch("verification_push_canari._lister_abonnements_push", return_value=None), \
         patch("verification_push_canari._envoyer_push") as push_mock, \
         patch("verification_push_canari.envoyer_telegram") as tg_mock, \
         patch("verification_push_canari.sauvegarder_memoire_supabase") as save_mock:
        main()
    push_mock.assert_not_called()
    tg_mock.assert_not_called()
    save_mock.assert_not_called()
