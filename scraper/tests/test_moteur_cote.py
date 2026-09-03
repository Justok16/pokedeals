"""Tests de non-regression pour moteur_cote.py (extrait de main.py le
17/08/2026, septieme module du decoupage progressif -- cf.
SESSION_NOTES.md). Un cas par comportement documente par un commentaire
VNN dans le code (V15, V16, V17, V18, V20, V22.8, V23, V26, V36, V39,
V40, V41, V44, V45), plus la persistance de l'historique/anciennete.

Aucun test ici n'ecrit dans data/cotes.json ni data/anciennete_annonces.json
(fichiers de production) : l'etat en cache (_historique/_anciennete) est
manipule directement en memoire via monkeypatch, jamais via les fonctions
de sauvegarde reelles."""

import time

import pytest

import moteur_cote as mc


CFG_REGLES = {
    "cote_min": 5.0,
    "prix_max": 0,
    "frais_port_max": 5.0,
    "frais_port_max_international": 10.0,
    "marge_achat": 0.10,
    "marge_revente": 0.10,
    "frais_revente_estimes": 0.13,
    "profit_min": 1.0,
    "prix_plancher_ratio": 0.15,
}
CFG = {"regles": CFG_REGLES, "etats_acceptes": [], "etats_refuses": ["gradée", "gradee"]}


@pytest.fixture(autouse=True)
def _isole_caches(monkeypatch):
    """Isole _historique/_anciennete du disque reel pour chaque test."""
    monkeypatch.setattr(mc, "_historique", {})
    monkeypatch.setattr(mc, "_anciennete", {})
    yield


# ------------------------- _localisation_incoherente -------------------------

def test_localisation_incoherente_carte_fr_depuis_letranger():
    assert mc._localisation_incoherente({"plateforme": "eBay (JP)"}, "fr") is True
    assert mc._localisation_incoherente({"plateforme": "eBay (DE)"}, "fr") is True


def test_localisation_coherente_carte_fr_depuis_la_france():
    assert mc._localisation_incoherente({"plateforme": "eBay (FR)"}, "fr") is False
    assert mc._localisation_incoherente({"plateforme": "Vinted"}, "fr") is False


def test_localisation_toujours_coherente_pour_carte_etrangere():
    # V18 : une carte JP/KR/CN venant de l'etranger est normale, jamais suspecte.
    assert mc._localisation_incoherente({"plateforme": "eBay (JP)"}, "jp") is False
    assert mc._localisation_incoherente({"plateforme": "eBay (KR)"}, "kr") is False


# ------------------------- calculer_cote -------------------------

def _annonces(prix_liste, titre="Dracaufeu ex 199/165", plateforme="eBay (FR)"):
    return [{"prix": p, "titre": titre, "plateforme": plateforme, "id": f"a{i}"}
            for i, p in enumerate(prix_liste)]


def test_calculer_cote_sous_le_minimum_renvoie_none():
    annonces = _annonces([10, 20, 30])
    cote, n = mc.calculer_cote(annonces, {"minimum_annonces": 8}, "Dracaufeu ex 199/165", "fr", "")
    assert cote is None
    assert n == 3


def test_calculer_cote_mediane_v17():
    prix = [90, 95, 100, 100, 105, 110, 95, 100]
    cote, n = mc.calculer_cote(_annonces(prix), {"minimum_annonces": 8, "coefficient_marche": 1.0},
                               "Dracaufeu ex 199/165", "fr", "")
    assert cote == 100.0
    assert n == 8


def test_calculer_cote_applique_le_coefficient_marche():
    prix = [100] * 8
    cote, _ = mc.calculer_cote(_annonces(prix), {"minimum_annonces": 8, "coefficient_marche": 0.9},
                               "Dracaufeu ex 199/165", "fr", "")
    assert cote == 90.0


def test_calculer_cote_ecarte_les_valeurs_aberrantes_iqr():
    # V17 : une seule annonce a 5000€ (erreur/fantaisie) ne doit pas gonfler
    # la mediane -- filtre IQR avant calcul.
    prix = [95, 98, 100, 102, 105, 97, 99, 5000]
    cote, n = mc.calculer_cote(_annonces(prix), {"minimum_annonces": 8, "coefficient_marche": 1.0},
                               "Dracaufeu ex 199/165", "fr", "")
    assert cote < 200  # la valeur aberrante ne doit pas peser dans le resultat
    assert n == 7  # 1 annonce ecartee par l'IQR


def test_calculer_cote_ignore_annonce_localisee_a_letranger_pour_carte_fr():
    # V18 : les annonces eBay (JP) gonflaient la cote d'une carte FR.
    prix_fr = [100] * 8
    annonces = _annonces(prix_fr, plateforme="eBay (FR)")
    annonces += _annonces([900, 950, 980], plateforme="eBay (JP)")
    cote, n = mc.calculer_cote(annonces, {"minimum_annonces": 8, "coefficient_marche": 1.0},
                               "Dracaufeu ex 199/165", "fr", "")
    assert cote == 100.0
    assert n == 8  # les 3 annonces JP ne comptent pas


def test_calculer_cote_ignore_annonce_non_pertinente():
    # V15 : filtre par numero exact -- une annonce sans le bon numero est ignoree.
    annonces = _annonces([100] * 8, titre="Dracaufeu ex 199/165")
    annonces += _annonces([1, 2, 3], titre="Dracaufeu ex 200/165")  # mauvais numero
    cote, n = mc.calculer_cote(annonces, {"minimum_annonces": 8, "coefficient_marche": 1.0},
                               "Dracaufeu ex 199/165", "fr", "")
    assert cote == 100.0
    assert n == 8


def test_calculer_cote_methode_bas_marche_v23():
    prix = [50, 55, 60, 65, 70, 200, 210, 220]  # panier bas-marche vs mediane tres differents
    cfg = {"minimum_annonces": 8, "coefficient_marche": 1.0, "nb_prix_bas": 5, "methode": "bas_marche"}
    cote_bas, _ = mc.calculer_cote(_annonces(prix), cfg, "Dracaufeu ex 199/165", "fr", "")
    cfg_mediane = dict(cfg, methode="mediane")
    cote_med, _ = mc.calculer_cote(_annonces(prix), cfg_mediane, "Dracaufeu ex 199/165", "fr", "")
    assert cote_bas < cote_med
    assert cote_bas == round((50 + 55 + 60 + 65 + 70) / 5, 2)


def test_calculer_cote_exclut_annonce_stagnante_du_panier_bas_marche(monkeypatch):
    # V44 : une annonce en ligne depuis plus de seuil_jours_stagnant jours
    # ne doit pas composer le panier bas-marche si des annonces fraiches
    # suffisent.
    ancien_ts = time.time() - 20 * 86400  # 20 jours = stagnante
    mc._anciennete.clear()
    mc._anciennete["a0"] = {"premiere_vue": ancien_ts}  # la moins chere, stagnante
    prix = [10, 60, 65, 70, 75, 80, 85, 90]  # a0=10 stagnante, le reste frais
    annonces = _annonces(prix)
    cfg = {"minimum_annonces": 8, "coefficient_marche": 1.0, "nb_prix_bas": 5,
           "seuil_jours_stagnant": 10, "methode": "bas_marche"}
    cote, _ = mc.calculer_cote(annonces, cfg, "Dracaufeu ex 199/165", "fr", "")
    # Le panier bas-marche doit exclure le prix stagnant (10) et prendre les
    # 5 suivants (60..80), pas (10,60,65,70,75).
    assert cote == round((60 + 65 + 70 + 75 + 80) / 5, 2)


# ------------------------- anciennete / jours_en_ligne -------------------------

def test_jours_en_ligne_premiere_vue_renvoie_zero():
    assert mc.jours_en_ligne("nouvel-id") == 0.0
    assert "nouvel-id" in mc.anciennete()


def test_jours_en_ligne_calcule_lecart_depuis_premiere_vue():
    mc._anciennete["ancien-id"] = {"premiere_vue": time.time() - 5 * 86400}
    jours = mc.jours_en_ligne("ancien-id")
    assert 4.9 < jours < 5.1


# ------------------------- historique / cle_cote / cote_lissee -------------------------

def test_cle_cote_combine_nom_et_langue():
    assert mc.cle_cote("Dracaufeu ex 199/165", "fr") == "Dracaufeu ex 199/165|fr"
    assert mc.cle_cote("Dracaufeu ex 199/165", None) == "Dracaufeu ex 199/165|fr"


def test_cle_cote_distingue_les_langues_v26():
    # V26 : meme nom, langues differentes -> cles differentes (pas de fuite JP<-KR).
    assert mc.cle_cote("Charizard ex 201/165", "jp") != mc.cle_cote("Charizard ex 201/165", "kr")


def test_cote_lissee_sans_historique_renvoie_none():
    assert mc.cote_lissee("Carte inconnue", "fr") is None


def test_cote_lissee_mediane_des_valeurs_recentes():
    mc._historique["Dracaufeu ex 199/165|fr"] = [
        {"cote": 100.0, "ts": time.time()},
        {"cote": 110.0, "ts": time.time()},
        {"cote": 120.0, "ts": time.time()},
    ]
    assert mc.cote_lissee("Dracaufeu ex 199/165", "fr") == 110.0


def test_cote_lissee_ignore_les_valeurs_perimees():
    trop_vieux = time.time() - (mc.VALIDITE_JOURS + 1) * 86400
    mc._historique["Dracaufeu ex 199/165|fr"] = [{"cote": 999.0, "ts": trop_vieux}]
    assert mc.cote_lissee("Dracaufeu ex 199/165", "fr") is None


def test_enregistrer_cote_ajoute_et_plafonne_lhistorique():
    for i in range(mc.HISTORIQUE_MAX + 3):
        mc.enregistrer_cote("Dracaufeu ex 199/165", 100.0 + i, "fr")
    entrees = mc._historique["Dracaufeu ex 199/165|fr"]
    assert len(entrees) == mc.HISTORIQUE_MAX
    # Les plus anciennes sont ecartees -- seules les dernieres restent.
    assert entrees[-1]["cote"] == 100.0 + mc.HISTORIQUE_MAX + 2


def test_enregistrer_cote_persiste_nb_annonces():
    # 03/09/2026 (audit) : nb_annonces est desormais persiste a cote de
    # cote/ts -- purement additif, ne doit rien casser des lecteurs
    # existants (cf. tests ci-dessus, toujours verts sans ce parametre).
    mc.enregistrer_cote("Dracaufeu ex 199/165", 150.0, "fr", 12)
    entrees = mc._historique["Dracaufeu ex 199/165|fr"]
    assert entrees[-1]["nb_annonces"] == 12
    assert entrees[-1]["cote"] == 150.0


def test_enregistrer_cote_nb_annonces_optionnel():
    # Un appelant qui ne connait pas de vrai decompte (ex. re-enregistrement
    # d'une cote corrigee par Cardtrader/TCGdex dans main.py) doit pouvoir
    # omettre nb_annonces -- stocke alors a None, jamais une valeur inventee.
    mc.enregistrer_cote("Dracaufeu ex 199/165", 150.0, "fr")
    entrees = mc._historique["Dracaufeu ex 199/165|fr"]
    assert entrees[-1]["nb_annonces"] is None


def test_derniere_nb_annonces_prend_lentree_la_plus_recente():
    mc._historique["Dracaufeu ex 199/165|fr"] = [
        {"cote": 100.0, "ts": 1000, "nb_annonces": 5},
        {"cote": 120.0, "ts": 2000, "nb_annonces": 9},
    ]
    assert mc.derniere_nb_annonces("Dracaufeu ex 199/165", "fr") == 9


def test_derniere_nb_annonces_sans_historique_renvoie_none():
    assert mc.derniere_nb_annonces("Carte inconnue", "fr") is None


def test_derniere_nb_annonces_entree_sans_le_champ_renvoie_none():
    # Compatibilite avec une entree ecrite avant ce changement (pas de cle
    # "nb_annonces" du tout) -- ne doit jamais lever de KeyError.
    mc._historique["Dracaufeu ex 199/165|fr"] = [{"cote": 100.0, "ts": 1000}]
    assert mc.derniere_nb_annonces("Dracaufeu ex 199/165", "fr") is None


def test_obtenir_cote_enregistre_le_nb_dannonces_reel(monkeypatch):
    # obtenir_cote() doit transmettre le vrai nb_pertinentes de
    # calculer_cote() a enregistrer_cote(), pas le laisser a None.
    monkeypatch.setattr(mc, "calculer_cote", lambda *a, **k: (42.0, 7))
    carte = {"nom": "Dracaufeu ex 199/165", "langue": "fr"}
    mc.obtenir_cote(carte, [], {"cote": {}})
    entrees = mc._historique["Dracaufeu ex 199/165|fr"]
    assert entrees[-1]["nb_annonces"] == 7


def test_charger_historique_purge_si_mauvaise_version(tmp_path, monkeypatch):
    fichier = tmp_path / "cotes.json"
    fichier.write_text('{"_purge_version": 1, "Dracaufeu ex 199/165|fr": [{"cote": 50.0, "ts": 1}]}',
                        encoding="utf-8")
    monkeypatch.setattr(mc, "FICHIER_COTES", str(fichier))
    h = mc._charger_historique()
    assert h == {}  # version 1 != PURGE_VERSION actuelle -> tout est jete


def test_charger_historique_garde_les_donnees_a_jour(tmp_path, monkeypatch):
    fichier = tmp_path / "cotes.json"
    fichier.write_text(
        '{"_purge_version": %d, "Dracaufeu ex 199/165|fr": [{"cote": 50.0, "ts": 1}]}' % mc.PURGE_VERSION,
        encoding="utf-8")
    monkeypatch.setattr(mc, "FICHIER_COTES", str(fichier))
    h = mc._charger_historique()
    assert h == {"Dracaufeu ex 199/165|fr": [{"cote": 50.0, "ts": 1}]}
    assert "_purge_version" not in h


def test_charger_historique_fichier_absent_renvoie_dict_vide(tmp_path, monkeypatch):
    monkeypatch.setattr(mc, "FICHIER_COTES", str(tmp_path / "inexistant.json"))
    assert mc._charger_historique() == {}


def test_sauvegarder_historique_ecrit_le_tag_de_version(tmp_path, monkeypatch):
    fichier = tmp_path / "cotes.json"
    monkeypatch.setattr(mc, "FICHIER_COTES", str(fichier))
    mc._historique["Dracaufeu ex 199/165|fr"] = [{"cote": 50.0, "ts": 1}]
    mc.sauvegarder_historique()
    import json
    donnees = json.loads(fichier.read_text(encoding="utf-8"))
    assert donnees["_purge_version"] == mc.PURGE_VERSION
    assert donnees["Dracaufeu ex 199/165|fr"] == [{"cote": 50.0, "ts": 1}]


# ---------------- initialiser_historique/anciennete (migration Supabase, 25/08/2026) ----------------
# Chemin Supabase de main.py : amorce le cache module depuis un dict deja
# charge en amont (pas un fichier local) -- meme comportement de purge par
# version que le chemin fichier existant.

def test_initialiser_historique_garde_les_donnees_a_bonne_version():
    mc.initialiser_historique({"_purge_version": mc.PURGE_VERSION, "Carte|fr": [{"cote": 10.0, "ts": 1}]})
    assert mc.historique() == {"Carte|fr": [{"cote": 10.0, "ts": 1}]}


def test_initialiser_historique_purge_si_mauvaise_version():
    mc.initialiser_historique({"_purge_version": mc.PURGE_VERSION - 1, "Carte|fr": [{"cote": 10.0, "ts": 1}]})
    assert mc.historique() == {}


def test_donnees_historique_a_sauvegarder_inclut_le_tag_de_version():
    mc.initialiser_historique({"_purge_version": mc.PURGE_VERSION, "Carte|fr": [{"cote": 10.0, "ts": 1}]})
    donnees = mc.donnees_historique_a_sauvegarder()
    assert donnees["_purge_version"] == mc.PURGE_VERSION
    assert donnees["Carte|fr"] == [{"cote": 10.0, "ts": 1}]


def test_initialiser_anciennete_amorce_le_cache():
    mc.initialiser_anciennete({"ebay-123": {"premiere_vue": 1000.0}})
    assert mc.anciennete() == {"ebay-123": {"premiere_vue": 1000.0}}


def test_donnees_anciennete_a_sauvegarder_applique_la_retention():
    maintenant = time.time()
    ancien = maintenant - (mc.ANCIENNETE_RETENTION_JOURS + 1) * 86400
    mc.initialiser_anciennete({"recente": {"premiere_vue": maintenant}, "trop_vieille": {"premiere_vue": ancien}})
    donnees = mc.donnees_anciennete_a_sauvegarder()
    assert "recente" in donnees
    assert "trop_vieille" not in donnees


# ------------------------- obtenir_cote -------------------------

def test_obtenir_cote_priorite_a_la_cote_manuelle():
    carte = {"nom": "Carte manuelle", "cote": 42.0, "langue": "fr"}
    cote, confiance = mc.obtenir_cote(carte, [], {"cote": {"minimum_annonces": 8}})
    assert cote == 42.0
    assert confiance == 99


def test_obtenir_cote_cote_manuelle_invalide_ignoree(caplog):
    carte = {"nom": "Carte", "cote": "pas un nombre", "langue": "fr"}
    cote, confiance = mc.obtenir_cote(carte, [], {"cote": {"minimum_annonces": 8}})
    assert cote is None
    assert confiance == 0


def test_obtenir_cote_utilise_la_cote_instantanee_et_lenregistre():
    carte = {"nom": "Dracaufeu ex 199/165", "langue": "fr"}
    annonces = _annonces([100] * 8)
    cote, confiance = mc.obtenir_cote(carte, annonces, {"cote": {"minimum_annonces": 8, "coefficient_marche": 1.0}})
    assert cote == 100.0
    assert confiance == 8
    assert "Dracaufeu ex 199/165|fr" in mc._historique


def test_obtenir_cote_repli_sur_cote_memorisee_sans_annonce_du_jour():
    mc._historique["Dracaufeu ex 199/165|fr"] = [{"cote": 200.0, "ts": time.time()}]
    carte = {"nom": "Dracaufeu ex 199/165", "langue": "fr"}
    cote, confiance = mc.obtenir_cote(carte, [], {"cote": {"minimum_annonces": 8}})
    assert cote == 200.0
    assert confiance == 0  # 0 annonce pertinente ce scan


def test_obtenir_cote_introuvable_renvoie_none():
    carte = {"nom": "Carte totalement inconnue", "langue": "fr"}
    cote, confiance = mc.obtenir_cote(carte, [], {"cote": {"minimum_annonces": 8}})
    assert cote is None
    assert confiance == 0


# ------------------------- _etat_ok -------------------------

def test_etat_ok_rejette_les_mots_refuses():
    assert mc._etat_ok("Carte gradée PSA 9", [], ["gradée"]) is False


def test_etat_ok_accepte_sans_label_dfetat():
    assert mc._etat_ok("", [], ["gradée"]) is True


def test_etat_ok_neutralise_les_negations_v36():
    # Cas reel : "Non gradée" contient "gradée" mais signifie l'inverse.
    assert mc._etat_ok("Non gradée, très bon état", [], ["gradée"]) is True
    assert mc._etat_ok("Carte pas gradee, TBE", [], ["gradee"]) is True
    assert mc._etat_ok("ungraded card, NM", [], ["graded"]) is True


def test_etat_ok_etats_acceptes_est_decoratif_v39():
    # V39 : etats_acceptes ne filtre jamais -- seule etats_refuses agit.
    assert mc._etat_ok("nimporte quoi", ["neuf"], []) is True


# ------------------------- evaluate -------------------------

def _annonce(**overrides):
    base = {
        "titre": "Dracaufeu ex 199/165",
        "carte": "Dracaufeu ex 199/165",
        "langue": "fr",
        "alias": "",
        "plateforme": "eBay (FR)",
        "prix": 80.0,
        "port": 3.0,
        "etat_texte": "",
    }
    base.update(overrides)
    return base


def test_evaluate_deal_simple():
    deal, status = mc.evaluate(_annonce(), 100.0, CFG, confiance=8)
    assert status == "DEAL"
    assert deal["total"] == 83.0
    assert deal["decote_pct"] == 17.0


def test_evaluate_cote_indisponible():
    deal, status = mc.evaluate(_annonce(), None, CFG, confiance=0)
    assert deal is None
    assert status == "cote indisponible"


def test_evaluate_cote_trop_faible():
    deal, status = mc.evaluate(_annonce(), 3.0, CFG, confiance=8)
    assert deal is None
    assert "cote trop faible" in status


def test_evaluate_rejette_annonce_non_pertinente():
    deal, status = mc.evaluate(_annonce(titre="Autre carte 200/165"), 100.0, CFG, confiance=8)
    assert deal is None


def test_evaluate_rejette_localisation_incoherente_v18():
    # annonce_pertinente() (filtre_annonces.py) rejette deja ce cas avant
    # meme d'atteindre le controle _localisation_incoherente() propre a
    # evaluate() -- les deux garde-fous se recouvrent, ce qui est voulu.
    deal, status = mc.evaluate(_annonce(plateforme="eBay (JP)"), 100.0, CFG, confiance=8)
    assert deal is None
    assert "étrang" in status


def test_evaluate_rejette_port_trop_cher_v40_v41():
    # Port plafonne a 7% de la cote (V41) ou au minimum frais_port_max.
    deal, status = mc.evaluate(_annonce(prix=80.0, port=20.0), 100.0, CFG, confiance=8)
    assert deal is None
    assert "port trop cher" in status


def test_evaluate_rejette_etat_refuse():
    deal, status = mc.evaluate(_annonce(etat_texte="Carte gradée PSA 10"), 100.0, CFG, confiance=8)
    assert deal is None
    assert "état refusé" in status


def test_evaluate_rejette_pas_assez_sous_la_cote():
    deal, status = mc.evaluate(_annonce(prix=95.0, port=3.0), 100.0, CFG, confiance=8)
    assert deal is None
    assert "pas assez sous la cote" in status


def test_evaluate_rejette_prix_dappel_suspect_v22_8():
    deal, status = mc.evaluate(_annonce(prix=1.0, port=0.0), 100.0, CFG, confiance=8)
    assert deal is None
    assert "suspect" in status


def test_evaluate_rejette_annonce_denchere_deguisee():
    deal, status = mc.evaluate(_annonce(titre="Dracaufeu ex 199/165 comme neuf faire offre"),
                               100.0, CFG, confiance=8)
    assert deal is None
    assert "enchère" in status


def test_evaluate_rejette_profit_trop_faible():
    cfg = {**CFG, "regles": {**CFG_REGLES, "marge_achat": 0.001, "profit_min": 50.0}}
    deal, status = mc.evaluate(_annonce(prix=99.5, port=0.0), 100.0, cfg, confiance=8)
    assert deal is None
    assert "profit trop faible" in status


def test_evaluate_seuil_fixe_prioritaire_v45():
    annonce = _annonce(prix=12.0, port=1.0)
    annonce["prix_max_fixe"] = 15.0
    deal, status = mc.evaluate(annonce, None, CFG, confiance=0)  # cote inconnue, sans importance
    assert status == "DEAL (seuil fixe)"
    assert deal["cote"] == 15.0
    assert deal["confiance"] == 100


def test_evaluate_seuil_fixe_rejette_au_dessus_du_seuil():
    annonce = _annonce(prix=20.0, port=1.0)
    annonce["prix_max_fixe"] = 15.0
    deal, status = mc.evaluate(annonce, None, CFG, confiance=0)
    assert deal is None
    assert "au-dessus du seuil fixe" in status


def test_evaluate_seuil_fixe_respecte_letat_et_la_localisation():
    annonce = _annonce(prix=10.0, port=1.0, plateforme="eBay (JP)")
    annonce["prix_max_fixe"] = 15.0
    deal, status = mc.evaluate(annonce, None, CFG, confiance=0)
    assert deal is None
    assert "étrang" in status


# ------------------------- calculer_tendance_cote -------------------------

def test_calculer_tendance_cote_pas_assez_de_donnees():
    assert mc.calculer_tendance_cote("Carte inconnue", "fr") == "="


def test_calculer_tendance_cote_hausse():
    mc._historique["Dracaufeu ex 199/165|fr"] = [{"cote": 100.0, "ts": 1}, {"cote": 120.0, "ts": 2}]
    assert mc.calculer_tendance_cote("Dracaufeu ex 199/165", "fr") == "↗️"


def test_calculer_tendance_cote_baisse():
    mc._historique["Dracaufeu ex 199/165|fr"] = [{"cote": 100.0, "ts": 1}, {"cote": 80.0, "ts": 2}]
    assert mc.calculer_tendance_cote("Dracaufeu ex 199/165", "fr") == "↘️"


def test_calculer_tendance_cote_stable():
    mc._historique["Dracaufeu ex 199/165|fr"] = [{"cote": 100.0, "ts": 1}, {"cote": 101.0, "ts": 2}]
    assert mc.calculer_tendance_cote("Dracaufeu ex 199/165", "fr") == "="
