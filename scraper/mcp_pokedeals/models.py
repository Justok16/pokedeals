"""Structures de donnees partagees entre providers et services.

Chaque modele a une methode to_dict() : les outils MCP retournent des
dictionnaires JSON-serialisables, jamais des objets Python bruts."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Card:
    id: str
    name: str
    local_id: str | None = None
    set_id: str | None = None
    set_name: str | None = None
    series: str | None = None
    rarity: str | None = None
    category: str | None = None
    types: list[str] = field(default_factory=list)
    hp: int | None = None
    illustrator: str | None = None
    image_url: str | None = None
    language: str = "en"
    source: str = "tcgdex"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "local_id": self.local_id,
            "set_id": self.set_id,
            "set_name": self.set_name,
            "series": self.series,
            "rarity": self.rarity,
            "category": self.category,
            "types": self.types,
            "hp": self.hp,
            "illustrator": self.illustrator,
            "image_url": self.image_url,
            "language": self.language,
            "source": self.source,
        }


@dataclass
class CardSet:
    id: str
    name: str
    series: str | None = None
    release_date: str | None = None
    card_count_official: int | None = None
    card_count_total: int | None = None
    logo_url: str | None = None
    source: str = "tcgdex"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "series": self.series,
            "release_date": self.release_date,
            "card_count_official": self.card_count_official,
            "card_count_total": self.card_count_total,
            "logo_url": self.logo_url,
            "source": self.source,
        }


@dataclass
class PriceResult:
    """Un prix, TOUJOURS rattache explicitement a sa source -- jamais
    fusionne silencieusement avec un prix d'une autre source (consigne du
    projet). `price_type` : "trend" | "market" | "avg7" | "avg30" | ..."""
    card_id: str
    source: str
    currency: str
    price: float
    price_type: str
    retrieved_at: str
    trend: float | None = None
    note: str | None = None

    def to_dict(self) -> dict:
        return {
            "card_id": self.card_id,
            "source": self.source,
            "currency": self.currency,
            "price": self.price,
            "price_type": self.price_type,
            "retrieved_at": self.retrieved_at,
            "trend": self.trend,
            "note": self.note,
        }
