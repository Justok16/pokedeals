"""Tests du service prix -- verifie surtout que les sources ne sont jamais
melangees entre elles (consigne du projet)."""

from mcp_pokedeals.models import PriceResult
from mcp_pokedeals.services.prices import PricesService


class _FauxCardDex:
    def obtenir_prix(self, card_id):
        return [
            PriceResult(
                card_id=card_id, source="carddex", currency="USD",
                price=4.5, price_type="trend", retrieved_at="2026-01-01T00:00:00+00:00",
            )
        ]


class _FauxCardmarket:
    def obtenir_prix_par_id_produit(self, id_produit):
        return PriceResult(
            card_id=str(id_produit), source="cardmarket", currency="EUR",
            price=3.9, price_type="trend", retrieved_at="2026-01-01T00:00:00+00:00",
        )


def test_deux_sources_restent_distinctes():
    service = PricesService(_FauxCardDex(), _FauxCardmarket())
    resultat = service.get_card_prices("me01-001", cardmarket_product_id=271439)

    sources = {p["source"] for p in resultat["prices"]}
    assert sources == {"carddex", "cardmarket"}

    carddex_prix = next(p for p in resultat["prices"] if p["source"] == "carddex")
    cardmarket_prix = next(p for p in resultat["prices"] if p["source"] == "cardmarket")
    assert carddex_prix["currency"] == "USD"
    assert cardmarket_prix["currency"] == "EUR"
    assert carddex_prix["price"] != cardmarket_prix["price"]
    assert resultat["errors"] == []


def test_sans_cardmarket_product_id_seul_carddex_repond():
    service = PricesService(_FauxCardDex(), _FauxCardmarket())
    resultat = service.get_card_prices("me01-001")
    assert len(resultat["prices"]) == 1
    assert resultat["prices"][0]["source"] == "carddex"


def test_provider_filtre_un_seul():
    service = PricesService(_FauxCardDex(), _FauxCardmarket())
    resultat = service.get_card_prices("me01-001", cardmarket_product_id=271439, provider="carddex")
    assert len(resultat["prices"]) == 1
    assert resultat["prices"][0]["source"] == "carddex"
