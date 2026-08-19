"""
Fournisseur CardDex (https://carddex.dev) : prix, tendances.

STATUT : integration NON VERIFIEE en conditions reelles. L'acces web etait
bloque pendant le developpement de ce module (voir mcp_pokedeals/README.md,
section "Statut des sources") -- CARDDEX_BASE_URL par defaut est une
DEDUCTION a partir de la documentation publique, PAS une valeur confirmee.

Avant la premiere utilisation :
  1. Va sur https://carddex.dev/ et verifie l'URL de base exacte de l'API
     ainsi que le chemin/les parametres de l'endpoint de recherche/prix.
  2. Si CARDDEX_BASE_URL par defaut ne fonctionne pas (erreur "route
     introuvable" ci-dessous), corrige-la dans ton .env -- aucune
     modification de code necessaire.

Cle API : optionnelle. Sans cle, un jeu de donnees public est accessible
(limite de requetes non precisee). Avec une cle gratuite (header
"X-API-Key", format "pk_live_..."), la limite annoncee monte a 100
requetes/minute (a confirmer sur ton propre compte CardDex).
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

import requests

from mcp_pokedeals.cache import CacheJSON
from mcp_pokedeals.config import Config
from mcp_pokedeals.models import PriceResult

log = logging.getLogger("mcp_pokedeals.providers.carddex")

TIMEOUT = 15


class CardDexError(Exception):
    """Erreur CardDex avec un message clair. Un HTTP 404 sur une route
    "/cards/..." est probablement le signe que CARDDEX_BASE_URL (ou le
    chemin de l'endpoint) doit etre corrige -- voir le statut en tete de
    ce fichier."""


class CardDexProvider:
    def __init__(self, config: Config, cache: CacheJSON):
        self._base_url = config.carddex_base_url.rstrip("/")
        self._api_key = config.carddex_api_key
        self._cache = cache
        self._ttl_prix = config.cache_ttl_prix

    def _entetes(self) -> dict:
        if self._api_key:
            return {"X-API-Key": self._api_key}
        return {}

    def _requete(self, chemin: str, params: dict | None = None) -> Any:
        url = f"{self._base_url}{chemin}"
        try:
            rep = requests.get(url, params=params, headers=self._entetes(), timeout=TIMEOUT)
        except requests.exceptions.Timeout:
            raise CardDexError(f"CardDex indisponible : delai depasse ({TIMEOUT}s) sur {url}")
        except requests.exceptions.RequestException as e:
            raise CardDexError(f"CardDex injoignable : {e}")

        if rep.status_code == 401:
            raise CardDexError("CardDex : cle API invalide (HTTP 401) -- verifie CARDDEX_API_KEY")
        if rep.status_code == 404:
            raise CardDexError(
                f"CardDex : route introuvable (HTTP 404) sur {url} -- l'URL de base ou le "
                "chemin de l'endpoint n'est peut-etre pas a jour, verifie CARDDEX_BASE_URL "
                "(voir le statut documente en tete de mcp_pokedeals/providers/carddex.py)"
            )
        if rep.status_code == 429:
            raise CardDexError("CardDex : limite de requetes atteinte (HTTP 429), reessaie plus tard")
        if rep.status_code >= 500:
            raise CardDexError(f"CardDex : erreur serveur (HTTP {rep.status_code}), reessaie plus tard")
        if rep.status_code != 200:
            raise CardDexError(f"CardDex : reponse inattendue (HTTP {rep.status_code}) sur {url}")

        try:
            return rep.json()
        except ValueError:
            raise CardDexError(f"CardDex : reponse illisible (pas du JSON valide) sur {url}")

    def obtenir_prix(self, card_id: str) -> list[PriceResult]:
        cle_cache = f"prix:{card_id}"
        valeur_cache = self._cache.get(cle_cache, self._ttl_prix)
        if valeur_cache is not None:
            return [PriceResult(**p) for p in valeur_cache]

        data = self._requete(f"/cards/{card_id}")
        carte = data.get("data", data) if isinstance(data, dict) else {}
        prix_bruts = (carte or {}).get("prices") or {}

        if prix_bruts.get("trend") is None:
            raise CardDexError(f"CardDex : aucun prix disponible pour la carte '{card_id}'")

        # Devise non confirmee explicitement dans la reponse (a verifier) --
        # deduite a USD par defaut si absente, avec une note transparente.
        devise = prix_bruts.get("currency") or carte.get("currency")
        note = None
        if not devise:
            devise = "USD"
            note = "Devise non confirmee dans la reponse CardDex : USD suppose par defaut, a verifier"

        resultat = PriceResult(
            card_id=card_id,
            source="carddex",
            currency=devise,
            price=float(prix_bruts["trend"]),
            price_type="trend",
            retrieved_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            trend=prix_bruts.get("avg_7d"),
            note=note,
        )
        self._cache.set(cle_cache, [resultat.to_dict()])
        return [resultat]
