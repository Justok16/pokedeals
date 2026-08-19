"""Tests de non-regression pour connecteur_prestashop_sitemap.py.

Premiere couverture de test dediee a ce connecteur (audit du 18/08/2026,
cf. SESSION_NOTES.md) -- se concentre sur le correctif de
recuperer_toutes_les_urls_produits() : un echec TOTAL de decouverte du
sitemap (aucun sitemap racine trouve, ou tous en echec de recuperation)
renvoyait auparavant une liste vide SANS lever, indiscernable d'un sitemap
reellement vide -- consequence reelle : alerte_stock.py enregistrait
`en_stock: False` pour chaque carte suivie sur cette boutique, creant une
fausse alerte 📦 de retour en stock des que le reseau se retablissait.
Cf. le commentaire de recuperer_toutes_les_urls_produits() pour le detail
complet, et connecteur_shopify.py pour le meme correctif applique en
premier a la plateforme Shopify."""

from unittest.mock import patch

import pytest

from connecteur_prestashop_sitemap import ConnecteurPrestaShopSitemap


def test_recuperer_urls_leve_si_aucun_sitemap_racine_trouve():
    c = ConnecteurPrestaShopSitemap("boutique-en-panne.fr")
    with patch.object(c, "_decouvrir_sitemaps_racine", return_value=[]):
        with pytest.raises(RuntimeError):
            c.recuperer_toutes_les_urls_produits()


def test_recuperer_urls_leve_si_le_sitemap_racine_ne_renvoie_aucune_url():
    c = ConnecteurPrestaShopSitemap("boutique-cassee.fr")
    with patch.object(c, "_decouvrir_sitemaps_racine", return_value=["https://boutique-cassee.fr/sitemap.xml"]), \
         patch.object(c, "_lister_urls_recursif", return_value=[]):
        with pytest.raises(RuntimeError):
            c.recuperer_toutes_les_urls_produits()


def test_recuperer_urls_naffecte_pas_un_resultat_vide_apres_filtre_segments():
    # Le sitemap contient de vraies URLs (fetch reussi), mais toutes
    # exclues par SEGMENTS_EXCLUS (ex: uniquement des pages techniques
    # panier/compte) -- resultat legitime, pas une erreur.
    c = ConnecteurPrestaShopSitemap("boutique-toute-neuve.fr")
    with patch.object(c, "_decouvrir_sitemaps_racine", return_value=["https://boutique-toute-neuve.fr/sitemap.xml"]), \
         patch.object(c, "_lister_urls_recursif", return_value=["https://boutique-toute-neuve.fr/mon-compte"]):
        assert c.recuperer_toutes_les_urls_produits() == []


def test_recuperer_urls_renvoie_les_urls_produits_reellement_trouvees():
    c = ConnecteurPrestaShopSitemap("boutique-ok.fr")
    urls = [
        "https://boutique-ok.fr/12-dracaufeu-ex-199-165.html",
        "https://boutique-ok.fr/panier",  # exclue
    ]
    with patch.object(c, "_decouvrir_sitemaps_racine", return_value=["https://boutique-ok.fr/sitemap.xml"]), \
         patch.object(c, "_lister_urls_recursif", return_value=urls):
        resultat = c.recuperer_toutes_les_urls_produits()
    assert resultat == ["https://boutique-ok.fr/12-dracaufeu-ex-199-165.html"]
