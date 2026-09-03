"""Tests de non-regression pour l'alerte de fiabilite Vinted/Leboncoin
(main.py, V50, 17/08/2026) -- detecte un connecteur CASSE (echecs quasi
systematiques sur un cycle), a distinguer d'un echec isole normal."""

import main


def _stats_vierges():
    return {"vinted_appels": 0, "vinted_echecs": 0, "leboncoin_appels": 0, "leboncoin_echecs": 0}


def setup_function():
    # Chaque test repart d'un compteur propre -- _stats_fiabilite est un
    # dict module-level partage, meme risque que tout etat global en test.
    main._reinitialiser_stats_fiabilite()
    # 03/09/2026 (audit) : idem pour les coupe-circuits Vinted/Leboncoin --
    # sinon un test d'un AUTRE fichier (ex. test_circuit_vinted_leboncoin.py)
    # qui laisse le coupe-circuit declenche pourrait fausser
    # test_vinted_rechercher_compte_les_echecs_reels/
    # test_lbc_rechercher_403_nest_pas_compte_comme_un_echec ci-dessous (qui
    # appellent la VRAIE fonction, court-circuitee si le coupe-circuit est
    # deja ouvert).
    main._reinitialiser_circuits_vinted_leboncoin()


def test_aucune_alerte_sous_le_seuil_minimum_dappels():
    # 4 appels, tous en echec -- mais sous SEUIL_MIN_APPELS_FIABILITE (5) :
    # pas assez d'echantillon pour conclure, meme a 100% d'echec.
    main._stats_fiabilite.update({"vinted_appels": 4, "vinted_echecs": 4})
    alertes = main.verifier_fiabilite_plateformes({})
    assert alertes == []


def test_aucune_alerte_si_taux_dechec_normal():
    # 20 appels, 3 echecs (15%) -- taux normal, pas d'alerte.
    main._stats_fiabilite.update({"vinted_appels": 20, "vinted_echecs": 3})
    alertes = main.verifier_fiabilite_plateformes({})
    assert alertes == []


def test_alerte_vinted_si_echecs_quasi_systematiques():
    main._stats_fiabilite.update({"vinted_appels": 10, "vinted_echecs": 9})  # 90%
    alertes = main.verifier_fiabilite_plateformes({})
    assert len(alertes) == 1
    assert "Vinted" in alertes[0]
    assert "9/10" in alertes[0]


def test_alerte_leboncoin_si_echecs_quasi_systematiques():
    main._stats_fiabilite.update({"leboncoin_appels": 8, "leboncoin_echecs": 8})  # 100%
    alertes = main.verifier_fiabilite_plateformes({})
    assert len(alertes) == 1
    assert "Leboncoin" in alertes[0]


def test_alerte_double_si_les_deux_plateformes_sont_cassees():
    main._stats_fiabilite.update({
        "vinted_appels": 10, "vinted_echecs": 10,
        "leboncoin_appels": 10, "leboncoin_echecs": 10,
    })
    alertes = main.verifier_fiabilite_plateformes({})
    assert len(alertes) == 2


def test_anti_spam_empeche_la_repetition_immediate():
    main._stats_fiabilite.update({"vinted_appels": 10, "vinted_echecs": 10})
    vues = {}
    premiere = main.verifier_fiabilite_plateformes(vues)
    assert len(premiere) == 1
    # Meme etat degrade, meme cycle logique juste apres -- l'anti-spam
    # (6h) doit bloquer une deuxieme alerte identique.
    seconde = main.verifier_fiabilite_plateformes(vues)
    assert seconde == []


def test_reinitialiser_stats_fiabilite_remet_a_zero():
    main._stats_fiabilite.update({"vinted_appels": 50, "vinted_echecs": 50})
    main._reinitialiser_stats_fiabilite()
    assert main._stats_fiabilite == _stats_vierges()


def test_vinted_rechercher_compte_les_echecs_reels(monkeypatch):
    def _session_indisponible():
        return None
    monkeypatch.setattr(main, "_get_vinted_session", _session_indisponible)
    resultat = main.vinted_rechercher("Dracaufeu ex 199/165", "fr")
    assert resultat == []
    assert main._stats_fiabilite["vinted_appels"] == 1
    assert main._stats_fiabilite["vinted_echecs"] == 1


def test_lbc_rechercher_403_nest_pas_compte_comme_un_echec(monkeypatch):
    # Un blocage 403/429 Leboncoin est un comportement anti-bot ROUTINE,
    # deja documente et tolere -- ne doit JAMAIS compter comme un "echec"
    # au sens de cette alerte (sinon elle se declencherait en continu,
    # Leboncoin bloquant frequemment par design).
    # lbc_rechercher vit desormais dans connecteur_leboncoin.py (extrait le
    # 17/08/2026) : main.lbc_rechercher n'est qu'une reference reimportee,
    # donc le monkeypatch doit cibler le module ou l'appel reseau a lieu
    # reellement -- patcher main.requete_avec_retry n'aurait ici aucun effet.
    import connecteur_leboncoin

    class _ReponseBloquee:
        status_code = 403
        text = "forbidden"

    def _requete_bloquee(*args, **kwargs):
        return _ReponseBloquee()

    monkeypatch.setattr(connecteur_leboncoin, "requete_avec_retry", _requete_bloquee)
    resultat = main.lbc_rechercher("Dracaufeu ex 199/165", "fr")
    assert resultat == []
    assert main._stats_fiabilite["leboncoin_appels"] == 1
    assert main._stats_fiabilite["leboncoin_echecs"] == 0
