"""Tests de non-regression pour connecteur_cardtrader.py (extrait de
main.py le 17/08/2026) -- fonctions pures de matching/calibration, et le
piege specifique de reassignation de _ct_cache (cf. SESSION_NOTES.md)."""

import connecteur_cardtrader as ct
import main


def test_cardtrader_prix_sans_token_ne_fait_aucun_appel_reseau():
    assert ct.cardtrader_prix({"nom": "Dracaufeu ex 199/165", "langue": "fr"}, "") is None


def test_ct_numero_de_extrait_le_format_fraction():
    bp = {"name": "Charizard ex (199/165)"}
    assert ct._ct_numero_de(bp) == "199"


def test_ct_numero_de_extrait_le_format_diese():
    bp = {"name": "Pikachu #173"}
    assert ct._ct_numero_de(bp) == "173"


def test_ct_numero_de_ignore_lid_dans_le_slug():
    # Le slug commence par l'ID Cardtrader -- ne doit jamais etre pris
    # pour le numero de la carte (cas reel documente dans le code).
    bp = {"slug": "110706-pikachu-48-162-breakthrough"}
    assert ct._ct_numero_de(bp) == "48"


def test_ct_numero_de_champ_dedie_prioritaire():
    bp = {"fixed_properties": {"collector_number": "042"}, "name": "Autre chose 199/165"}
    assert ct._ct_numero_de(bp) == "042"


def test_ct_indices_set_par_denominateur():
    assert ct._ct_indices_set("Dracaufeu ex 199/165", "165") == ["151"]


def test_ct_indices_set_par_code_jp():
    assert ct._ct_indices_set("Mega Darkrai ex 114 m3", "") == ["nihil zero"]


def test_ct_indices_set_sans_correspondance():
    assert ct._ct_indices_set("Carte inconnue", "999") == []


def test_ct_incoherent_entre_langues_detecte_ecart_absurde():
    ct._ct_prix_par_carte.clear()
    ct._ct_memoriser_prix({"nom": "Mew ex 208", "langue": "jp"}, 51.0)
    suspect, motif = ct._ct_incoherent_entre_langues({"nom": "Mew ex 208", "langue": "kr"}, 5020.0, 5.0)
    assert suspect is True
    assert "51.00" in motif


def test_ct_incoherent_entre_langues_ecart_normal_nest_pas_suspect():
    ct._ct_prix_par_carte.clear()
    ct._ct_memoriser_prix({"nom": "Dracaufeu ex 199/165", "langue": "fr"}, 100.0)
    suspect, _ = ct._ct_incoherent_entre_langues({"nom": "Dracaufeu ex 199/165", "langue": "jp"}, 120.0, 5.0)
    assert suspect is False


def test_calibration_ajoute_seulement_les_rapports_raisonnables():
    ct._calibration_paires.clear()
    ct._calibration_ajouter(100.0, 110.0)   # rapport 1.1 -- garde
    ct._calibration_ajouter(100.0, 5000.0)  # rapport 50 -- absurde, ignore
    assert ct._calibration_paires == [1.1]


def test_calibration_coefficient_none_sous_le_minimum():
    ct._calibration_paires.clear()
    ct._calibration_paires.extend([1.0, 1.1, 1.2])  # 3 < 5 minimum
    assert ct._calibration_coefficient() is None


def test_calibration_coefficient_median_au_dessus_du_minimum():
    ct._calibration_paires.clear()
    ct._calibration_paires.extend([1.0, 1.1, 1.2, 0.9, 1.05])
    assert ct._calibration_coefficient() == 1.05


def test_ct_signature_code_ne_plante_jamais():
    # Fonction utilisee pour purger le cache -- ne doit jamais lever, meme
    # si inspect.getsource echoue (repli sur CT_CACHE_VERSION).
    sig = ct._ct_signature_code()
    assert isinstance(sig, str)
    assert len(sig) > 0


def test_ct_cache_reassignation_visible_via_acces_qualifie():
    """Piege specifique corrige lors de l'extraction (17/08/2026) :
    _ct_charger_cache() REASSIGNE _ct_cache (global _ct_cache; _ct_cache =
    {...}), pas juste .update(). cardmarket_prix() (reste dans main.py)
    doit donc lire via connecteur_cardtrader._ct_cache (acces qualifie),
    jamais via un `from connecteur_cardtrader import _ct_cache` qui
    figerait la liaison sur l'ancien objet et lirait un cache perime."""
    ct._ct_cache = {"blueprints": {"fr|Test": {"id": 1, "cm_id": 777}}, "prix": {}}
    assert ct._ct_cache["blueprints"]["fr|Test"]["cm_id"] == 777

    # main.cardmarket_prix() doit utiliser l'acces qualifie -- verifie que
    # le code source ne reintroduit jamais un import direct de _ct_cache.
    import inspect
    source = inspect.getsource(main.cardmarket_prix)
    assert "connecteur_cardtrader._ct_cache" in source
    assert "_ct_cache[" not in source.replace("connecteur_cardtrader._ct_cache[", "")
