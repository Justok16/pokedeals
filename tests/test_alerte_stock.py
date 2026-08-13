"""Test de non-regression pour le garde-fou carte gradee dans
alerte_stock.py (meme correctif que bonne_affaire_shopify.py, cf.
tests/test_bonne_affaire_shopify.py pour le cas reel du 13/08/2026)."""

from connecteur_shopify import ResultatRecherche
from alerte_stock import detecter_retours_en_stock
from watchlist_shopify import CarteWatchlist


def _resultat(**kwargs) -> ResultatRecherche:
    base = dict(
        boutique="exemple.fr",
        titre="Evoli ex 167/131",
        prix=150.0,
        en_stock=True,
        url_produit="https://exemple.fr/produit",
        variante_titre="",
        image_url=None,
        langue_detectee=None,
        confiance="forte",
        etat_detecte=None,
    )
    base.update(kwargs)
    return ResultatRecherche(**base)


def test_retour_en_stock_dune_carte_gradee_ignore():
    carte = CarteWatchlist(nom_recherche="Evoli", numero="167/131", langue="fr",
                            nom_config="Evoli ex 167/131", qualificatif="ex")
    cle = carte.cle_recherche
    resultats_par_critere = {cle: [_resultat(titre="Evoli ex 167/131 - PSA 8 - FR")]}
    cartes_par_critere = {cle: carte}
    # Etat precedent = rupture, pour verifier qu'une "vraie" transition ne
    # se produit PAS a cause de l'annonce gradee (seule candidate).
    memoire = {"exemple.fr|Evoli ex 167/131": {"en_stock": False, "derniere_verification": "2026-01-01T00:00:00+00:00"}}

    evenements = detecter_retours_en_stock("exemple.fr", resultats_par_critere, cartes_par_critere, memoire)
    assert evenements == []


def test_retour_en_stock_etat_excellent_ignore():
    # Meme garde-fou que bonne_affaire_shopify.py : une carte en "Excellent"
    # (pas Near Mint) ne doit pas declencher d'alerte retour en stock.
    carte = CarteWatchlist(nom_recherche="Evoli", numero="167/131", langue="fr",
                            nom_config="Evoli ex 167/131", qualificatif="ex")
    cle = carte.cle_recherche
    resultats_par_critere = {cle: [_resultat(titre="Evoli ex 167/131", etat_detecte="exc")]}
    cartes_par_critere = {cle: carte}
    memoire = {"exemple.fr|Evoli ex 167/131": {"en_stock": False, "derniere_verification": "2026-01-01T00:00:00+00:00"}}

    evenements = detecter_retours_en_stock("exemple.fr", resultats_par_critere, cartes_par_critere, memoire)
    assert evenements == []
