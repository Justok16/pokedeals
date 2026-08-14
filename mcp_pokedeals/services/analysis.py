"""
Service "analyse" : synthese INFORMATIVE combinant carte + prix connus.

IMPORTANT : ne pretend jamais predire une valeur future. Se contente de
rassembler des indicateurs objectifs deja mesures (prix actuels connus,
ecart entre sources) pour aider un humain -- ou Claude -- a raisonner. La
decision reste humaine.
"""

from __future__ import annotations

from mcp_pokedeals.services.cards import CardsService
from mcp_pokedeals.services.prices import PricesService


class AnalysisService:
    def __init__(self, cards: CardsService, prices: PricesService):
        self._cards = cards
        self._prices = prices

    def analyze_card(
        self,
        card_id: str,
        language: str = "en",
        cardmarket_product_id: str | int | None = None,
    ) -> dict:
        carte = self._cards.get_card(card_id, language=language)
        prix = self._prices.get_card_prices(card_id, cardmarket_product_id=cardmarket_product_id)

        valeurs = [p["price"] for p in prix["prices"] if p.get("price") is not None]
        ecart_pct = None
        if len(valeurs) >= 2:
            ecart_pct = round((max(valeurs) - min(valeurs)) / min(valeurs) * 100, 1)

        return {
            "card": carte,
            "prices": prix["prices"],
            "price_errors": prix["errors"],
            "indicators": {
                "sources_count": len(prix["prices"]),
                "spread_pct_between_sources": ecart_pct,
            },
            "disclaimer": (
                "Synthese informative basee sur les donnees disponibles au moment de la "
                "requete -- ce n'est PAS une prediction de valeur future."
            ),
        }
