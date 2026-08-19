"""Tests du fournisseur TCGdex -- AUCUN appel reseau reel (requests.get
mocke), pour ne jamais dependre de la disponibilite de l'API externe."""

from unittest.mock import Mock, patch

import pytest

from mcp_pokedeals.cache import CacheJSON
from mcp_pokedeals.config import Config
from mcp_pokedeals.providers.tcgdex import TCGdexError, TCGdexProvider


def _config() -> Config:
    return Config(
        tcgdex_base_url="https://api.tcgdex.net/v2",
        carddex_base_url="https://api.carddex.dev",
        carddex_api_key=None,
        cardmarket_base_url="https://api.cardmarket.com/ws/v2.0",
        cardmarket_api_key=None,
        cardmarket_price_guide_url="https://example.invalid/guide.json",
        cache_ttl_cartes=3600,
        cache_ttl_sets=3600,
        cache_ttl_prix=3600,
    )


def _provider(tmp_path) -> TCGdexProvider:
    cache = CacheJSON(tmp_path / "cache.json")
    return TCGdexProvider(_config(), cache)


CARTE_EXEMPLE = {
    "id": "swsh3-136",
    "localId": "136",
    "name": "Charizard",
    "rarity": "Rare Holo",
    "category": "Pokemon",
    "types": ["Fire"],
    "hp": 170,
    "illustrator": "5ban Graphics",
    "image": "https://assets.tcgdex.net/en/swsh/swsh3/136",
    "set": {"id": "swsh3", "name": "Darkness Ablaze", "cardCount": {"official": 189, "total": 201}},
}


def test_get_card_ok(tmp_path):
    provider = _provider(tmp_path)
    reponse = Mock(status_code=200)
    reponse.json.return_value = CARTE_EXEMPLE
    with patch("mcp_pokedeals.providers.tcgdex.requests.get", return_value=reponse) as m:
        carte = provider.obtenir_carte("swsh3-136")
    assert carte.name == "Charizard"
    assert carte.set_id == "swsh3"
    assert carte.hp == 170
    assert m.call_count == 1


def test_get_card_cache_evite_un_second_appel_reseau(tmp_path):
    provider = _provider(tmp_path)
    reponse = Mock(status_code=200)
    reponse.json.return_value = CARTE_EXEMPLE
    with patch("mcp_pokedeals.providers.tcgdex.requests.get", return_value=reponse) as m:
        provider.obtenir_carte("swsh3-136")
        provider.obtenir_carte("swsh3-136")
    assert m.call_count == 1  # 2e appel servi depuis le cache


def test_get_card_404(tmp_path):
    provider = _provider(tmp_path)
    reponse = Mock(status_code=404)
    with patch("mcp_pokedeals.providers.tcgdex.requests.get", return_value=reponse):
        with pytest.raises(TCGdexError):
            provider.obtenir_carte("carte-inexistante")


def test_rate_limit_429(tmp_path):
    provider = _provider(tmp_path)
    reponse = Mock(status_code=429)
    with patch("mcp_pokedeals.providers.tcgdex.requests.get", return_value=reponse):
        with pytest.raises(TCGdexError, match="429"):
            provider.obtenir_carte("x")


def test_reponse_json_invalide(tmp_path):
    provider = _provider(tmp_path)
    reponse = Mock(status_code=200)
    reponse.json.side_effect = ValueError("boom")
    with patch("mcp_pokedeals.providers.tcgdex.requests.get", return_value=reponse):
        with pytest.raises(TCGdexError, match="illisible"):
            provider.obtenir_carte("x")


def test_rechercher_cartes_ok(tmp_path):
    provider = _provider(tmp_path)
    reponse = Mock(status_code=200)
    reponse.json.return_value = [
        {"id": "swsh3-136", "localId": "136", "name": "Charizard", "image": "https://assets.tcgdex.net/en/swsh/swsh3/136"}
    ]
    with patch("mcp_pokedeals.providers.tcgdex.requests.get", return_value=reponse):
        resultats = provider.rechercher_cartes(nom="charizard")
    assert len(resultats) == 1
    assert resultats[0].name == "Charizard"


def test_rechercher_cartes_reponse_inattendue(tmp_path):
    provider = _provider(tmp_path)
    reponse = Mock(status_code=200)
    reponse.json.return_value = {"pas": "une liste"}
    with patch("mcp_pokedeals.providers.tcgdex.requests.get", return_value=reponse):
        with pytest.raises(TCGdexError):
            provider.rechercher_cartes(nom="pikachu")


def test_rechercher_sets_ok(tmp_path):
    provider = _provider(tmp_path)
    reponse = Mock(status_code=200)
    reponse.json.return_value = [
        {"id": "swsh3", "name": "Darkness Ablaze", "cardCount": {"official": 189, "total": 201}}
    ]
    with patch("mcp_pokedeals.providers.tcgdex.requests.get", return_value=reponse):
        resultats = provider.rechercher_sets(nom="darkness")
    assert resultats[0].id == "swsh3"
    assert resultats[0].card_count_official == 189


def test_obtenir_cartes_du_set_pagine(tmp_path):
    provider = _provider(tmp_path)
    reponse = Mock(status_code=200)
    reponse.json.return_value = {
        "id": "swsh3",
        "name": "Darkness Ablaze",
        "cards": [{"id": f"swsh3-{i}", "localId": str(i), "name": f"Carte {i}"} for i in range(1, 31)],
    }
    with patch("mcp_pokedeals.providers.tcgdex.requests.get", return_value=reponse):
        page1 = provider.obtenir_cartes_du_set("swsh3", page=1, par_page=25)
        page2 = provider.obtenir_cartes_du_set("swsh3", page=2, par_page=25)
    assert len(page1) == 25
    assert len(page2) == 5
