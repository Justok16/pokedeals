"""Test de non-regression pour le garde-fou qualificatif/gradee/etat/langue
dans radar_prix_bas.py -- meme piege deja corrige dans bonne_affaire_shopify.py
et alerte_stock.py (cf. SESSION_NOTES.md), mais jamais applique ici avant ce
correctif. Cas reel (14/08/2026) : "Plumeline ex 024" confondu avec
"Plumeline 24 Sun & Moon REVERSE" (1,50€, homonyme sans "ex") sur kyoriyu.fr."""

from unittest.mock import patch

from connecteur_shopify import ResultatRecherche
from radar_prix_bas import _resultat_boutique_fiable, analyser_famille
from watchlist_prix_bas import FamillePrixBas, VariantePrixBas
from watchlist_shopify import CarteWatchlist


def _resultat(**kwargs) -> ResultatRecherche:
    base = dict(
        boutique="kyoriyu.fr",
        titre="Plumeline 24 Sun & Moon REVERSE",
        prix=1.50,
        en_stock=True,
        url_produit="https://kyoriyu.fr/produit",
        variante_titre="",
        image_url=None,
        langue_detectee=None,
        confiance="forte",
        etat_detecte=None,
    )
    base.update(kwargs)
    return ResultatRecherche(**base)


def _carte(**kwargs) -> CarteWatchlist:
    base = dict(
        nom_recherche="Plumeline",
        numero="024",
        langue="fr",
        nom_config="Plumeline ex 024",
        prix_max_fixe=15,
        qualificatif="ex",
    )
    base.update(kwargs)
    return CarteWatchlist(**base)


def test_homonyme_sans_qualificatif_rejete():
    # Cas reel : "Plumeline 24 Sun & Moon REVERSE" n'a pas "ex" -> rejete.
    assert _resultat_boutique_fiable(_resultat(), _carte()) is False


def test_bonne_carte_avec_qualificatif_acceptee():
    titre = "Carte Plumeline Ex FR 024 Promo Upc Flammes Fantasmagoriques"
    assert _resultat_boutique_fiable(_resultat(titre=titre), _carte()) is True


def test_carte_gradee_rejetee():
    titre = "Plumeline ex 024 - PSA 9"
    assert _resultat_boutique_fiable(_resultat(titre=titre), _carte()) is False


def test_etat_excellent_rejete():
    titre = "Plumeline ex 024"
    assert _resultat_boutique_fiable(_resultat(titre=titre, etat_detecte="exc"), _carte()) is False


def test_langue_incoherente_rejetee():
    titre = "Plumeline ex 024"
    assert _resultat_boutique_fiable(_resultat(titre=titre, langue_detectee="jp"), _carte(langue="fr")) is False


def test_qualificatif_inattendu_rejete_symetrique():
    # Carte SANS qualificatif en config ne doit pas matcher un titre "ex" homonyme.
    carte = _carte(qualificatif=None, nom_config="Plumeline 024")
    titre = "Plumeline ex 024 - Edition Speciale"
    assert _resultat_boutique_fiable(_resultat(titre=titre), carte) is False


def test_analyser_famille_etiquette_la_bonne_langue_boutique():
    """Cas reel (16/08/2026) : JP/KR (et desormais CN-T, meme numerotation
    que JP/KR selon Justok) partagent EXACTEMENT le meme nom_config dans
    config.yaml -- cartes_boutiques_par_nom_config[nom_config] contient donc
    plusieurs CarteWatchlist de langues differentes sous la meme cle. Sans
    filtre, un resultat boutique COREEN trouve pendant l'iteration de la
    variante JP se voyait etiquete a tort "langue: jp" dans le digest
    Telegram (bug trouve en corrigeant l'entree CN de Carapuce, qui
    reproduisait exactement ce partage de nom_config)."""
    nom_config = "Squirtle 170/165 sv2a"
    carte_jp = _carte(nom_recherche="Squirtle", numero="170/165", langue="jp",
                      nom_config=nom_config, qualificatif=None)
    carte_kr = _carte(nom_recherche="Squirtle", numero="170/165", langue="kr",
                      nom_config=nom_config, qualificatif=None)

    resultat_kr = _resultat(
        boutique="kyoriyu.fr", titre="Squirtle 170/165 sv2a coreen",
        prix=10.0, langue_detectee="kr",
    )

    famille = FamillePrixBas(
        nom_affichage="Carapuce (Squirtle)",
        variantes=[
            VariantePrixBas("jp", nom_config),
            VariantePrixBas("kr", nom_config),
        ],
    )
    cartes_boutiques_par_nom_config = {nom_config: [carte_jp, carte_kr]}
    resultats_boutiques = {carte_jp.cle_recherche: [resultat_kr]}

    with patch("radar_prix_bas._rechercher_ebay_vinted", return_value=[]):
        meilleur = analyser_famille(
            famille, entrees_brutes={}, secrets={}, cfg_regles={},
            resultats_boutiques=resultats_boutiques,
            cartes_boutiques_par_nom_config=cartes_boutiques_par_nom_config,
        )

    assert meilleur is not None
    assert meilleur["langue"] == "kr"
