"""Tests du guide de prix officiel Cardmarket -- AUCUN appel reseau reel."""

from unittest.mock import Mock, patch

import pytest

from mcp_pokedeals.cache import CacheJSON
from mcp_pokedeals.config import Config
from mcp_pokedeals.providers.cardmarket import (
    CardmarketError,
    CardmarketMarketplaceProvider,
    CardmarketPriceGuideProvider,
)


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


def test_obtenir_prix_par_id_produit_ok(tmp_path):
    cache = CacheJSON(tmp_path / "cache.json")
    provider = CardmarketPriceGuideProvider(_config(), cache)
    reponse = Mock(status_code=200)
    reponse.raise_for_status = Mock()
    reponse.json.return_value = {"priceGuides": [{"idProduct": 271439, "trend": 12.5}]}
    with patch("mcp_pokedeals.providers.cardmarket.requests.get", return_value=reponse):
        prix = provider.obtenir_prix_par_id_produit(271439)
    assert prix.price == 12.5
    assert prix.currency == "EUR"
    assert prix.source == "cardmarket"


def test_id_produit_absent_du_guide(tmp_path):
    cache = CacheJSON(tmp_path / "cache.json")
    provider = CardmarketPriceGuideProvider(_config(), cache)
    reponse = Mock(status_code=200)
    reponse.raise_for_status = Mock()
    reponse.json.return_value = {"priceGuides": []}
    with patch("mcp_pokedeals.providers.cardmarket.requests.get", return_value=reponse):
        with pytest.raises(CardmarketError):
            provider.obtenir_prix_par_id_produit(999999)


def test_guide_mis_en_cache_evite_un_second_telechargement(tmp_path):
    cache = CacheJSON(tmp_path / "cache.json")
    provider = CardmarketPriceGuideProvider(_config(), cache)
    reponse = Mock(status_code=200)
    reponse.raise_for_status = Mock()
    reponse.json.return_value = {"priceGuides": [{"idProduct": 1, "trend": 1.0}, {"idProduct": 2, "trend": 2.0}]}
    with patch("mcp_pokedeals.providers.cardmarket.requests.get", return_value=reponse) as m:
        provider.obtenir_prix_par_id_produit(1)
        provider.obtenir_prix_par_id_produit(2)
    assert m.call_count == 1  # le guide entier est mis en cache, pas re-telecharge


def test_marketplace_provider_leve_une_erreur_explicite():
    provider = CardmarketMarketplaceProvider(_config())
    assert provider.est_configuree() is False
    with pytest.raises(NotImplementedError, match="OAuth"):
        provider.rechercher_annonces()
