"""Telegram perso coupe volontairement (config.yaml) : les evenements perso sont
memorises comme traites au lieu d'etre redetectes a chaque cycle (07/10/2026)."""

import notifications_perso as np_


def _config(tmp_path, telegram):
    chemin = tmp_path / "config.yaml"
    chemin.write_text(f"notifications:\n  telegram: {'true' if telegram else 'false'}\n  email: false\n", encoding="utf-8")
    return chemin


def _evenements():
    return [
        {"_cle_memoire": "a.fr|x", "_nouvel_etat": {"en_stock": True}},
        {"titre": "echec Supabase, cle retiree par l'appelant"},
        {"_cle_memoire": "b.fr|y", "_nouvel_etat": {"en_stock": True}},
    ]


def test_coupe_memorise_les_evenements(monkeypatch, tmp_path):
    monkeypatch.setattr(np_, "CHEMIN_CONFIG_DEFAUT", _config(tmp_path, telegram=False))
    memoire = {}
    np_.memoriser_si_telegram_perso_coupe(_evenements(), memoire)
    assert memoire == {"a.fr|x": {"en_stock": True}, "b.fr|y": {"en_stock": True}}


def test_actif_ne_memorise_rien(monkeypatch, tmp_path):
    monkeypatch.setattr(np_, "CHEMIN_CONFIG_DEFAUT", _config(tmp_path, telegram=True))
    memoire = {}
    np_.memoriser_si_telegram_perso_coupe(_evenements(), memoire)
    assert memoire == {}   # l'envoi Telegram reste seul juge (retente si echec)


def test_aucun_evenement(monkeypatch, tmp_path):
    monkeypatch.setattr(np_, "CHEMIN_CONFIG_DEFAUT", _config(tmp_path, telegram=False))
    memoire = {"deja": 1}
    np_.memoriser_si_telegram_perso_coupe([], memoire)
    assert memoire == {"deja": 1}
