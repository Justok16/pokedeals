"""
Serveur MCP PokeDeals -- expose des outils Pokemon TCG (cartes, sets, prix)
a une IA comme Claude Code, via le protocole MCP (transport stdio).

Lancement direct (verification manuelle) :
    python -m mcp_pokedeals.server

Voir mcp_pokedeals/README.md pour l'installation complete et la
configuration Claude Code (fichier .mcp.json a la racine du depot).
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

from mcp_pokedeals.cache import CacheJSON
from mcp_pokedeals.config import charger_config
from mcp_pokedeals.providers.carddex import CardDexProvider
from mcp_pokedeals.providers.cardmarket import CardmarketPriceGuideProvider
from mcp_pokedeals.providers.tcgdex import TCGdexProvider
from mcp_pokedeals.services.analysis import AnalysisService
from mcp_pokedeals.services.cards import CardsService
from mcp_pokedeals.services.prices import PricesService

# IMPORTANT : les logs partent sur stderr, JAMAIS sur stdout -- stdout est
# reserve aux messages du protocole MCP (stdio). Un simple print() cassait
# la communication avec Claude Code.
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
log = logging.getLogger("mcp_pokedeals")

CHEMIN_CACHE = Path(__file__).resolve().parent / ".cache" / "cache.json"

_config = charger_config()
_cache = CacheJSON(CHEMIN_CACHE)

_tcgdex = TCGdexProvider(_config, _cache)
_carddex = CardDexProvider(_config, _cache)
_cardmarket = CardmarketPriceGuideProvider(_config, _cache)

_cards_service = CardsService(_tcgdex)
_prices_service = PricesService(_carddex, _cardmarket)
_analysis_service = AnalysisService(_cards_service, _prices_service)

mcp = MCPServer("pokedeals")


@mcp.tool()
def search_cards(
    name: str | None = None,
    number: str | None = None,
    set_id: str | None = None,
    rarity: str | None = None,
    language: str = "en",
    limit: int = 20,
) -> list[dict]:
    """Recherche des cartes Pokemon TCG par nom, numero, set ou rarete (source : TCGdex).

    `name` fait une recherche par sous-chaine (insensible a la casse).
    `language` : code de langue TCGdex (ex. "en", "fr", "ja"). `limit` est
    plafonne a 100 pour eviter une reponse gigantesque."""
    try:
        return _cards_service.search_cards(name, number, set_id, rarity, language, limit)
    except Exception as e:  # noqa: BLE001 -- jamais de traceback brute vers Claude
        return [{"error": str(e)}]


@mcp.tool()
def get_card(card_id: str, language: str = "en") -> dict:
    """Retourne les informations detaillees d'une carte a partir de son
    identifiant TCGdex (ex. "swsh3-136") (source : TCGdex)."""
    try:
        return _cards_service.get_card(card_id, language)
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}


@mcp.tool()
def search_set(name: str | None = None, series: str | None = None, language: str = "en") -> list[dict]:
    """Recherche une extension/set Pokemon TCG par nom ou serie (source : TCGdex)."""
    try:
        return _cards_service.search_set(name, series, language)
    except Exception as e:  # noqa: BLE001
        return [{"error": str(e)}]


@mcp.tool()
def get_set_cards(set_id: str, language: str = "en", page: int = 1, per_page: int = 25) -> list[dict]:
    """Retourne les cartes d'un set donne, paginees (source : TCGdex).
    `per_page` plafonne le nombre de cartes renvoyees par appel."""
    try:
        return _cards_service.get_set_cards(set_id, language, page, per_page)
    except Exception as e:  # noqa: BLE001
        return [{"error": str(e)}]


@mcp.tool()
def get_card_prices(
    card_id: str,
    cardmarket_product_id: str | None = None,
    provider: str | None = None,
) -> dict:
    """Retourne les prix connus d'une carte, SOURCE PAR SOURCE (CardDex et/ou
    guide officiel Cardmarket) -- jamais melanges en un seul chiffre.

    `card_id` : identifiant CardDex de la carte. `cardmarket_product_id` :
    idProduct Cardmarket (optionnel, necessaire pour obtenir aussi le prix
    du guide officiel Cardmarket). `provider` : "carddex", "cardmarket", ou
    vide pour interroger les deux."""
    return _prices_service.get_card_prices(card_id, cardmarket_product_id, provider)


@mcp.tool()
def analyze_card(card_id: str, language: str = "en", cardmarket_product_id: str | None = None) -> dict:
    """Synthese informative combinant fiche carte (TCGdex) et prix connus.
    N'EST PAS une prediction de valeur future -- rassemble uniquement des
    indicateurs objectifs deja mesures (prix actuels, ecart entre sources)."""
    try:
        return _analysis_service.analyze_card(card_id, language, cardmarket_product_id)
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run()
