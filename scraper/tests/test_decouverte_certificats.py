"""Tests de decouverte_certificats.py (crt.sh) : parsing, garde-fous stricts,
tolerance aux pannes du service."""

from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

import requests

import decouverte_certificats as C

MAINTENANT = datetime(2026, 10, 4, tzinfo=timezone.utc)
ANCIEN = MAINTENANT - timedelta(days=400)
RECENT = MAINTENANT - timedelta(days=10)


def test_domaine_enregistrable():
    assert C.domaine_enregistrable("*.Shop.Pokemon-Cartes.fr") == "pokemon-cartes.fr"
    assert C.domaine_enregistrable("boutique.exemple.co.uk") == "exemple.co.uk"
    assert C.domaine_enregistrable("contact@exemple.fr") is None
    assert C.domaine_enregistrable("10.0.0.1") is None
    assert C.domaine_enregistrable("localhost") is None


def test_candidats_gardent_le_plus_ancien_certificat_et_exigent_le_mot_cle_dans_le_domaine():
    entrees = [
        {"not_before": "2026-08-01T00:00:00", "name_value": "pokemon-shop.com\nwww.pokemon-shop.com"},
        {"not_before": "2025-01-01T00:00:00", "name_value": "*.pokemon-shop.com"},
        {"not_before": "2026-01-01T00:00:00", "name_value": "pokemon.cdn-sans-rapport.net"},
        {"not_before": "2026-01-01T00:00:00", "name_value": "pokemon.com"},
        {"not_before": "invalide", "name_value": "pokemon-autre.fr"},
    ]
    c = C.candidats_depuis_entrees(entrees, "pokemon")
    assert set(c) == {"pokemon-shop.com"}
    assert c["pokemon-shop.com"].year == 2025


def _evaluer(domaine="boutique.com", debut=ANCIEN, noire=frozenset(), classer=lambda d: "shopify",
             verifier=lambda d: {"verdict": "singles"}, legit=lambda d: {"https_ok": True, "mentions_legales": True, "siret": "1", "raison": ""},
             francais=lambda d: True):
    return C.evaluer_candidat(domaine, debut, set(noire), MAINTENANT, classer, verifier, legit, francais)


def test_boutique_complete_est_ajoutee():
    assert _evaluer() == ("ajout", "shopify", "ok")


def test_arnaque_signalee_rejetee_en_premier():
    assert _evaluer(noire={"boutique.com"})[0] == "rejet"


def test_domaine_recent_mis_en_observation_sans_requete_reseau():
    classer = Mock()
    verdict, _, raison = _evaluer(debut=RECENT, classer=classer)
    assert verdict == "observation" and "60 jours" in raison
    classer.assert_not_called()


def test_site_non_francophone_rejete():
    assert _evaluer(francais=lambda d: False)[2] == "aucun produit en francais"


def test_plateforme_non_supportee_rejetee():
    assert _evaluer(classer=lambda d: None)[2] == "plateforme non supportee"


def test_catalogue_pokemon_insuffisant_rejete():
    assert _evaluer(verifier=lambda d: {"verdict": "insuffisant"})[2] == "catalogue Pokemon insuffisant"


def test_sans_siret_rejete():
    r = _evaluer(legit=lambda d: {"https_ok": True, "mentions_legales": True, "siret": None, "raison": "aucun SIRET"})
    assert r[0] == "rejet" and "SIRET" in r[2]


def test_crtsh_reessaie_puis_abandonne_sans_exception():
    s = Mock()
    s.get.side_effect = [Mock(status_code=502), requests.exceptions.ConnectTimeout(), Mock(status_code=404)]
    assert C.interroger_crtsh("pokemon", s, tentatives=3, pause=0) is None
    assert s.get.call_count == 3


def test_crtsh_reussit_apres_une_panne():
    ok = Mock(status_code=200)
    ok.json.return_value = [{"a": 1}]
    s = Mock()
    s.get.side_effect = [Mock(status_code=502), ok]
    assert C.interroger_crtsh("pokemon", s, tentatives=3, pause=0) == [{"a": 1}]


def test_ecriture_puis_relecture(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "FICHIER_CT", tmp_path / "boutiques_complement_ct.py")
    listes = {k: [] for k in C.CLES_LISTES}
    listes["woocommerce_sitemap"] = ["b.com", "a.com"]
    C.ecrire_listes_ct(listes)
    assert C.charger_listes_ct()["woocommerce_sitemap"] == ["a.com", "b.com"]


def test_site_etranger_vendant_des_produits_francais_accepte():
    s = Mock()
    ok = Mock(status_code=200)
    ok.json.return_value = {"products": [
        {"title": "Pokémon - Coffret Dresseur d'Élite 30e Anniversaire - FR"},
        {"title": "Booster Bundle 30e Anniversaire"},
        {"title": "Display 36 boosters français"},
        {"title": "Playmat"},
    ]}
    s.get.return_value = ok
    assert C.vend_des_produits_francais("shop-etranger.com", s) is True
    assert C.site_en_francais("shop-etranger.com", s) is True


def test_site_etranger_sans_produits_francais_refuse():
    s = Mock()
    r = Mock(status_code=200, text="<html lang='en'>")
    r.json.return_value = {"products": [{"title": "Pokemon TCG Elite Trainer Box"}, {"title": "Sleeves"}]}
    s.get.return_value = r
    assert C.vend_des_produits_francais("us-shop.com", s) is False
    assert C.site_en_francais("us-shop.com", s) is False
