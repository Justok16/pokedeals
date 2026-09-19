"""Tests pour l'interrupteur maitre des notifications personnelles de
Justok (notifications_perso.py, ajoute le 19/09/2026 a sa demande
explicite -- cf. son commentaire d'en-tete pour le contexte complet)."""

import textwrap

import notifications_perso


def _ecrire_config(tmp_path, telegram, email):
    chemin = tmp_path / "config.yaml"
    chemin.write_text(textwrap.dedent(f"""\
        notifications:
          telegram: {str(telegram).lower()}
          email: {str(email).lower()}
        """), encoding="utf-8")
    return chemin


def test_token_telegram_perso_vide_si_desactive(tmp_path, monkeypatch):
    chemin = _ecrire_config(tmp_path, telegram=False, email=True)
    monkeypatch.setattr(notifications_perso, "CHEMIN_CONFIG_DEFAUT", chemin)
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "vrai-token")

    assert notifications_perso.token_telegram_perso() == ""


def test_token_telegram_perso_actif_si_notifications_telegram_true(tmp_path, monkeypatch):
    chemin = _ecrire_config(tmp_path, telegram=True, email=False)
    monkeypatch.setattr(notifications_perso, "CHEMIN_CONFIG_DEFAUT", chemin)
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "vrai-token")

    assert notifications_perso.token_telegram_perso() == "vrai-token"


def test_mdp_email_perso_vide_si_desactive(tmp_path, monkeypatch):
    chemin = _ecrire_config(tmp_path, telegram=True, email=False)
    monkeypatch.setattr(notifications_perso, "CHEMIN_CONFIG_DEFAUT", chemin)
    monkeypatch.setenv("GMAIL_APP_PASSWORD", "vrai-mdp")

    assert notifications_perso.mdp_email_perso() == ""


def test_mdp_email_perso_actif_si_notifications_email_true(tmp_path, monkeypatch):
    chemin = _ecrire_config(tmp_path, telegram=False, email=True)
    monkeypatch.setattr(notifications_perso, "CHEMIN_CONFIG_DEFAUT", chemin)
    monkeypatch.setenv("GMAIL_APP_PASSWORD", "vrai-mdp")

    assert notifications_perso.mdp_email_perso() == "vrai-mdp"


def test_cle_absente_de_config_yaml_reste_active_par_defaut(tmp_path, monkeypatch):
    # Retro-compatibilite : un config.yaml sans section "notifications" du
    # tout (ancien format, ou fichier de test minimal) ne doit JAMAIS
    # couper silencieusement les notifications -- comportement inchange
    # tant que Justok ne les a pas explicitement desactivees.
    chemin = tmp_path / "config.yaml"
    chemin.write_text("watchlist: []\n", encoding="utf-8")
    monkeypatch.setattr(notifications_perso, "CHEMIN_CONFIG_DEFAUT", chemin)
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "vrai-token")
    monkeypatch.setenv("GMAIL_APP_PASSWORD", "vrai-mdp")

    assert notifications_perso.token_telegram_perso() == "vrai-token"
    assert notifications_perso.mdp_email_perso() == "vrai-mdp"


def test_secret_absent_reste_vide_meme_si_notifications_actives(tmp_path, monkeypatch):
    chemin = _ecrire_config(tmp_path, telegram=True, email=True)
    monkeypatch.setattr(notifications_perso, "CHEMIN_CONFIG_DEFAUT", chemin)
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("GMAIL_APP_PASSWORD", raising=False)

    assert notifications_perso.token_telegram_perso() == ""
    assert notifications_perso.mdp_email_perso() == ""
