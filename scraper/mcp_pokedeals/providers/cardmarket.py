"""
Fournisseur Cardmarket : DEUX integrations bien distinctes, jamais melangees.

1) Guide de prix officiel (CardmarketPriceGuideProvider) -- ACTIF PAR DEFAUT
   Cardmarket publie lui-meme, gratuitement et SANS authentification, un
   fichier JSON contenant le prix ("trend") de la quasi-totalite de ses
   produits :
   https://downloads.s3.cardmarket.com/productCatalog/priceGuide/price_guide_6.json
   Aucun scraping, aucune violation des conditions d'utilisation -- c'est
   exactement ce que fait deja main.py (racine du depot, fonctions
   cardmarket_prix()/_cm_charger_guide_prix(), en production depuis le
   26/07/2026). Limite connue : ce fichier identifie chaque carte par un
   "idProduct" Cardmarket numerique, pas par nom -- il faut deja connaitre
   cet identifiant (main.py l'obtient aujourd'hui via Cardtrader, hors
   perimetre de ce MCP).

2) API Marketplace officielle (CardmarketMarketplaceProvider) --
   DESACTIVEE PAR DEFAUT, NON IMPLEMENTEE
   Cardmarket propose une vraie API (https://api.cardmarket.com/ws/
   documentation) pour les annonces individuelles et la vente, mais elle :
     - necessite un COMPTE VENDEUR Cardmarket (pas juste une cle API) ;
     - s'authentifie en OAuth 1.0 (cle + token + signature HMAC-SHA1
       generee sur CHAQUE requete a partir des identifiants du compte) ;
     - n'est donc pas une simple variable d'environnement a remplir.
   Conformement a la consigne du projet ("ne jamais contourner une
   authentification/restriction technique"), cette voie n'est PAS
   implementee. La classe ci-dessous documente la situation et pourra
   etre completee plus tard si tu obtiens un compte + des identifiants
   OAuth Cardmarket.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

import requests

from mcp_pokedeals.cache import CacheJSON
from mcp_pokedeals.config import Config
from mcp_pokedeals.models import PriceResult

log = logging.getLogger("mcp_pokedeals.providers.cardmarket")

TIMEOUT = 60  # le fichier de guide de prix est volumineux (plusieurs Mo)


class CardmarketError(Exception):
    """Erreur Cardmarket avec un message clair."""


class CardmarketPriceGuideProvider:
    """Couche 1 : guide de prix officiel, gratuit, sans authentification."""

    def __init__(self, config: Config, cache: CacheJSON):
        self._url = config.cardmarket_price_guide_url
        self._cache = cache
        # Le guide n'est publie par Cardmarket qu'une fois par jour --
        # inutile de le re-telecharger plus souvent (fichier de plusieurs
        # Mo). On force donc un minimum de 20h meme si MCP_CACHE_TTL_PRIX
        # (pense pour des prix plus volatils, ex. CardDex) est plus court.
        self._ttl = max(config.cache_ttl_prix, 20 * 3600)

    def obtenir_prix_par_id_produit(self, id_produit: int | str) -> PriceResult:
        guide = self._guide_charge()
        trend = guide.get(str(id_produit))
        if trend is None:
            raise CardmarketError(
                f"Cardmarket : aucun prix trouve pour l'idProduct '{id_produit}' "
                "dans le guide de prix officiel"
            )
        return PriceResult(
            card_id=str(id_produit),
            source="cardmarket",
            currency="EUR",
            price=float(trend),
            price_type="trend",
            retrieved_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            note="Guide de prix officiel Cardmarket (mis a jour par Cardmarket une fois par jour)",
        )

    def _guide_charge(self) -> dict:
        cle_cache = "guide_prix_cardmarket"
        valeur_cache = self._cache.get(cle_cache, self._ttl)
        if valeur_cache is not None:
            return valeur_cache

        try:
            rep = requests.get(self._url, timeout=TIMEOUT)
            rep.raise_for_status()
            data = rep.json()
        except requests.exceptions.Timeout:
            raise CardmarketError(f"Cardmarket : delai depasse au telechargement du guide de prix ({TIMEOUT}s)")
        except requests.exceptions.RequestException as e:
            raise CardmarketError(f"Cardmarket : echec du telechargement du guide de prix ({e})")
        except ValueError:
            raise CardmarketError("Cardmarket : guide de prix illisible (pas du JSON valide)")

        guides = data.get("priceGuides", [])
        prix_par_id = {
            str(g["idProduct"]): g.get("trend")
            for g in guides
            if g.get("idProduct") and g.get("trend") is not None
        }
        self._cache.set(cle_cache, prix_par_id)
        return prix_par_id


class CardmarketMarketplaceProvider:
    """Couche 2 : API Marketplace officielle (annonces individuelles, vente...).

    DESACTIVEE PAR DEFAUT -- necessite un compte vendeur Cardmarket et une
    authentification OAuth 1.0 non implementee ici (voir docstring du
    fichier). Toute methode leve NotImplementedError avec un message
    explicite plutot que d'echouer silencieusement ou de deviner un
    comportement."""

    def __init__(self, config: Config):
        self._configuree = bool(config.cardmarket_api_key)

    def est_configuree(self) -> bool:
        return self._configuree

    def rechercher_annonces(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError(
            "L'API Marketplace Cardmarket necessite un compte vendeur et une "
            "authentification OAuth 1.0 (cle + token + signature HMAC-SHA1 par "
            "requete), non implementee dans ce MCP. Voir la docstring de "
            "mcp_pokedeals/providers/cardmarket.py et "
            "https://api.cardmarket.com/ws/documentation si tu veux completer "
            "cette integration toi-meme."
        )
