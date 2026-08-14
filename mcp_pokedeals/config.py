"""
Configuration centralisee du MCP PokeDeals : URLs et cles API, toutes lues
depuis des variables d'environnement -- AUCUNE cle en dur dans le code.

Charge automatiquement un fichier .env s'il existe (jamais committe, voir
.gitignore) via python-dotenv -- evite d'avoir a "export" chaque variable
a la main a chaque session.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    tcgdex_base_url: str
    carddex_base_url: str
    carddex_api_key: str | None
    cardmarket_base_url: str
    cardmarket_api_key: str | None
    cardmarket_price_guide_url: str
    cache_ttl_cartes: int
    cache_ttl_sets: int
    cache_ttl_prix: int


def charger_config() -> Config:
    """Lit la configuration depuis les variables d'environnement, avec des
    valeurs par defaut raisonnables pour tout ce qui est public/gratuit.

    IMPORTANT (voir mcp_pokedeals/README.md, section "Statut des sources") :
    CARDDEX_BASE_URL par defaut est une DEDUCTION a partir de la
    documentation publique de CardDex, pas une valeur confirmee -- corrige
    ton .env si besoin, aucune modification de code necessaire.
    """
    return Config(
        tcgdex_base_url=os.environ.get("TCGDEX_BASE_URL", "https://api.tcgdex.net/v2"),
        carddex_base_url=os.environ.get("CARDDEX_BASE_URL", "https://api.carddex.dev"),
        carddex_api_key=os.environ.get("CARDDEX_API_KEY") or None,
        cardmarket_base_url=os.environ.get("CARDMARKET_BASE_URL", "https://api.cardmarket.com/ws/v2.0"),
        cardmarket_api_key=os.environ.get("CARDMARKET_API_KEY") or None,
        cardmarket_price_guide_url=os.environ.get(
            "CARDMARKET_PRICE_GUIDE_URL",
            "https://downloads.s3.cardmarket.com/productCatalog/priceGuide/price_guide_6.json",
        ),
        cache_ttl_cartes=int(os.environ.get("MCP_CACHE_TTL_CARTES", 86400)),
        cache_ttl_sets=int(os.environ.get("MCP_CACHE_TTL_SETS", 86400)),
        cache_ttl_prix=int(os.environ.get("MCP_CACHE_TTL_PRIX", 10800)),
    )
