"""Une variante commandable ne doit pas ouvrir une autre UPC/langue."""
from unittest.mock import Mock

import pytest

from precommandes_watchlist import PRODUITS_SURVEILLES
from radar_precommandes import scanner_shopify

PRODUITS = [p for p in PRODUITS_SURVEILLES if p.alerte_disponibilite]
MENTALI = next(p for p in PRODUITS if "Espeon" in p.nom)
NOCTALI = next(p for p in PRODUITS if "Umbreon" in p.nom)
BUNDLE = next(p for p in PRODUITS if "Booster Bundle" in p.nom)


def scanner(titre, description, variantes, produits):
    c = Mock()
    c.base_url = "https://exemple.fr"
    c.recuperer_tout_le_catalogue.return_value = [{
        "title": titre, "body_html": description, "handle": "produit",
        "variants": variantes,
    }]
    return scanner_shopify("exemple.fr", produits, c)


@pytest.mark.parametrize("mentali,noctali", [(True, False), (False, True), (False, False), (True, True)])
def test_stock_par_personnage(mentali, noctali):
    # Meme structure que la fiche LorenZone verifiee le 08/10/2026.
    r = scanner("Coffret Ultra-Premium (UPC) - 30ème Anniversaire",
                "Français. Mentali-ex Journée et Noctali-ex Soirée. Sortie 6 novembre 2026.", [
                    {"id": 1, "title": "Journée - Mentali-ex", "price": "259.90", "available": mentali},
                    {"id": 2, "title": "Soirée - Noctali-ex", "price": "299.90", "available": noctali},
                ], [MENTALI, NOCTALI])
    assert [(c["nom_produit"], c["en_stock"], c["prix"], c["url_produit"]) for c in r] == [
        (MENTALI.nom, mentali, 259.90, "https://exemple.fr/products/produit?variant=1"),
        (NOCTALI.nom, noctali, 299.90, "https://exemple.fr/products/produit?variant=2"),
    ]


def test_seule_variante_anglaise_disponible_n_ouvre_pas_le_francais():
    r = scanner("Booster Bundle 30e Anniversaire", "Versions françaises et anglaises", [
        {"id": 1, "title": "FR", "available": False, "price": "95.00"},
        {"id": 2, "title": "English", "available": True, "price": "39.00"},
    ], [BUNDLE])
    assert len(r) == 1
    assert r[0]["en_stock"] is False
    assert r[0]["prix"] == 95
    assert r[0]["url_produit"].endswith("variant=1")


def test_prix_variante_commandable_pas_premiere_variante_hors_stock():
    r = scanner("Booster Bundle 30e Anniversaire FR", "Français", [
        {"id": 1, "title": "Standard", "available": False, "price": "35.99"},
        {"id": 2, "title": "Standard scellé", "available": True, "price": "95.00"},
    ], [BUNDLE])
    assert len(r) == 1
    assert r[0]["en_stock"] is True
    assert r[0]["prix"] == 95


def test_available_manquant_reste_indetermine():
    r = scanner("Booster Bundle 30e Anniversaire FR", "Français", [
        {"id": 1, "title": "Default Title", "price": "95.00"},
    ], [BUNDLE])
    assert r[0]["en_stock"] is None


def test_fiche_sans_variante_reste_indeterminee():
    r = scanner("Booster Bundle 30e Anniversaire FR", "Français", [], [BUNDLE])
    assert r[0]["en_stock"] is None


def test_stock_string_false_n_est_pas_un_booleen_true():
    r = scanner("Booster Bundle 30e Anniversaire FR", "Français", [
        {"id": 1, "title": "Default Title", "available": "false", "price": "95.00"},
    ], [BUNDLE])
    assert r[0]["en_stock"] is None
