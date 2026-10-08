"""
Connecteur Auchan (auchan.fr), ajoute le 08/10/2026 (demande de Justok :
scanner un maximum de magasins pour les produits des 30 ans, sans plafond
de prix).

Plateforme maison, mais la page de recherche est rendue cote serveur avec des
microdonnees schema.org sur chaque carte produit (verifie le 08/10/2026) :
  <article itemtype="http://schema.org/Product"> ... href=".../pr-XXXX" ...
  <source alt="TITRE"> ... itemprop="availability" content=".../InStock"
  itemprop="price" content="12.34"
Une carte peut porter PLUSIEURS offres (marketplace) : le produit est
commandable si au moins une est InStock/PreOrder ; prix = le plus bas d'entre
elles. Aucune fiche a charger : tout est sur la carte.

Politesse : une seule "boutique", quelques recherches par cycle, pause
DELAI_ENTRE_REQUETES entre deux requetes, une seule session HTTP.
"""
from __future__ import annotations

import html as html_module
import re
import time
from urllib.parse import quote, urljoin

import requests

from connecteur_leclerc import DISPONIBILITES_COMMANDABLES
from connecteur_shopify import HEADERS_HTML, TIMEOUT

DOMAINE = "auchan.fr"
BASE = "https://www.auchan.fr"
DELAI_ENTRE_REQUETES = 1.0

_RE_ARTICLE = re.compile(r'<article[^>]*itemtype="https?://schema.org/Product"[^>]*>(.*?)</article>', re.S)
_RE_LIEN = re.compile(r'href="(/[^"]+/pr-[^"]+)"')
_RE_TITRE = re.compile(r'<source alt="([^"]*)"|itemprop="name"[^>]*content="([^"]*)"')
_RE_DISPO = re.compile(r'itemprop="availability"[^>]*(?:content|href)="([^"]*)"')
_RE_PRIX = re.compile(r'itemprop="price"[^>]*content="([^"]*)"')


def analyser_recherche(page: str) -> list[dict]:
    """[{titre, url, en_stock, prix}] -- prix = plus bas parmi les offres
    commandables (sinon parmi toutes), None si aucun."""
    resultats = []
    for carte in _RE_ARTICLE.findall(page):
        lien, titre = _RE_LIEN.search(carte), _RE_TITRE.search(carte)
        if not lien or not titre:
            continue
        dispos = _RE_DISPO.findall(carte)
        prix_bruts = _RE_PRIX.findall(carte)
        offres = list(zip(dispos, prix_bruts)) if len(dispos) == len(prix_bruts) else [(d, None) for d in dispos]
        commandables = [p for d, p in offres if d in DISPONIBILITES_COMMANDABLES]
        prix = None
        for p in commandables or prix_bruts:
            try:
                v = float(p)
            except (TypeError, ValueError):
                continue
            prix = v if prix is None else min(prix, v)
        resultats.append({
            "titre": html_module.unescape(titre.group(1) or titre.group(2) or "").strip(),
            "url": urljoin(BASE, html_module.unescape(lien.group(1))),
            "en_stock": any(d in DISPONIBILITES_COMMANDABLES for d in dispos),
            "prix": prix,
        })
    return resultats


class ConnecteurAuchan:
    def __init__(self):
        self.session = requests.Session()
        self._derniere_requete = 0.0

    def rechercher(self, requete: str) -> list[dict]:
        attente = DELAI_ENTRE_REQUETES - (time.monotonic() - self._derniere_requete)
        if attente > 0:
            time.sleep(attente)
        try:
            r = self.session.get(f"{BASE}/recherche?text={quote(requete)}", headers=HEADERS_HTML, timeout=TIMEOUT)
        finally:
            self._derniere_requete = time.monotonic()
        r.raise_for_status()
        return analyser_recherche(r.content.decode("utf-8", errors="replace"))
