"""Tests de non-regression pour detecter_nouvelles_precommandes_generiques()
et envoyer_telegram_precommandes_generiques() (radar_precommande_generique.py).

Contrairement au radar a produits fixes (alerte_precommande.py), il n'y a
ici AUCUNE notion de confiance/date confirmee -- un produit inconnu a
l'avance n'a pas de date attendue a comparer. Regle simplifiee : la
premiere apparition d'un (domaine, slug) est TOUJOURS silencieuse (meme si
deja en stock), seule une transition "pas en stock -> en stock" sur un
produit deja connu declenche une alerte -- une seule fois."""

from unittest.mock import Mock, patch

import requests

from radar_precommande_generique import (
    detecter_nouvelles_precommandes_generiques,
    envoyer_telegram_precommandes_generiques,
    scanner_shopify_precommandes_generiques,
)


def _candidat(slug="etb-151", en_stock=True, **kw):
    base = dict(
        domaine="exemple.fr",
        slug=slug,
        titre="Précommande Pokémon Coffret Dresseur d'Élite 151",
        url_produit="https://exemple.fr/products/etb-151",
        prix=59.99,
        en_stock=en_stock,
        raison="pokemon + precommande + type de produit scelle confirmes, aucune autre franchise",
        horodatage="2026-08-23T12:00:00+00:00",
    )
    base.update(kw)
    return base


# ------------------- detecter_nouvelles_precommandes_generiques -------------------

def test_premiere_fois_ne_declenche_jamais_dalerte_meme_en_stock():
    memoire = {}
    evenements = detecter_nouvelles_precommandes_generiques([_candidat(en_stock=True)], memoire)
    assert evenements == []
    assert memoire["exemple.fr|etb-151"]["en_stock"] is True


def test_deuxieme_fois_meme_etat_ne_redeclenche_pas():
    memoire = {"exemple.fr|etb-151": {"en_stock": True, "titre_produit": "x", "url_produit": "x",
                                        "prix": 59.99, "derniere_verification": "hier"}}
    evenements = detecter_nouvelles_precommandes_generiques([_candidat(en_stock=True)], memoire)
    assert evenements == []


def test_transition_hors_stock_vers_en_stock_declenche_une_alerte():
    memoire = {"exemple.fr|etb-151": {"en_stock": False, "titre_produit": "x", "url_produit": "x",
                                        "prix": 59.99, "derniere_verification": "hier"}}
    evenements = detecter_nouvelles_precommandes_generiques([_candidat(en_stock=True)], memoire)
    assert len(evenements) == 1
    # Ecriture memoire DIFFEREE (V57) : pas encore commitee avant l'envoi Telegram.
    assert memoire["exemple.fr|etb-151"]["en_stock"] is False


def test_transition_stock_indetermine_vers_en_stock_declenche_une_alerte():
    memoire = {"exemple.fr|etb-151": {"en_stock": None, "titre_produit": "x", "url_produit": "x",
                                        "prix": 59.99, "derniere_verification": "hier"}}
    evenements = detecter_nouvelles_precommandes_generiques([_candidat(en_stock=True)], memoire)
    assert len(evenements) == 1


def test_produit_deja_connu_toujours_hors_stock_ne_declenche_rien():
    memoire = {"exemple.fr|etb-151": {"en_stock": False, "titre_produit": "x", "url_produit": "x",
                                        "prix": 59.99, "derniere_verification": "hier"}}
    evenements = detecter_nouvelles_precommandes_generiques([_candidat(en_stock=False)], memoire)
    assert evenements == []
    assert memoire["exemple.fr|etb-151"]["en_stock"] is False


def test_deux_boutiques_meme_slug_ne_se_melangent_pas():
    memoire = {"exemple.fr|etb-151": {"en_stock": True, "titre_produit": "x", "url_produit": "x",
                                        "prix": 59.99, "derniere_verification": "hier"}}
    # "autre.fr" n'a jamais ete vu -- premiere fois, silencieux, meme slug.
    evenements = detecter_nouvelles_precommandes_generiques(
        [_candidat(domaine="autre.fr", slug="etb-151", en_stock=True)], memoire
    )
    assert evenements == []
    assert "autre.fr|etb-151" in memoire


# ------------------- envoyer_telegram_precommandes_generiques -------------------

def test_envoi_reussi_commite_la_memoire():
    memoire = {"exemple.fr|etb-151": {"en_stock": False}}
    evenement = _candidat(en_stock=True)
    evenement["_cle_memoire"] = "exemple.fr|etb-151"
    evenement["_nouvel_etat"] = {"en_stock": True, "titre_produit": evenement["titre"]}

    reponse = Mock(status_code=200)
    with patch("radar_precommande_generique.requests.post", return_value=reponse):
        ok = envoyer_telegram_precommandes_generiques([evenement], "chat123", "token", memoire)

    assert ok is True
    assert memoire["exemple.fr|etb-151"]["en_stock"] is True


def test_echec_envoi_ne_commite_pas_la_memoire():
    memoire = {"exemple.fr|etb-151": {"en_stock": False}}
    evenement = _candidat(en_stock=True)
    evenement["_cle_memoire"] = "exemple.fr|etb-151"
    evenement["_nouvel_etat"] = {"en_stock": True, "titre_produit": evenement["titre"]}

    with patch("radar_precommande_generique.requests.post", side_effect=requests.RequestException("boom")):
        ok = envoyer_telegram_precommandes_generiques([evenement], "chat123", "token", memoire)

    assert ok is False
    # Toujours False -- l'evenement pourra etre redetecte au prochain cycle.
    assert memoire["exemple.fr|etb-151"]["en_stock"] is False


def test_sans_token_najoute_rien_et_ne_leve_pas():
    ok = envoyer_telegram_precommandes_generiques([_candidat()], "chat123", "", None)
    assert ok is False


def test_liste_vide_najoute_rien():
    ok = envoyer_telegram_precommandes_generiques([], "chat123", "token", None)
    assert ok is True


# ------------------- scanner_shopify_precommandes_generiques -------------------

def test_scanner_shopify_filtre_le_catalogue_et_extrait_le_stock():
    connecteur = Mock()
    connecteur.base_url = "https://exemple.fr"
    connecteur.recuperer_tout_le_catalogue.return_value = [
        {
            "title": "Précommande Pokémon Coffret Dresseur d'Élite 151",
            "body_html": "<p>Disponible en précommande</p>",
            "handle": "etb-151",
            "variants": [{"price": "59.99", "available": True}],
        },
        {
            "title": "Dracaufeu ex 199/165",
            "body_html": "",
            "handle": "dracaufeu-ex",
            "variants": [{"price": "38.50", "available": True}],
        },
    ]

    candidats = scanner_shopify_precommandes_generiques("exemple.fr", connecteur=connecteur)

    assert len(candidats) == 1
    assert candidats[0]["slug"] == "etb-151"
    assert candidats[0]["url_produit"] == "https://exemple.fr/products/etb-151"
    assert candidats[0]["en_stock"] is True
    assert candidats[0]["prix"] == 59.99
