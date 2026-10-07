"""Scans PrestaShop et WooCommerce : lecture reseau des boutiques en parallele
(07/10/2026). Meme resultat que l'ancien comportement sequentiel."""

import threading
import time

import pytest

import scan_boutique_prestashop as sbp
import scan_boutique_woocommerce as sbw

BOUTIQUES = [f"boutique{i}.fr" for i in range(10)]


class _Carte:
    def __init__(self, cle):
        self.cle_recherche = cle


CARTES = [_Carte("pikachu"), _Carte("dracaufeu")]


def _installer(monkeypatch, module, delai=0.0, echecs=()):
    en_cours, pic, replis = [0], [0], []
    verrou = threading.Lock()

    def faux_lire(domaine, criteres, repli=False):
        with verrou:
            en_cours[0] += 1
            pic[0] = max(pic[0], en_cours[0])
            if repli:
                replis.append(domaine)
        time.sleep(delai)
        with verrou:
            en_cours[0] -= 1
        if domaine in echecs:
            raise RuntimeError(f"boutique {domaine} en panne")
        assert criteres == ["pikachu", "dracaufeu"]
        return {"domaine": domaine}

    def faux_deals(resultats, cartes_par_critere, cotes, regles):
        return [{"deal": resultats["domaine"]}]

    def faux_stock(domaine, resultats, cartes_par_critere, memoire):
        memoire.setdefault("ordre", []).append(domaine)   # trace l'ordre de traitement
        return [{"stock": domaine}]

    monkeypatch.setattr(module, "lire_resultats", faux_lire)
    monkeypatch.setattr(module, "detecter_bonnes_affaires", faux_deals)
    monkeypatch.setattr(module, "detecter_retours_en_stock", faux_stock)
    monkeypatch.setattr(module, "DELAI_ENTRE_BOUTIQUES", 0)
    return pic, replis


def _lancer(monkeypatch, module, parallelisme, replis=None, **kw):
    monkeypatch.setenv("SCAN_PARALLELISME", str(parallelisme))
    pic, vus_repli = _installer(monkeypatch, module, **kw)
    memoire = {}
    res = module.scanner_plusieurs_boutiques(BOUTIQUES, CARTES, memoire, {}, {}, replis or set())
    return res, memoire, pic, vus_repli


MODULES = [pytest.param(sbp, id="prestashop"), pytest.param(sbw, id="woocommerce")]


@pytest.mark.parametrize("module", MODULES)
def test_resultat_identique_en_parallele_et_en_sequentiel(monkeypatch, module):
    seq, mem_seq, _, _ = _lancer(monkeypatch, module, 1)
    par, mem_par, _, _ = _lancer(monkeypatch, module, 4)
    assert par["deals"] == seq["deals"]
    assert par["evenements_stock"] == seq["evenements_stock"]
    assert par["boutiques_ok"] == seq["boutiques_ok"] == BOUTIQUES
    assert mem_par == mem_seq == {"ordre": BOUTIQUES}


@pytest.mark.parametrize("module", MODULES)
def test_echec_isole_sans_ecriture_memoire(monkeypatch, module):
    res, memoire, _, _ = _lancer(monkeypatch, module, 4, echecs={"boutique2.fr", "boutique8.fr"})
    assert [e["domaine"] for e in res["boutiques_echec"]] == ["boutique2.fr", "boutique8.fr"]
    assert "en panne" in res["boutiques_echec"][1]["raison"]
    assert "boutique2.fr" not in memoire["ordre"]
    assert len(res["boutiques_ok"]) == 8


@pytest.mark.parametrize("module", MODULES)
def test_mode_repli_transmis(monkeypatch, module):
    _, _, _, vus = _lancer(monkeypatch, module, 4, replis={"boutique5.fr"})
    assert vus == ["boutique5.fr"]


@pytest.mark.parametrize("module", MODULES)
def test_lectures_reellement_paralleles_et_bornees(monkeypatch, module):
    _, _, pic, _ = _lancer(monkeypatch, module, 4, delai=0.05)
    assert 2 <= pic[0] <= 4
    _, _, pic, _ = _lancer(monkeypatch, module, 1, delai=0.01)
    assert pic[0] == 1


@pytest.mark.parametrize("module", MODULES)
def test_scanner_boutique_complet_inchange(monkeypatch, module):
    _installer(monkeypatch, module)
    memoire = {}
    deals, evts = module.scanner_boutique_complet("x.fr", CARTES, memoire, {}, {})
    assert deals == [{"deal": "x.fr"}] and evts == [{"stock": "x.fr"}]
    assert memoire == {"ordre": ["x.fr"]}
