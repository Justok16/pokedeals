"""Tests de non-regression pour le coupe-circuit du repli API REST
WooCommerce (connecteur_woocommerce.py, ajoute le 16/08/2026 -- cf.
SESSION_NOTES.md, diagnostic du flake scan_lot_a / mymesis.fr bloque 7+
min sans jamais finir)."""

from unittest.mock import patch

from connecteur_woocommerce import ConnecteurWooCommerce


def _connecteur() -> ConnecteurWooCommerce:
    return ConnecteurWooCommerce("exemple.fr")


def test_decouvrir_produits_api_rest_succes_renvoie_ok_true():
    c = _connecteur()
    reponse = type("R", (), {
        "raise_for_status": lambda self: None,
        "json": lambda self: [{"id": 1, "name": "Dracaufeu"}],
    })()
    with patch.object(c.session, "get", return_value=reponse):
        produits, ok = c._decouvrir_produits_api_rest("Dracaufeu")
    assert ok is True
    assert produits == [{"id": 1, "name": "Dracaufeu"}]


def test_decouvrir_produits_api_rest_timeout_renvoie_ok_false():
    import requests
    c = _connecteur()
    with patch.object(c.session, "get", side_effect=requests.exceptions.Timeout("trop long")):
        produits, ok = c._decouvrir_produits_api_rest("Dracaufeu")
    assert ok is False
    assert produits == []


def test_coupe_circuit_sarrete_apres_3_echecs_consecutifs():
    # 6 criteres (noms uniques), tous en echec -- le coupe-circuit doit
    # arreter d'appeler l'API des le 4e nom (seuil = 3 echecs consecutifs),
    # sans jamais planter et sans jamais faire les 3 derniers appels reseau.
    c = _connecteur()
    criteres = [(f"Carte{i}", "199/165") for i in range(6)]
    with patch.object(c, "_decouvrir_produits_api_rest", return_value=([], False)) as appel_mock, \
         patch("connecteur_woocommerce.time.sleep"):
        resultats = c.rechercher_via_api_rest(criteres)
    assert appel_mock.call_count == 3  # coupe-circuit declenche pile au 3e echec
    assert len(resultats) == 6  # toutes les cles presentes, meme celles jamais interrogees
    assert all(v == [] for v in resultats.values())


def test_echec_non_consecutif_ne_declenche_pas_le_coupe_circuit():
    # 2 echecs, 1 succes, puis a nouveau des echecs -- le compteur doit se
    # reinitialiser sur le succes, donc jamais 3 echecs D'AFFILEE.
    c = _connecteur()
    criteres = [(f"Carte{i}", "199/165") for i in range(5)]
    sequence = [([], False), ([], False), ([{"id": 9, "name": "ok"}], True), ([], False), ([], False)]
    with patch.object(c, "_decouvrir_produits_api_rest", side_effect=sequence) as appel_mock, \
         patch("connecteur_woocommerce.time.sleep"):
        c.rechercher_via_api_rest(criteres)
    assert appel_mock.call_count == 5  # jamais abandonne : le succes du milieu a reinitialise le compteur


def test_tout_succes_naffecte_jamais_le_coupe_circuit():
    c = _connecteur()
    criteres = [(f"Carte{i}", "199/165") for i in range(5)]
    with patch.object(c, "_decouvrir_produits_api_rest", return_value=([], True)) as appel_mock, \
         patch("connecteur_woocommerce.time.sleep"):
        c.rechercher_via_api_rest(criteres)
    assert appel_mock.call_count == 5


def test_noms_deja_vus_ne_re_appellent_jamais_lapi():
    # Meme nom utilise par 2 criteres differents (numero different, ex.
    # alias) -- l'API ne doit etre interrogee qu'une seule fois par NOM.
    c = _connecteur()
    criteres = [("Dracaufeu", "199/165"), ("Dracaufeu", "056/165")]
    with patch.object(c, "_decouvrir_produits_api_rest", return_value=([], True)) as appel_mock, \
         patch("connecteur_woocommerce.time.sleep"):
        c.rechercher_via_api_rest(criteres)
    assert appel_mock.call_count == 1
