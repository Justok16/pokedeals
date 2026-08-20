"""Tests de non-regression pour le coupe-circuit 429 eBay (main.py, V61,
20/08/2026) -- cf. SESSION_NOTES.md : 2 episodes de blocage eBay generalise
les 19-20/08/2026, le second ayant annule 13 cycles consecutifs de
pokedeals.yml sur plus de 8h (chaque carte epuisait ses tentatives de
retry sans jamais completer le cycle dans le budget de 15 min, empechant
meme la sauvegarde de la memoire). Meme principe que le coupe-circuit deja
en place pour mymesis.fr (connecteur_woocommerce.py,
SEUIL_ECHECS_CONSECUTIFS_API_REST)."""

import time
from unittest.mock import Mock, patch

import requests

import main


def setup_function():
    # Chaque test repart d'un coupe-circuit propre -- _ebay_circuit est un
    # dict module-level partage, meme risque que _stats_fiabilite.
    main._reinitialiser_circuit_ebay()
    main._token_cache["token"] = "faux-token"
    main._token_cache["expire"] = time.time() + 9999


def _reponse_429():
    r = Mock()
    r.status_code = 429
    r.raise_for_status.side_effect = requests.exceptions.HTTPError(response=r)
    return r


def _reponse_ok(items=None):
    r = Mock()
    r.status_code = 200
    r.raise_for_status.side_effect = None
    r.json.return_value = {"itemSummaries": items or []}
    return r


def test_moins_de_3_echecs_429_ne_declenche_rien():
    with patch("main.requete_avec_retry", return_value=_reponse_429()):
        main.ebay_rechercher("Dracaufeu 199/165", "fr", {"EBAY_CLIENT_ID": "x", "EBAY_CLIENT_SECRET": "y"})
        main.ebay_rechercher("Pikachu 173/165", "fr", {"EBAY_CLIENT_ID": "x", "EBAY_CLIENT_SECRET": "y"})
    assert main._ebay_circuit["abandonne"] is False


def test_3_echecs_429_consecutifs_declenche_le_coupe_circuit():
    with patch("main.requete_avec_retry", return_value=_reponse_429()):
        for nom in ("Dracaufeu 199/165", "Pikachu 173/165", "Mew 193/165"):
            main.ebay_rechercher(nom, "fr", {"EBAY_CLIENT_ID": "x", "EBAY_CLIENT_SECRET": "y"})
    assert main._ebay_circuit["abandonne"] is True


def test_un_succes_entre_deux_echecs_remet_le_compteur_a_zero():
    sequence = [_reponse_429(), _reponse_ok(), _reponse_429(), _reponse_429()]
    with patch("main.requete_avec_retry", side_effect=sequence):
        for nom in ("Dracaufeu 199/165", "Pikachu 173/165", "Mew 193/165", "Evoli 167/131"):
            main.ebay_rechercher(nom, "fr", {"EBAY_CLIENT_ID": "x", "EBAY_CLIENT_SECRET": "y"})
    # 4 appels : 429, OK (reset), 429, 429 -- jamais 3 D'AFFILEE
    assert main._ebay_circuit["abandonne"] is False


def test_erreur_non_429_ne_declenche_pas_le_coupe_circuit():
    # Une vraie panne reseau (pas un 429) ne doit pas etre traitee comme un
    # signal de rate-limiting -- portee volontairement etroite (V61,
    # coupe-circuit specifique au blocage constate, pas une panne generique).
    with patch("main.requete_avec_retry", side_effect=requests.exceptions.ConnectionError("panne")):
        for nom in ("Dracaufeu 199/165", "Pikachu 173/165", "Mew 193/165"):
            main.ebay_rechercher(nom, "fr", {"EBAY_CLIENT_ID": "x", "EBAY_CLIENT_SECRET": "y"})
    assert main._ebay_circuit["abandonne"] is False


def test_une_fois_declenche_ebay_rechercher_ne_fait_plus_aucun_appel_reseau():
    main._ebay_circuit["abandonne"] = True
    with patch("main.requete_avec_retry") as appel_mock:
        resultat = main.ebay_rechercher("Dracaufeu 199/165", "fr", {"EBAY_CLIENT_ID": "x", "EBAY_CLIENT_SECRET": "y"})
    assert resultat == []
    appel_mock.assert_not_called()


def test_recherche_alias_sautee_si_le_coupe_circuit_se_declenche_sur_la_recherche_principale():
    # Le 3e 429 D'AFFILEE tombe pile sur la recherche PRINCIPALE de cette
    # carte -- la recherche alias qui suit ne doit plus etre tentee.
    main._ebay_circuit["echecs_consecutifs"] = 2
    with patch("main.requete_avec_retry", return_value=_reponse_429()) as appel_mock:
        main.ebay_rechercher("Blastoise 202/165", "fr",
                             {"EBAY_CLIENT_ID": "x", "EBAY_CLIENT_SECRET": "y"}, alias="Tortank")
    assert main._ebay_circuit["abandonne"] is True
    appel_mock.assert_called_once()  # seule la recherche principale a ete tentee


def test_reinitialiser_circuit_ebay_remet_tout_a_zero():
    main._ebay_circuit["echecs_consecutifs"] = 5
    main._ebay_circuit["abandonne"] = True
    main._reinitialiser_circuit_ebay()
    assert main._ebay_circuit == {"echecs_consecutifs": 0, "abandonne": False}


def test_recherche_reussie_renvoie_bien_les_annonces():
    with patch("main.requete_avec_retry", return_value=_reponse_ok([{"itemId": "1", "price": {"value": "10.0", "currency": "EUR"}, "itemLocation": {"country": "FR"}, "shippingOptions": [{"shippingCost": {"value": "3.0"}}], "title": "Dracaufeu 199/165"}])):
        resultat = main.ebay_rechercher("Dracaufeu 199/165", "fr", {"EBAY_CLIENT_ID": "x", "EBAY_CLIENT_SECRET": "y"})
    assert len(resultat) == 1
    assert resultat[0]["prix"] == 10.0


# ------------------- verifier_circuit_ebay (alerte Telegram, V61) -------------------
# Meme principe que verifier_fiabilite_plateformes() (Vinted/Leboncoin) : signale
# sur Telegram quand le coupe-circuit se declenche, avec le meme anti-spam
# (DELAI_ANTI_SPAM_FIABILITE, 6h) pour ne pas spammer a chaque cycle de 15 min
# tant qu'un blocage eBay persiste (cas vecu : 13 cycles consecutifs).

def test_verifier_circuit_ebay_silencieux_si_coupe_circuit_non_declenche():
    assert main._ebay_circuit["abandonne"] is False
    assert main.verifier_circuit_ebay({}) == []


def test_verifier_circuit_ebay_alerte_si_coupe_circuit_declenche():
    main._ebay_circuit["abandonne"] = True
    main._ebay_circuit["echecs_consecutifs"] = 3
    alertes = main.verifier_circuit_ebay({})
    assert len(alertes) == 1
    assert "eBay" in alertes[0]
    assert "429" in alertes[0]


def test_verifier_circuit_ebay_respecte_lanti_spam():
    main._ebay_circuit["abandonne"] = True
    vues = {}
    premiere = main.verifier_circuit_ebay(vues)
    assert len(premiere) == 1
    # Meme cycle "declenche" derechef (comme un cycle suivant qui retrouve
    # le coupe-circuit encore actif) -- pas de 2e alerte avant le delai anti-spam.
    seconde = main.verifier_circuit_ebay(vues)
    assert seconde == []
