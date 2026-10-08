"""
Connecteur Lidl (lidl.fr), ajoute le 08/10/2026 (demande de Justok :
scanner un maximum de magasins pour les produits des 30 ans, sans plafond
de prix). Lidl vend ponctuellement des produits Pokemon TCG en ligne.

L'API de recherche du site est publique et renvoie du JSON (verifie le
08/10/2026) :
  https://www.lidl.fr/q/api/search?q=...&assortment=FR&locale=fr_FR&version=v2.0.0
  items[].gridbox.data : fullTitle, canonicalPath, price.price,
  stockAvailability.onlineAvailable (bool).
La recherche est tres permissive (poeles et pyjamas pour "pokemon") : le
filtre edition + type de radar_precommandes fait le tri.

Politesse : une seule "boutique", quelques recherches par cycle, pause
DELAI_ENTRE_REQUETES entre deux requetes, une seule session HTTP.
"""
from __future__ import annotations

import time
from urllib.parse import urljoin

import requests

from connecteur_shopify import HEADERS_HTML, TIMEOUT

DOMAINE = "lidl.fr"
BASE = "https://www.lidl.fr"
API = f"{BASE}/q/api/search"
DELAI_ENTRE_REQUETES = 1.0
TAILLE_PAGE = 100   # "pokemon" : ~50 articles le 08/10/2026, une seule page


def analyser_recherche(donnees: dict) -> list[dict]:
    """[{titre, url, en_stock, prix}] depuis la reponse JSON de l'API."""
    resultats = []
    for item in (donnees or {}).get("items") or []:
        d = ((item or {}).get("gridbox") or {}).get("data") or {}
        titre = (d.get("fullTitle") or d.get("title") or "").strip()
        chemin = d.get("canonicalPath") or d.get("canonicalUrl")
        if not titre or not chemin:
            continue
        stock = d.get("stockAvailability") or {}
        try:
            prix = float((d.get("price") or {}).get("price"))
        except (TypeError, ValueError):
            prix = None
        resultats.append({
            "titre": titre,
            "url": urljoin(BASE, chemin),
            "en_stock": bool(stock.get("onlineAvailable")) and not d.get("preventSelling"),
            "prix": prix,
        })
    return resultats


class ConnecteurLidl:
    def __init__(self):
        self.session = requests.Session()
        self._derniere_requete = 0.0

    def rechercher(self, requete: str) -> list[dict]:
        attente = DELAI_ENTRE_REQUETES - (time.monotonic() - self._derniere_requete)
        if attente > 0:
            time.sleep(attente)
        params = {"q": requete, "assortment": "FR", "locale": "fr_FR",
                  "version": "v2.0.0", "fetchsize": TAILLE_PAGE}
        try:
            r = self.session.get(API, params=params, headers={**HEADERS_HTML, "Accept": "application/json"}, timeout=TIMEOUT)
        finally:
            self._derniere_requete = time.monotonic()
        r.raise_for_status()
        return analyser_recherche(r.json())
