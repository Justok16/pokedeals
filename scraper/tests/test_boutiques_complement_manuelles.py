from scan_precommandes import _boutiques_et_replis_complement


def test_sources_manuelles_persistantes_et_vendeur_belge_exclu():
    boutiques, modes = _boutiques_et_replis_complement("shopify")
    assert {"etw-tcg.com", "lorenzone.fr"} <= set(boutiques)
    assert "outpostbrussels.be" not in boutiques
    assert len(boutiques) == len(set(boutiques))
    assert modes == {}
