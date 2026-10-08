"""Connecteur E.Leclerc (08/10/2026) : lecture des resultats de recherche et
des fiches JSON-LD, et scanner du radar 30e anniversaire."""

import json

import precommandes_watchlist as w
import radar_precommandes as r
from connecteur_leclerc import analyser_fiche, analyser_recherche

CARTE = ('<article data-offer-id="{offre}" data-ean="0196" data-product-card class="x">'
         '<h3><a tabindex="0" href="{href}" class="t" data-product-card-title title="{titre}">{titre}</a></h3>'
         '<p>Vendu par</p></article>')


def _recherche(*cartes):
    return "<html>" + "".join(CARTE.format(**c) for c in cartes) + "</html>"


def _fiche(nom, dispo="https://schema.org/InStock", prix=59.9, description="Coffret officiel."):
    produit = {"@type": "Product", "name": nom, "description": description,
               "offers": [{"@type": "Offer", "price": prix, "availability": dispo},
                          {"@type": "AggregateOffer", "lowPrice": prix}]}
    return f'<script type="application/ld+json">{json.dumps(produit)}</script>'


def test_recherche_offre_active_selon_identifiant():
    page = _recherche(
        {"offre": "236880428", "href": "/fp/a-1?offerId=236880428", "titre": "Pokémon ME04 : coffret Dresseur d&apos;Elite"},
        {"offre": "", "href": "/fp/b-2", "titre": "Pokémon : Pokébox"},
        {"offre": "o-0820650557446", "href": "/fp/c-3", "titre": "Pokémon : Coffret Académie"},
    )
    res = analyser_recherche(page)
    assert [x["offre_active"] for x in res] == [True, False, False]
    assert res[0]["titre"] == "Pokémon ME04 : coffret Dresseur d'Elite"
    assert res[0]["url"] == "https://www.e.leclerc/fp/a-1?offerId=236880428"


def test_fiche_disponibilite_et_prix():
    f = analyser_fiche(_fiche("Pokémon ME05.5 : Bundle", prix=34.99))
    assert f == {"titre": "Pokémon ME05.5 : Bundle", "description": "Coffret officiel.", "prix": 34.99, "en_stock": True}
    assert analyser_fiche(_fiche("X", dispo="https://schema.org/OutOfStock"))["en_stock"] is False
    assert analyser_fiche(_fiche("X", dispo="https://schema.org/PreOrder"))["en_stock"] is True
    assert analyser_fiche("<html>rien</html>") is None


class _FauxLeclerc:
    def __init__(self, resultats, fiches):
        self.resultats, self.fiches, self.fiches_lues = resultats, fiches, []

    def rechercher(self, requete):
        return self.resultats

    def lire_fiche(self, url):
        self.fiches_lues.append(url)
        return self.fiches.get(url)


def test_scanner_leclerc_detecte_le_produit_et_ignore_le_reste():
    resultats = [
        {"titre": "Pokémon ME05.5 : Bundle - 6 boosters", "url": "https://www.e.leclerc/fp/bundle-1?offerId=9", "offre_active": True},
        {"titre": "Pokémon ME04 : coffret Dresseur d'Elite", "url": "https://www.e.leclerc/fp/etb-me04", "offre_active": True},
    ]
    fiches = {"https://www.e.leclerc/fp/bundle-1?offerId=9":
              analyser_fiche(_fiche("Pokémon ME05.5 : Bundle - 6 boosters", prix=89.0,
                                    description="Le Pokémon légendaire à l'honneur"))}
    faux = _FauxLeclerc(resultats, fiches)
    produits = [p for p in w.PRODUITS_SURVEILLES if p.alerte_disponibilite]
    cand = r.scanner_leclerc("e.leclerc", produits, faux)
    assert [(c["nom_produit"], c["en_stock"], c["prix"]) for c in cand] == [
        ("Booster Bundle — 30e Anniversaire (30th Celebration) FR", True, 89.0)]
    assert faux.fiches_lues == ["https://www.e.leclerc/fp/bundle-1?offerId=9"]   # ME04 jamais chargee
    assert cand[0]["url_produit"] == "https://www.e.leclerc/fp/bundle-1"         # sans ?offerId


def test_scanner_leclerc_rejette_une_version_anglaise():
    resultats = [{"titre": "Pokémon ME05.5 : Bundle - EN", "url": "https://www.e.leclerc/fp/en", "offre_active": True}]
    faux = _FauxLeclerc(resultats, {"https://www.e.leclerc/fp/en": analyser_fiche(_fiche("Pokémon ME05.5 : Bundle - EN"))})
    produits = [p for p in w.PRODUITS_SURVEILLES if p.alerte_disponibilite]
    assert r.scanner_leclerc("e.leclerc", produits, faux) == []
