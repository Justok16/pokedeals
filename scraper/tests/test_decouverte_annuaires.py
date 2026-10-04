"""Tests de decouverte_annuaires.py : calculer_changements() est pure (reseau
injecte), on verifie ajouts / conflits / retraits / ignores."""

import decouverte_annuaires as D

LISTES_VIDES = {cle: [] for cle in D.CLES_LISTES}
OK = lambda d: {"https_ok": True, "mentions_legales": True, "siret": "1", "raison": ""}  # noqa: E731
KO = lambda d: {"https_ok": False, "mentions_legales": False, "siret": None, "raison": "certificat HTTPS invalide"}  # noqa: E731


def _calc(annuaire, noire=frozenset(), listes=None, ailleurs=frozenset(), classer=lambda d: "shopify", legit=OK):
    return D.calculer_changements(set(annuaire), set(noire), listes or {k: [] for k in D.CLES_LISTES},
                                  set(ailleurs), classer=classer, legitimite=legit, pause=0)


def test_extraire_boutiques_annuaire():
    html = "Visiter amazon.fr ... Visiter pokesumo.com ... Visiter e.leclerc"
    assert D.extraire_boutiques_annuaire(html) == {"amazon.fr", "pokesumo.com", "e.leclerc"}


def test_ajout_dune_nouvelle_boutique_verifiee():
    listes, ajouts, retraits, conflits, ignores = _calc({"nouvelle.fr"})
    assert listes["shopify"] == ["nouvelle.fr"] and ajouts == [("nouvelle.fr", "shopify")]
    assert not retraits and not conflits and not ignores


def test_plateforme_inconnue_range_a_connecteur_dedie():
    listes, ajouts, *_ = _calc({"enseigne.fr"}, classer=lambda d: None)
    assert listes["a_connecteur_dedie"] == ["enseigne.fr"]


def test_boutique_de_lannuaire_sur_liste_noire_nest_jamais_ajoutee():
    listes, ajouts, retraits, conflits, _ = _calc({"douteuse.fr"}, noire={"douteuse.fr"})
    assert not ajouts and conflits == ["douteuse.fr"] and not any(listes.values())


def test_https_invalide_ignoree_ce_cycle():
    listes, ajouts, _, _, ignores = _calc({"cassee.fr"}, legit=KO)
    assert not ajouts and ignores == [("cassee.fr", "certificat HTTPS invalide")]


def test_boutique_deja_scannee_ailleurs_nest_pas_dupliquee():
    _, ajouts, *_ = _calc({"connue.fr"}, ailleurs={"connue.fr"})
    assert not ajouts


def test_retrait_si_devenue_arnaque_ou_sortie_de_lannuaire():
    listes = {k: [] for k in D.CLES_LISTES}
    listes["shopify"] = ["devenue-arnaque.fr", "sortie.fr", "ok.fr"]
    nouvelles, ajouts, retraits, _, _ = _calc({"devenue-arnaque.fr", "ok.fr"}, noire={"devenue-arnaque.fr"}, listes=listes)
    assert nouvelles["shopify"] == ["ok.fr"]
    assert dict(retraits) == {"devenue-arnaque.fr": "signalee comme arnaque",
                              "sortie.fr": "sortie de l'annuaire des boutiques verifiees"}


def test_domaine_refuse_manuellement_nest_jamais_ajoute(monkeypatch):
    monkeypatch.setattr(D, "DOMAINES_REFUSES", {"refuse.fr"})
    _, ajouts, *_ = _calc({"refuse.fr"})
    assert not ajouts


def test_ecriture_puis_relecture_du_fichier(tmp_path, monkeypatch):
    monkeypatch.setattr(D, "FICHIER_COMPLEMENT", tmp_path / "boutiques_complement.py")
    listes = {k: [] for k in D.CLES_LISTES}
    listes["shopify"] = ["b.fr", "a.fr"]
    D.ecrire_listes_complement(listes)
    assert D.charger_listes_complement()["shopify"] == ["a.fr", "b.fr"]
    assert not (tmp_path / "boutiques_complement.py.tmp").exists()
