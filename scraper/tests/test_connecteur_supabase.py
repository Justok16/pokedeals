"""Tests de non-regression pour connecteur_supabase.py -- systeme
OPTIONNEL et NON BLOQUANT (cf. module docstring) : secrets absents ou
erreur reseau -> no-op silencieux, jamais une exception qui remonte."""

from unittest.mock import Mock, patch

import requests

from connecteur_supabase import enregistrer_alertes, lister_watchlist_items, trouver_correspondances


# ------------------- lister_watchlist_items -------------------

def test_lister_sans_secrets_ne_declenche_aucun_appel_reseau():
    with patch("connecteur_supabase.requests.get") as get_mock:
        items = lister_watchlist_items("", "")
    assert items == []
    get_mock.assert_not_called()


def test_lister_url_sans_cle_ne_declenche_aucun_appel_reseau():
    with patch("connecteur_supabase.requests.get") as get_mock:
        items = lister_watchlist_items("https://x.supabase.co", "")
    assert items == []
    get_mock.assert_not_called()


def test_lister_erreur_reseau_retourne_liste_vide():
    with patch("connecteur_supabase.requests.get", side_effect=requests.RequestException("boom")):
        items = lister_watchlist_items("https://x.supabase.co", "cle-secrete")
    assert items == []


def test_lister_succes_retourne_le_json():
    reponse = Mock()
    reponse.json.return_value = [{"id": "1", "nom_carte": "Dracaufeu ex 199/165"}]
    reponse.raise_for_status = Mock()
    with patch("connecteur_supabase.requests.get", return_value=reponse) as get_mock:
        items = lister_watchlist_items("https://x.supabase.co", "cle-secrete")
    assert items == [{"id": "1", "nom_carte": "Dracaufeu ex 199/165"}]
    args, kwargs = get_mock.call_args
    assert args[0] == "https://x.supabase.co/rest/v1/watchlist_items"
    assert kwargs["headers"]["apikey"] == "cle-secrete"


def test_lister_url_avec_slash_final_normalisee():
    reponse = Mock()
    reponse.json.return_value = []
    reponse.raise_for_status = Mock()
    with patch("connecteur_supabase.requests.get", return_value=reponse) as get_mock:
        lister_watchlist_items("https://x.supabase.co/", "cle-secrete")
    args, _ = get_mock.call_args
    assert args[0] == "https://x.supabase.co/rest/v1/watchlist_items"


# ------------------- trouver_correspondances -------------------

def _item(nom_carte="Dracaufeu ex 199/165", langue="fr", prix_seuil=50.0, user_id="u1", item_id="i1"):
    return {"id": item_id, "user_id": user_id, "nom_carte": nom_carte, "langue": langue, "prix_seuil": prix_seuil}


def _deal(carte="Dracaufeu ex 199/165", langue="fr", total=40.0, titre="Belle carte", url="https://x/1"):
    return {"carte": carte, "langue": langue, "total": total, "titre": titre, "url": url, "plateforme": "eBay"}


def test_correspondance_simple():
    alertes = trouver_correspondances([_deal()], [_item()])
    assert len(alertes) == 1
    assert alertes[0]["user_id"] == "u1"
    assert alertes[0]["watchlist_item_id"] == "i1"
    assert alertes[0]["prix"] == 40.0


def test_pas_de_correspondance_nom_different():
    alertes = trouver_correspondances([_deal(carte="Tortank ex 200/165")], [_item()])
    assert alertes == []


def test_pas_de_correspondance_langue_differente():
    alertes = trouver_correspondances([_deal(langue="jp")], [_item(langue="fr")])
    assert alertes == []


def test_pas_de_correspondance_prix_au_dessus_du_seuil():
    alertes = trouver_correspondances([_deal(total=60.0)], [_item(prix_seuil=50.0)])
    assert alertes == []


def test_correspondance_nom_insensible_a_la_casse_et_accents():
    alertes = trouver_correspondances(
        [_deal(carte="DRACAUFEU EX 199/165")], [_item(nom_carte="dracaufeu ex 199/165")])
    assert len(alertes) == 1


def test_liste_deals_vide_retourne_liste_vide():
    assert trouver_correspondances([], [_item()]) == []


def test_liste_items_vide_retourne_liste_vide():
    assert trouver_correspondances([_deal()], []) == []


def test_item_avec_seuil_invalide_est_ignore():
    alertes = trouver_correspondances([_deal()], [_item(prix_seuil="pas-un-nombre")])
    assert alertes == []


def test_plusieurs_utilisateurs_meme_carte_donnent_plusieurs_alertes():
    items = [_item(user_id="u1", item_id="i1"), _item(user_id="u2", item_id="i2")]
    alertes = trouver_correspondances([_deal()], items)
    assert {a["user_id"] for a in alertes} == {"u1", "u2"}


# ------------------- enregistrer_alertes -------------------

def test_enregistrer_liste_vide_ne_declenche_aucun_appel_reseau():
    with patch("connecteur_supabase.requests.post") as post_mock:
        enregistrer_alertes("https://x.supabase.co", "cle-secrete", [])
    post_mock.assert_not_called()


def test_enregistrer_sans_secrets_ne_declenche_aucun_appel_reseau():
    with patch("connecteur_supabase.requests.post") as post_mock:
        enregistrer_alertes("", "", [{"user_id": "u1"}])
    post_mock.assert_not_called()


def test_enregistrer_erreur_reseau_ne_leve_pas_dexception():
    with patch("connecteur_supabase.requests.post", side_effect=requests.RequestException("boom")):
        enregistrer_alertes("https://x.supabase.co", "cle-secrete", [{"user_id": "u1"}])  # ne doit pas lever


def test_enregistrer_succes_envoie_bien_les_alertes():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    alertes = [{"user_id": "u1", "watchlist_item_id": "i1", "titre": "t", "prix": 10.0, "url": "https://x/1"}]
    reponse.json.return_value = alertes
    with patch("connecteur_supabase.requests.post", return_value=reponse) as post_mock:
        nouvelles = enregistrer_alertes("https://x.supabase.co", "cle-secrete", alertes)
    args, kwargs = post_mock.call_args
    assert args[0] == "https://x.supabase.co/rest/v1/watchlist_alerts"
    assert kwargs["json"] == alertes
    assert "ignore-duplicates" in kwargs["headers"]["Prefer"]
    assert "return=representation" in kwargs["headers"]["Prefer"]
    assert nouvelles == alertes


def test_enregistrer_ne_retourne_que_les_lignes_reellement_inserees():
    """Les doublons ignores (resolution=ignore-duplicates) n'apparaissent pas
    dans la reponse -- notifications_saas.py depend de ce comportement pour
    ne pas re-notifier une alerte deja connue."""
    reponse = Mock()
    reponse.raise_for_status = Mock()
    reponse.json.return_value = []  # tout etait deja connu, rien de nouveau
    with patch("connecteur_supabase.requests.post", return_value=reponse):
        nouvelles = enregistrer_alertes(
            "https://x.supabase.co", "cle-secrete",
            [{"user_id": "u1", "watchlist_item_id": "i1", "titre": "t", "prix": 10.0, "url": "https://x/1"}])
    assert nouvelles == []


def test_enregistrer_liste_vide_retourne_liste_vide():
    assert enregistrer_alertes("https://x.supabase.co", "cle-secrete", []) == []


def test_enregistrer_erreur_reseau_retourne_liste_vide():
    with patch("connecteur_supabase.requests.post", side_effect=requests.RequestException("boom")):
        nouvelles = enregistrer_alertes("https://x.supabase.co", "cle-secrete", [{"user_id": "u1"}])
    assert nouvelles == []
