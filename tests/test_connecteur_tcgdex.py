"""Tests de non-regression pour connecteur_tcgdex.py (extrait de main.py
le 17/08/2026) -- deduction d'identifiant TCGdex, un cas par piege reel
deja documente en commentaire (V47 : padding a 3 chiffres, sets JP
exclusifs, denominateur inconnu = pas de match)."""

import connecteur_tcgdex as tcgdex


def test_deduire_api_id_priorite_au_champ_config():
    assert tcgdex.deduire_api_id({"nom": "X", "langue": "fr", "api_id": "swshp-SWSH087"}) == "swshp-SWSH087"


def test_deduire_api_id_coreen_toujours_none():
    assert tcgdex.deduire_api_id({"nom": "Dracaufeu ex 199/165", "langue": "kr"}) is None


def test_deduire_api_id_serie_151_fr():
    assert tcgdex.deduire_api_id({"nom": "Dracaufeu ex 199/165", "langue": "fr"}) == "sv03.5-199"


def test_deduire_api_id_jp_avec_code_de_set_padding_3_chiffres():
    # V47 : le numero local DOIT etre complete a 3 chiffres, jamais "m2-85".
    assert tcgdex.deduire_api_id({"nom": "Piplup 085 m2", "langue": "jp"}) == "m2-085"


def test_deduire_api_id_jp_sans_code_set_via_denominateur_connu():
    assert tcgdex.deduire_api_id({"nom": "Goldeen 084/081", "langue": "jp"}) == "m5-084"


def test_deduire_api_id_jp_sans_aucun_indice_retourne_none():
    assert tcgdex.deduire_api_id({"nom": "Morpeko ex 117", "langue": "jp"}) is None


def test_deduire_api_id_promo_swsh():
    assert tcgdex.deduire_api_id({"nom": "Dracaufeu SWSH087", "langue": "fr"}) == "swshp-SWSH087"


def test_deduire_api_id_promo_sv_mot_cle():
    assert tcgdex.deduire_api_id({"nom": "Dracaufeu promo 056", "langue": "fr"}) == "svp-056"


def test_api_lire_prix_prend_le_premier_champ_disponible():
    data = {"pricing": {"cardmarket": {"trend": 42.5}}}
    assert tcgdex._api_lire_prix(data) == 42.5


def test_api_lire_prix_repli_sur_low_si_trend_absent():
    data = {"pricing": {"cardmarket": {"low": 12.0}}}
    assert tcgdex._api_lire_prix(data) == 12.0


def test_api_lire_prix_aucune_donnee_renvoie_none():
    assert tcgdex._api_lire_prix({}) is None
    assert tcgdex._api_lire_prix({"pricing": {"cardmarket": {"trend": 0}}}) is None


def test_api_prix_carte_coreen_ne_fait_aucun_appel_reseau(monkeypatch):
    def _echoue(*args, **kwargs):
        raise AssertionError("aucun appel reseau attendu pour une carte coreenne")
    monkeypatch.setattr(tcgdex.requests, "get", _echoue)
    assert tcgdex.api_prix_carte({"nom": "Dracaufeu ex 199/165", "langue": "kr"}) is None
