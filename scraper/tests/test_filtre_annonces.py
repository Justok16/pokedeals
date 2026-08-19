"""Tests de non-regression pour filtre_annonces.py (extrait de main.py le
16/08/2026) -- un cas par bug reel deja rencontre en prod, documente dans
les commentaires V15/V17.4/V26/V28/V30/V38/V39 du module."""

from filtre_annonces import (
    annonce_pertinente,
    extraire_numero,
    extraire_numero_annonce,
    normaliser,
    numero_nu_voulu,
    preuve_francais,
)


def test_numero_obligatoire_v15():
    # "Dracaufeu" seul (5€) ne doit jamais matcher "Dracaufeu ex 199/165" (200€).
    ok, raison = annonce_pertinente("Dracaufeu carte holo", "Dracaufeu ex 199/165")
    assert ok is False
    assert "numéro" in raison


def test_bon_numero_et_bon_pokemon_acceptes():
    ok, _ = annonce_pertinente("Dracaufeu ex 199/165 carte holo NM", "Dracaufeu ex 199/165")
    assert ok is True


def test_mauvais_numero_rejete():
    ok, raison = annonce_pertinente("Dracaufeu ex 200/165 carte holo", "Dracaufeu ex 199/165")
    assert ok is False
    assert "mauvais numéro" in raison


def test_separateur_tiret_v38():
    # "199-165" au lieu du slash standard "199/165" -- doit quand meme matcher.
    ok, _ = annonce_pertinente("Dracaufeu ex 199-165 carte holo", "Dracaufeu ex 199/165")
    assert ok is True


def test_carte_coreenne_avec_code_set_japonais_rejetee_pour_fr_v28():
    # Cas reel : carte COREENNE (sv2a 173/165) faussement comparee a la cote FR.
    ok, raison = annonce_pertinente(
        "Pikachu AR sv2a 173/165 - État parfait", "Pikachu AR 173/165", langue="fr",
    )
    assert ok is False
    assert "japonais" in raison


def test_carte_italienne_giapponese_detectee_v30():
    ok, raison = annonce_pertinente(
        "Pokémon Pikachu AR 173/165 – Giapponese – Art Rare", "Pikachu AR 173/165", langue="fr",
    )
    assert ok is False
    assert "étrangère" in raison


def test_preuve_positive_francais_v26_rejette_italienne_neutre():
    # "Mew" s'ecrit pareil en FR/EN/IT/DE/ES : le nom seul ne prouve rien.
    # Sans mot francais explicite dans le titre, doit etre rejete pour une carte FR.
    ok, raison = annonce_pertinente("Mew ex 205/165 carta condizioni", "Mew ex 205/165", langue="fr")
    assert ok is False


def test_non_gradee_neutralisee_avant_exclusion_v39():
    # "non gradée" ne doit pas etre rejetee a cause du mot "gradee" dans EXCLUSIONS.
    ok, _ = annonce_pertinente("Dracaufeu ex 199/165 non gradée NM", "Dracaufeu ex 199/165")
    assert ok is True


def test_carte_gradee_reellement_rejetee():
    ok, raison = annonce_pertinente("Dracaufeu ex 199/165 PSA 9", "Dracaufeu ex 199/165")
    assert ok is False
    assert "exclue" in raison


def test_lot_rejete():
    ok, raison = annonce_pertinente("Lot de 10 cartes Pokémon", "Dracaufeu ex 199/165")
    assert ok is False
    assert "exclue" in raison


def test_numero_nu_pbl_v17_4_bonne_carte():
    # Darkrai ex 116 (sans denominateur) vs Darkrai ex 120 -- meme Pokemon,
    # numeros nus differents, ne doivent pas se confondre.
    ok, _ = annonce_pertinente("Darkrai ex 116 carte holo NM", "Darkrai ex 116")
    assert ok is True


def test_numero_nu_pbl_v17_4_mauvaise_carte_rejetee():
    ok, raison = annonce_pertinente("Darkrai ex 120 carte holo NM", "Darkrai ex 116")
    assert ok is False
    assert "116" in raison


def test_carte_mega_ne_pollue_pas_recherche_non_mega():
    ok, raison = annonce_pertinente("Méga-Dracaufeu ex 116/165 carte holo", "Dracaufeu ex 199/165")
    assert ok is False
    assert "Méga" in raison


def test_nom_de_set_mega_evolution_nest_pas_confondu_avec_carte_mega():
    # "Méga-Évolution" est un nom de SET japonais, pas une carte Méga.
    ok, _ = annonce_pertinente(
        "Bulbizarre 010/070 - Méga-Évolution carte holo", "Bulbizarre 010/070",
    )
    assert ok is True


def test_alias_accepte_a_la_place_du_nom_principal():
    ok, _ = annonce_pertinente(
        "Tortank ex 200/165 carte holo NM", "Blastoise ex 200/165", alias="Tortank",
    )
    assert ok is True


def test_langue_jp_confirmee_par_script_asiatique():
    ok, _ = annonce_pertinente("Pikachu AR 173/165 ピカチュウ", "Pikachu AR 173/165", langue="jp")
    assert ok is True


def test_langue_jp_rejetee_si_script_coreen():
    ok, raison = annonce_pertinente("Dracaufeu ex 199/165 card 리자몽", "Dracaufeu ex 199/165", langue="jp")
    assert ok is False
    assert "script" in raison


def test_extraire_numero_formats():
    assert extraire_numero("Dracaufeu ex 199/165") == "199/165"
    assert extraire_numero("Dracaufeu ex sans numero") is None


def test_extraire_numero_annonce_repli_tiret():
    assert extraire_numero_annonce("199-165") == "199/165"
    assert extraire_numero_annonce("aucun numero") is None


def test_numero_nu_voulu_absent_si_format_xy():
    assert numero_nu_voulu("Dracaufeu ex 199/165") is None
    assert numero_nu_voulu("Darkrai ex 116") == "116"


def test_normaliser_accents_et_tirets():
    assert normaliser("Méga-Dracaufeu") == "mega dracaufeu"


def test_preuve_francais_detecte_mot_francais():
    assert preuve_francais("Dracaufeu ex 199/165 carte française neuve") is True
    assert preuve_francais("Dracaufeu ex 199/165 carta italiana") is False
