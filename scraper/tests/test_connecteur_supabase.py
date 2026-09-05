"""Tests de non-regression pour connecteur_supabase.py -- systeme
OPTIONNEL et NON BLOQUANT (cf. module docstring) : secrets absents ou
erreur reseau -> no-op silencieux, jamais une exception qui remonte."""

from unittest.mock import Mock, patch

import requests

from connecteur_supabase import (
    TAILLE_PAGE_WATCHLIST,
    enregistrer_alertes,
    lister_alertes_a_notifier,
    lister_watchlist_items,
    marquer_notification_envoyee,
    trouver_correspondances,
)


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


def test_lister_trie_explicitement_par_created_at_croissant():
    # 03/09/2026 (signale par Justok) : sans ORDER BY explicite, l'ordre de
    # retour de PostgREST n'est pas garanti, ce dont watchlist_saas.
    # _grouper_par_carte() a pourtant besoin pour departager les egalites de
    # nb_utilisateurs avant d'appliquer MAX_CARTES_SAAS_EBAY.
    reponse = Mock()
    reponse.json.return_value = []
    reponse.raise_for_status = Mock()
    with patch("connecteur_supabase.requests.get", return_value=reponse) as get_mock:
        lister_watchlist_items("https://x.supabase.co", "cle-secrete")
    assert get_mock.call_args.kwargs["params"]["order"] == "created_at.asc"


def test_lister_pagine_au_dela_de_la_taille_de_page():
    # Audit externe du 30/08/2026 : Supabase/PostgREST plafonne une requete a
    # TAILLE_PAGE_WATCHLIST lignes par defaut -- sans pagination, les
    # utilisateurs au-dela de la 1ere page etaient silencieusement absents.
    page_pleine = [{"id": str(i)} for i in range(TAILLE_PAGE_WATCHLIST)]
    derniere_page = [{"id": "dernier"}]
    reponse1, reponse2 = Mock(), Mock()
    reponse1.json.return_value = page_pleine
    reponse1.raise_for_status = Mock()
    reponse2.json.return_value = derniere_page
    reponse2.raise_for_status = Mock()
    with patch("connecteur_supabase.requests.get", side_effect=[reponse1, reponse2]) as get_mock:
        items = lister_watchlist_items("https://x.supabase.co", "cle-secrete")
    assert len(items) == TAILLE_PAGE_WATCHLIST + 1
    assert items[-1] == {"id": "dernier"}
    assert get_mock.call_count == 2
    premier_range = get_mock.call_args_list[0].kwargs["headers"]["Range"]
    second_range = get_mock.call_args_list[1].kwargs["headers"]["Range"]
    assert premier_range == f"0-{TAILLE_PAGE_WATCHLIST - 1}"
    assert second_range == f"{TAILLE_PAGE_WATCHLIST}-{2 * TAILLE_PAGE_WATCHLIST - 1}"


def test_lister_page_exactement_pleine_puis_page_vide_arrete_la_pagination():
    # Cas limite : le nombre total de lignes est un multiple exact de
    # TAILLE_PAGE_WATCHLIST -- il faut quand meme redemander une page de
    # plus pour verifier qu'il n'y a rien derriere (elle revient vide).
    page_pleine = [{"id": str(i)} for i in range(TAILLE_PAGE_WATCHLIST)]
    reponse1, reponse2 = Mock(), Mock()
    reponse1.json.return_value = page_pleine
    reponse1.raise_for_status = Mock()
    reponse2.json.return_value = []
    reponse2.raise_for_status = Mock()
    with patch("connecteur_supabase.requests.get", side_effect=[reponse1, reponse2]) as get_mock:
        items = lister_watchlist_items("https://x.supabase.co", "cle-secrete")
    assert len(items) == TAILLE_PAGE_WATCHLIST
    assert get_mock.call_count == 2


def test_lister_erreur_reseau_en_cours_de_pagination_garde_les_pages_deja_recuperees():
    page_pleine = [{"id": str(i)} for i in range(TAILLE_PAGE_WATCHLIST)]
    reponse1 = Mock()
    reponse1.json.return_value = page_pleine
    reponse1.raise_for_status = Mock()
    with patch("connecteur_supabase.requests.get",
               side_effect=[reponse1, requests.RequestException("boom")]):
        items = lister_watchlist_items("https://x.supabase.co", "cle-secrete")
    assert len(items) == TAILLE_PAGE_WATCHLIST


def test_lister_url_avec_slash_final_normalisee():
    reponse = Mock()
    reponse.json.return_value = []
    reponse.raise_for_status = Mock()
    with patch("connecteur_supabase.requests.get", return_value=reponse) as get_mock:
        lister_watchlist_items("https://x.supabase.co/", "cle-secrete")
    args, _ = get_mock.call_args
    assert args[0] == "https://x.supabase.co/rest/v1/watchlist_items"


# ------------------- trouver_correspondances -------------------

def _item(nom_carte="Dracaufeu ex 199/165", langue="fr", prix_seuil=50.0, user_id="u1", item_id="i1", actif=True):
    return {"id": item_id, "user_id": user_id, "nom_carte": nom_carte, "langue": langue,
            "prix_seuil": prix_seuil, "actif": actif}


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


def test_carte_en_pause_nest_jamais_alertee():
    # Bug reel corrige le 05/09/2026 (audit externe multi-IA) : trouver_
    # correspondances() ne filtrait jamais `actif`, contrairement a
    # watchlist_saas._grouper_par_carte() (scan) -- un utilisateur en pause
    # sur une carte surveillee activement par quelqu'un d'autre (ou presente
    # dans config.yaml) continuait a recevoir des alertes pour elle.
    alertes = trouver_correspondances([_deal()], [_item(actif=False)])
    assert alertes == []


def test_carte_en_pause_nempeche_pas_lalerte_dun_autre_utilisateur_actif():
    alertes = trouver_correspondances(
        [_deal()], [_item(user_id="u1", item_id="i1", actif=False), _item(user_id="u2", item_id="i2", actif=True)])
    assert len(alertes) == 1
    assert alertes[0]["user_id"] == "u2"


def test_item_sans_colonne_actif_est_traite_comme_actif():
    item_sans_colonne = {"id": "i1", "user_id": "u1", "nom_carte": "Dracaufeu ex 199/165",
                          "langue": "fr", "prix_seuil": 50.0}
    alertes = trouver_correspondances([_deal()], [item_sans_colonne])
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


def test_plusieurs_deals_meme_carte_matchent_tous_le_meme_item():
    # Regression sur l'indexation par (nom_norm, langue) : chaque deal
    # partageant la même clé doit retrouver le(s) même(s) item(s) candidat(s),
    # pas seulement celui du dernier deal traité.
    deals = [_deal(url="https://x/1", total=30.0), _deal(url="https://x/2", total=45.0)]
    alertes = trouver_correspondances(deals, [_item()])
    assert {a["url"] for a in alertes} == {"https://x/1", "https://x/2"}
    assert all(a["watchlist_item_id"] == "i1" for a in alertes)


def test_items_de_cartes_differentes_ne_se_polluent_pas():
    items = [_item(nom_carte="Dracaufeu ex 199/165", item_id="i1"),
             _item(nom_carte="Tortank ex 200/165", item_id="i2")]
    alertes = trouver_correspondances([_deal(carte="Tortank ex 200/165")], items)
    assert len(alertes) == 1
    assert alertes[0]["watchlist_item_id"] == "i2"


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
    # Bug reel corrige le 31/08/2026 : sans on_conflict nommant la contrainte
    # unique (watchlist_item_id, url), PostgREST ne sait pas sur quoi
    # appliquer resolution=ignore-duplicates -- une alerte deja connue (carte
    # boutique restee sous le seuil sur plusieurs cycles, cas courant) fait
    # alors echouer TOUTE la requete en 409, y compris les alertes vraiment
    # nouvelles du meme lot.
    assert kwargs["params"]["on_conflict"] == "watchlist_item_id,url"
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


# ------------------- lister_alertes_a_notifier -------------------
# Audit externe du 30/08/2026 : une alerte dont push ET email echouaient au
# meme cycle n'etait auparavant plus jamais retentee (enregistrer_alertes()
# ne renvoie que les lignes fraichement inserees). Cette fonction est la
# correction : elle retrouve TOUTES les alertes encore en attente d'au moins
# un canal, cycle apres cycle, jusqu'a livraison reelle.

def test_lister_a_notifier_sans_secrets_ne_declenche_aucun_appel_reseau():
    with patch("connecteur_supabase.requests.get") as get_mock:
        alertes = lister_alertes_a_notifier("", "")
    assert alertes == []
    get_mock.assert_not_called()


def test_lister_a_notifier_succes_retourne_le_json():
    reponse = Mock()
    reponse.json.return_value = [{"id": "a1", "push_envoye": False, "email_envoye": True}]
    reponse.raise_for_status = Mock()
    with patch("connecteur_supabase.requests.get", return_value=reponse) as get_mock:
        alertes = lister_alertes_a_notifier("https://x.supabase.co", "cle-secrete")
    assert alertes == [{"id": "a1", "push_envoye": False, "email_envoye": True}]
    args, kwargs = get_mock.call_args
    assert args[0] == "https://x.supabase.co/rest/v1/watchlist_alerts"
    assert kwargs["params"]["or"] == "(push_envoye.eq.false,email_envoye.eq.false)"


def test_lister_a_notifier_erreur_reseau_retourne_liste_vide():
    with patch("connecteur_supabase.requests.get", side_effect=requests.RequestException("boom")):
        alertes = lister_alertes_a_notifier("https://x.supabase.co", "cle-secrete")
    assert alertes == []


def test_lister_a_notifier_pagine_au_dela_de_la_taille_de_page():
    page_pleine = [{"id": str(i)} for i in range(TAILLE_PAGE_WATCHLIST)]
    derniere_page = [{"id": "dernier"}]
    reponse1, reponse2 = Mock(), Mock()
    reponse1.json.return_value = page_pleine
    reponse1.raise_for_status = Mock()
    reponse2.json.return_value = derniere_page
    reponse2.raise_for_status = Mock()
    with patch("connecteur_supabase.requests.get", side_effect=[reponse1, reponse2]) as get_mock:
        alertes = lister_alertes_a_notifier("https://x.supabase.co", "cle-secrete")
    assert len(alertes) == TAILLE_PAGE_WATCHLIST + 1
    assert get_mock.call_count == 2


# ------------------- marquer_notification_envoyee -------------------

def test_marquer_sans_secrets_ne_declenche_aucun_appel_reseau():
    with patch("connecteur_supabase.requests.patch") as patch_mock:
        marquer_notification_envoyee("", "", "a1", "push")
    patch_mock.assert_not_called()


def test_marquer_canal_invalide_ne_declenche_aucun_appel_reseau():
    with patch("connecteur_supabase.requests.patch") as patch_mock:
        marquer_notification_envoyee("https://x.supabase.co", "cle-secrete", "a1", "sms")
    patch_mock.assert_not_called()


def test_marquer_push_envoie_bien_la_bonne_colonne():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    with patch("connecteur_supabase.requests.patch", return_value=reponse) as patch_mock:
        marquer_notification_envoyee("https://x.supabase.co", "cle-secrete", "a1", "push")
    args, kwargs = patch_mock.call_args
    assert args[0] == "https://x.supabase.co/rest/v1/watchlist_alerts"
    assert kwargs["params"]["id"] == "eq.a1"
    assert kwargs["json"] == {"push_envoye": True}


def test_marquer_email_envoie_bien_la_bonne_colonne():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    with patch("connecteur_supabase.requests.patch", return_value=reponse) as patch_mock:
        marquer_notification_envoyee("https://x.supabase.co", "cle-secrete", "a1", "email")
    args, kwargs = patch_mock.call_args
    assert kwargs["json"] == {"email_envoye": True}


def test_marquer_erreur_reseau_ne_leve_pas_dexception():
    with patch("connecteur_supabase.requests.patch", side_effect=requests.RequestException("boom")):
        marquer_notification_envoyee("https://x.supabase.co", "cle-secrete", "a1", "push")  # ne doit pas lever
