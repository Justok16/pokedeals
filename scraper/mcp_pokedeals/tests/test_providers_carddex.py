"""Tests du fournisseur CardDex -- AUCUN appel reseau reel."""

from unittest.mock import Mock, patch

import pytest

from mcp_pokedeals.cache import CacheJSON
from mcp_pokedeals.config import Config
from mcp_pokedeals.providers.carddex import CardDexError, CardDexProvider


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


def _provider(tmp_path) -> CardDexProvider:
    cache = CacheJSON(tmp_path / "cache.json")
    return CardDexProvider(_config(), cache)


def test_obtenir_prix_ok(tmp_path):
    provider = _provider(tmp_path)
    reponse = Mock(status_code=200)
    reponse.json.return_value = {"data": {"id": "me01-001", "prices": {"trend": 4.5, "avg_7d": 4.2}}}
    with patch("mcp_pokedeals.providers.carddex.requests.get", return_value=reponse):
        prix = provider.obtenir_prix("me01-001")
    assert prix[0].price == 4.5
    assert prix[0].source == "carddex"
    assert prix[0].trend == 4.2


def test_obtenir_prix_aucun_prix_disponible(tmp_path):
    provider = _provider(tmp_path)
    reponse = Mock(status_code=200)
    reponse.json.return_value = {"data": {"id": "me01-001", "prices": {}}}
    with patch("mcp_pokedeals.providers.carddex.requests.get", return_value=reponse):
        with pytest.raises(CardDexError):
            provider.obtenir_prix("me01-001")


def test_cle_invalide_401(tmp_path):
    provider = _provider(tmp_path)
    reponse = Mock(status_code=401)
    with patch("mcp_pokedeals.providers.carddex.requests.get", return_value=reponse):
        with pytest.raises(CardDexError, match="401"):
            provider.obtenir_prix("x")


def test_route_introuvable_404_message_explicite(tmp_path):
    provider = _provider(tmp_path)
    reponse = Mock(status_code=404)
    with patch("mcp_pokedeals.providers.carddex.requests.get", return_value=reponse):
        with pytest.raises(CardDexError, match="CARDDEX_BASE_URL"):
            provider.obtenir_prix("x")


def test_absence_de_cle_fonctionne_quand_meme_sans_entete(tmp_path):
    provider = _provider(tmp_path)
    reponse = Mock(status_code=200)
    reponse.json.return_value = {"data": {"prices": {"trend": 1.0}}}
    with patch("mcp_pokedeals.providers.carddex.requests.get", return_value=reponse) as m:
        provider.obtenir_prix("x")
    _, kwargs = m.call_args
    assert "X-API-Key" not in kwargs.get("headers", {})


def test_avec_cle_entete_envoyee(tmp_path):
    cfg = Config(
        tcgdex_base_url="https://api.tcgdex.net/v2",
        carddex_base_url="https://api.carddex.dev",
        carddex_api_key="pk_live_test",
        cardmarket_base_url="https://api.cardmarket.com/ws/v2.0",
        cardmarket_api_key=None,
        cardmarket_price_guide_url="https://example.invalid/guide.json",
        cache_ttl_cartes=3600,
        cache_ttl_sets=3600,
        cache_ttl_prix=3600,
    )
    cache = CacheJSON(tmp_path / "cache.json")
    provider = CardDexProvider(cfg, cache)
    reponse = Mock(status_code=200)
    reponse.json.return_value = {"data": {"prices": {"trend": 1.0}}}
    with patch("mcp_pokedeals.providers.carddex.requests.get", return_value=reponse) as m:
        provider.obtenir_prix("x")
    _, kwargs = m.call_args
    assert kwargs["headers"]["X-API-Key"] == "pk_live_test"
