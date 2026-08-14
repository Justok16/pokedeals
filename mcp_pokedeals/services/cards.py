"""
Service "cartes" : appelle TCGdexProvider et met les resultats en forme
pour les outils MCP (search_cards, get_card, search_set, get_set_cards).
"""

from __future__ import annotations

from mcp_pokedeals.providers.tcgdex import TCGdexProvider


class CardsService:
    def __init__(self, tcgdex: TCGdexProvider):
        self._tcgdex = tcgdex

    def search_cards(
        self,
        name: str | None = None,
        number: str | None = None,
        set_id: str | None = None,
        rarity: str | None = None,
        language: str = "en",
        limit: int = 20,
    ) -> list[dict]:
        cartes = self._tcgdex.rechercher_cartes(
            nom=name, numero=number, set_id=set_id, rarete=rarity, langue=language, limite=limit,
        )
        return [c.to_dict() for c in cartes]

    def get_card(self, card_id: str, language: str = "en") -> dict:
        carte = self._tcgdex.obtenir_carte(card_id, langue=language)
        return carte.to_dict()

    def search_set(
        self, name: str | None = None, series: str | None = None, language: str = "en"
    ) -> list[dict]:
        sets = self._tcgdex.rechercher_sets(nom=name, serie=series, langue=language)
        return [s.to_dict() for s in sets]

    def get_set_cards(
        self, set_id: str, language: str = "en", page: int = 1, per_page: int = 25
    ) -> list[dict]:
        cartes = self._tcgdex.obtenir_cartes_du_set(set_id, langue=language, page=page, par_page=per_page)
        return [c.to_dict() for c in cartes]
