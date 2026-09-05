"""Tests de non-regression pour connecteur_supabase_precoms.py -- systeme
OPTIONNEL et NON BLOQUANT (cf. module docstring) : service gratuit et
illimite, modele BROADCAST (tous les utilisateurs inscrits recoivent
toutes les alertes), erreur reseau -> log + skip, jamais une exception qui
remonte.

Depuis l'audit externe du 30/08/2026 (meme bug que celui deja corrige cote
watchlist_alerts/PokeDeals) : une precommande n'est plus notifiee une seule
fois a l'insertion, mais retentee canal par canal (push_diffuse/email_diffuse)
tant qu'elle n'a pas ete diffusee avec succes -- cf. lister_precommandes_a_diffuser()
et marquer_diffusion_terminee()."""

from unittest.mock import Mock, patch

import requests

from connecteur_supabase_precoms import (
    _email_utilisateur,
    _envoyer_email,
    _lister_abonnements_push,
    _lister_tous_utilisateurs,
    _preferences_email,
    enregistrer_precommande_alertes,
    lister_precommandes_a_diffuser,
    marquer_diffusion_terminee,
    notifier_abonnes_precoms,
)


def _evenement(titre="ETB 30e Anniversaire", domaine="boutique.fr",
               url="https://boutique.fr/products/etb-30e", prix=59.99):
    return {"titre": titre, "domaine": domaine, "url_produit": url, "prix": prix}


def _precommande(id="p1", titre_produit="ETB 30e Anniversaire", boutique="boutique.fr",
                  url_produit="https://boutique.fr/products/etb-30e",
                  push_diffuse=False, email_diffuse=False):
    return {
        "id": id, "titre_produit": titre_produit, "boutique": boutique, "url_produit": url_produit,
        "push_diffuse": push_diffuse, "email_diffuse": email_diffuse,
    }


# ------------------- enregistrer_precommande_alertes -------------------

def test_enregistrer_liste_vide_ne_declenche_aucun_appel():
    with patch("connecteur_supabase_precoms.requests.post") as post_mock:
        result = enregistrer_precommande_alertes("https://x.supabase.co", "cle", [])
    assert result == []
    post_mock.assert_not_called()


def test_enregistrer_sans_secrets_ne_declenche_aucun_appel():
    with patch("connecteur_supabase_precoms.requests.post") as post_mock:
        result = enregistrer_precommande_alertes("", "", [_evenement()])
    assert result == []
    post_mock.assert_not_called()


def test_enregistrer_erreur_reseau_retourne_none():
    # None (pas []) sur un echec reseau reel -- distinct du no-op legitime
    # ([] pour liste vide/secrets absents ci-dessus), pour que l'appelant
    # sache qu'il doit annuler le commit memoire de Telegram sur ce cycle
    # (cf. correctif du 31/08/2026, scan_precommandes_generique.py/
    # scan_precommandes_philibert.py).
    with patch("connecteur_supabase_precoms.requests.post",
               side_effect=requests.RequestException("boom")):
        result = enregistrer_precommande_alertes("https://x.supabase.co", "cle", [_evenement()])
    assert result is None


def test_enregistrer_succes_retourne_les_lignes_inserees_et_dedupe_par_url():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    reponse.json.return_value = [{"id": "a1", "titre_produit": "ETB 30e Anniversaire"}]
    with patch("connecteur_supabase_precoms.requests.post", return_value=reponse) as post_mock:
        result = enregistrer_precommande_alertes("https://x.supabase.co", "cle", [_evenement()])
    assert len(result) == 1
    _, kwargs = post_mock.call_args
    assert kwargs["params"]["on_conflict"] == "url_produit"
    assert "resolution=ignore-duplicates" in kwargs["headers"]["Prefer"]
    assert kwargs["json"][0]["url_produit"] == "https://boutique.fr/products/etb-30e"


# ------------------- lister_precommandes_a_diffuser -------------------

def test_lister_a_diffuser_sans_secrets_ne_declenche_aucun_appel():
    with patch("connecteur_supabase_precoms.requests.get") as get_mock:
        result = lister_precommandes_a_diffuser("", "")
    assert result == []
    get_mock.assert_not_called()


def test_lister_a_diffuser_erreur_reseau_retourne_ce_qui_a_deja_ete_recupere():
    with patch("connecteur_supabase_precoms.requests.get",
               side_effect=requests.RequestException("boom")):
        result = lister_precommandes_a_diffuser("https://x.supabase.co", "cle")
    assert result == []


def test_lister_a_diffuser_filtre_sur_au_moins_un_canal_non_diffuse():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    reponse.json.return_value = [_precommande()]
    with patch("connecteur_supabase_precoms.requests.get", return_value=reponse) as get_mock:
        result = lister_precommandes_a_diffuser("https://x.supabase.co", "cle")
    assert len(result) == 1
    _, kwargs = get_mock.call_args
    assert kwargs["params"]["or"] == "(push_diffuse.eq.false,email_diffuse.eq.false)"


def test_lister_a_diffuser_pagine_jusqu_a_page_incomplete():
    page_pleine = Mock()
    page_pleine.raise_for_status = Mock()
    page_pleine.json.return_value = [_precommande(id=f"p{i}") for i in range(1000)]
    page_partielle = Mock()
    page_partielle.raise_for_status = Mock()
    page_partielle.json.return_value = [_precommande(id="p1000")]
    with patch("connecteur_supabase_precoms.requests.get",
               side_effect=[page_pleine, page_partielle]) as get_mock:
        result = lister_precommandes_a_diffuser("https://x.supabase.co", "cle")
    assert len(result) == 1001
    assert get_mock.call_count == 2


# ------------------- marquer_diffusion_terminee -------------------

def test_marquer_diffusion_sans_secrets_ne_declenche_aucun_appel():
    with patch("connecteur_supabase_precoms.requests.patch") as patch_mock:
        marquer_diffusion_terminee("", "", "p1", "push")
    patch_mock.assert_not_called()


def test_marquer_diffusion_canal_invalide_ne_declenche_aucun_appel():
    with patch("connecteur_supabase_precoms.requests.patch") as patch_mock:
        marquer_diffusion_terminee("https://x.supabase.co", "cle", "p1", "sms")
    patch_mock.assert_not_called()


def test_marquer_diffusion_erreur_reseau_ne_leve_pas():
    with patch("connecteur_supabase_precoms.requests.patch",
               side_effect=requests.RequestException("boom")):
        marquer_diffusion_terminee("https://x.supabase.co", "cle", "p1", "push")  # ne doit pas lever


def test_marquer_diffusion_succes_envoie_le_bon_flag():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    with patch("connecteur_supabase_precoms.requests.patch", return_value=reponse) as patch_mock:
        marquer_diffusion_terminee("https://x.supabase.co", "cle", "p1", "email")
    _, kwargs = patch_mock.call_args
    assert kwargs["params"]["id"] == "eq.p1"
    assert kwargs["json"] == {"email_diffuse": True}


# ------------------- notifier_abonnes_precoms (orchestration) -------------------

def test_notifier_liste_vide_ne_declenche_aucun_appel():
    with patch("connecteur_supabase_precoms._lister_tous_utilisateurs") as actifs_mock:
        notifier_abonnes_precoms(
            {"POKEPRECOMS_SUPABASE_URL": "u", "POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY": "k"}, [],
        )
    actifs_mock.assert_not_called()


def test_notifier_sans_secrets_supabase_ne_declenche_aucun_appel():
    with patch("connecteur_supabase_precoms._lister_tous_utilisateurs") as actifs_mock:
        notifier_abonnes_precoms({}, [_precommande()])
    actifs_mock.assert_not_called()


def test_notifier_sans_aucun_canal_configure_ne_declenche_aucun_appel():
    secrets = {"POKEPRECOMS_SUPABASE_URL": "https://x.supabase.co", "POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY": "k"}
    with patch("connecteur_supabase_precoms._lister_tous_utilisateurs") as actifs_mock:
        notifier_abonnes_precoms(secrets, [_precommande()])
    actifs_mock.assert_not_called()


def test_notifier_sans_utilisateur_inscrit_ne_notifie_personne():
    secrets = {
        "POKEPRECOMS_SUPABASE_URL": "https://x.supabase.co", "POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY": "k",
        "VAPID_PRIVATE_KEY": "priv", "VAPID_CLAIM_EMAIL": "a@b.com",
    }
    with patch("connecteur_supabase_precoms._lister_tous_utilisateurs", return_value=[]), \
         patch("connecteur_supabase_precoms._lister_abonnements_push") as push_list_mock:
        notifier_abonnes_precoms(secrets, [_precommande()])
    push_list_mock.assert_not_called()


def test_notifier_push_reussi_notifie_les_abonnes_et_marque_le_canal_diffuse():
    secrets = {
        "POKEPRECOMS_SUPABASE_URL": "https://x.supabase.co", "POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY": "k",
        "VAPID_PRIVATE_KEY": "priv", "VAPID_CLAIM_EMAIL": "a@b.com",
    }
    with patch("connecteur_supabase_precoms._lister_tous_utilisateurs", return_value=["u1", "u2"]), \
         patch("connecteur_supabase_precoms._lister_abonnements_push",
               return_value=[{"user_id": "u1", "endpoint": "e1", "p256dh": "p", "auth": "a"}]), \
         patch("connecteur_supabase_precoms._preferences_email", return_value={}) as pref_mock, \
         patch("connecteur_supabase_precoms._envoyer_push", return_value=True) as push_send_mock, \
         patch("connecteur_supabase_precoms._envoyer_email") as email_send_mock, \
         patch("connecteur_supabase_precoms.marquer_diffusion_terminee") as marquer_mock:
        notifier_abonnes_precoms(secrets, [_precommande()])
    # Seul u1 a un abonnement push -- u2 (inscrit mais pas abonné push) n'est pas notifié par push.
    push_send_mock.assert_called_once()
    email_send_mock.assert_not_called()
    pref_mock.assert_not_called()  # email désactivé -> pas besoin des préférences
    marquer_mock.assert_called_once_with("https://x.supabase.co", "k", "p1", "push")


def test_notifier_email_reussi_notifie_les_abonnes_et_marque_le_canal_diffuse():
    secrets = {
        "POKEPRECOMS_SUPABASE_URL": "https://x.supabase.co", "POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY": "k",
        "SENDGRID_API_KEY": "SG.xxx", "SENDGRID_FROM_EMAIL": "noreply@pokeprecoms.app",
    }
    with patch("connecteur_supabase_precoms._lister_tous_utilisateurs", return_value=["u1", "u2"]), \
         patch("connecteur_supabase_precoms._lister_abonnements_push") as push_list_mock, \
         patch("connecteur_supabase_precoms._preferences_email", return_value={"u1": False}), \
         patch("connecteur_supabase_precoms._email_utilisateur", return_value="user@example.com") as lookup_mock, \
         patch("connecteur_supabase_precoms._envoyer_email", return_value=True) as email_send_mock, \
         patch("connecteur_supabase_precoms.marquer_diffusion_terminee") as marquer_mock:
        notifier_abonnes_precoms(secrets, [_precommande()])
    push_list_mock.assert_not_called()  # push désactivé -> pas besoin des abonnements
    # u1 a désactivé l'email, seul u2 (actif par défaut) est notifié.
    assert lookup_mock.call_count == 1
    email_send_mock.assert_called_once()
    assert email_send_mock.call_args.kwargs["custom_args"] == {
        "produit": "pokeprecoms", "type_notification": "precommande", "reference_id": "p1",
    }
    marquer_mock.assert_called_once_with("https://x.supabase.co", "k", "p1", "email")


def test_notifier_deux_precommandes_meme_utilisateur_email_recherche_une_seule_fois():
    secrets = {
        "POKEPRECOMS_SUPABASE_URL": "https://x.supabase.co", "POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY": "k",
        "SENDGRID_API_KEY": "SG.xxx", "SENDGRID_FROM_EMAIL": "noreply@pokeprecoms.app",
    }
    precommandes = [_precommande(id="p1", url_produit="https://x/1"),
                    _precommande(id="p2", url_produit="https://x/2")]
    with patch("connecteur_supabase_precoms._lister_tous_utilisateurs", return_value=["u1"]), \
         patch("connecteur_supabase_precoms._preferences_email", return_value={}), \
         patch("connecteur_supabase_precoms._email_utilisateur", return_value="user@example.com") as lookup_mock, \
         patch("connecteur_supabase_precoms._envoyer_email", return_value=True) as email_send_mock, \
         patch("connecteur_supabase_precoms.marquer_diffusion_terminee"):
        notifier_abonnes_precoms(secrets, precommandes)
    lookup_mock.assert_called_once()
    assert email_send_mock.call_count == 2


def test_notifier_ne_retente_pas_un_canal_deja_diffuse():
    secrets = {
        "POKEPRECOMS_SUPABASE_URL": "https://x.supabase.co", "POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY": "k",
        "VAPID_PRIVATE_KEY": "priv", "VAPID_CLAIM_EMAIL": "a@b.com",
        "SENDGRID_API_KEY": "SG.xxx", "SENDGRID_FROM_EMAIL": "noreply@pokeprecoms.app",
    }
    precommande = _precommande(push_diffuse=True, email_diffuse=False)
    with patch("connecteur_supabase_precoms._lister_tous_utilisateurs", return_value=["u1"]), \
         patch("connecteur_supabase_precoms._lister_abonnements_push",
               return_value=[{"user_id": "u1", "endpoint": "e1", "p256dh": "p", "auth": "a"}]), \
         patch("connecteur_supabase_precoms._preferences_email", return_value={}), \
         patch("connecteur_supabase_precoms._email_utilisateur", return_value="user@example.com"), \
         patch("connecteur_supabase_precoms._envoyer_push") as push_send_mock, \
         patch("connecteur_supabase_precoms._envoyer_email", return_value=True) as email_send_mock, \
         patch("connecteur_supabase_precoms.marquer_diffusion_terminee") as marquer_mock:
        notifier_abonnes_precoms(secrets, [precommande])
    push_send_mock.assert_not_called()  # push déjà diffusé -> pas retenté
    email_send_mock.assert_called_once()
    marquer_mock.assert_called_once_with("https://x.supabase.co", "k", "p1", "email")


def test_notifier_echec_envoi_ne_marque_pas_le_canal_diffuse():
    secrets = {
        "POKEPRECOMS_SUPABASE_URL": "https://x.supabase.co", "POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY": "k",
        "VAPID_PRIVATE_KEY": "priv", "VAPID_CLAIM_EMAIL": "a@b.com",
    }
    with patch("connecteur_supabase_precoms._lister_tous_utilisateurs", return_value=["u1"]), \
         patch("connecteur_supabase_precoms._lister_abonnements_push",
               return_value=[{"user_id": "u1", "endpoint": "e1", "p256dh": "p", "auth": "a"}]), \
         patch("connecteur_supabase_precoms._preferences_email", return_value={}), \
         patch("connecteur_supabase_precoms._envoyer_push", return_value=False), \
         patch("connecteur_supabase_precoms.marquer_diffusion_terminee") as marquer_mock:
        notifier_abonnes_precoms(secrets, [_precommande()])
    marquer_mock.assert_not_called()


def test_notifier_panne_lecture_abonnements_push_ne_marque_pas_le_broadcast_diffuse():
    # Bug reel corrige le 05/09/2026 (audit externe multi-IA) : avant, une
    # panne de lecture des abonnements ([] au lieu de None) faisait passer
    # TOUS les utilisateurs pour "sans abonnement push" -- aucun envoi
    # n'etait meme tente (donc echec_push restait False) et le canal push du
    # broadcast ENTIER etait quand meme marque diffuse, empechant tout retry
    # au cycle suivant alors que zero push n'avait ete livre.
    secrets = {
        "POKEPRECOMS_SUPABASE_URL": "https://x.supabase.co", "POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY": "k",
        "VAPID_PRIVATE_KEY": "priv", "VAPID_CLAIM_EMAIL": "a@b.com",
    }
    with patch("connecteur_supabase_precoms._lister_tous_utilisateurs", return_value=["u1", "u2"]), \
         patch("connecteur_supabase_precoms._lister_abonnements_push", return_value=None), \
         patch("connecteur_supabase_precoms._envoyer_push") as push_send_mock, \
         patch("connecteur_supabase_precoms.marquer_diffusion_terminee") as marquer_mock:
        notifier_abonnes_precoms(secrets, [_precommande()])
    push_send_mock.assert_not_called()
    marquer_mock.assert_not_called()


def test_notifier_panne_lecture_preferences_email_ne_marque_pas_le_broadcast_diffuse():
    # Meme classe de bug que ci-dessus, cote email.
    secrets = {
        "POKEPRECOMS_SUPABASE_URL": "https://x.supabase.co", "POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY": "k",
        "SENDGRID_API_KEY": "SG.xxx", "SENDGRID_FROM_EMAIL": "noreply@pokeprecoms.app",
    }
    with patch("connecteur_supabase_precoms._lister_tous_utilisateurs", return_value=["u1", "u2"]), \
         patch("connecteur_supabase_precoms._preferences_email", return_value=None), \
         patch("connecteur_supabase_precoms._email_utilisateur") as lookup_mock, \
         patch("connecteur_supabase_precoms._envoyer_email") as email_send_mock, \
         patch("connecteur_supabase_precoms.marquer_diffusion_terminee") as marquer_mock:
        notifier_abonnes_precoms(secrets, [_precommande()])
    lookup_mock.assert_not_called()
    email_send_mock.assert_not_called()
    marquer_mock.assert_not_called()


# ------------------- _lister_tous_utilisateurs -------------------

def test_lister_tous_utilisateurs_sans_secrets_ne_declenche_aucun_appel_reseau():
    with patch("connecteur_supabase_precoms.requests.get") as get_mock:
        result = _lister_tous_utilisateurs("", "")
    assert result == []
    get_mock.assert_not_called()


def test_lister_tous_utilisateurs_erreur_reseau_retourne_liste_vide():
    with patch("connecteur_supabase_precoms.requests.get", side_effect=requests.RequestException("boom")):
        result = _lister_tous_utilisateurs("https://x.supabase.co", "cle")
    assert result == []


def test_lister_tous_utilisateurs_succes_une_seule_page():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    reponse.json.return_value = {"users": [{"id": "u1"}, {"id": "u2"}]}
    with patch("connecteur_supabase_precoms.requests.get", return_value=reponse) as get_mock:
        result = _lister_tous_utilisateurs("https://x.supabase.co", "cle")
    assert result == ["u1", "u2"]
    get_mock.assert_called_once()
    _, kwargs = get_mock.call_args
    assert kwargs["params"] == {"page": 1, "per_page": 1000}


def test_lister_tous_utilisateurs_pagine_jusqu_a_page_incomplete():
    page_pleine = Mock()
    page_pleine.raise_for_status = Mock()
    page_pleine.json.return_value = {"users": [{"id": f"u{i}"} for i in range(1000)]}
    page_partielle = Mock()
    page_partielle.raise_for_status = Mock()
    page_partielle.json.return_value = {"users": [{"id": "u1000"}]}
    with patch("connecteur_supabase_precoms.requests.get",
               side_effect=[page_pleine, page_partielle]) as get_mock:
        result = _lister_tous_utilisateurs("https://x.supabase.co", "cle")
    assert len(result) == 1001
    assert get_mock.call_count == 2


# ------------------- _lister_abonnements_push -------------------

def test_lister_abonnements_push_sans_user_ids_ne_declenche_aucun_appel_reseau():
    with patch("connecteur_supabase_precoms.requests.get") as get_mock:
        result = _lister_abonnements_push("https://x.supabase.co", "cle", [])
    assert result == []
    get_mock.assert_not_called()


def test_lister_abonnements_push_erreur_reseau_retourne_none():
    # Distinct de [] (lecture reussie, aucun abonnement) -- audit du
    # 05/09/2026, cf. docstring de _lister_abonnements_push().
    with patch("connecteur_supabase_precoms.requests.get", side_effect=requests.RequestException("boom")):
        result = _lister_abonnements_push("https://x.supabase.co", "cle", ["u1"])
    assert result is None


# ------------------- _preferences_email -------------------

def test_preferences_email_erreur_reseau_retourne_none():
    # Distinct de {} (lecture reussie, aucune preference enregistree) --
    # audit du 05/09/2026, cf. docstring de _preferences_email().
    with patch("connecteur_supabase_precoms.requests.get", side_effect=requests.RequestException("boom")):
        result = _preferences_email("https://x.supabase.co", "cle", ["u1"])
    assert result is None


# ------------------- _envoyer_email -------------------

def test_envoyer_email_sans_custom_args_ne_les_inclut_pas():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    with patch("connecteur_supabase_precoms.requests.post", return_value=reponse) as post_mock:
        _envoyer_email("SG.xxx", "noreply@pokeprecoms.app", "user@example.com", "titre", "corps", "https://x/1")
    assert "custom_args" not in post_mock.call_args.kwargs["json"]


def test_envoyer_email_avec_custom_args_les_transmet_a_sendgrid():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    with patch("connecteur_supabase_precoms.requests.post", return_value=reponse) as post_mock:
        _envoyer_email(
            "SG.xxx", "noreply@pokeprecoms.app", "user@example.com", "titre", "corps", "https://x/1",
            custom_args={"produit": "pokeprecoms", "type_notification": "precommande", "reference_id": "p1"},
        )
    assert post_mock.call_args.kwargs["json"]["custom_args"] == {
        "produit": "pokeprecoms", "type_notification": "precommande", "reference_id": "p1",
    }


# ------------------- _email_utilisateur -------------------

def test_email_utilisateur_erreur_reseau_retourne_none():
    with patch("connecteur_supabase_precoms.requests.get", side_effect=requests.RequestException("boom")):
        result = _email_utilisateur("https://x.supabase.co", "cle", "u1")
    assert result is None
