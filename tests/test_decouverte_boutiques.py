"""Tests de non-regression pour decouverte_boutiques.py -- premiere
couverture dediee (audit du 18/08/2026).

Bug corrige : un domaine ajoute automatiquement (BOUTIQUES_*_AUTO) AVANT
d'etre rejete manuellement par Justok (DOMAINES_REJETES_MANUELLEMENT)
restait actif dans boutiques_decouvertes.py et continuait d'etre scanne --
la synchronisation memoire (dans main()) empechait seulement une
RE-proposition future, jamais un retrait retroactif."""

from unittest.mock import patch

from decouverte_boutiques import _retirer_domaines_rejetes


def test_retire_un_domaine_deja_auto_ajoute_puis_rejete_manuellement():
    listes = {
        "shopify": ["boutique-ok.fr", "nemee-tcg.fr"],
        "shopify_precommande": [],
        "woocommerce": [],
        "woocommerce_precommande": ["nemee-tcg.fr"],
    }
    with patch("decouverte_boutiques.DOMAINES_REJETES_MANUELLEMENT", {"nemee-tcg.fr"}):
        resultat = _retirer_domaines_rejetes(listes)
    assert resultat["shopify"] == ["boutique-ok.fr"]
    assert resultat["woocommerce_precommande"] == []


def test_naffecte_pas_les_domaines_non_rejetes():
    listes = {"shopify": ["a.fr", "b.fr"], "shopify_precommande": [], "woocommerce": [], "woocommerce_precommande": []}
    with patch("decouverte_boutiques.DOMAINES_REJETES_MANUELLEMENT", {"autre-domaine.fr"}):
        resultat = _retirer_domaines_rejetes(listes)
    assert resultat["shopify"] == ["a.fr", "b.fr"]


def test_aucun_rejet_manuel_laisse_toutes_les_listes_intactes():
    listes = {"shopify": ["a.fr"], "shopify_precommande": ["b.fr"], "woocommerce": [], "woocommerce_precommande": []}
    with patch("decouverte_boutiques.DOMAINES_REJETES_MANUELLEMENT", set()):
        resultat = _retirer_domaines_rejetes(listes)
    assert resultat == listes
