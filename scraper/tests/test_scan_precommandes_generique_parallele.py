"""Radar precommandes generiques : lecture des catalogues en parallele (07/10/2026).
Meme resultat que l'ancien comportement sequentiel, mais plus rapide."""

import threading
import time

import scan_precommandes_generique as spg

BOUTIQUES = [f"boutique{i}.fr" for i in range(10)]


def _installer(monkeypatch, delai=0.0, echecs=()):
    en_cours, pic = [0], [0]
    verrou = threading.Lock()

    def faux_scanner(domaine):
        with verrou:
            en_cours[0] += 1
            pic[0] = max(pic[0], en_cours[0])
        time.sleep(delai)
        with verrou:
            en_cours[0] -= 1
        if domaine in echecs:
            raise RuntimeError(f"boutique {domaine} en panne")
        return [{"domaine": domaine}]

    def faux_detecter(candidats, memoire):
        domaine = candidats[0]["domaine"]
        memoire.setdefault("ordre", []).append(domaine)
        return [{"domaine": domaine}]

    monkeypatch.setattr(spg, "scanner_shopify_precommandes_generiques", faux_scanner)
    monkeypatch.setattr(spg, "detecter_nouvelles_precommandes_generiques", faux_detecter)
    monkeypatch.setattr(spg, "DELAI_ENTRE_BOUTIQUES", 0)
    return pic


def _lancer(monkeypatch, parallelisme, **kw):
    monkeypatch.setenv("PRECO_GENERIQUE_PARALLELISME", str(parallelisme))
    pic = _installer(monkeypatch, **kw)
    memoire = {}
    return spg.scanner_plusieurs_boutiques(BOUTIQUES, memoire), memoire, pic


def test_resultat_identique_en_parallele_et_en_sequentiel(monkeypatch):
    seq, mem_seq, _ = _lancer(monkeypatch, 1)
    par, mem_par, _ = _lancer(monkeypatch, 4)
    assert par["evenements"] == seq["evenements"]
    assert par["boutiques_ok"] == seq["boutiques_ok"] == BOUTIQUES
    assert mem_par == mem_seq == {"ordre": BOUTIQUES}


def test_echec_isole_et_dans_l_ordre(monkeypatch):
    res, memoire, _ = _lancer(monkeypatch, 4, echecs={"boutique3.fr", "boutique7.fr"})
    assert [e["domaine"] for e in res["boutiques_echec"]] == ["boutique3.fr", "boutique7.fr"]
    assert "en panne" in res["boutiques_echec"][0]["raison"]
    assert "boutique3.fr" not in memoire["ordre"]
    assert len(res["boutiques_ok"]) == 8


def test_lectures_reellement_paralleles_et_bornees(monkeypatch):
    _, _, pic = _lancer(monkeypatch, 4, delai=0.05)
    assert 2 <= pic[0] <= 4
    _, _, pic = _lancer(monkeypatch, 1, delai=0.01)
    assert pic[0] == 1


def test_parallelisme_borne(monkeypatch):
    monkeypatch.setenv("PRECO_GENERIQUE_PARALLELISME", "50")
    assert spg._parallelisme() == spg.PARALLELISME_MAX
    monkeypatch.setenv("PRECO_GENERIQUE_PARALLELISME", "abc")
    assert spg._parallelisme() == spg.PARALLELISME_PAR_DEFAUT
    monkeypatch.setenv("PRECO_GENERIQUE_PARALLELISME", "0")
    assert spg._parallelisme() == 1
