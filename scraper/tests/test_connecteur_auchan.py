"""Connecteur Auchan (08/10/2026) : cartes de recherche a microdonnees
schema.org, plusieurs offres par carte possibles."""

import precommandes_watchlist as w
import radar_precommandes as r
from connecteur_auchan import analyser_recherche


def _carte(titre, href, offres):
    microdata = "".join(
        f'<meta itemprop="availability" content="https://schema.org/{d}"><meta itemprop="price" content="{p}">'
        for d, p in offres)
    return (f'<article itemscope="itemscope" itemtype="http://schema.org/Product" class="x">'
            f'<a class="productThumbnailLink" href="{href}"><source alt="{titre}" height="150">{microdata}</a></article>')


def test_carte_commandable_si_au_moins_une_offre_en_stock():
    page = _carte("POKEMON Coffret Dresseur d&apos;Élite", "/coffret/pr-C1", [("OutOfStock", "40"), ("InStock", "218.39"), ("InStock", "99.5")])
    page += _carte("POKEMON Coffret Noel", "/noel/pr-C2", [("OutOfStock", "34.99")])
    res = analyser_recherche(page)
    assert res[0] == {"titre": "POKEMON Coffret Dresseur d'Élite", "url": "https://www.auchan.fr/coffret/pr-C1",
                      "en_stock": True, "prix": 99.5}
    assert res[1]["en_stock"] is False and res[1]["prix"] == 34.99


class _FauxAuchan:   # pas de lire_fiche : donnees de la carte utilisees
    def __init__(self, resultats):
        self.resultats = resultats

    def rechercher(self, requete):
        return self.resultats


def test_scanner_auchan_sans_fiche():
    faux = _FauxAuchan([
        {"titre": "POKEMON Mini Tin ME05.5 30e Anniversaire", "url": "https://www.auchan.fr/tin/pr-C9", "en_stock": True, "prix": 14.99},
        {"titre": "POKEMON Coffret Dresseur d'Élite Héros Transcendant", "url": "https://www.auchan.fr/etb/pr-C1", "en_stock": True, "prix": 218.39},
    ])
    produits = [p for p in w.PRODUITS_SURVEILLES if p.alerte_disponibilite]
    cand = r.scanner_auchan("auchan.fr", produits, faux)
    assert [(c["nom_produit"], c["en_stock"], c["prix"]) for c in cand] == [
        ("Mini Tin — 30e Anniversaire (30th Celebration) FR", True, 14.99)]
