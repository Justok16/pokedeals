"""Tests de non-regression pour notifications_saas.py -- systeme OPTIONNEL
et NON BLOQUANT (cf. module docstring) : chaque canal (push, email) est
independant selon les secrets configures ; erreur reseau -> log + skip,
jamais une exception qui remonte."""

from unittest.mock import Mock, patch

import requests

from notifications_saas import (
    _email_utilisateur,
    _envoyer_email,
    _envoyer_push,
    _lister_abonnements_push,
    _preferences_email,
    notifier_nouvelles_alertes,
)


def _alerte(user_id="u1", watchlist_item_id="i1", titre="Dracaufeu", prix=40.0,
            url="https://x/1", plateforme="eBay"):
    return {"user_id": user_id, "watchlist_item_id": watchlist_item_id,
            "titre": titre, "prix": prix, "url": url, "plateforme": plateforme}


# ------------------- notifier_nouvelles_alertes (orchestration) -------------------

def test_liste_vide_ne_declenche_aucun_appel():
    with patch("notifications_saas._lister_abonnements_push") as push_mock, \
         patch("notifications_saas._preferences_email") as email_mock:
        notifier_nouvelles_alertes({"SUPABASE_URL": "u", "SUPABASE_SERVICE_ROLE_KEY": "k"}, [])
    push_mock.assert_not_called()
    email_mock.assert_not_called()


def test_sans_secrets_supabase_ne_declenche_aucun_appel():
    with patch("notifications_saas._lister_abonnements_push") as push_mock:
        notifier_nouvelles_alertes({}, [_alerte()])
    push_mock.assert_not_called()


def test_sans_aucun_canal_configure_ne_declenche_aucun_appel():
    secrets = {"SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k"}
    with patch("notifications_saas._lister_abonnements_push") as push_mock, \
         patch("notifications_saas._preferences_email") as email_mock:
        notifier_nouvelles_alertes(secrets, [_alerte()])
    push_mock.assert_not_called()
    email_mock.assert_not_called()


def test_push_actif_seul_notifie_par_push_uniquement():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "VAPID_PRIVATE_KEY": "priv", "VAPID_CLAIM_EMAIL": "a@b.com",
    }
    with patch("notifications_saas._lister_abonnements_push",
               return_value=[{"user_id": "u1", "endpoint": "e1", "p256dh": "p", "auth": "a"}]), \
         patch("notifications_saas._preferences_email", return_value={}) as pref_mock, \
         patch("notifications_saas._envoyer_push") as push_send_mock, \
         patch("notifications_saas._envoyer_email") as email_send_mock:
        notifier_nouvelles_alertes(secrets, [_alerte()])
    push_send_mock.assert_called_once()
    email_send_mock.assert_not_called()
    pref_mock.assert_not_called()  # email desactive -> pas besoin des preferences


def test_email_actif_seul_notifie_par_email_si_utilisateur_a_un_abonnement():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "RESEND_API_KEY": "re_xxx", "RESEND_FROM_EMAIL": "noreply@pokedeals.app",
    }
    with patch("notifications_saas._lister_abonnements_push") as push_list_mock, \
         patch("notifications_saas._preferences_email", return_value={"u1": True}), \
         patch("notifications_saas._email_utilisateur", return_value="user@example.com"), \
         patch("notifications_saas._envoyer_push") as push_send_mock, \
         patch("notifications_saas._envoyer_email") as email_send_mock:
        notifier_nouvelles_alertes(secrets, [_alerte()])
    push_send_mock.assert_not_called()
    email_send_mock.assert_called_once()
    push_list_mock.assert_not_called()  # push desactive -> pas besoin des abonnements
    args, _ = email_send_mock.call_args
    assert args[2] == "user@example.com"


def test_email_saute_si_preference_desactivee():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "RESEND_API_KEY": "re_xxx", "RESEND_FROM_EMAIL": "noreply@pokedeals.app",
    }
    with patch("notifications_saas._preferences_email", return_value={"u1": False}), \
         patch("notifications_saas._email_utilisateur") as email_lookup_mock, \
         patch("notifications_saas._envoyer_email") as email_send_mock:
        notifier_nouvelles_alertes(secrets, [_alerte(user_id="u1")])
    email_lookup_mock.assert_not_called()
    email_send_mock.assert_not_called()


def test_email_actif_par_defaut_si_aucune_preference_enregistree():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "RESEND_API_KEY": "re_xxx", "RESEND_FROM_EMAIL": "noreply@pokedeals.app",
    }
    with patch("notifications_saas._preferences_email", return_value={}), \
         patch("notifications_saas._email_utilisateur", return_value="user@example.com"), \
         patch("notifications_saas._envoyer_email") as email_send_mock:
        notifier_nouvelles_alertes(secrets, [_alerte(user_id="u1")])
    email_send_mock.assert_called_once()


def test_utilisateur_sans_abonnement_push_nest_pas_notifie_par_push():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "VAPID_PRIVATE_KEY": "priv", "VAPID_CLAIM_EMAIL": "a@b.com",
    }
    with patch("notifications_saas._lister_abonnements_push", return_value=[]), \
         patch("notifications_saas._envoyer_push") as push_send_mock:
        notifier_nouvelles_alertes(secrets, [_alerte(user_id="u1")])
    push_send_mock.assert_not_called()


def test_email_sans_adresse_trouvee_nenvoie_rien():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "RESEND_API_KEY": "re_xxx", "RESEND_FROM_EMAIL": "noreply@pokedeals.app",
    }
    with patch("notifications_saas._preferences_email", return_value={}), \
         patch("notifications_saas._email_utilisateur", return_value=None), \
         patch("notifications_saas._envoyer_email") as email_send_mock:
        notifier_nouvelles_alertes(secrets, [_alerte(user_id="u1")])
    email_send_mock.assert_not_called()


def test_meme_utilisateur_email_recherche_une_seule_fois_pour_plusieurs_alertes():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "RESEND_API_KEY": "re_xxx", "RESEND_FROM_EMAIL": "noreply@pokedeals.app",
    }
    alertes = [_alerte(user_id="u1", watchlist_item_id="i1"), _alerte(user_id="u1", watchlist_item_id="i2")]
    with patch("notifications_saas._preferences_email", return_value={}), \
         patch("notifications_saas._email_utilisateur", return_value="user@example.com") as lookup_mock, \
         patch("notifications_saas._envoyer_email"):
        notifier_nouvelles_alertes(secrets, alertes)
    lookup_mock.assert_called_once()


# ------------------- _lister_abonnements_push -------------------

def test_lister_abonnements_sans_user_ids_ne_declenche_aucun_appel_reseau():
    with patch("notifications_saas.requests.get") as get_mock:
        result = _lister_abonnements_push("https://x.supabase.co", "cle", [])
    assert result == []
    get_mock.assert_not_called()


def test_lister_abonnements_erreur_reseau_retourne_liste_vide():
    with patch("notifications_saas.requests.get", side_effect=requests.RequestException("boom")):
        result = _lister_abonnements_push("https://x.supabase.co", "cle", ["u1"])
    assert result == []


def test_lister_abonnements_succes():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    reponse.json.return_value = [{"user_id": "u1", "endpoint": "e", "p256dh": "p", "auth": "a"}]
    with patch("notifications_saas.requests.get", return_value=reponse) as get_mock:
        result = _lister_abonnements_push("https://x.supabase.co", "cle", ["u1", "u2"])
    assert result[0]["user_id"] == "u1"
    _, kwargs = get_mock.call_args
    assert kwargs["params"]["user_id"] == "in.(u1,u2)"


# ------------------- _preferences_email -------------------

def test_preferences_email_erreur_reseau_retourne_dict_vide():
    with patch("notifications_saas.requests.get", side_effect=requests.RequestException("boom")):
        result = _preferences_email("https://x.supabase.co", "cle", ["u1"])
    assert result == {}


def test_preferences_email_succes():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    reponse.json.return_value = [{"user_id": "u1", "notif_email": False}]
    with patch("notifications_saas.requests.get", return_value=reponse):
        result = _preferences_email("https://x.supabase.co", "cle", ["u1"])
    assert result == {"u1": False}


# ------------------- _email_utilisateur -------------------

def test_email_utilisateur_erreur_reseau_retourne_none():
    with patch("notifications_saas.requests.get", side_effect=requests.RequestException("boom")):
        result = _email_utilisateur("https://x.supabase.co", "cle", "u1")
    assert result is None


def test_email_utilisateur_succes():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    reponse.json.return_value = {"email": "user@example.com"}
    with patch("notifications_saas.requests.get", return_value=reponse):
        result = _email_utilisateur("https://x.supabase.co", "cle", "u1")
    assert result == "user@example.com"


# ------------------- _envoyer_email -------------------

def test_envoyer_email_erreur_reseau_ne_leve_pas_dexception():
    with patch("notifications_saas.requests.post", side_effect=requests.RequestException("boom")):
        _envoyer_email("re_xxx", "noreply@pokedeals.app", "user@example.com", "titre", "corps", "https://x/1")


def test_envoyer_email_appelle_lapi_resend():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    with patch("notifications_saas.requests.post", return_value=reponse) as post_mock:
        _envoyer_email("re_xxx", "noreply@pokedeals.app", "user@example.com", "titre", "corps", "https://x/1")
    args, kwargs = post_mock.call_args
    assert args[0] == "https://api.resend.com/emails"
    assert kwargs["json"]["to"] == ["user@example.com"]
    assert kwargs["json"]["subject"] == "titre"


def test_envoyer_email_echappe_le_html_du_corps_et_de_lurl():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    corps = "<script>alert(1)</script> Dracaufeu & Cie"
    url = 'https://x/1?a="b"&c=<d>'
    with patch("notifications_saas.requests.post", return_value=reponse) as post_mock:
        _envoyer_email("re_xxx", "noreply@pokedeals.app", "user@example.com", "titre", corps, url)
    html_envoye = post_mock.call_args.kwargs["json"]["html"]
    assert "<script>" not in html_envoye
    assert "&lt;script&gt;" in html_envoye
    assert "&amp;" in html_envoye
    assert 'href="https://x/1?a=&quot;b&quot;&amp;c=&lt;d&gt;"' in html_envoye


# ------------------- _envoyer_push -------------------

def test_envoyer_push_appelle_webpush_par_abonnement():
    abonnements = [
        {"user_id": "u1", "endpoint": "e1", "p256dh": "p1", "auth": "a1"},
        {"user_id": "u1", "endpoint": "e2", "p256dh": "p2", "auth": "a2"},
    ]
    with patch("pywebpush.webpush") as webpush_mock:
        _envoyer_push("https://x.supabase.co", "cle", "priv", "a@b.com", abonnements, "titre", "corps", "https://x/1")
    assert webpush_mock.call_count == 2


def test_envoyer_push_purge_abonnement_expire_sur_410():
    from pywebpush import WebPushException

    reponse_410 = Mock()
    reponse_410.status_code = 410
    exception = WebPushException("expired", response=reponse_410)

    abonnements = [{"user_id": "u1", "endpoint": "e1", "p256dh": "p1", "auth": "a1"}]
    with patch("pywebpush.webpush", side_effect=exception), \
         patch("notifications_saas._supprimer_abonnement_push") as purge_mock:
        _envoyer_push("https://x.supabase.co", "cle", "priv", "a@b.com", abonnements, "titre", "corps", "https://x/1")
    purge_mock.assert_called_once_with("https://x.supabase.co", "cle", "e1")


def test_envoyer_push_erreur_reseau_ne_purge_pas():
    from pywebpush import WebPushException

    reponse_500 = Mock()
    reponse_500.status_code = 500
    exception = WebPushException("boom", response=reponse_500)

    abonnements = [{"user_id": "u1", "endpoint": "e1", "p256dh": "p1", "auth": "a1"}]
    with patch("pywebpush.webpush", side_effect=exception), \
         patch("notifications_saas._supprimer_abonnement_push") as purge_mock:
        _envoyer_push("https://x.supabase.co", "cle", "priv", "a@b.com", abonnements, "titre", "corps", "https://x/1")
    purge_mock.assert_not_called()
