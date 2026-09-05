"""Tests de non-regression pour notifications_saas.py -- systeme OPTIONNEL
et NON BLOQUANT (cf. module docstring) : chaque canal (push, email) est
independant selon les secrets configures ; erreur reseau -> log + skip,
jamais une exception qui remonte.

Depuis l'audit externe du 30/08/2026, notifier_alertes_en_attente() prend
des alertes DEJA en base (avec push_envoye/email_envoye) et ne marque un
canal comme envoye (via connecteur_supabase.marquer_notification_envoyee)
qu'apres un succes reel ou une situation "rien a livrer" -- jamais apres un
echec, pour que le prochain cycle retente."""

from unittest.mock import Mock, patch

import requests

from notifications_saas import (
    _email_utilisateur,
    _envoyer_email,
    _envoyer_push,
    _lister_abonnements_push,
    _preferences_email,
    notifier_alertes_en_attente,
    notifier_transition_verification,
)


def _alerte(alerte_id="a1", user_id="u1", titre="Dracaufeu", prix=40.0,
            url="https://x/1", plateforme="eBay", push_envoye=False, email_envoye=False):
    return {"id": alerte_id, "user_id": user_id, "titre": titre, "prix": prix,
            "url": url, "plateforme": plateforme,
            "push_envoye": push_envoye, "email_envoye": email_envoye}


# ------------------- notifier_alertes_en_attente (orchestration) -------------------

def test_liste_vide_ne_declenche_aucun_appel():
    with patch("notifications_saas._lister_abonnements_push") as push_mock, \
         patch("notifications_saas._preferences_email") as email_mock:
        notifier_alertes_en_attente({"SUPABASE_URL": "u", "SUPABASE_SERVICE_ROLE_KEY": "k"}, [])
    push_mock.assert_not_called()
    email_mock.assert_not_called()


def test_sans_secrets_supabase_ne_declenche_aucun_appel():
    with patch("notifications_saas._lister_abonnements_push") as push_mock:
        notifier_alertes_en_attente({}, [_alerte()])
    push_mock.assert_not_called()


def test_sans_aucun_canal_configure_ne_declenche_aucun_appel():
    secrets = {"SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k"}
    with patch("notifications_saas._lister_abonnements_push") as push_mock, \
         patch("notifications_saas._preferences_email") as email_mock:
        notifier_alertes_en_attente(secrets, [_alerte()])
    push_mock.assert_not_called()
    email_mock.assert_not_called()


def test_push_reussi_marque_le_canal_envoye():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "VAPID_PRIVATE_KEY": "priv", "VAPID_CLAIM_EMAIL": "a@b.com",
    }
    with patch("notifications_saas._lister_abonnements_push",
               return_value=[{"user_id": "u1", "endpoint": "e1", "p256dh": "p", "auth": "a"}]), \
         patch("notifications_saas._preferences_email", return_value={}), \
         patch("notifications_saas._envoyer_push", return_value=True) as push_send_mock, \
         patch("notifications_saas._envoyer_email") as email_send_mock, \
         patch("connecteur_supabase.marquer_notification_envoyee") as marquer_mock:
        notifier_alertes_en_attente(secrets, [_alerte()])
    push_send_mock.assert_called_once()
    email_send_mock.assert_not_called()
    marquer_mock.assert_called_once_with("https://x.supabase.co", "k", "a1", "push")


def test_push_echoue_ne_marque_pas_le_canal_envoye():
    # Audit du 30/08/2026 : un echec ne doit JAMAIS marquer le canal comme
    # envoye, sinon l'alerte ne serait plus jamais retentee -- exactement le
    # bug corrige.
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "VAPID_PRIVATE_KEY": "priv", "VAPID_CLAIM_EMAIL": "a@b.com",
    }
    with patch("notifications_saas._lister_abonnements_push",
               return_value=[{"user_id": "u1", "endpoint": "e1", "p256dh": "p", "auth": "a"}]), \
         patch("notifications_saas._preferences_email", return_value={}), \
         patch("notifications_saas._envoyer_push", return_value=False), \
         patch("connecteur_supabase.marquer_notification_envoyee") as marquer_mock:
        notifier_alertes_en_attente(secrets, [_alerte()])
    marquer_mock.assert_not_called()


def test_push_deja_envoye_nest_pas_retente():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "VAPID_PRIVATE_KEY": "priv", "VAPID_CLAIM_EMAIL": "a@b.com",
    }
    with patch("notifications_saas._lister_abonnements_push",
               return_value=[{"user_id": "u1", "endpoint": "e1", "p256dh": "p", "auth": "a"}]), \
         patch("notifications_saas._envoyer_push") as push_send_mock, \
         patch("connecteur_supabase.marquer_notification_envoyee") as marquer_mock:
        notifier_alertes_en_attente(secrets, [_alerte(push_envoye=True)])
    push_send_mock.assert_not_called()
    marquer_mock.assert_not_called()


def test_utilisateur_sans_abonnement_push_marque_quand_meme_envoye():
    # Rien a livrer (pas d'abonnement) n'est pas un echec -- ne doit pas
    # rester "en attente" indefiniment.
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "VAPID_PRIVATE_KEY": "priv", "VAPID_CLAIM_EMAIL": "a@b.com",
    }
    with patch("notifications_saas._lister_abonnements_push", return_value=[]), \
         patch("notifications_saas._envoyer_push") as push_send_mock, \
         patch("connecteur_supabase.marquer_notification_envoyee") as marquer_mock:
        notifier_alertes_en_attente(secrets, [_alerte(user_id="u1")])
    push_send_mock.assert_not_called()
    marquer_mock.assert_called_once_with("https://x.supabase.co", "k", "a1", "push")


def test_email_reussi_marque_le_canal_envoye():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "SENDGRID_API_KEY": "SG.xxx", "SENDGRID_FROM_EMAIL": "noreply@pokedeals.app",
    }
    with patch("notifications_saas._preferences_email", return_value={"u1": True}), \
         patch("notifications_saas._email_utilisateur", return_value="user@example.com"), \
         patch("notifications_saas._envoyer_push") as push_send_mock, \
         patch("notifications_saas._envoyer_email", return_value=True) as email_send_mock, \
         patch("connecteur_supabase.marquer_notification_envoyee") as marquer_mock:
        notifier_alertes_en_attente(secrets, [_alerte()])
    push_send_mock.assert_not_called()
    email_send_mock.assert_called_once()
    args, kwargs = email_send_mock.call_args
    assert args[2] == "user@example.com"
    assert kwargs["custom_args"] == {"produit": "pokedeals", "type_notification": "alerte", "reference_id": "a1"}
    marquer_mock.assert_called_once_with("https://x.supabase.co", "k", "a1", "email")


def test_email_echoue_ne_marque_pas_le_canal_envoye():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "SENDGRID_API_KEY": "SG.xxx", "SENDGRID_FROM_EMAIL": "noreply@pokedeals.app",
    }
    with patch("notifications_saas._preferences_email", return_value={"u1": True}), \
         patch("notifications_saas._email_utilisateur", return_value="user@example.com"), \
         patch("notifications_saas._envoyer_email", return_value=False), \
         patch("connecteur_supabase.marquer_notification_envoyee") as marquer_mock:
        notifier_alertes_en_attente(secrets, [_alerte(user_id="u1")])
    marquer_mock.assert_not_called()


def test_email_deja_envoye_nest_pas_retente():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "SENDGRID_API_KEY": "SG.xxx", "SENDGRID_FROM_EMAIL": "noreply@pokedeals.app",
    }
    with patch("notifications_saas._preferences_email", return_value={"u1": True}), \
         patch("notifications_saas._envoyer_email") as email_send_mock, \
         patch("connecteur_supabase.marquer_notification_envoyee") as marquer_mock:
        notifier_alertes_en_attente(secrets, [_alerte(email_envoye=True)])
    email_send_mock.assert_not_called()
    marquer_mock.assert_not_called()


def test_email_desactive_marque_quand_meme_envoye():
    # Choix de l'utilisateur de ne pas recevoir d'email n'est pas un echec
    # -- ne doit pas rester "en attente" indefiniment.
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "SENDGRID_API_KEY": "SG.xxx", "SENDGRID_FROM_EMAIL": "noreply@pokedeals.app",
    }
    with patch("notifications_saas._preferences_email", return_value={"u1": False}), \
         patch("notifications_saas._email_utilisateur") as email_lookup_mock, \
         patch("notifications_saas._envoyer_email") as email_send_mock, \
         patch("connecteur_supabase.marquer_notification_envoyee") as marquer_mock:
        notifier_alertes_en_attente(secrets, [_alerte(user_id="u1")])
    email_lookup_mock.assert_not_called()
    email_send_mock.assert_not_called()
    marquer_mock.assert_called_once_with("https://x.supabase.co", "k", "a1", "email")


def test_email_actif_par_defaut_si_aucune_preference_enregistree():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "SENDGRID_API_KEY": "SG.xxx", "SENDGRID_FROM_EMAIL": "noreply@pokedeals.app",
    }
    with patch("notifications_saas._preferences_email", return_value={}), \
         patch("notifications_saas._email_utilisateur", return_value="user@example.com"), \
         patch("notifications_saas._envoyer_email", return_value=True) as email_send_mock, \
         patch("connecteur_supabase.marquer_notification_envoyee"):
        notifier_alertes_en_attente(secrets, [_alerte(user_id="u1")])
    email_send_mock.assert_called_once()


def test_email_sans_adresse_trouvee_nenvoie_rien_et_ne_marque_pas():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "SENDGRID_API_KEY": "SG.xxx", "SENDGRID_FROM_EMAIL": "noreply@pokedeals.app",
    }
    with patch("notifications_saas._preferences_email", return_value={}), \
         patch("notifications_saas._email_utilisateur", return_value=None), \
         patch("notifications_saas._envoyer_email") as email_send_mock, \
         patch("connecteur_supabase.marquer_notification_envoyee") as marquer_mock:
        notifier_alertes_en_attente(secrets, [_alerte(user_id="u1")])
    email_send_mock.assert_not_called()
    marquer_mock.assert_not_called()


def test_meme_utilisateur_email_recherche_une_seule_fois_pour_plusieurs_alertes():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "SENDGRID_API_KEY": "SG.xxx", "SENDGRID_FROM_EMAIL": "noreply@pokedeals.app",
    }
    alertes = [_alerte(alerte_id="a1", user_id="u1"), _alerte(alerte_id="a2", user_id="u1")]
    with patch("notifications_saas._preferences_email", return_value={}), \
         patch("notifications_saas._email_utilisateur", return_value="user@example.com") as lookup_mock, \
         patch("notifications_saas._envoyer_email", return_value=True), \
         patch("connecteur_supabase.marquer_notification_envoyee"):
        notifier_alertes_en_attente(secrets, alertes)
    lookup_mock.assert_called_once()


def test_panne_lecture_abonnements_push_ne_marque_pas_envoye():
    # Bug reel corrige le 05/09/2026 (audit externe multi-IA) : avant, une
    # panne de lecture ([] au lieu de None) etait indiscernable de "aucun
    # abonnement" -- un utilisateur ayant reellement un abonnement se
    # voyait son push marque envoye a tort, sans qu'aucun envoi n'ait eu
    # lieu, et sans plus jamais etre retente.
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "VAPID_PRIVATE_KEY": "priv", "VAPID_CLAIM_EMAIL": "a@b.com",
    }
    with patch("notifications_saas._lister_abonnements_push", return_value=None), \
         patch("notifications_saas._envoyer_push") as push_send_mock, \
         patch("connecteur_supabase.marquer_notification_envoyee") as marquer_mock:
        notifier_alertes_en_attente(secrets, [_alerte(user_id="u1")])
    push_send_mock.assert_not_called()
    marquer_mock.assert_not_called()


def test_panne_lecture_preferences_email_ne_marque_pas_envoye():
    # Meme classe de bug que ci-dessus, cote email : une panne de lecture des
    # preferences ({} au lieu de None) etait indiscernable de "aucune
    # preference enregistree" (actif par defaut), ce qui pouvait a la fois
    # ignorer un opt-out reel ET, avec l'ancien code, marquer le canal comme
    # traite si l'envoi echouait pour une autre raison. Le comportement
    # correct est de sauter entierement le canal ce cycle-ci (ni envoi, ni
    # marquage) pour qu'il soit retente au prochain cycle.
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "SENDGRID_API_KEY": "SG.xxx", "SENDGRID_FROM_EMAIL": "noreply@pokedeals.app",
    }
    with patch("notifications_saas._preferences_email", return_value=None), \
         patch("notifications_saas._email_utilisateur") as lookup_mock, \
         patch("notifications_saas._envoyer_email") as email_send_mock, \
         patch("connecteur_supabase.marquer_notification_envoyee") as marquer_mock:
        notifier_alertes_en_attente(secrets, [_alerte(user_id="u1")])
    lookup_mock.assert_not_called()
    email_send_mock.assert_not_called()
    marquer_mock.assert_not_called()


def test_push_et_email_actifs_notifie_les_deux_canaux_independamment():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "VAPID_PRIVATE_KEY": "priv", "VAPID_CLAIM_EMAIL": "a@b.com",
        "SENDGRID_API_KEY": "SG.xxx", "SENDGRID_FROM_EMAIL": "noreply@pokedeals.app",
    }
    with patch("notifications_saas._lister_abonnements_push",
               return_value=[{"user_id": "u1", "endpoint": "e1", "p256dh": "p", "auth": "a"}]), \
         patch("notifications_saas._preferences_email", return_value={"u1": True}), \
         patch("notifications_saas._email_utilisateur", return_value="user@example.com"), \
         patch("notifications_saas._envoyer_push", return_value=True), \
         patch("notifications_saas._envoyer_email", return_value=True), \
         patch("connecteur_supabase.marquer_notification_envoyee") as marquer_mock:
        notifier_alertes_en_attente(secrets, [_alerte()])
    canaux_marques = {appel.args[3] for appel in marquer_mock.call_args_list}
    assert canaux_marques == {"push", "email"}


# ------------------- _lister_abonnements_push -------------------

def test_lister_abonnements_sans_user_ids_ne_declenche_aucun_appel_reseau():
    with patch("notifications_saas.requests.get") as get_mock:
        result = _lister_abonnements_push("https://x.supabase.co", "cle", [])
    assert result == []
    get_mock.assert_not_called()


def test_lister_abonnements_erreur_reseau_retourne_none():
    # Distinct de [] (lecture reussie, aucun abonnement) -- audit du
    # 05/09/2026, cf. docstring de _lister_abonnements_push().
    with patch("notifications_saas.requests.get", side_effect=requests.RequestException("boom")):
        result = _lister_abonnements_push("https://x.supabase.co", "cle", ["u1"])
    assert result is None


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

def test_preferences_email_erreur_reseau_retourne_none():
    # Distinct de {} (lecture reussie, aucune preference enregistree) --
    # audit du 05/09/2026, cf. docstring de _preferences_email().
    with patch("notifications_saas.requests.get", side_effect=requests.RequestException("boom")):
        result = _preferences_email("https://x.supabase.co", "cle", ["u1"])
    assert result is None


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

def test_envoyer_email_erreur_reseau_retourne_false():
    with patch("notifications_saas.requests.post", side_effect=requests.RequestException("boom")):
        reussi = _envoyer_email("SG.xxx", "noreply@pokedeals.app", "user@example.com", "titre", "corps", "https://x/1")
    assert reussi is False


def test_envoyer_email_appelle_lapi_sendgrid_et_retourne_true():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    with patch("notifications_saas.requests.post", return_value=reponse) as post_mock:
        reussi = _envoyer_email("SG.xxx", "noreply@pokedeals.app", "user@example.com", "titre", "corps", "https://x/1")
    assert reussi is True
    args, kwargs = post_mock.call_args
    assert args[0] == "https://api.sendgrid.com/v3/mail/send"
    assert kwargs["json"]["personalizations"][0]["to"] == [{"email": "user@example.com"}]
    assert kwargs["json"]["subject"] == "titre"


def test_envoyer_email_echappe_le_html_du_corps_et_de_lurl():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    corps = "<script>alert(1)</script> Dracaufeu & Cie"
    url = 'https://x/1?a="b"&c=<d>'
    with patch("notifications_saas.requests.post", return_value=reponse) as post_mock:
        _envoyer_email("SG.xxx", "noreply@pokedeals.app", "user@example.com", "titre", corps, url)
    contenu = post_mock.call_args.kwargs["json"]["content"]
    html_envoye = next(c["value"] for c in contenu if c["type"] == "text/html")
    assert "<script>" not in html_envoye
    assert "&lt;script&gt;" in html_envoye
    assert "&amp;" in html_envoye
    assert 'href="https://x/1?a=&quot;b&quot;&amp;c=&lt;d&gt;"' in html_envoye


def test_envoyer_email_sans_custom_args_ne_les_inclut_pas():
    # Retro-compatibilite : un appel sans custom_args (ancien comportement)
    # ne doit pas envoyer de cle "custom_args" du tout a SendGrid.
    reponse = Mock()
    reponse.raise_for_status = Mock()
    with patch("notifications_saas.requests.post", return_value=reponse) as post_mock:
        _envoyer_email("SG.xxx", "noreply@pokedeals.app", "user@example.com", "titre", "corps", "https://x/1")
    assert "custom_args" not in post_mock.call_args.kwargs["json"]


def test_envoyer_email_avec_custom_args_les_transmet_a_sendgrid():
    # Ajoute le 05/09/2026 (webhook SendGrid, pokedeals-saas) : permet de
    # correler un evenement de livraison recu par le webhook a l'alerte
    # precise qui l'a declenche.
    reponse = Mock()
    reponse.raise_for_status = Mock()
    with patch("notifications_saas.requests.post", return_value=reponse) as post_mock:
        _envoyer_email(
            "SG.xxx", "noreply@pokedeals.app", "user@example.com", "titre", "corps", "https://x/1",
            custom_args={"produit": "pokedeals", "type_notification": "alerte", "reference_id": "a1"},
        )
    assert post_mock.call_args.kwargs["json"]["custom_args"] == {
        "produit": "pokedeals", "type_notification": "alerte", "reference_id": "a1",
    }


# ------------------- _envoyer_push -------------------

def test_envoyer_push_appelle_webpush_par_abonnement_et_retourne_true():
    abonnements = [
        {"user_id": "u1", "endpoint": "e1", "p256dh": "p1", "auth": "a1"},
        {"user_id": "u1", "endpoint": "e2", "p256dh": "p2", "auth": "a2"},
    ]
    with patch("pywebpush.webpush") as webpush_mock:
        reussi = _envoyer_push("https://x.supabase.co", "cle", "priv", "a@b.com", abonnements, "titre", "corps", "https://x/1")
    assert webpush_mock.call_count == 2
    assert reussi is True


def test_envoyer_push_purge_abonnement_expire_sur_410_et_retourne_true():
    # Un abonnement expire/revoque est purge, pas retente -- ce n'est pas un
    # echec transitoire, donc le canal reste marquable comme envoye.
    from pywebpush import WebPushException

    reponse_410 = Mock()
    reponse_410.status_code = 410
    exception = WebPushException("expired", response=reponse_410)

    abonnements = [{"user_id": "u1", "endpoint": "e1", "p256dh": "p1", "auth": "a1"}]
    with patch("pywebpush.webpush", side_effect=exception), \
         patch("notifications_saas._supprimer_abonnement_push") as purge_mock:
        reussi = _envoyer_push("https://x.supabase.co", "cle", "priv", "a@b.com", abonnements, "titre", "corps", "https://x/1")
    purge_mock.assert_called_once_with("https://x.supabase.co", "cle", "e1")
    assert reussi is True


# ------------------- notifier_transition_verification (03/09/2026) -------------------
# Notification PONCTUELLE (vendu / encore moins cher, cf. verification_alertes.py) --
# contrairement a notifier_alertes_en_attente(), pas de colonnes
# push_envoye/email_envoye a marquer : c'est detecter_transition() (cote
# appelant) qui garantit qu'une meme transition n'est signalee qu'une fois.

def test_transition_sans_user_id_ne_declenche_aucun_appel():
    with patch("notifications_saas._lister_abonnements_push") as push_mock:
        notifier_transition_verification(
            {"SUPABASE_URL": "u", "SUPABASE_SERVICE_ROLE_KEY": "k"}, "", "titre", "corps", "https://x/1",
        )
    push_mock.assert_not_called()


def test_transition_sans_secrets_supabase_ne_declenche_aucun_appel():
    with patch("notifications_saas._lister_abonnements_push") as push_mock:
        notifier_transition_verification({}, "u1", "titre", "corps", "https://x/1")
    push_mock.assert_not_called()


def test_transition_sans_aucun_canal_configure_ne_declenche_aucun_appel():
    secrets = {"SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k"}
    with patch("notifications_saas._lister_abonnements_push") as push_mock, \
         patch("notifications_saas._preferences_email") as email_mock:
        notifier_transition_verification(secrets, "u1", "titre", "corps", "https://x/1")
    push_mock.assert_not_called()
    email_mock.assert_not_called()


def test_transition_push_actif_envoie_aux_abonnements_de_lutilisateur():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "VAPID_PRIVATE_KEY": "priv", "VAPID_CLAIM_EMAIL": "a@b.com",
    }
    with patch("notifications_saas._lister_abonnements_push",
               return_value=[{"user_id": "u1", "endpoint": "e1", "p256dh": "p", "auth": "a"}]) as list_mock, \
         patch("notifications_saas._envoyer_push", return_value=True) as push_send_mock:
        notifier_transition_verification(secrets, "u1", "titre", "corps", "https://x/1")
    list_mock.assert_called_once_with("https://x.supabase.co", "k", ["u1"])
    push_send_mock.assert_called_once()
    args, _ = push_send_mock.call_args
    assert args[5] == "titre"
    assert args[6] == "corps"
    assert args[7] == "https://x/1"


def test_transition_push_sans_abonnement_ne_declenche_aucun_envoi():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "VAPID_PRIVATE_KEY": "priv", "VAPID_CLAIM_EMAIL": "a@b.com",
    }
    with patch("notifications_saas._lister_abonnements_push", return_value=[]), \
         patch("notifications_saas._envoyer_push") as push_send_mock:
        notifier_transition_verification(secrets, "u1", "titre", "corps", "https://x/1")
    push_send_mock.assert_not_called()


def test_transition_email_actif_envoie_si_preference_active():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "SENDGRID_API_KEY": "SG.xxx", "SENDGRID_FROM_EMAIL": "noreply@pokedeals.app",
    }
    with patch("notifications_saas._preferences_email", return_value={"u1": True}), \
         patch("notifications_saas._email_utilisateur", return_value="user@example.com"), \
         patch("notifications_saas._envoyer_email", return_value=True) as email_send_mock:
        notifier_transition_verification(secrets, "u1", "titre", "corps", "https://x/1")
    email_send_mock.assert_called_once_with(
        "SG.xxx", "noreply@pokedeals.app", "user@example.com", "titre", "corps", "https://x/1",
        custom_args={"produit": "pokedeals", "type_notification": "verification"},
    )


def test_transition_email_panne_lecture_preferences_ne_plante_pas():
    # _preferences_email() peut desormais retourner None (panne reseau,
    # audit du 05/09/2026). notifier_transition_verification() est
    # deliberement best-effort (pas de colonne a marquer, pas de retry, cf.
    # docstring du module) -- une panne de lecture y est donc traitee comme
    # l'absence de preference (actif par defaut, on tente quand meme),
    # exactement comme avant ce correctif (qui visait seulement a eviter le
    # crash sur None.get(...), pas a changer ce comportement fail-open deja
    # existant pour cette fonction ponctuelle).
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "SENDGRID_API_KEY": "SG.xxx", "SENDGRID_FROM_EMAIL": "noreply@pokedeals.app",
    }
    with patch("notifications_saas._preferences_email", return_value=None), \
         patch("notifications_saas._email_utilisateur", return_value="user@example.com"), \
         patch("notifications_saas._envoyer_email", return_value=True) as email_send_mock:
        notifier_transition_verification(secrets, "u1", "titre", "corps", "https://x/1")
    email_send_mock.assert_called_once()


def test_transition_email_desactive_ne_declenche_aucun_envoi():
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "SENDGRID_API_KEY": "SG.xxx", "SENDGRID_FROM_EMAIL": "noreply@pokedeals.app",
    }
    with patch("notifications_saas._preferences_email", return_value={"u1": False}), \
         patch("notifications_saas._email_utilisateur") as lookup_mock, \
         patch("notifications_saas._envoyer_email") as email_send_mock:
        notifier_transition_verification(secrets, "u1", "titre", "corps", "https://x/1")
    lookup_mock.assert_not_called()
    email_send_mock.assert_not_called()


def test_transition_echec_push_nempeche_pas_lenvoi_email():
    # Non bloquant : un canal qui echoue n'empeche jamais l'autre de
    # continuer (meme esprit que notifier_alertes_en_attente()).
    secrets = {
        "SUPABASE_URL": "https://x.supabase.co", "SUPABASE_SERVICE_ROLE_KEY": "k",
        "VAPID_PRIVATE_KEY": "priv", "VAPID_CLAIM_EMAIL": "a@b.com",
        "SENDGRID_API_KEY": "SG.xxx", "SENDGRID_FROM_EMAIL": "noreply@pokedeals.app",
    }
    with patch("notifications_saas._lister_abonnements_push",
               return_value=[{"user_id": "u1", "endpoint": "e1", "p256dh": "p", "auth": "a"}]), \
         patch("notifications_saas._envoyer_push", return_value=False), \
         patch("notifications_saas._preferences_email", return_value={"u1": True}), \
         patch("notifications_saas._email_utilisateur", return_value="user@example.com"), \
         patch("notifications_saas._envoyer_email", return_value=True) as email_send_mock:
        notifier_transition_verification(secrets, "u1", "titre", "corps", "https://x/1")
    email_send_mock.assert_called_once()


def test_envoyer_push_erreur_reseau_ne_purge_pas_et_retourne_false():
    # Audit du 30/08/2026 : un echec transitoire (pas 404/410) ne doit PAS
    # etre traite comme un succes, sinon le canal serait marque envoye a
    # tort et jamais retente.
    from pywebpush import WebPushException

    reponse_500 = Mock()
    reponse_500.status_code = 500
    exception = WebPushException("boom", response=reponse_500)

    abonnements = [{"user_id": "u1", "endpoint": "e1", "p256dh": "p1", "auth": "a1"}]
    with patch("pywebpush.webpush", side_effect=exception), \
         patch("notifications_saas._supprimer_abonnement_push") as purge_mock:
        reussi = _envoyer_push("https://x.supabase.co", "cle", "priv", "a@b.com", abonnements, "titre", "corps", "https://x/1")
    purge_mock.assert_not_called()
    assert reussi is False
