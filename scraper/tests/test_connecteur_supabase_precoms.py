"""Tests de non-regression pour connecteur_supabase_precoms.py -- systeme
OPTIONNEL et NON BLOQUANT (cf. module docstring) : service gratuit et
illimite, modele BROADCAST (tous les utilisateurs inscrits recoivent
toutes les alertes), erreur reseau -> log + skip, jamais une exception qui
remonte."""

from unittest.mock import Mock, patch

import requests

from connecteur_supabase_precoms import (
    _email_utilisateur,
    _lister_abonnements_push,
    _lister_tous_utilisateurs,
    _preferences_email,
    enregistrer_precommande_alertes,
    notifier_abonnes_precoms,
)


def _evenement(titre="ETB 30e Anniversaire", domaine="boutique.fr",
               url="https://boutique.fr/products/etb-30e", prix=59.99):
    return {"titre": titre, "domaine": domaine, "url_produit": url, "prix": prix}


def _precommande(titre_produit="ETB 30e Anniversaire", boutique="boutique.fr",
                  url_produit="https://boutique.fr/products/etb-30e"):
    return {"titre_produit": titre_produit, "boutique": boutique, "url_produit": url_produit}


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


def test_enregistrer_erreur_reseau_retourne_liste_vide():
    with patch("connecteur_supabase_precoms.requests.post",
               side_effect=requests.RequestException("boom")):
        result = enregistrer_precommande_alertes("https://x.supabase.co", "cle", [_evenement()])
    assert result == []


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


def test_notifier_push_actif_notifie_tous_les_utilisateurs_abonnes_au_push():
    secrets = {
        "POKEPRECOMS_SUPABASE_URL": "https://x.supabase.co", "POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY": "k",
        "VAPID_PRIVATE_KEY": "priv", "VAPID_CLAIM_EMAIL": "a@b.com",
    }
    with patch("connecteur_supabase_precoms._lister_tous_utilisateurs", return_value=["u1", "u2"]), \
         patch("connecteur_supabase_precoms._lister_abonnements_push",
               return_value=[{"user_id": "u1", "endpoint": "e1", "p256dh": "p", "auth": "a"}]), \
         patch("connecteur_supabase_precoms._preferences_email", return_value={}) as pref_mock, \
         patch("connecteur_supabase_precoms._envoyer_push") as push_send_mock, \
         patch("connecteur_supabase_precoms._envoyer_email") as email_send_mock:
        notifier_abonnes_precoms(secrets, [_precommande()])
    # Seul u1 a un abonnement push -- u2 (inscrit mais pas abonné push) n'est pas notifié par push.
    push_send_mock.assert_called_once()
    email_send_mock.assert_not_called()
    pref_mock.assert_not_called()  # email désactivé -> pas besoin des préférences


def test_notifier_email_actif_notifie_tous_les_utilisateurs_sans_preference_desactivee():
    secrets = {
        "POKEPRECOMS_SUPABASE_URL": "https://x.supabase.co", "POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY": "k",
        "RESEND_API_KEY": "re_xxx", "RESEND_FROM_EMAIL": "noreply@pokeprecoms.app",
    }
    with patch("connecteur_supabase_precoms._lister_tous_utilisateurs", return_value=["u1", "u2"]), \
         patch("connecteur_supabase_precoms._lister_abonnements_push") as push_list_mock, \
         patch("connecteur_supabase_precoms._preferences_email", return_value={"u1": False}), \
         patch("connecteur_supabase_precoms._email_utilisateur", return_value="user@example.com") as lookup_mock, \
         patch("connecteur_supabase_precoms._envoyer_email") as email_send_mock:
        notifier_abonnes_precoms(secrets, [_precommande()])
    push_list_mock.assert_not_called()  # push désactivé -> pas besoin des abonnements
    # u1 a désactivé l'email, seul u2 (actif par défaut) est notifié.
    assert lookup_mock.call_count == 1
    email_send_mock.assert_called_once()


def test_notifier_deux_precommandes_meme_utilisateur_email_recherche_une_seule_fois():
    secrets = {
        "POKEPRECOMS_SUPABASE_URL": "https://x.supabase.co", "POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY": "k",
        "RESEND_API_KEY": "re_xxx", "RESEND_FROM_EMAIL": "noreply@pokeprecoms.app",
    }
    precommandes = [_precommande(url_produit="https://x/1"), _precommande(url_produit="https://x/2")]
    with patch("connecteur_supabase_precoms._lister_tous_utilisateurs", return_value=["u1"]), \
         patch("connecteur_supabase_precoms._preferences_email", return_value={}), \
         patch("connecteur_supabase_precoms._email_utilisateur", return_value="user@example.com") as lookup_mock, \
         patch("connecteur_supabase_precoms._envoyer_email") as email_send_mock:
        notifier_abonnes_precoms(secrets, precommandes)
    lookup_mock.assert_called_once()
    assert email_send_mock.call_count == 2


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


# ------------------- _preferences_email -------------------

def test_preferences_email_erreur_reseau_retourne_dict_vide():
    with patch("connecteur_supabase_precoms.requests.get", side_effect=requests.RequestException("boom")):
        result = _preferences_email("https://x.supabase.co", "cle", ["u1"])
    assert result == {}


# ------------------- _email_utilisateur -------------------

def test_email_utilisateur_erreur_reseau_retourne_none():
    with patch("connecteur_supabase_precoms.requests.get", side_effect=requests.RequestException("boom")):
        result = _email_utilisateur("https://x.supabase.co", "cle", "u1")
    assert result is None
