"""Connecteur Ultrajeux (08/10/2026) : pages categorie rendues cote serveur."""

import precommandes_watchlist as w
import radar_precommandes as r
from connecteur_ultrajeux import analyser_categorie


def _carte(alt, href, prix, dispo, commandable, drapeau="fr"):
    selecteur = ('<select name="quantite[0][1]"><option>1</option></select> <input type="submit" value="Ajouter">'
                 if commandable else '<input type="button" value="Alertez-moi !" onclick="x">')
    return (f'<div class="block_produit"><div class="contenu"><p class="titre"><a href="{href}" title="t"><b>t</b></a> '
            f'<img src="/images/pays/{drapeau}.png" /></p><form><p class="image"><a href="{href}">'
            f'<img src="https://x/1.jpg" alt="{alt}" title="{alt}" class="produit_scan" /></a></p>'
            f'<p class="prix"><span class="prix">{prix} &euro;</span></p>'
            f'<p class="disponibilite"><b>{dispo}</b></p><p class="selecteur">{selecteur}</p></form></div></div>')


def test_analyse_categorie():
    page = (_carte("ETB Coffret Dresseur d&#039;Elite Pokémon 30e Anniversaire", "produit-32960-x.html", "229,90", "Disponible", True)
            + _carte("Mini-Tin Pokémon 30e Anniversaire - Noctali (Version Nuit)", "produit-33279-x.html", "29,90", "Disponible en Magasin", False)
            + _carte("Ultra Premium Collection Umbreon", "produit-1-x.html", "149,90", "Disponible", True, drapeau="gb"))
    assert analyser_categorie(page) == [
        {"titre": "ETB Coffret Dresseur d'Elite Pokémon 30e Anniversaire", "url": "https://www.ultrajeux.com/produit-32960-x.html",
         "en_stock": True, "prix": 229.9},
        {"titre": "Mini-Tin Pokémon 30e Anniversaire - Noctali (Version Nuit)", "url": "https://www.ultrajeux.com/produit-33279-x.html",
         "en_stock": False, "prix": 29.9},
    ]


class _FauxUltrajeux:
    def __init__(self, resultats):
        self.resultats = resultats

    def rechercher(self, categorie):
        return self.resultats


def test_scanner_ultrajeux():
    faux = _FauxUltrajeux([
        {"titre": "Bundle de 6 Boosters Pokémon 30e Anniversaire", "url": "https://www.ultrajeux.com/produit-33282-x.html", "en_stock": True, "prix": 94.9},
        {"titre": "ETB Coffret Dresseur d'Elite Pokémon Méga-Évolution", "url": "https://www.ultrajeux.com/produit-1-x.html", "en_stock": True, "prix": 59.9},
    ])
    produits = [p for p in w.PRODUITS_SURVEILLES if p.alerte_disponibilite]
    cand = r.scanner_ultrajeux("ultrajeux.com", produits, faux)
    assert [(c["nom_produit"], c["en_stock"], c["prix"]) for c in cand] == [
        ("Booster Bundle — 30e Anniversaire (30th Celebration) FR", True, 94.9)]
