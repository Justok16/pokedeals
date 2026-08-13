"""Tests de non-regression pour les fonctions de matching partagees par les
3 connecteurs (connecteur_shopify.py), issues de bugs reels deja rencontres
et corriges -- cf. SESSION_NOTES.md pour le detail de chaque cas."""

from connecteur_shopify import (
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
