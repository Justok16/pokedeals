"""Tests de non-regression pour les fonctions de matching partagees par les
3 connecteurs (connecteur_shopify.py), issues de bugs reels deja rencontres
et corriges -- cf. SESSION_NOTES.md pour le detail de chaque cas."""

from unittest.mock import Mock, patch

import pytest
import requests

from connecteur_shopify import (
    ConnecteurShopify,
    CritereRecherche,
    _regex_numero_sans_denominateur,
    _retirer_fractions,
    _titre_correspond,
    detecter_etat,
    detecter_langue,
)


def test_detecter_langue_mot_explicite():
    assert detecter_langue("Dracaufeu ex 199/165 - Version Japonaise") == "jp"
    assert detecter_langue("Charizard ex - English Version") == "en"


def test_detecter_langue_aucune_mention():
    assert detecter_langue("Dracaufeu ex 199/165") is None


def test_detecter_langue_code_set_asiatique_sans_mot_explicite():
    # Bug reel corrige (2026-08-10) : "Bulbizarre AR 166/165 - SV2A" n'etait
    # detecte dans AUCUNE langue faute de mot explicite "japonais" -- SV2A
    # est pourtant un code de set exclusivement japonais.
    assert detecter_langue("Bulbizarre AR 166/165 - SV2A") == "jp_ou_kr"


def test_retirer_fractions_garde_le_numerateur():
    # Bug reel corrige (2026-08-11) : "054/078" est une fraction SANS
    # RAPPORT avec une carte dont le numero nu est "078" (le "078" ici est
    # le DENOMINATEUR, pas le numero de la carte).
    resultat = _retirer_fractions("Evoli 054/078 Commune Pokemon GO")
    assert "078" not in resultat
    assert "054" in resultat


def test_retirer_fractions_garde_un_vrai_numero_avec_denominateur():
    # Le numerateur d'une fraction legitime doit rester trouvable ensuite.
    resultat = _retirer_fractions("Eevee 078/069 SAR sv5a Crimson Haze")
    assert "078" in resultat


def test_regex_numero_sans_denominateur_tolere_le_padding_de_zeros():
    regex = _regex_numero_sans_denominateur("087")
    assert regex.search("SWSH087")
    assert regex.search("swsh87")
    assert not regex.search("swsh1087")  # ne doit pas matcher a l'interieur d'un plus grand nombre


def test_titre_correspond_faux_positif_fraction_denominateur():
    # Reproduction du bug reel : "Eevee 078 sv5a" (numero nu "078") ne doit
    # PAS matcher "Evoli 054/078 Commune Pokemon GO" (carte FR sans rapport).
    critere = CritereRecherche(nom="Evoli", numero="078")
    assert _titre_correspond("Carte Pokemon Evoli 054/078 Commune Pokemon GO (JCC)", critere) is False


def test_titre_correspond_vrai_numero_sans_denominateur_toujours_valide():
    critere = CritereRecherche(nom="Eevee", numero="078")
    assert _titre_correspond("Eevee 078/069 SAR sv5a Crimson Haze", critere) is True


def test_detecter_etat_label_simple():
    # Cas reel (14/08/2026) : kairyu.fr, fiche produit "Etat : Exc".
    assert detecter_etat("<p>Série : Terastal Fest ex</p><p>Etat : Exc</p>") == "exc"


def test_detecter_etat_avec_accent_et_valeur_composee():
    assert detecter_etat("État: Near Mint") == "near mint"


def test_detecter_etat_aucun_label_present():
    assert detecter_etat("<h1>223/187 Eevee ex</h1><p>Prix : 32.90€</p>") is None


def test_detecter_etat_ignore_le_mot_excellent_hors_champ_dedie():
    # "excellent" perdu dans un paragraphe marketing (pas apres un label
    # d'etat) ne doit PAS etre capture -- seul un vrai champ structure compte.
    assert detecter_etat("<p>Carte conservee en excellent etat de collection</p>") is None


# ------------------- recuperer_tout_le_catalogue (audit du 18/08/2026) -------------------
# Avant ce correctif, un echec de la page 1 (reseau/timeout/JSON invalide)
# renvoyait un catalogue vide SANS lever -- indiscernable d'une boutique sans
# aucun produit ce cycle. Consequence reelle : alerte_stock.py enregistrait
# `en_stock: False` pour chaque carte suivie, creant une fausse alerte
# "retour en stock" des que le reseau se retablissait. Cf. commentaire de
# recuperer_tout_le_catalogue() pour le detail complet.

def test_recuperer_catalogue_leve_si_la_page_1_echoue_reseau():
    c = ConnecteurShopify("boutique-en-panne.fr")
    with patch.object(c.session, "get", side_effect=requests.exceptions.ConnectionError("panne")):
        with pytest.raises(RuntimeError):
            c.recuperer_tout_le_catalogue()


def test_recuperer_catalogue_leve_si_la_page_1_renvoie_un_json_invalide():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    reponse.json = Mock(side_effect=ValueError("JSON invalide"))
    c = ConnecteurShopify("boutique-cassee.fr")
    with patch.object(c.session, "get", return_value=reponse):
        with pytest.raises(RuntimeError):
            c.recuperer_tout_le_catalogue()


def test_recuperer_catalogue_ne_leve_pas_si_la_page_1_est_reellement_vide():
    # Boutique reelle sans aucun produit -- resultat legitime, pas une erreur.
    reponse = Mock()
    reponse.raise_for_status = Mock()
    reponse.json = Mock(return_value={"products": []})
    c = ConnecteurShopify("boutique-vide.fr")
    with patch.object(c.session, "get", return_value=reponse):
        assert c.recuperer_tout_le_catalogue() == []


def test_recuperer_catalogue_tolere_un_echec_sur_une_page_suivante():
    # Page 1 OK (catalogue partiel deja utile) -> une page 2 en echec ne
    # doit PAS faire lever d'exception, juste arreter la pagination.
    page_1 = Mock()
    page_1.raise_for_status = Mock()
    page_1.json = Mock(return_value={"products": [{"id": 1, "title": "Dracaufeu ex 199/165"}] * 250})
    c = ConnecteurShopify("boutique-ok.fr")
    with patch.object(c.session, "get", side_effect=[page_1, requests.exceptions.Timeout("trop long")]):
        produits = c.recuperer_tout_le_catalogue()
    assert len(produits) == 250
