"""Perimetre COMPLEMENT du radar (04/10/2026) : memes plateformes, listes et
memoire distinctes du perimetre principal."""

import boutiques_complement as bc
import scan_precommandes as sp
import boutiques_complement_manuelles as manuelles


def test_complement_utilise_les_listes_du_fichier_complement():
    boutiques_shopify, modes_shopify = sp._boutiques_et_replis("shopify", complement=True)
    assert (set(bc.BOUTIQUES_COMPLEMENT_SHOPIFY) - manuelles.VENDEURS_SANS_LIVRAISON_FRANCE) <= set(boutiques_shopify)
    assert set(manuelles.BOUTIQUES_SHOPIFY) <= set(boutiques_shopify)
    assert modes_shopify == {}
    boutiques, modes = sp._boutiques_et_replis("prestashop", complement=True)
    assert set(bc.BOUTIQUES_COMPLEMENT_PRESTASHOP_REPLI_HTML) <= set(boutiques)
    assert all(modes[d] == "html" for d in bc.BOUTIQUES_COMPLEMENT_PRESTASHOP_REPLI_HTML)
    boutiques_woo, modes_woo = sp._boutiques_et_replis("woocommerce", complement=True)
    assert boutiques_woo[:len(bc.BOUTIQUES_COMPLEMENT_WOOCOMMERCE_SITEMAP)] == list(bc.BOUTIQUES_COMPLEMENT_WOOCOMMERCE_SITEMAP)
    # 08/10/2026 : PixelHeart, lue par la Store API (pas de sitemap).
    assert modes_woo == {d: "api_rest" for d in manuelles.BOUTIQUES_WOOCOMMERCE_API_REST}
    assert set(manuelles.BOUTIQUES_WOOCOMMERCE_API_REST) <= set(boutiques_woo)


def test_aucune_boutique_complement_nest_deja_dans_le_perimetre_principal():
    for plateforme in ("shopify", "prestashop", "woocommerce"):
        principal = set(sp._boutiques_et_replis(plateforme)[0])
        complement = set(sp._boutiques_et_replis(plateforme, complement=True)[0])
        assert not (principal & complement), principal & complement


def test_cles_memoire_distinctes_entre_perimetres():
    for cle in sp.CLE_MEMOIRE_PAR_PLATEFORME.values():
        assert cle + sp.SUFFIXE_MEMOIRE_COMPLEMENT != cle
