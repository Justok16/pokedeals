from unittest.mock import Mock, patch

import requests

from memoire_supabase import charger_memoire_supabase, sauvegarder_memoire_supabase


# ------------------- charger_memoire_supabase -------------------

def test_charger_sans_secrets_renvoie_none():
    assert charger_memoire_supabase("stock_boutiques_tcg", "", "") is None
    assert charger_memoire_supabase("stock_boutiques_tcg", "https://x.supabase.co", "") is None


def test_charger_cle_inconnue_renvoie_dict_vide():
    reponse = Mock(status_code=200)
    reponse.json.return_value = []
    reponse.raise_for_status.return_value = None
    with patch("memoire_supabase.requests.get", return_value=reponse):
        assert charger_memoire_supabase("stock_boutiques_tcg", "https://x.supabase.co", "cle") == {}


def test_charger_cle_connue_renvoie_les_donnees():
    reponse = Mock(status_code=200)
    reponse.json.return_value = [{"donnees": {"a.fr|Carte 1/1": {"en_stock": True}}}]
    reponse.raise_for_status.return_value = None
    with patch("memoire_supabase.requests.get", return_value=reponse):
        memoire = charger_memoire_supabase("stock_boutiques_tcg", "https://x.supabase.co", "cle")
    assert memoire == {"a.fr|Carte 1/1": {"en_stock": True}}


def test_charger_erreur_reseau_renvoie_none():
    with patch("memoire_supabase.requests.get", side_effect=requests.RequestException("boom")):
        assert charger_memoire_supabase("stock_boutiques_tcg", "https://x.supabase.co", "cle") is None


def test_charger_reponse_http_en_erreur_renvoie_none():
    reponse = Mock(status_code=500)
    reponse.raise_for_status.side_effect = requests.HTTPError("500")
    with patch("memoire_supabase.requests.get", return_value=reponse):
        assert charger_memoire_supabase("stock_boutiques_tcg", "https://x.supabase.co", "cle") is None


def test_charger_reponse_json_mal_formee_renvoie_none():
    reponse = Mock(status_code=200)
    reponse.json.return_value = [{}]  # pas de cle "donnees"
    reponse.raise_for_status.return_value = None
    with patch("memoire_supabase.requests.get", return_value=reponse):
        assert charger_memoire_supabase("stock_boutiques_tcg", "https://x.supabase.co", "cle") is None


# ------------------- sauvegarder_memoire_supabase -------------------

def test_sauvegarder_sans_secrets_renvoie_false():
    assert sauvegarder_memoire_supabase({}, "stock_boutiques_tcg", "", "") is False


def test_sauvegarder_succes_renvoie_true_et_upsert_sur_cle():
    reponse = Mock(status_code=201)
    reponse.raise_for_status.return_value = None
    with patch("memoire_supabase.requests.post", return_value=reponse) as mock_post:
        ok = sauvegarder_memoire_supabase(
            {"a.fr|Carte 1/1": {"en_stock": True}}, "stock_boutiques_tcg",
            "https://x.supabase.co", "cle",
        )
    assert ok is True
    appel = mock_post.call_args
    assert appel.kwargs["params"] == {"on_conflict": "cle"}
    assert appel.kwargs["json"]["cle"] == "stock_boutiques_tcg"
    assert appel.kwargs["json"]["donnees"] == {"a.fr|Carte 1/1": {"en_stock": True}}
    assert appel.kwargs["headers"]["Prefer"] == "resolution=merge-duplicates"


def test_sauvegarder_erreur_reseau_renvoie_false():
    with patch("memoire_supabase.requests.post", side_effect=requests.RequestException("boom")):
        assert sauvegarder_memoire_supabase({}, "stock_boutiques_tcg", "https://x.supabase.co", "cle") is False
