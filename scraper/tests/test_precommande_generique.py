from precommande_generique import produit_est_candidat_precommande


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
