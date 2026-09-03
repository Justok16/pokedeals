"""Tests de non-regression pour watchdog_workflows.py -- watchdog de sante
des workflows de scan programmes (audit externe du 30/08/2026 ; liste
WORKFLOWS_SURVEILLES a 10 entrees depuis le 03/09/2026, ajout de
verifier_alertes_watchlist.yml). Les tests ci-dessous derivent le nombre
attendu de WORKFLOWS_SURVEILLES plutot que de le figer en dur, pour ne
pas se casser a chaque futur ajout dans cette liste."""

from unittest.mock import Mock, patch

import requests

from watchdog_workflows import (
    WORKFLOWS_SURVEILLES,
    dernieres_conclusions,
    echecs_consecutifs,
    envoyer_telegram,
    main,
    verifier_sante,
)

NB_WORKFLOWS_SURVEILLES = len(WORKFLOWS_SURVEILLES)


# ------------------- echecs_consecutifs -------------------

def test_echecs_consecutifs_liste_vide():
    assert echecs_consecutifs([]) == 0


def test_echecs_consecutifs_dernier_succes():
    assert echecs_consecutifs(["success", "failure", "failure"]) == 0


def test_echecs_consecutifs_deux_echecs_puis_succes():
    assert echecs_consecutifs(["failure", "failure", "success", "failure"]) == 2


def test_echecs_consecutifs_que_des_echecs():
    assert echecs_consecutifs(["failure", "failure", "failure"]) == 3


def test_echecs_consecutifs_annulation_neutre_ne_casse_ni_ne_compte():
    # Une annulation manuelle isolée ne doit ni compter comme un échec ni
    # réinitialiser le compteur -- sinon elle masquerait une vraie série
    # d'échecs consécutifs.
    assert echecs_consecutifs(["failure", "cancelled", "failure"]) == 2


def test_echecs_consecutifs_none_neutre():
    assert echecs_consecutifs(["failure", None, "failure"]) == 2


# ------------------- dernieres_conclusions -------------------

def test_dernieres_conclusions_erreur_reseau_retourne_liste_vide():
    with patch("watchdog_workflows.requests.get", side_effect=requests.RequestException("boom")):
        result = dernieres_conclusions("Justok16", "pokedeals", "tok", "pokedeals.yml")
    assert result == []


def test_dernieres_conclusions_succes_extrait_les_conclusions_dans_l_ordre():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    reponse.json.return_value = {
        "workflow_runs": [{"conclusion": "failure"}, {"conclusion": "success"}],
    }
    with patch("watchdog_workflows.requests.get", return_value=reponse) as get_mock:
        result = dernieres_conclusions("Justok16", "pokedeals", "tok", "pokedeals.yml")
    assert result == ["failure", "success"]
    _, kwargs = get_mock.call_args
    assert kwargs["params"]["status"] == "completed"
    assert kwargs["headers"]["Authorization"] == "Bearer tok"


# ------------------- envoyer_telegram -------------------

def test_envoyer_telegram_sans_secrets_ne_declenche_aucun_appel():
    with patch("watchdog_workflows.requests.post") as post_mock:
        result = envoyer_telegram("texte", "", "")
    assert result is False
    post_mock.assert_not_called()


def test_envoyer_telegram_erreur_reseau_retourne_false():
    with patch("watchdog_workflows.requests.post", side_effect=requests.RequestException("boom")):
        result = envoyer_telegram("texte", "chat123", "tok")
    assert result is False


def test_envoyer_telegram_succes_retourne_true():
    reponse = Mock()
    reponse.status_code = 200
    with patch("watchdog_workflows.requests.post", return_value=reponse):
        result = envoyer_telegram("texte", "chat123", "tok")
    assert result is True


# ------------------- verifier_sante -------------------

def test_verifier_sante_interroge_tous_les_workflows_surveilles():
    with patch("watchdog_workflows.dernieres_conclusions", return_value=["failure", "failure", "failure"]) as dc_mock:
        result = verifier_sante("Justok16", "pokedeals", "tok")
    assert len(result) == NB_WORKFLOWS_SURVEILLES
    assert all(v == 3 for v in result.values())
    assert dc_mock.call_count == NB_WORKFLOWS_SURVEILLES


# ------------------- main (orchestration + anti-spam) -------------------

_ENV_BASE = {
    "GITHUB_REPOSITORY_OWNER": "Justok16",
    "GITHUB_REPOSITORY": "Justok16/pokedeals",
    "GITHUB_TOKEN": "tok",
    "TELEGRAM_BOT_TOKEN": "tg-tok",
    "SUPABASE_URL": "https://x.supabase.co",
    "SUPABASE_SERVICE_ROLE_KEY": "cle",
}


def _sante_uniforme(valeur: int) -> dict[str, int]:
    from watchdog_workflows import WORKFLOWS_SURVEILLES
    return {f: valeur for f in WORKFLOWS_SURVEILLES}


def test_main_sans_github_repository_abandonne_sans_appel():
    with patch.dict("os.environ", {}, clear=True), \
         patch("watchdog_workflows.verifier_sante") as sante_mock:
        main()
    sante_mock.assert_not_called()


def test_main_seuil_atteint_alerte_et_persiste_l_etat():
    with patch.dict("os.environ", _ENV_BASE, clear=True), \
         patch("watchdog_workflows.charger_memoire_supabase", return_value={}), \
         patch("watchdog_workflows.verifier_sante", return_value=_sante_uniforme(3)), \
         patch("watchdog_workflows.envoyer_telegram", return_value=True) as tg_mock, \
         patch("watchdog_workflows.sauvegarder_memoire_supabase", return_value=True) as save_mock:
        main()
    assert tg_mock.call_count == NB_WORKFLOWS_SURVEILLES  # une alerte par workflow en échec
    save_mock.assert_called_once()
    etat_sauve = save_mock.call_args[0][0]
    assert all(v is True for v in etat_sauve.values())


def test_main_deja_alerte_ne_re_notifie_pas():
    etat_existant = {f: True for f in _sante_uniforme(0)}
    with patch.dict("os.environ", _ENV_BASE, clear=True), \
         patch("watchdog_workflows.charger_memoire_supabase", return_value=etat_existant), \
         patch("watchdog_workflows.verifier_sante", return_value=_sante_uniforme(5)), \
         patch("watchdog_workflows.envoyer_telegram") as tg_mock, \
         patch("watchdog_workflows.sauvegarder_memoire_supabase") as save_mock:
        main()
    tg_mock.assert_not_called()
    save_mock.assert_not_called()


def test_main_retour_au_vert_envoie_resolution_et_reinitialise_l_etat():
    etat_existant = {f: True for f in _sante_uniforme(0)}
    with patch.dict("os.environ", _ENV_BASE, clear=True), \
         patch("watchdog_workflows.charger_memoire_supabase", return_value=etat_existant), \
         patch("watchdog_workflows.verifier_sante", return_value=_sante_uniforme(0)), \
         patch("watchdog_workflows.envoyer_telegram", return_value=True) as tg_mock, \
         patch("watchdog_workflows.sauvegarder_memoire_supabase", return_value=True) as save_mock:
        main()
    assert tg_mock.call_count == NB_WORKFLOWS_SURVEILLES
    etat_sauve = save_mock.call_args[0][0]
    assert all(v is False for v in etat_sauve.values())


def test_main_sous_le_seuil_sans_alerte_prealable_ne_declenche_rien():
    with patch.dict("os.environ", _ENV_BASE, clear=True), \
         patch("watchdog_workflows.charger_memoire_supabase", return_value={}), \
         patch("watchdog_workflows.verifier_sante", return_value=_sante_uniforme(1)), \
         patch("watchdog_workflows.envoyer_telegram") as tg_mock, \
         patch("watchdog_workflows.sauvegarder_memoire_supabase") as save_mock:
        main()
    tg_mock.assert_not_called()
    save_mock.assert_not_called()


def test_main_supabase_injoignable_continue_avec_etat_vide():
    with patch.dict("os.environ", _ENV_BASE, clear=True), \
         patch("watchdog_workflows.charger_memoire_supabase", return_value=None), \
         patch("watchdog_workflows.verifier_sante", return_value=_sante_uniforme(3)), \
         patch("watchdog_workflows.envoyer_telegram", return_value=True) as tg_mock, \
         patch("watchdog_workflows.sauvegarder_memoire_supabase", return_value=True):
        main()
    assert tg_mock.call_count == NB_WORKFLOWS_SURVEILLES
