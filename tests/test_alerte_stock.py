"""Test de non-regression pour le garde-fou carte gradee dans
alerte_stock.py (meme correctif que bonne_affaire_shopify.py, cf.
tests/test_bonne_affaire_shopify.py pour le cas reel du 13/08/2026)."""

from unittest.mock import Mock, patch

from connecteur_shopify import ResultatRecherche
from alerte_stock import detecter_retours_en_stock, envoyer_telegram_retours_stock
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


# ------------------- Ecriture memoire differee jusqu'a confirmation Telegram -------------------
# Audit externe du 18/08/2026 (verifie contre le code reel) : avant ce
# correctif, detecter_retours_en_stock() ecrivait `memoire[cle] =
# {"en_stock": True, ...}` IMMEDIATEMENT pour toute transition, et
# scan_boutique*.py sauvegardait la memoire sur disque AVANT meme la
# tentative d'envoi Telegram -- un echec Telegram survenant apres perdait
# l'evenement DEFINITIVEMENT (la transition rupture->stock ne pouvait
# plus jamais etre redetectee).

def _carte_et_resultats(en_stock=True):
    carte = CarteWatchlist(nom_recherche="Dracaufeu", numero="199/165", langue="fr",
                            nom_config="Dracaufeu ex 199/165", qualificatif="ex")
    cle = carte.cle_recherche
    resultats_par_critere = {cle: [_resultat(titre="Dracaufeu ex 199/165", en_stock=en_stock, prix=45.0)]}
    cartes_par_critere = {cle: carte}
    return cartes_par_critere, resultats_par_critere


def test_transition_ecrit_pas_immediatement_en_memoire():
    cartes_par_critere, resultats_par_critere = _carte_et_resultats(en_stock=True)
    memoire = {"exemple.fr|Dracaufeu ex 199/165": {"en_stock": False, "derniere_verification": "2026-01-01T00:00:00+00:00"}}

    evenements = detecter_retours_en_stock("exemple.fr", resultats_par_critere, cartes_par_critere, memoire)

    assert len(evenements) == 1
    # Toujours l'ANCIEN etat tant que Telegram n'a pas confirme.
    assert memoire["exemple.fr|Dracaufeu ex 199/165"]["en_stock"] is False
    assert evenements[0]["_nouvel_etat"]["en_stock"] is True


def test_envoi_reussi_commite_letat_en_memoire():
    cartes_par_critere, resultats_par_critere = _carte_et_resultats(en_stock=True)
    memoire = {"exemple.fr|Dracaufeu ex 199/165": {"en_stock": False, "derniere_verification": "2026-01-01T00:00:00+00:00"}}
    evenements = detecter_retours_en_stock("exemple.fr", resultats_par_critere, cartes_par_critere, memoire)

    reponse = Mock(status_code=200, text="")
    with patch("alerte_stock.requests.post", return_value=reponse):
        ok = envoyer_telegram_retours_stock(evenements, "123", "token", memoire)

    assert ok is True
    assert memoire["exemple.fr|Dracaufeu ex 199/165"]["en_stock"] is True


def test_echec_telegram_ne_commite_pas_et_reste_redetectable():
    cartes_par_critere, resultats_par_critere = _carte_et_resultats(en_stock=True)
    memoire = {"exemple.fr|Dracaufeu ex 199/165": {"en_stock": False, "derniere_verification": "2026-01-01T00:00:00+00:00"}}
    evenements = detecter_retours_en_stock("exemple.fr", resultats_par_critere, cartes_par_critere, memoire)

    reponse = Mock(status_code=500, text="erreur serveur")
    with patch("alerte_stock.requests.post", return_value=reponse):
        ok = envoyer_telegram_retours_stock(evenements, "123", "token", memoire)

    assert ok is False
    assert memoire["exemple.fr|Dracaufeu ex 199/165"]["en_stock"] is False  # pas commite

    # Redetection au cycle suivant : la memoire n'ayant pas change, la
    # transition rupture->stock est toujours visible.
    evenements_2 = detecter_retours_en_stock("exemple.fr", resultats_par_critere, cartes_par_critere, memoire)
    assert len(evenements_2) == 1


def test_pas_de_transition_ecrit_immediatement_comme_avant():
    # Une carte sans evenement (rien n'est du a l'utilisateur) doit
    # toujours ecrire sa memoire immediatement -- pas de risque de perte
    # puisqu'aucune alerte n'est en jeu.
    cartes_par_critere, resultats_par_critere = _carte_et_resultats(en_stock=True)
    memoire = {"exemple.fr|Dracaufeu ex 199/165": {"en_stock": True, "derniere_verification": "2026-01-01T00:00:00+00:00"}}

    evenements = detecter_retours_en_stock("exemple.fr", resultats_par_critere, cartes_par_critere, memoire)

    assert evenements == []
    assert memoire["exemple.fr|Dracaufeu ex 199/165"]["en_stock"] is True


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
