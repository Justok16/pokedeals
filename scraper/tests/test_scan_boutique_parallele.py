"""scan_boutique.py (deals/retours en stock Shopify) : lecture reseau des
catalogues en parallele (06/10/2026), traitement et memoire toujours
sequentiels. Meme resultat que l'ancien comportement, cycle ~4x plus court."""

import threading
import time

import pytest

import parallelisme
import scan_boutique as sb

BOUTIQUES = [f"boutique{i}.fr" for i in range(10)]
EN_PANNE = {"boutique3.fr", "boutique7.fr"}


class _FauxConnecteur:
    delai = 0.0
    appels: list = []
    en_cours = [0]
    pic = [0]
    verrou = threading.Lock()

    def __init__(self, domaine):
        self.domaine = domaine
        self.base_url = f"https://{domaine}"

    def recuperer_tout_le_catalogue(self):
        cls = type(self)
        with cls.verrou:
            cls.en_cours[0] += 1
            cls.pic[0] = max(cls.pic[0], cls.en_cours[0])
            cls.appels.append(self.domaine)
        time.sleep(cls.delai)
        with cls.verrou:
            cls.en_cours[0] -= 1
        if self.domaine in EN_PANNE:
            raise RuntimeError(f"echec recuperation catalogue Shopify pour {self.domaine} (page 1)")
        return [{"title": f"produit de {self.domaine}"}]

    def rechercher_dans_catalogue(self, catalogue, criteres):
        return {"catalogue": catalogue, "domaine": self.domaine}


@pytest.fixture
def faux_monde(monkeypatch):
    _FauxConnecteur.appels, _FauxConnecteur.en_cours, _FauxConnecteur.pic = [], [0], [0]
    _FauxConnecteur.delai = 0.0
    monkeypatch.setattr(sb, "ConnecteurShopify", _FauxConnecteur)
    monkeypatch.setattr(sb, "DELAI_ENTRE_BOUTIQUES", 0)
    monkeypatch.setattr(sb, "detecter_bonnes_affaires",
                        lambda res, cartes, cotes, regles: [{"nom": "deal", "boutique": res["domaine"]}])

    def faux_stock(domaine, res, cartes, memoire):
        memoire.setdefault("ordre", []).append(domaine)        # trace de l'ordre des ecritures memoire
        return [{"nom": "retour", "boutique": domaine}]

    monkeypatch.setattr(sb, "detecter_retours_en_stock", faux_stock)
    return monkeypatch


def _lancer(monkeypatch, parallelisme_voulu):
    monkeypatch.setenv("SCAN_PARALLELISME", str(parallelisme_voulu))
    memoire = {}
    res = sb.scanner_plusieurs_boutiques(BOUTIQUES, [], memoire, {}, {})
    return res, memoire


def test_resultat_identique_en_parallele_et_en_sequentiel(faux_monde):
    seq, mem_seq = _lancer(faux_monde, 1)
    par, mem_par = _lancer(faux_monde, 4)
    assert par["deals"] == seq["deals"]
    assert par["evenements_stock"] == seq["evenements_stock"]
    assert par["boutiques_ok"] == seq["boutiques_ok"]
    assert par["boutiques_echec"] == seq["boutiques_echec"]
    assert mem_par == mem_seq


def test_memoire_ecrite_dans_lordre_dorigine_meme_si_les_boutiques_repondent_dans_le_desordre(faux_monde):
    delais = {d: (len(BOUTIQUES) - i) * 0.01 for i, d in enumerate(BOUTIQUES)}  # la 1re est la plus lente

    class Lent(_FauxConnecteur):
        def recuperer_tout_le_catalogue(self):
            time.sleep(delais[self.domaine])
            return []

    faux_monde.setattr(sb, "ConnecteurShopify", Lent)
    _, memoire = _lancer(faux_monde, 4)
    assert memoire["ordre"] == BOUTIQUES


def test_boutique_en_echec_page_1_nalimente_jamais_la_memoire_et_narrete_pas_les_autres(faux_monde):
    res, memoire = _lancer(faux_monde, 4)
    assert {e["domaine"] for e in res["boutiques_echec"]} == EN_PANNE
    assert all("RuntimeError" in e["raison"] for e in res["boutiques_echec"])
    assert res["boutiques_ok"] == [d for d in BOUTIQUES if d not in EN_PANNE]
    # Garde-fou de l'audit du 18/08/2026 : une boutique injoignable ne doit JAMAIS
    # enregistrer "en_stock: False" (fausse transition rupture->stock au retour du reseau).
    assert not (set(memoire["ordre"]) & EN_PANNE)


def test_chaque_boutique_nest_lue_quune_fois(faux_monde):
    _lancer(faux_monde, 4)
    assert sorted(_FauxConnecteur.appels) == sorted(BOUTIQUES)


def test_le_parallelisme_reduit_vraiment_la_duree(faux_monde):
    _FauxConnecteur.delai = 0.05
    t0 = time.monotonic(); _lancer(faux_monde, 1); seq = time.monotonic() - t0
    _FauxConnecteur.pic[0] = 0
    t0 = time.monotonic(); _lancer(faux_monde, 4); par = time.monotonic() - t0
    assert 1 < _FauxConnecteur.pic[0] <= 4
    assert par < seq * 0.6, (seq, par)


def test_scanner_boutique_complet_reste_utilisable_seul(faux_monde):
    memoire = {}
    deals, evenements = sb.scanner_boutique_complet("boutique0.fr", [], memoire, {}, {})
    assert deals == [{"nom": "deal", "boutique": "boutique0.fr"}]
    assert evenements == [{"nom": "retour", "boutique": "boutique0.fr"}]
    assert memoire["ordre"] == ["boutique0.fr"]


def test_traiter_catalogue_ne_fait_aucun_appel_reseau(faux_monde):
    connecteur = _FauxConnecteur("boutique1.fr")
    sb.traiter_catalogue("boutique1.fr", connecteur, [{"title": "x"}], [], {}, {}, {})
    assert _FauxConnecteur.appels == []                    # recuperer_tout_le_catalogue jamais appele


@pytest.mark.parametrize("valeur,attendu", [
    (None, 4), ("1", 1), ("3", 3), ("0", 1), ("-5", 1), ("999", 8), ("abc", 4), ("", 4),
])
def test_lire_parallelisme_borne_et_tolerant(monkeypatch, valeur, attendu):
    if valeur is None:
        monkeypatch.delenv("UNE_VARIABLE", raising=False)
    else:
        monkeypatch.setenv("UNE_VARIABLE", valeur)
    assert parallelisme.lire_parallelisme("UNE_VARIABLE") == attendu
