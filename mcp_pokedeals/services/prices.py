"""
Service "prix" : interroge CardDex et/ou le guide de prix Cardmarket,
SANS JAMAIS melanger silencieusement les sources -- chaque resultat garde
sa source, sa devise et sa date de recuperation propres.
"""

from __future__ import annotations

from mcp_pokedeals.providers.carddex import CardDexError, CardDexProvider
from mcp_pokedeals.providers.cardmarket import CardmarketError, CardmarketPriceGuideProvider


class PricesService:
    def __init__(self, carddex: CardDexProvider, cardmarket: CardmarketPriceGuideProvider):
        self._carddex = carddex
        self._cardmarket = cardmarket

    def get_card_prices(
        self,
        card_id: str,
        cardmarket_product_id: str | int | None = None,
        provider: str | None = None,
    ) -> dict:
        """Retourne les prix disponibles, groupes PAR SOURCE (jamais fusionnes
        en un seul chiffre).

        `card_id` : identifiant CardDex de la carte.
        `cardmarket_product_id` : idProduct Cardmarket, optionnel -- necessaire
        UNIQUEMENT si tu veux aussi le prix du guide officiel Cardmarket (le
        guide identifie les cartes par cet id numerique, pas par nom).
        `provider` : None (toutes les sources dispo) | "carddex" | "cardmarket".
        """
        resultats: list[dict] = []
        erreurs: list[str] = []

        if provider in (None, "carddex"):
            try:
                for p in self._carddex.obtenir_prix(card_id):
                    resultats.append(p.to_dict())
            except CardDexError as e:
                erreurs.append(str(e))

        if provider in (None, "cardmarket") and cardmarket_product_id is not None:
            try:
                p = self._cardmarket.obtenir_prix_par_id_produit(cardmarket_product_id)
                resultats.append(p.to_dict())
            except CardmarketError as e:
                erreurs.append(str(e))

        return {"card_id": card_id, "prices": resultats, "errors": erreurs}
