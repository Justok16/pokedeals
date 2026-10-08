from scan_precommandes import _boutiques_et_replis_complement


def test_sources_manuelles_persistantes_et_vendeur_belge_livrant_la_france_garde():
    boutiques, modes = _boutiques_et_replis_complement("shopify")
    assert {"etw-tcg.com", "lorenzone.fr"} <= set(boutiques)
    assert "outpostbrussels.be" in boutiques   # livre en France (regle de Justok, 08/10/2026)
    assert len(boutiques) == len(set(boutiques))
    assert modes == {}
