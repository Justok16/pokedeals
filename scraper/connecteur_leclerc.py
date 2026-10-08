"""
Connecteur E.Leclerc (e.leclerc), ajoute le 08/10/2026 a la demande de Justok
(alertes de disponibilite des produits des 30 ans, SANS plafond de prix).

Leclerc n'est ni Shopify, ni PrestaShop, ni WooCommerce : plateforme maison,
mais sa page de recherche est rendue cote serveur (HTML lisible sans
JavaScript), et chaque fiche produit expose un bloc JSON-LD "Product"
(prix, disponibilite, description). Verifie le 08/10/2026 :
  - recherche : https://www.e.leclerc/recherche?q=... -> une balise
    <article data-product-card> par produit, avec data-offer-id (numerique
    = une offre active ; vide ou "o-..." = aucune offre en vente) et un
    lien titre `data-product-card-title` ;
  - fiche : <script type="application/ld+json"> de type Product, "offers"
    avec "availability" (schema.org InStock / PreOrder...).

Leclerc est une MARKETPLACE : une offre peut venir d'un revendeur tiers a
prix gonfle. Choix explicite de Justok (08/10/2026) : aucun plafond de prix,
toute offre disponible doit alerter. Le vendeur et le prix sont donc
remontes tels quels dans l'alerte, pour qu'il juge lui-meme.

Politesse : une seule "boutique", quelques recherches par cycle, pause
DELAI_ENTRE_REQUETES entre deux requetes, une seule session HTTP.
"""
from __future__ import annotations

import html as html_module
import json
import re
import time
from urllib.parse import quote, urljoin

import requests

from connecteur_shopify import HEADERS_HTML, TIMEOUT

DOMAINE = "e.leclerc"
BASE = "https://www.e.leclerc"
DELAI_ENTRE_REQUETES = 1.0

DISPONIBILITES_COMMANDABLES = {
    "https://schema.org/InStock", "http://schema.org/InStock",
    "https://schema.org/PreOrder", "http://schema.org/PreOrder",
    "https://schema.org/LimitedAvailability", "http://schema.org/LimitedAvailability",
}

_RE_ARTICLE = re.compile(r"<article([^>]*data-product-card[^>]*)>(.*?)</article>", re.S)
_RE_OFFRE = re.compile(r'data-offer-id="([^"]*)"')
_RE_TITRE = re.compile(r'<a[^>]*href="([^"]+)"[^>]*data-product-card-title[^>]*title="([^"]*)"', re.S)
_RE_TITRE_INVERSE = re.compile(r'<a[^>]*data-product-card-title[^>]*title="([^"]*)"[^>]*href="([^"]+)"', re.S)
_RE_JSONLD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def analyser_recherche(page: str) -> list[dict]:
    """Resultats d'une page de recherche : [{titre, url, offre_active}]."""
    resultats = []
    for attrs, corps in _RE_ARTICLE.findall(page):
        m = _RE_TITRE.search(corps)
        if m:
            url, titre = m.group(1), m.group(2)
        else:
            m = _RE_TITRE_INVERSE.search(corps)
            if not m:
                continue
            titre, url = m.group(1), m.group(2)
        offre = _RE_OFFRE.search(attrs)
        resultats.append({
            "titre": html_module.unescape(titre).strip(),
            "url": urljoin(BASE, html_module.unescape(url)),
            # Numerique = offre en vente ; vide/absent/"o-..." = aucune offre.
            "offre_active": bool(offre and offre.group(1).isdigit()),
        })
    return resultats


def analyser_fiche(page: str) -> dict | None:
    """Bloc JSON-LD Product d'une fiche : {titre, description, prix, en_stock}.
    None si absent ou illisible."""
    for brut in _RE_JSONLD.findall(page):
        try:
            donnees = json.loads(brut)
        except ValueError:
            continue
        for d in donnees if isinstance(donnees, list) else [donnees]:
            if not isinstance(d, dict) or d.get("@type") != "Product":
                continue
            offres = d.get("offers") or []
            offres = offres if isinstance(offres, list) else [offres]
            unitaires = [o for o in offres if isinstance(o, dict) and o.get("@type") == "Offer"]
            commandables = [o for o in unitaires if o.get("availability") in DISPONIBILITES_COMMANDABLES]
            prix = None
            for o in commandables or unitaires:
                try:
                    p = float(o.get("price"))
                except (TypeError, ValueError):
                    continue
                prix = p if prix is None else min(prix, p)
            return {
                "titre": html_module.unescape(d.get("name") or "").strip(),
                "description": html_module.unescape(d.get("description") or ""),
                "prix": prix,
                "en_stock": bool(commandables),
            }
    return None


class ConnecteurLeclerc:
    def __init__(self):
        self.session = requests.Session()
        self._derniere_requete = 0.0

    def _get(self, url: str) -> str:
        attente = DELAI_ENTRE_REQUETES - (time.monotonic() - self._derniere_requete)
        if attente > 0:
            time.sleep(attente)
        try:
            r = self.session.get(url, headers=HEADERS_HTML, timeout=TIMEOUT)
        finally:
            self._derniere_requete = time.monotonic()
        r.raise_for_status()
        # Leclerc n'annonce pas de charset : requests supposerait du latin-1
        # ("PokÃ©mon"). Les pages sont en UTF-8.
        return r.content.decode("utf-8", errors="replace")

    def rechercher(self, requete: str) -> list[dict]:
        return analyser_recherche(self._get(f"{BASE}/recherche?q={quote(requete)}"))

    def lire_fiche(self, url: str) -> dict | None:
        return analyser_fiche(self._get(url))
