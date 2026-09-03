"""Tests de non-regression pour verification_alertes.py (ajoute le
03/09/2026 -- verification periodique de disponibilite/prix des alertes
watchlist_alerts pour le dashboard SaaS). Couvre : le dispatch par
plateforme, les 3 connecteurs (Shopify/PrestaShop/WooCommerce) sur un cas
"disponible" et un cas ou le garde-fou DOM doit forcer disponible=False
malgre un JSON-LD optimiste, et le cas eBay (volontairement non couvert,
doit toujours renvoyer None -- jamais une conclusion par exces de
confiance)."""

from unittest.mock import Mock, patch

import verification_alertes as va


def test_plateforme_boutique_reconnait_les_3_types():
    assert va._plateforme_boutique("kairyu.fr") == "shopify"
    assert va._plateforme_boutique("plazatcg.com") == "prestashop"
    assert va._plateforme_boutique("mymesis.fr") == "woocommerce"


def test_plateforme_boutique_ebay_non_couvert():
    assert va._plateforme_boutique("ebay.fr") is None


def test_domaine_depuis_url_retire_www():
    assert va._domaine_depuis_url("https://www.blazingtail.fr/59033-x.html") == "blazingtail.fr"


def test_verifier_shopify_disponible():
    with patch.object(va, "requests") as mrequests:
        reponse = Mock(status_code=200, ok=True)
        reponse.json.return_value = {"product": {"variants": [{"available": True, "price": "12.50"}]}}
        mrequests.get.return_value = reponse
        assert va._verifier_shopify("https://kairyu.fr/products/x") == {"disponible": True, "prix": 12.50}


def test_verifier_shopify_404_signifie_vendu_ou_supprime():
    with patch.object(va, "requests") as mrequests:
        mrequests.get.return_value = Mock(status_code=404)
        assert va._verifier_shopify("https://kairyu.fr/products/x") == {"disponible": False, "prix": None}


def _html_jsonld(prix: str, disponibilite: str = "https://schema.org/InStock") -> str:
    return (
        '<html><script type="application/ld+json">'
        f'{{"@type":"Product","offers":{{"price":"{prix}","priceCurrency":"EUR",'
        f'"availability":"{disponibilite}"}}}}'
        "</script></html>"
    )


def test_verifier_prestashop_disponible():
    with patch.object(va, "requests") as mrequests:
        mrequests.get.return_value = Mock(status_code=200, ok=True, text=_html_jsonld("29.90"))
        assert va._verifier_prestashop("https://plazatcg.com/x.html") == {"disponible": True, "prix": 29.90}


def test_verifier_prestashop_garde_fou_dom_force_indisponible():
    # JSON-LD annonce InStock, mais le span de rupture PrestaShop dit le
    # contraire -- le signal RENDU (DOM) doit toujours l'emporter (meme
    # garde-fou que connecteur_prestashop_sitemap.py).
    html = _html_jsonld("29.90").replace(
        "</html>", '<span id="product-availability">Rupture de stock</span></html>'
    )
    with patch.object(va, "requests") as mrequests:
        mrequests.get.return_value = Mock(status_code=200, ok=True, text=html)
        assert va._verifier_prestashop("https://plazatcg.com/x.html") == {"disponible": False, "prix": 29.90}


def test_verifier_woocommerce_disponible():
    with patch.object(va, "requests") as mrequests:
        mrequests.get.return_value = Mock(status_code=200, ok=True, text=_html_jsonld("18.90"))
        assert va._verifier_woocommerce("https://mymesis.fr/x/") == {"disponible": True, "prix": 18.90}


def test_verifier_woocommerce_garde_fou_dom_classe_outofstock():
    html = _html_jsonld("18.90").replace("<html>", '<html><div class="product outofstock">')
    with patch.object(va, "requests") as mrequests:
        mrequests.get.return_value = Mock(status_code=200, ok=True, text=html)
        assert va._verifier_woocommerce("https://mymesis.fr/x/") == {"disponible": False, "prix": 18.90}


def test_verifier_une_alerte_ebay_jamais_de_conclusion_par_defaut():
    # Plateforme non couverte -- doit toujours renvoyer None, jamais
    # interpreter l'absence de verification comme "indisponible".
    assert va.verifier_une_alerte("https://www.ebay.fr/itm/123456") is None


def test_verifier_shopify_erreur_reseau_renvoie_none():
    import requests as requests_reel

    with patch.object(va, "requests") as mrequests:
        mrequests.RequestException = requests_reel.RequestException
        mrequests.get.side_effect = requests_reel.RequestException("boom")
        assert va._verifier_shopify("https://kairyu.fr/products/x") is None
