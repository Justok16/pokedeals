"""Tests de non-regression pour radar_precommandes.py.

Premiere couverture dediee a ce module (audit externe du 18/08/2026, cf.
SESSION_NOTES.md) -- se concentre sur le coupe-circuit de
scanner_woocommerce_api_rest() : cette fonction appelait auparavant
_decouvrir_produits_api_rest() directement, une fois par (produit,
mot-cle type), SANS reprendre le coupe-circuit deja present dans
rechercher_via_api_rest() (connecteur_woocommerce.py) -- une boutique
lente/instable pouvait donc consommer un nombre non borne de timeouts
avant de passer a la suivante."""

from datetime import date
from unittest.mock import Mock, patch

from connecteur_woocommerce import ConnecteurWooCommerce
from precommandes_watchlist import ProduitSurveille
from radar_precommandes import _evaluer_page, scanner_woocommerce_api_rest


def _produit(nom="Coffret Test", mots_type=("etb", "elite trainer box")):
    return ProduitSurveille(
        nom=nom,
        mots_cles_edition=frozenset({"30e anniversaire"}),
        mots_cles_type=frozenset(mots_type),
        date_sortie=date(2026, 9, 16),
    )


def test_sarrete_apres_3_echecs_consecutifs():
    produits = [_produit(mots_type=("mot1", "mot2", "mot3", "mot4"))]
    with patch.object(ConnecteurWooCommerce, "_decouvrir_produits_api_rest", return_value=([], False)) as appel_mock, \
         patch("radar_precommandes.time.sleep"):
        scanner_woocommerce_api_rest("exemple.fr", produits)
    assert appel_mock.call_count == 3  # coupe-circuit declenche pile au 3e echec


def test_echec_non_consecutif_ne_declenche_pas_le_coupe_circuit():
    produits = [_produit(mots_type=("mot1", "mot2", "mot3", "mot4", "mot5"))]
    sequence = [([], False), ([], False), ([{"id": 9, "name": "ok"}], True), ([], False), ([], False)]
    with patch.object(ConnecteurWooCommerce, "_decouvrir_produits_api_rest", side_effect=sequence) as appel_mock, \
         patch("radar_precommandes.time.sleep"):
        scanner_woocommerce_api_rest("exemple.fr", produits)
    assert appel_mock.call_count == 5  # jamais abandonne : le succes du milieu a reinitialise le compteur


def test_tout_succes_naffecte_jamais_le_coupe_circuit():
    produits = [_produit(mots_type=("mot1", "mot2", "mot3"))]
    with patch.object(ConnecteurWooCommerce, "_decouvrir_produits_api_rest", return_value=([], True)) as appel_mock, \
         patch("radar_precommandes.time.sleep"):
        scanner_woocommerce_api_rest("exemple.fr", produits)
    assert appel_mock.call_count == 3


def test_coupe_circuit_sapplique_a_travers_plusieurs_produits():
    # Le compteur d'echecs consecutifs traverse les differents produits
    # surveilles, pas seulement les mots-cles d'UN SEUL produit.
    produits = [_produit(nom="A", mots_type=("mot1",)), _produit(nom="B", mots_type=("mot2", "mot3", "mot4"))]
    with patch.object(ConnecteurWooCommerce, "_decouvrir_produits_api_rest", return_value=([], False)) as appel_mock, \
         patch("radar_precommandes.time.sleep"):
        scanner_woocommerce_api_rest("exemple.fr", produits)
    assert appel_mock.call_count == 3


# ------------------- _evaluer_page : plus de troncature a 5000 caracteres -------------------

def test_evaluer_page_trouve_une_date_situee_apres_5000_caracteres():
    # Audit externe du 18/08/2026 : le texte de page etait auparavant
    # tronque a 5000 caracteres avant d'etre passe a evaluer_correspondance
    # -- une date de sortie situee plus loin dans une page a rallonge
    # (nav/en-tete/description longue avant la date) ne pouvait jamais
    # etre trouvee, plafonnant la confiance a "moyenne" indefiniment.
    produit = ProduitSurveille(
        nom="Coffret Test",
        mots_cles_edition=frozenset({"30e anniversaire"}),
        mots_cles_type=frozenset({"etb"}),
        date_sortie=date(2026, 9, 16),
    )
    remplissage = "<p>du contenu sans rapport</p>" * 300  # bien plus de 5000 caracteres
    html = f"<html><title>ETB 30e anniversaire</title><body>{remplissage}<p>Date de sortie : 16 septembre 2026</p></body></html>"
    assert len(html) > 5000

    connecteur = Mock()
    connecteur.nom_affiche = "exemple.fr"
    reponse = Mock()
    reponse.raise_for_status = Mock()
    reponse.content = html.encode("utf-8")
    connecteur.session.get.return_value = reponse

    with patch("radar_precommandes.time.sleep"):
        candidats = _evaluer_page(connecteur, "https://exemple.fr/produit", [produit])

    assert len(candidats) == 1
    assert candidats[0]["confiance"] == "forte"


# ------------------- _evaluer_page : statut de stock reel (fix du 25/08/2026) -------------------
# Bug reel signale par l'utilisateur : une alerte "precommande detectee"
# recue pour un produit affichant 0,00€ et "rupture de stock" sur
# plazatcg.com (PrestaShop) -- _evaluer_page ne determinait auparavant
# JAMAIS le stock reel (toujours None), donc alerte_precommande.py ne
# pouvait jamais utiliser la regle "alerte seulement si le stock vient
# de s'ouvrir".

def _page(connecteur_nom, html):
    connecteur = Mock()
    connecteur.nom_affiche = connecteur_nom
    reponse = Mock()
    reponse.raise_for_status = Mock()
    reponse.content = html.encode("utf-8")
    connecteur.session.get.return_value = reponse
    return connecteur


def _produit_test():
    return ProduitSurveille(
        nom="Coffret Test",
        mots_cles_edition=frozenset({"30e anniversaire"}),
        mots_cles_type=frozenset({"etb"}),
        date_sortie=date(2026, 9, 16),
    )


def test_evaluer_page_lit_le_stock_via_jsonld():
    html = (
        '<html><title>ETB 30e anniversaire</title><body>'
        '<script type="application/ld+json">'
        '{"@type": "Product", "offers": {"price": "59.99", "availability": "https://schema.org/InStock"}}'
        '</script>'
        '<p>Date de sortie : 16 septembre 2026</p></body></html>'
    )
    connecteur = _page("exemple.fr", html)
    with patch("radar_precommandes.time.sleep"):
        candidats = _evaluer_page(connecteur, "https://exemple.fr/produit", [_produit_test()])
    assert candidats[0]["en_stock"] is True
    assert candidats[0]["prix"] == 59.99


def test_evaluer_page_jsonld_instock_mais_dom_annonce_rupture_force_en_stock_false():
    # Meme piege deja corrige cote ConnecteurPrestaShopSitemap (cf.
    # investcollect.com, CLAUDE.md) : le DOM rendu prime toujours sur le
    # JSON-LD en cas de contradiction.
    html = (
        '<html><title>ETB 30e anniversaire</title><body>'
        '<script type="application/ld+json">'
        '{"@type": "Product", "offers": {"price": "0.00", "availability": "https://schema.org/InStock"}}'
        '</script>'
        '<span id="product-availability">Rupture de stock</span>'
        '<p>Date de sortie : 16 septembre 2026</p></body></html>'
    )
    connecteur = _page("plazatcg.com", html)
    with patch("radar_precommandes.time.sleep"):
        candidats = _evaluer_page(connecteur, "https://plazatcg.com/produit", [_produit_test()])
    assert candidats[0]["en_stock"] is False


def test_evaluer_page_sans_donnees_structurees_renvoie_stock_indetermine():
    html = "<html><title>ETB 30e anniversaire</title><body><p>Date de sortie : 16 septembre 2026</p></body></html>"
    connecteur = _page("exemple.fr", html)
    with patch("radar_precommandes.time.sleep"):
        candidats = _evaluer_page(connecteur, "https://exemple.fr/produit", [_produit_test()])
    assert candidats[0]["en_stock"] is None


# ------------------- _evaluer_page : override DOM WooCommerce (fix du 25/08/2026, 2e bug) -------------------
# Bug reel signale par l'utilisateur : alerte "precommande detectee" recue
# pour golden-poke.fr (WooCommerce) avec "En stock / commandable" alors que
# la page affichait une liste d'attente ("Rejoindre la liste d'attente",
# aucun bouton ajouter au panier) -- le premier fix (ci-dessus) n'appliquait
# QUE l'override DOM PrestaShop (span id="product-availability", absent de
# toute page WooCommerce), donc l'override ne se declenchait jamais sur ces
# pages : le JSON-LD (souvent errone/en cache sur une precommande) faisait
# foi sans jamais pouvoir etre corrige par le rendu reel.

def _page_woocommerce(connecteur_nom, html):
    # Instance REELLE (pas Mock(spec=...)) : session est un attribut
    # d'instance (cf. __init__), invisible pour spec= qui ne connait que
    # les attributs de CLASSE -- isinstance(..., ConnecteurWooCommerce) doit
    # rester vrai pour que _evaluer_page choisisse le bon override DOM.
    connecteur = ConnecteurWooCommerce("exemple.invalide", nom_affiche=connecteur_nom)
    reponse = Mock()
    reponse.raise_for_status = Mock()
    reponse.content = html.encode("utf-8")
    connecteur.session = Mock()
    connecteur.session.get.return_value = reponse
    return connecteur


def test_evaluer_page_woocommerce_jsonld_instock_mais_classe_outofstock_force_en_stock_false():
    html = (
        '<html><title>ETB 30e anniversaire</title><body>'
        '<script type="application/ld+json">'
        '{"@type": "Product", "offers": {"price": "42.99", "availability": "https://schema.org/InStock"}}'
        '</script>'
        '<div class="product type-product outofstock">Rejoindre la liste d\'attente</div>'
        '<p>Date de sortie : 16 septembre 2026</p></body></html>'
    )
    connecteur = _page_woocommerce("golden-poke.fr", html)
    with patch("radar_precommandes.time.sleep"):
        candidats = _evaluer_page(connecteur, "https://golden-poke.fr/produit", [_produit_test()])
    assert candidats[0]["en_stock"] is False


def test_evaluer_page_woocommerce_jsonld_instock_et_classe_instock_reste_en_stock_true():
    html = (
        '<html><title>ETB 30e anniversaire</title><body>'
        '<script type="application/ld+json">'
        '{"@type": "Product", "offers": {"price": "59.99", "availability": "https://schema.org/InStock"}}'
        '</script>'
        '<div class="product type-product instock">Ajouter au panier</div>'
        '<p>Date de sortie : 16 septembre 2026</p></body></html>'
    )
    connecteur = _page_woocommerce("exemple.fr", html)
    with patch("radar_precommandes.time.sleep"):
        candidats = _evaluer_page(connecteur, "https://exemple.fr/produit", [_produit_test()])
    assert candidats[0]["en_stock"] is True
