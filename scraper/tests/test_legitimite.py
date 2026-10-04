"""Tests de legitimite.py : parseurs des listes d'arnaques (cas reels du
04/10/2026 : l'encart "sites fiables" de la page Pokescam des arnaques ne
doit JAMAIS finir dans la liste noire) et detection SIRET."""

from unittest.mock import Mock

import requests

import legitimite as L


HTML_POKESCAM = '''
<aside>Voir les 50 sites fiables <a>pokesumo.com</a> Boutique vérifiée <a>pikadisplay.com</a></aside>
<h3 class="pap-sc-h"><a class="pap-sc-name" href="https://pokescam.com/arnaques/fantasy-sphere-fr-com/">fantasy-sphere-fr.com</a></h3>
<h3 class="pap-sc-h"><a class="pap-sc-name" href="https://pokescam.com/arnaques/x/">www.Faux-Shop.com</a></h3>
'''


def test_pokescam_ne_lit_que_les_fiches_arnaque_pas_lencart_sites_fiables():
    d = L.extraire_arnaques_pokescam(HTML_POKESCAM)
    assert d == {"fantasy-sphere-fr.com", "faux-shop.com"}
    assert "pokesumo.com" not in d and "pikadisplay.com" not in d


def test_pokegourou_lit_les_lignes_domaine_tiret_statut():
    html = "<ul><li>fantasy-sphere-fr.com — Arnaque confirmée</li><li>barons-tcg-france.com — </li></ul><p>facebook.fr</p>"
    d = L.extraire_arnaques_pokegourou(html)
    assert d == {"fantasy-sphere-fr.com", "barons-tcg-france.com"}


def test_le_vrai_site_nest_pas_confondu_avec_le_clone():
    d = L.extraire_arnaques_pokegourou("<li>fantasy-sphere-fr.com — Arnaque confirmée</li>")
    assert "fantasysphere.net" not in d


def test_charger_liste_noire_tolere_la_panne_dune_source():
    session = Mock()
    ok = Mock(status_code=200, text=HTML_POKESCAM)
    session.get.side_effect = [ok, requests.exceptions.ConnectTimeout()]
    assert L.charger_liste_noire(session) == {"fantasy-sphere-fr.com", "faux-shop.com"}


def test_charger_liste_noire_vide_si_tout_echoue():
    session = Mock()
    session.get.side_effect = requests.exceptions.ConnectionError()
    assert L.charger_liste_noire(session) == set()


def test_extraire_siret():
    assert L.extraire_siret("<p>SIRET : 934 557 091 00012</p>") == "93455709100012"
    assert L.extraire_siret("RCS Lyon 383 164 654") == "383164654"
    assert L.extraire_siret("Tel 01 23 45 67 89 siret non communique") is None
    assert L.extraire_siret("rien") is None


def _reponse(texte, code=200):
    return Mock(status_code=code, text=texte)


def test_verifier_legitimite_boutique_complete():
    session = Mock()
    session.get.side_effect = [
        _reponse('<a href="/pages/mentions-legales">ML</a>'),
        _reponse("Editeur : SARL X, SIRET 123 456 789 00012"),
    ]
    r = L.verifier_legitimite("boutique.fr", session)
    assert L.est_legitime(r) and r["siret"] == "12345678900012"


def test_verifier_legitimite_sans_siret():
    session = Mock()
    session.get.side_effect = [_reponse('<a href="/cgv">CGV</a>'), _reponse("Conditions generales sans identifiant")]
    r = L.verifier_legitimite("boutique.fr", session)
    assert not L.est_legitime(r) and "SIRET" in r["raison"]


def test_verifier_legitimite_certificat_invalide():
    session = Mock()
    session.get.side_effect = requests.exceptions.SSLError()
    r = L.verifier_legitimite("boutique.fr", session)
    assert r["https_ok"] is False and "certificat" in r["raison"]
