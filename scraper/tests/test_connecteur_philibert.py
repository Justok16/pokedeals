"""Tests de non-regression pour connecteur_philibert.py -- boutique DEDIEE
(sitemap filtre par mot-cle, pas de repli generique) car philibertnet.com
est trop volumineuse (457k+ produits) pour la strategie generique de
connecteur_prestashop_sitemap.py."""

from unittest.mock import Mock, patch

import requests

from connecteur_philibert import (
    _extraire_produit,
    lister_urls_pokemon_sitemap,
    scanner_philibert_precommandes_generiques,
)


# ------------------- lister_urls_pokemon_sitemap -------------------

def test_lister_urls_filtre_sur_le_mot_cle_pokemon():
    connecteur = Mock()
    connecteur._decouvrir_sitemaps_racine.return_value = ["https://philibertnet.com/sitemap.xml"]
    connecteur._lister_urls_recursif.return_value = [
        "https://philibertnet.com/fr/1-coffret-pokemon.html",
        "https://philibertnet.com/fr/2-jeu-de-societe.html",
        "https://philibertnet.com/fr/3-etb-POKEMON-ecarlate.html",
    ]
    result = lister_urls_pokemon_sitemap(connecteur)
    assert result == [
        "https://philibertnet.com/fr/1-coffret-pokemon.html",
        "https://philibertnet.com/fr/3-etb-POKEMON-ecarlate.html",
    ]


def test_lister_urls_sans_sitemap_renvoie_liste_vide():
    connecteur = Mock()
    connecteur._decouvrir_sitemaps_racine.return_value = []
    result = lister_urls_pokemon_sitemap(connecteur)
    assert result == []


# ------------------- _extraire_produit -------------------

def _reponse(status_code=200, text=""):
    r = Mock()
    r.status_code = status_code
    r.text = text
    return r


def test_extraire_produit_via_jsonld():
    html = """
    <script type="application/ld+json">
    {"@type": "Product", "name": "Coffret Pokémon ETB", "description": "Précommande",
     "offers": {"price": "59.99", "availability": "https://schema.org/InStock"}}
    </script>
    """
    with patch("connecteur_philibert.requests.get", return_value=_reponse(text=html)):
        r = _extraire_produit("https://philibertnet.com/fr/1-x.html")
    assert r["titre"] == "Coffret Pokémon ETB"
    assert r["description"] == "Précommande"
    assert r["en_stock"] is True
    assert r["prix"] == 59.99


def test_extraire_produit_via_microdata_si_pas_de_jsonld():
    html = (
        '<span itemprop="price" content="19.90"></span>'
        '<span itemprop="priceCurrency" content="EUR"></span>'
        '<span itemprop="availability" content="https://schema.org/InStock"></span>'
        '<h1 itemprop="name">Booster Pokémon</h1>'
    )
    with patch("connecteur_philibert.requests.get", return_value=_reponse(text=html)):
        r = _extraire_produit("https://philibertnet.com/fr/2-x.html")
    assert r["titre"] == "Booster Pokémon"
    assert r["en_stock"] is True
    assert r["prix"] == 19.90


def test_extraire_produit_dom_rupture_force_en_stock_false_meme_si_jsonld_dit_instock():
    html = """
    <span id="product-availability">Rupture de stock</span>
    <script type="application/ld+json">
    {"@type": "Product", "name": "X", "offers": {"price": "10", "availability": "https://schema.org/InStock"}}
    </script>
    """
    with patch("connecteur_philibert.requests.get", return_value=_reponse(text=html)):
        r = _extraire_produit("https://philibertnet.com/fr/3-x.html")
    assert r["en_stock"] is False


def test_extraire_produit_sans_donnees_structurees_renvoie_none():
    with patch("connecteur_philibert.requests.get", return_value=_reponse(text="<html>rien</html>")):
        r = _extraire_produit("https://philibertnet.com/fr/4-x.html")
    assert r is None


def test_extraire_produit_erreur_http_renvoie_none():
    with patch("connecteur_philibert.requests.get", return_value=_reponse(status_code=404)):
        r = _extraire_produit("https://philibertnet.com/fr/5-x.html")
    assert r is None


def test_extraire_produit_erreur_reseau_renvoie_none():
    with patch("connecteur_philibert.requests.get", side_effect=requests.RequestException("boom")):
        r = _extraire_produit("https://philibertnet.com/fr/6-x.html")
    assert r is None


# ------------------- scanner_philibert_precommandes_generiques -------------------

def test_scanner_filtre_les_non_candidats_precommande():
    urls = ["https://philibertnet.com/fr/1-x.html", "https://philibertnet.com/fr/2-x.html"]
    produits = [
        {"titre": "Coffret ETB Précommande Pokémon", "description": "", "en_stock": True, "prix": 59.99},
        {"titre": "Jeu de société non Pokémon", "description": "", "en_stock": True, "prix": 20.0},
    ]
    with patch("connecteur_philibert._extraire_produit", side_effect=produits), \
         patch("connecteur_philibert.time.sleep"):
        candidats = scanner_philibert_precommandes_generiques(urls)
    assert len(candidats) == 1
    assert candidats[0]["domaine"] == "philibertnet.com"
    assert candidats[0]["url_produit"] == urls[0]
    assert candidats[0]["categorie"] == "ETB"


def test_scanner_ignore_les_pages_sans_donnees_extraites():
    urls = ["https://philibertnet.com/fr/1-x.html"]
    with patch("connecteur_philibert._extraire_produit", return_value=None), \
         patch("connecteur_philibert.time.sleep"):
        candidats = scanner_philibert_precommandes_generiques(urls)
    assert candidats == []
