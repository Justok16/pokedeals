"""Fiches WooCommerce/PrestaShop du radar des 30 ans : trois faux negatifs
reels du 08/10/2026 sur missplaybros.com (ETB, Bundle et Mini Tin 30e FR
jamais detectes)."""

import json

import precommandes_watchlist as w
import radar_precommandes as r
from connecteur_prestashop_sitemap import _extraire_jsonld_produit
from connecteur_shopify import prix_offre


def _page(description, autres_produits="", ld_attrs=' class="rank-math-schema-pro"'):
    ld = {"@context": "https://schema.org/", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": []},
        {"@type": "Product", "name": "ETB 30e", "description": description,
         "offers": [{"@type": "Offer", "availability": "https://schema.org/InStock", "priceValidUntil": "2027-12-31",
                     "priceSpecification": [{"@type": "UnitPriceSpecification", "price": "110.00"}]}]}]}
    return (f'<html><head><title>ETB - Coffret Dresseur d&#039;Élite Pokémon 30e Anniversaire (ME 5.5) - Version Française</title>'
            f'<script type="application/ld+json"{ld_attrs}>{json.dumps(ld)}</script></head><body>'
            f'<h1>ETB Pokémon 30e Anniversaire</h1><p>{description}</p>'
            f'<section class="related">{autres_produits}</section></body></html>')


def test_jsonld_graph_avec_attributs_et_price_specification():
    produit = _extraire_jsonld_produit(_page("Coffret officiel en français."))
    assert produit and produit["@type"] == "Product"
    assert prix_offre(produit["offers"][0]) == 110.0
    assert prix_offre({"price": "12,5"}) is None and prix_offre({"price": "12.5"}) == 12.5


def test_mots_exclus_cherches_dans_la_description_du_produit_seulement():
    etb = next(p for p in w.PRODUITS_SURVEILLES if p.nom.startswith("Coffret Dresseur d'Élite — 30e Anniversaire FR"))
    titre = "ETB - Coffret Dresseur d'Élite Pokémon 30e Anniversaire - Version Française"
    page = "Coffret officiel en français. Vous aimerez aussi : Pikachu promo Pokémon Center Japonais"
    assert w.evaluer_correspondance(titre, page, etb)[0] is None                       # page entiere : rejete
    assert w.evaluer_correspondance(titre, page, etb, "Coffret officiel en français.")[0] == "moyenne"
    assert w.evaluer_correspondance(titre, page, etb, "Import japonais.")[0] is None   # description propre : rejete


class _Reponse:
    def __init__(self, html):
        self.content = html.encode("utf-8")

    def raise_for_status(self):
        pass


class _FauxConnecteur:
    nom_affiche = "boutique.fr"

    def __init__(self, html):
        self.session = self
        self._html = html

    def get(self, url, **_):
        return _Reponse(self._html)


def test_fiche_detectee_malgre_autres_produits_et_date_de_validite_du_prix(monkeypatch):
    monkeypatch.setattr(r, "DELAI_ENTRE_PAGES", 0)
    html = _page("Coffret Dresseur d'Élite officiel, version française.",
                 autres_produits="<a>Carte Pikachu promo Pokémon Center – Japonais</a>")
    produits = [p for p in w.PRODUITS_SURVEILLES if p.alerte_disponibilite]
    cand = r._evaluer_page(_FauxConnecteur(html), "https://boutique.fr/produit/etb-30e/", produits)
    assert {(c["nom_produit"], c["prix"], c["en_stock"]) for c in cand} == {
        ("Coffret Dresseur d'Élite — 30e Anniversaire FR (suivi restock)", 110.0, True)}


def _page_dispo(disponibilite):
    ld = {"@type": "Product", "name": "UPC", "description": "Version française.",
          "offers": {"@type": "Offer", "price": "429.90", "availability": disponibilite}}
    return (f'<html><head><title>UPC Noctali 30e Anniversaire - Version Française</title>'
            f'<script type="application/ld+json">{json.dumps(ld)}</script></head><body>'
            f'<p class="stock available-on-backorder">Produit en précommande</p>'
            f'<button class="single_add_to_cart_button">Ajouter</button></body></html>')


def test_schema_org_en_http_et_precommande_comptent_comme_commandables():
    """08/10/2026 (pixelheart.eu) : "http://schema.org/BackOrder" lu en rupture."""
    assert r._extraire_prix_et_stock(_page_dispo("http://schema.org/InStock"), "woocommerce") == (429.9, True)
    assert r._extraire_prix_et_stock(_page_dispo("http://schema.org/BackOrder"), "woocommerce") == (429.9, True)
    assert r._extraire_prix_et_stock(_page_dispo("https://schema.org/PreOrder"), "prestashop")[1] is True
    assert r._extraire_prix_et_stock(_page_dispo("http://schema.org/OutOfStock"), "woocommerce")[1] is False
