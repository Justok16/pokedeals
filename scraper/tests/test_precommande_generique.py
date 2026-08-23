from precommande_generique import (
    CATEGORIE_AUTRE,
    CATEGORIE_BOOSTERS_BLISTERS,
    CATEGORIE_COFFRETS,
    CATEGORIE_DISPLAYS,
    CATEGORIE_ETB,
    CATEGORIE_POKEBOX_TINS,
    determiner_categorie_produit,
    produit_est_candidat_precommande,
)


# ------------------- cas positifs -------------------

def test_match_coffret_dresseur_elite():
    ok, raison = produit_est_candidat_precommande(
        "Précommande - Coffret Dresseur d'Élite Pokémon ME07"
    )
    assert ok is True
    assert "confirmes" in raison


def test_match_via_description_pas_seulement_titre():
    ok, _ = produit_est_candidat_precommande(
        "ETB Pokemon", description="Article disponible en précommande, sortie prochaine."
    )
    assert ok is True


def test_match_insensible_accents_et_casse():
    ok, _ = produit_est_candidat_precommande(
        "PRECOMMANDE POKEMON DISPLAY BOOSTER BOX ECARLATE VIOLET"
    )
    assert ok is True


def test_match_upc():
    ok, _ = produit_est_candidat_precommande(
        "Précommande Pokémon UPC Umbreon 30e Anniversaire"
    )
    assert ok is True


# ------------------- rejets -------------------

def test_rejet_sans_mention_pokemon():
    ok, raison = produit_est_candidat_precommande(
        "Précommande Coffret Dresseur d'Élite Écarlate et Violet ME07"
    )
    assert ok is False
    assert "Pokemon" in raison


def test_rejet_autre_franchise():
    ok, raison = produit_est_candidat_precommande(
        "Précommande Pokémon x Yu-Gi-Oh Coffret Collector Croisé"
    )
    assert ok is False
    assert "franchise" in raison


def test_rejet_franchise_pure_meme_avec_pokemon_absent_du_flux():
    ok, raison = produit_est_candidat_precommande(
        "Précommande Display Pokémon One Piece Card Game"
    )
    assert ok is False
    assert "franchise" in raison


def test_rejet_sans_mention_precommande():
    ok, raison = produit_est_candidat_precommande(
        "Coffret Dresseur d'Élite Pokémon ME07"
    )
    assert ok is False
    assert "precommande" in raison


def test_rejet_precommande_en_anglais_seulement_ne_matche_pas():
    """Demande explicite de Justok (23/08/2026) : pas d'anglais "pre-order"/
    "preorder", seulement le francais "precommande"."""
    ok, raison = produit_est_candidat_precommande(
        "Pre-order Pokemon Elite Trainer Box"
    )
    assert ok is False
    assert "precommande" in raison


def test_rejet_sans_type_produit_scelle():
    ok, raison = produit_est_candidat_precommande(
        "Précommande Pokémon Dracaufeu ex 199/165"
    )
    assert ok is False
    assert "type de produit" in raison


def test_rejet_carte_a_lunite_deja_en_vente():
    ok, _ = produit_est_candidat_precommande(
        "Pokémon Pikachu 25/102 Base Set"
    )
    assert ok is False


# ------------------- determiner_categorie_produit -------------------

def test_categorie_etb():
    assert determiner_categorie_produit("Coffret Dresseur d'Élite Pokémon ME07") == CATEGORIE_ETB


def test_categorie_display():
    assert determiner_categorie_produit("Display Pokémon Écarlate Violet") == CATEGORIE_DISPLAYS


def test_categorie_boosters_blisters():
    assert determiner_categorie_produit("Blister Pokémon 3 boosters") == CATEGORIE_BOOSTERS_BLISTERS


def test_categorie_coffrets():
    assert determiner_categorie_produit("Collection Premium Pokémon Umbreon") == CATEGORIE_COFFRETS


def test_categorie_pokebox_tins():
    assert determiner_categorie_produit("Pokébox Tin Métal Pokémon Dracaufeu") == CATEGORIE_POKEBOX_TINS


def test_categorie_autre_si_aucun_mot_cle_ne_matche():
    assert determiner_categorie_produit("Précommande Pokémon Objet Mystère") == CATEGORIE_AUTRE


def test_categorie_etb_prioritaire_sur_coffret_generique():
    """"ETB" doit l'emporter meme si "boite"/"box" (mots-cles generiques de
    CATEGORIE_COFFRETS) apparaissent aussi dans le meme titre."""
    assert determiner_categorie_produit(
        "Précommande ETB Pokémon (Elite Trainer Box, coffret dresseur)"
    ) == CATEGORIE_ETB


def test_categorie_display_prioritaire_sur_booster():
    """"display" (categorie specifique) l'emporte sur "booster" (categorie
    plus generique) quand les deux mots apparaissent dans le meme titre."""
    assert determiner_categorie_produit("Display de boosters Pokémon") == CATEGORIE_DISPLAYS
