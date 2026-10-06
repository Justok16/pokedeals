"""Lecture des catalogues du radar en parallele (06/10/2026) : meme resultat que
l'ancien comportement sequentiel, mais beaucoup plus rapide."""

import threading
import time

import pytest

import scan_precommandes as sp


class _ProduitFactice:
    nom = "produit"
    alerte_disponibilite = False


def _installer_faux_scanner(monkeypatch, delai=0.0, echecs=()):
    appels, en_cours, pic = [], [0], [0]
    verrou = threading.Lock()

    def faux_scanner(plateforme, domaine, mode, produits):
        with verrou:
            en_cours[0] += 1
            pic[0] = max(pic[0], en_cours[0])
            appels.append(domaine)
        time.sleep(delai)
        with verrou:
            en_cours[0] -= 1
        if domaine in echecs:
            raise RuntimeError(f"boutique {domaine} en panne")
        return [{"domaine": domaine, "produit": "x"}]

    def faux_detecter(domaine, candidats, memoire):
        memoire.setdefault("ordre", []).append(domaine)   # trace l'ordre de traitement
        return [{"domaine": domaine, "evt": 1}]

    monkeypatch.setattr(sp, "scanner_une_boutique", faux_scanner)
    monkeypatch.setattr(sp, "detecter_nouvelles_precommandes", faux_detecter)
    monkeypatch.setattr(sp, "marquer_boutique_balayee", lambda *a, **k: None)
    monkeypatch.setattr(sp, "DELAI_ENTRE_BOUTIQUES", 0)
    return appels, pic


BOUTIQUES = [f"boutique{i}.fr" for i in range(10)]


def _lancer(monkeypatch, parallelisme, **kw):
    monkeypatch.setenv("RADAR_PARALLELISME", str(parallelisme))
    appels, pic = _installer_faux_scanner(monkeypatch, **kw)
    memoire = {}
    res = sp.scanner_plusieurs_boutiques("shopify", BOUTIQUES, {}, [_ProduitFactice()], memoire)
    return res, memoire, appels, pic


def test_resultat_identique_en_parallele_et_en_sequentiel(monkeypatch):
    seq, mem_seq, _, _ = _lancer(monkeypatch, 1)
    par, mem_par, _, _ = _lancer(monkeypatch, 4)
    assert par["evenements"] == seq["evenements"]
    assert par["boutiques_ok"] == seq["boutiques_ok"] == BOUTIQUES
    assert par["boutiques_echec"] == seq["boutiques_echec"] == []
    assert mem_par == mem_seq


def test_traitement_et_memoire_dans_lordre_dorigine_meme_si_les_boutiques_repondent_dans_le_desordre(monkeypatch):
    monkeypatch.setenv("RADAR_PARALLELISME", "4")
    delais = {d: (len(BOUTIQUES) - i) * 0.01 for i, d in enumerate(BOUTIQUES)}  # la 1re est la plus lente

    def faux_scanner(plateforme, domaine, mode, produits):
        time.sleep(delais[domaine])
        return []

    monkeypatch.setattr(sp, "scanner_une_boutique", faux_scanner)
    monkeypatch.setattr(sp, "detecter_nouvelles_precommandes",
                        lambda d, c, m: m.setdefault("ordre", []).append(d) or [])
    monkeypatch.setattr(sp, "marquer_boutique_balayee", lambda *a, **k: None)
    memoire = {}
    sp.scanner_plusieurs_boutiques("shopify", BOUTIQUES, {}, [_ProduitFactice()], memoire)
    assert memoire["ordre"] == BOUTIQUES


def test_une_boutique_en_echec_narrete_pas_les_autres(monkeypatch):
    res, memoire, appels, _ = _lancer(monkeypatch, 4, echecs={"boutique3.fr", "boutique7.fr"})
    assert [e["domaine"] for e in res["boutiques_echec"]] == ["boutique3.fr", "boutique7.fr"]
    assert "RuntimeError" in res["boutiques_echec"][0]["raison"]
    assert res["boutiques_ok"] == [d for d in BOUTIQUES if d not in ("boutique3.fr", "boutique7.fr")]
    assert sorted(appels) == sorted(BOUTIQUES)            # toutes interrogees, une seule fois
    assert "boutique3.fr" not in memoire["ordre"]          # un echec ne touche pas la memoire


def test_chaque_boutique_nest_interrogee_quune_fois(monkeypatch):
    _, _, appels, _ = _lancer(monkeypatch, 4)
    assert sorted(appels) == sorted(BOUTIQUES)


def test_le_parallelisme_reduit_vraiment_la_duree(monkeypatch):
    t0 = time.monotonic(); _lancer(monkeypatch, 1, delai=0.05); seq = time.monotonic() - t0
    t0 = time.monotonic(); _, _, _, pic = _lancer(monkeypatch, 4, delai=0.05); par = time.monotonic() - t0
    assert pic[0] > 1                       # des lectures se chevauchent bel et bien
    assert pic[0] <= 4                      # jamais plus que le plafond demande
    assert par < seq * 0.6, (seq, par)


@pytest.mark.parametrize("valeur,attendu", [
    (None, sp.PARALLELISME_PAR_DEFAUT), ("1", 1), ("3", 3), ("0", 1), ("-5", 1),
    ("999", sp.PARALLELISME_MAX), ("abc", sp.PARALLELISME_PAR_DEFAUT), ("", sp.PARALLELISME_PAR_DEFAUT),
])
def test_parallelisme_borne_et_tolerant(monkeypatch, valeur, attendu):
    if valeur is None:
        monkeypatch.delenv("RADAR_PARALLELISME", raising=False)
    else:
        monkeypatch.setenv("RADAR_PARALLELISME", valeur)
    assert sp._parallelisme() == attendu
