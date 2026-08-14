"""
Fournisseur TCGdex (https://tcgdex.dev) : cartes, sets, et prix Cardmarket
que TCGdex integre deja lui-meme (champ "pricing.cardmarket" d'une carte).

API publique, GRATUITE, SANS CLE. Endpoints et noms de champs verifies via
le code DEJA EN PRODUCTION dans main.py (racine du depot) -- pas devines :
api.tcgdex.net/v2/{langue}/cards, /sets, avec les memes noms de champs
(localId, set.cardCount.official, pricing.cardmarket.trend...) que ceux
deja lus par obtenir_cote()/api_prix_carte() dans main.py depuis des mois.

Remarque sur le SDK officiel : TCGdex publie aussi un SDK Python
("tcgdex-sdk" sur PyPI, https://github.com/tcgdex/python-sdk). Ce module
ne l'utilise PAS : son modele d'objets Python exact (noms d'attributs)
n'a pas pu etre verifie precisement dans l'environnement de developpement
(acces web bloque pendant la redaction de ce fichier -- voir
mcp_pokedeals/README.md, section "Statut des sources"). Utiliser des
appels REST bruts, dont les noms de CHAMPS JSON sont deja EMPIRIQUEMENT
valides en production, est le choix le plus sur pour l'instant.
"""

from __future__ import annotations

import logging
from typing import Any

import requests

from mcp_pokedeals.cache import CacheJSON
from mcp_pokedeals.config import Config
from mcp_pokedeals.models import Card, CardSet

log = logging.getLogger("mcp_pokedeals.providers.tcgdex")

TIMEOUT = 15


class TCGdexError(Exception):
    """Erreur TCGdex avec un message clair, pense pour etre lu par une IA
    ou un humain -- jamais une traceback Python brute."""


class TCGdexProvider:
    def __init__(self, config: Config, cache: CacheJSON):
        self._base_url = config.tcgdex_base_url.rstrip("/")
        self._cache = cache
        self._ttl_cartes = config.cache_ttl_cartes
        self._ttl_sets = config.cache_ttl_sets

    def _requete(self, chemin: str, params: dict | None = None) -> Any:
        url = f"{self._base_url}{chemin}"
        try:
            rep = requests.get(url, params=params, timeout=TIMEOUT)
        except requests.exceptions.Timeout:
            raise TCGdexError(f"TCGdex indisponible : delai depasse ({TIMEOUT}s) sur {url}")
        except requests.exceptions.RequestException as e:
            raise TCGdexError(f"TCGdex injoignable : {e}")

        if rep.status_code == 404:
            raise TCGdexError(f"TCGdex : ressource introuvable (HTTP 404) sur {url}")
        if rep.status_code == 429:
            raise TCGdexError("TCGdex : limite de requetes atteinte (HTTP 429), reessaie plus tard")
        if rep.status_code >= 500:
            raise TCGdexError(f"TCGdex : erreur serveur (HTTP {rep.status_code}), reessaie plus tard")
        if rep.status_code != 200:
            raise TCGdexError(f"TCGdex : reponse inattendue (HTTP {rep.status_code}) sur {url}")

        try:
            return rep.json()
        except ValueError:
            raise TCGdexError(f"TCGdex : reponse illisible (pas du JSON valide) sur {url}")

    # ------------------------------------------------------------------
    # Cartes
    # ------------------------------------------------------------------

    def obtenir_carte(self, id_carte: str, langue: str = "en") -> Card:
        cle_cache = f"carte:{langue}:{id_carte}"
        valeur_cache = self._cache.get(cle_cache, self._ttl_cartes)
        if valeur_cache is not None:
            return Card(**valeur_cache)

        data = self._requete(f"/{langue}/cards/{id_carte}")
        carte = self._carte_depuis_json(data, langue)
        self._cache.set(cle_cache, carte.to_dict())
        return carte

    def rechercher_cartes(
        self,
        nom: str | None = None,
        numero: str | None = None,
        set_id: str | None = None,
        rarete: str | None = None,
        langue: str = "en",
        limite: int = 20,
    ) -> list[Card]:
        """Recherche par substring insensible a la casse sur le nom (comportement
        par defaut de l'API TCGdex -- pas besoin d'ajouter des jokers "*")."""
        params: dict[str, str] = {}
        if nom:
            params["name"] = nom
        if numero:
            params["localId"] = numero
        if set_id:
            params["set.id"] = set_id
        if rarete:
            params["rarity"] = rarete

        data = self._requete(f"/{langue}/cards", params=params)
        if not isinstance(data, list):
            raise TCGdexError("TCGdex : reponse de recherche de cartes inattendue (pas une liste)")

        limite_reelle = max(1, min(limite, 100))
        return [self._carte_brief_depuis_json(item, langue) for item in data[:limite_reelle]]

    def _carte_depuis_json(self, d: dict, langue: str) -> Card:
        set_info = d.get("set") or {}
        pricing = ((d.get("pricing") or {}).get("cardmarket")) or {}
        return Card(
            id=d.get("id", ""),
            name=d.get("name", ""),
            local_id=d.get("localId"),
            set_id=set_info.get("id"),
            set_name=set_info.get("name"),
            # La structure exacte de la "serie" dans l'objet set EMBARQUE sur
            # une carte n'a pas pu etre verifiee (acces doc bloque) -- utilise
            # search_set()/get_set_cards() pour la serie complete d'un set.
            series=None,
            rarity=d.get("rarity"),
            category=d.get("category"),
            types=d.get("types") or [],
            hp=d.get("hp"),
            illustrator=d.get("illustrator"),
            # URL de base sans extension : ajouter "/high.webp" ou "/low.png"
            # (convention TCGdex, voir https://tcgdex.dev/reference/card).
            image_url=d.get("image"),
            language=langue,
            source="tcgdex",
        )
        # Note : `pricing` (prix Cardmarket deja integres par TCGdex) est
        # disponible sur la reponse brute mais volontairement pas copie dans
        # Card -- cf. services/prices.py, qui garde chaque source de prix
        # bien separee plutot que de la fusionner dans les infos carte.

    def _carte_brief_depuis_json(self, d: dict, langue: str) -> Card:
        # Les resultats de recherche TCGdex sont des objets "CardBrief"
        # (moins de champs que la fiche complete) -- get_card() donne le
        # detail complet ensuite.
        return Card(
            id=d.get("id", ""),
            name=d.get("name", ""),
            local_id=d.get("localId"),
            image_url=d.get("image"),
            language=langue,
            source="tcgdex",
        )

    # ------------------------------------------------------------------
    # Sets (extensions)
    # ------------------------------------------------------------------

    def obtenir_set(self, id_set: str, langue: str = "en") -> CardSet:
        cle_cache = f"set:{langue}:{id_set}"
        valeur_cache = self._cache.get(cle_cache, self._ttl_sets)
        if valeur_cache is not None:
            return CardSet(**valeur_cache)

        data = self._requete(f"/{langue}/sets/{id_set}")
        jeu = self._set_depuis_json(data)
        self._cache.set(cle_cache, jeu.to_dict())
        return jeu

    def rechercher_sets(
        self, nom: str | None = None, serie: str | None = None, langue: str = "en"
    ) -> list[CardSet]:
        params: dict[str, str] = {}
        if nom:
            params["name"] = nom
        if serie:
            params["serie.id"] = serie

        data = self._requete(f"/{langue}/sets", params=params)
        if not isinstance(data, list):
            raise TCGdexError("TCGdex : reponse de recherche de sets inattendue (pas une liste)")
        return [self._set_depuis_json(item) for item in data]

    def obtenir_cartes_du_set(
        self, id_set: str, langue: str = "en", page: int = 1, par_page: int = 25
    ) -> list[Card]:
        """Pagine COTE CLIENT : TCGdex renvoie la liste complete des cartes
        d'un set (generalement <300), on la decoupe nous-memes pour eviter
        une reponse gigantesque a l'appelant MCP."""
        data = self._requete(f"/{langue}/sets/{id_set}")
        if not isinstance(data, dict):
            raise TCGdexError(f"TCGdex : set introuvable ou reponse inattendue pour '{id_set}'")

        cartes = data.get("cards") or []
        debut = max(0, (page - 1) * max(1, par_page))
        fin = debut + max(1, par_page)
        return [self._carte_brief_depuis_json(c, langue) for c in cartes[debut:fin]]

    def _set_depuis_json(self, d: dict) -> CardSet:
        card_count = d.get("cardCount") or {}
        serie = d.get("serie") or {}
        return CardSet(
            id=d.get("id", ""),
            name=d.get("name", ""),
            series=serie.get("name") if isinstance(serie, dict) else None,
            release_date=d.get("releaseDate"),
            card_count_official=card_count.get("official"),
            card_count_total=card_count.get("total"),
            logo_url=d.get("logo"),
            source="tcgdex",
        )
