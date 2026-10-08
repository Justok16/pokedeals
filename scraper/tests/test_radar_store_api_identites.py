"""La deduplication Store API ne doit pas perdre un autre produit suivi."""
from unittest.mock import patch

from connecteur_woocommerce import ConnecteurWooCommerce
from precommandes_watchlist import PRODUITS_SURVEILLES
from radar_precommandes import scanner_woocommerce_api_rest

MENTALI = next(p for p in PRODUITS_SURVEILLES if "Espeon" in p.nom)
NOCTALI = next(p for p in PRODUITS_SURVEILLES if "Umbreon" in p.nom)


def page(identifiant=9, **champs):
    return {"id": identifiant, "name": "UPC 30e Anniversaire Noctali FR",
            "description": "Version française, sortie 6 novembre 2026",
            "permalink": "https://exemple.fr/produit/noctali/",
            "prices": {"price": "37500", "currency_minor_unit": 2},
            "is_in_stock": True, "is_purchasable": True, **champs}


def scan(p):
    with patch.object(ConnecteurWooCommerce, "_decouvrir_produits_api_rest", return_value=([p], True)), \
         patch("radar_precommandes.time.sleep"):
        return scanner_woocommerce_api_rest("exemple.fr", [MENTALI, NOCTALI])


def test_noctali_trouve_par_la_premiere_recherche_mentali_est_conserve():
    r = scan(page())
    assert len(r) == 1
    assert r[0]["nom_produit"] == NOCTALI.nom
    assert r[0]["prix"] == 375
    assert r[0]["en_stock"] is True


def test_non_achetable_prime_sur_le_stock():
    r = scan(page(is_purchasable=False))
    assert r[0]["en_stock"] is False


def test_stock_absent_reste_indetermine():
    p = page()
    del p["is_in_stock"]
    assert scan(p)[0]["en_stock"] is None


def test_vitrine_anglaise_en_ignoree_pour_eviter_les_doublons():
    """08/10/2026 (pixelheart.eu) : meme produit sur /fr/ et /en/, deux ID."""
    fr = page(1, permalink="https://exemple.fr/fr/produit/noctali/")
    en = page(2, permalink="https://exemple.fr/en/produit/noctali/")
    with patch.object(ConnecteurWooCommerce, "_decouvrir_produits_api_rest", return_value=([fr, en], True)), \
         patch("radar_precommandes.time.sleep"):
        r = scanner_woocommerce_api_rest("exemple.fr", [NOCTALI])
    assert [c["url_produit"] for c in r] == ["https://exemple.fr/fr/produit/noctali/"]
