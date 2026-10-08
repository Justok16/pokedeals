"""Connecteur Lidl (08/10/2026) : API de recherche JSON publique."""

import precommandes_watchlist as w
import radar_precommandes as r
from connecteur_lidl import analyser_recherche


def _item(titre, chemin, prix, en_ligne, bloque=False):
    return {"gridbox": {"data": {"fullTitle": titre, "canonicalPath": chemin, "price": {"price": prix},
                                 "stockAvailability": {"onlineAvailable": en_ligne}, "preventSelling": bloque}}}


def test_analyse_reponse_api():
    res = analyser_recherche({"items": [
        _item("Pokémon Coffret Dresseur d'Élite 30e anniversaire", "/p/etb/p1", 59.99, True),
        _item("Pokémon Mini Tin", "/p/tin/p2", "x", False),
        _item("Pokémon Pokébox", "/p/box/p3", 24.99, True, bloque=True),
        {"gridbox": {"data": {"fullTitle": "Sans lien"}}},
    ]})
    assert res == [
        {"titre": "Pokémon Coffret Dresseur d'Élite 30e anniversaire", "url": "https://www.lidl.fr/p/etb/p1", "en_stock": True, "prix": 59.99},
        {"titre": "Pokémon Mini Tin", "url": "https://www.lidl.fr/p/tin/p2", "en_stock": False, "prix": None},
        {"titre": "Pokémon Pokébox", "url": "https://www.lidl.fr/p/box/p3", "en_stock": False, "prix": 24.99},
    ]
    assert analyser_recherche({}) == [] and analyser_recherche(None) == []


class _FauxLidl:
    def __init__(self, resultats):
        self.resultats = resultats

    def rechercher(self, requete):
        return self.resultats


def test_scanner_lidl_filtre_les_titres_hors_sujet():
    faux = _FauxLidl([
        {"titre": "Pokémon Mini Tin 30e Anniversaire", "url": "https://www.lidl.fr/p/tin/p2", "en_stock": True, "prix": 12.99},
        {"titre": "Ensemble pyjama Minecraft ou Pokemon enfant", "url": "https://www.lidl.fr/p/pyj/p9", "en_stock": True, "prix": 9.99},
    ])
    produits = [p for p in w.PRODUITS_SURVEILLES if p.alerte_disponibilite]
    cand = r.scanner_lidl("lidl.fr", produits, faux)
    assert [(c["nom_produit"], c["en_stock"], c["prix"]) for c in cand] == [
        ("Mini Tin — 30e Anniversaire (30th Celebration) FR", True, 12.99)]
