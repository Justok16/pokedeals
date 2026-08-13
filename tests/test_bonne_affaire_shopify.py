"""Tests de non-regression pour les garde-fous de evaluer_deal
(bonne_affaire_shopify.py) : stock -> langue -> qualificatif -> prix. Chaque
garde-fou correspond a un bug reel deja rencontre en prod, cf.
SESSION_NOTES.md."""

from connecteur_shopify import ResultatRecherche
from bonne_affaire_shopify import _etat_refuse, evaluer_deal
from watchlist_shopify import CarteWatchlist


def _resultat(**kwargs) -> ResultatRecherche:
    base = dict(
        boutique="exemple.fr",
        titre="Dracaufeu 199/165",
        prix=50.0,
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


def _carte(**kwargs) -> CarteWatchlist:
    base = dict(
        nom_recherche="Dracaufeu",
        numero="199/165",
        langue="fr",
        nom_config="Dracaufeu ex 199/165",
        prix_max_fixe=None,
        qualificatif=None,
    )
    base.update(kwargs)
    return CarteWatchlist(**base)


REGLES = {"cote_min": 5.0, "marge_achat": 0.10, "prix_plancher_ratio": 0.15,
          "marge_revente": 0.10, "frais_revente_estimes": 0.13, "profit_min": 0}
COTES = {"Dracaufeu ex 199/165|fr": [{"cote": 100.0, "ts": 0}]}


def test_carte_gradee_psa_rejetee():
    # Cas reel signale par Justok le 13/08/2026 : Evoli ex 167/131 sur
    # relictcg.com, annonce "PSA 8" alertee comme "bonne affaire" a -53.9%
    # -- une carte gradee n'est pas comparable a la cote d'une carte brute.
    titre = "Acheter - Evoli ex SAR - PRE167/131 - EV8.5 - PSA 8 - FR"
    deal, raison = evaluer_deal(_resultat(titre=titre), _carte(), COTES, REGLES)
    assert deal is None
    assert "gradee" in raison


def test_carte_gradee_ccc_rejetee():
    # Meme soiree, 2e annonce sur la meme carte : notation de gradation
    # differente ("CCC 9.5") -- pas dans la liste initiale, ajoutee suite
    # a ce cas reel.
    titre = "Evoli ex - Evolutions Prismatiques 167/131 - CCC 9.5 - FR"
    deal, raison = evaluer_deal(_resultat(titre=titre), _carte(), COTES, REGLES)
    assert deal is None
    assert "gradee" in raison


def test_carte_non_gradee_nest_pas_rejetee_a_tort():
    # "non gradee" contient "gradee" en sous-chaine -- ne doit PAS etre
    # exclue (c'est justement une carte BRUTE), meme negation que main.py.
    # (titre volontairement SANS "ex" pour ne pas declencher le garde-fou
    # qualificatif symetrique, deja teste ailleurs dans ce fichier.)
    titre = "Dracaufeu 199/165 non gradee excellent etat"
    deal, raison = evaluer_deal(_resultat(titre=titre), _carte(), COTES, REGLES)
    assert deal is not None, raison


def test_etat_excellent_rejete():
    # Cas reel (14/08/2026) : kairyu.fr, Eevee ex 223 sv8a, "Etat : Exc"
    # alertee a tort comme bonne affaire -- Justok ne veut que du Neuf/NM.
    deal, raison = evaluer_deal(_resultat(etat_detecte="exc"), _carte(), COTES, REGLES)
    assert deal is None
    assert "etat refuse" in raison


def test_etat_near_mint_nest_pas_rejete():
    deal, raison = evaluer_deal(_resultat(etat_detecte="near mint"), _carte(), COTES, REGLES)
    assert deal is not None, raison


def test_etat_absent_nest_pas_rejete():
    # Aucun label d'etat trouve sur la fiche produit -> on alerte quand meme
    # (beaucoup de boutiques n'indiquent pas l'etat sur toutes leurs fiches).
    deal, raison = evaluer_deal(_resultat(etat_detecte=None), _carte(), COTES, REGLES)
    assert deal is not None, raison


def test_etat_refuse_fonction_directe():
    assert _etat_refuse("exc") is True
    assert _etat_refuse("excellent") is True
    assert _etat_refuse("light played") is True
    assert _etat_refuse("near mint") is False
    assert _etat_refuse("neuf") is False
    assert _etat_refuse(None) is False


def test_rupture_de_stock_rejetee():
    deal, raison = evaluer_deal(_resultat(en_stock=False), _carte(), COTES, REGLES)
    assert deal is None
    assert "rupture" in raison


def test_langue_incoherente_rejetee():
    # Une carte configuree FR ne doit jamais matcher un titre explicitement JP/KR.
    deal, raison = evaluer_deal(_resultat(langue_detectee="jp"), _carte(langue="fr"), COTES, REGLES)
    assert deal is None
    assert "langue" in raison


def test_jp_ou_kr_compatible_avec_carte_jp():
    cotes = {"Eevee 078|jp": [{"cote": 100.0, "ts": 0}]}
    carte = _carte(nom_config="Eevee 078", numero="078", langue="jp")
    deal, raison = evaluer_deal(_resultat(langue_detectee="jp_ou_kr", prix=50.0), carte, cotes, REGLES)
    assert deal is not None, raison


def test_qualificatif_manquant_dans_le_titre_rejete():
    # "Plumeline ex 024" (config) ne doit pas matcher un titre sans "ex".
    carte = _carte(nom_config="Plumeline ex 024", numero="024", qualificatif="ex")
    deal, raison = evaluer_deal(_resultat(titre="Plumeline 24 Sun & Moon REVERSE"), carte, COTES, REGLES)
    assert deal is None
    assert "qualificatif" in raison


def test_qualificatif_inattendu_dans_le_titre_rejete_symetrique():
    # Carte configuree SANS qualificatif ne doit pas matcher un titre "ex" homonyme.
    carte = _carte(qualificatif=None)
    deal, raison = evaluer_deal(_resultat(titre="Dracaufeu ex 199/165 - Edition Speciale"), carte, COTES, REGLES)
    assert deal is None
    assert "qualificatif" in raison


def test_prix_sous_la_cote_avec_marge_est_un_deal():
    deal, raison = evaluer_deal(_resultat(prix=50.0), _carte(), COTES, REGLES)
    assert deal is not None, raison
    assert deal["decote_pct"] == 50.0


def test_prix_trop_proche_de_la_cote_rejete():
    deal, raison = evaluer_deal(_resultat(prix=95.0), _carte(), COTES, REGLES)
    assert deal is None
    assert "pas assez sous la cote" in raison


def test_prix_suspect_trop_bas_rejete():
    # Garde-fou "trop beau pour etre vrai" : sous 15% de la cote.
    deal, raison = evaluer_deal(_resultat(prix=5.0), _carte(), COTES, REGLES)
    assert deal is None
    assert "suspect" in raison


def test_seuil_fixe_prioritaire_sur_la_cote():
    carte = _carte(prix_max_fixe=60.0)
    deal, raison = evaluer_deal(_resultat(prix=55.0), carte, COTES, REGLES)
    assert deal is not None, raison
    assert raison == "DEAL (seuil fixe)"

    deal, raison = evaluer_deal(_resultat(prix=65.0), carte, COTES, REGLES)
    assert deal is None
    assert "seuil fixe" in raison
