"""
Connecteur DEDIE a philibertnet.com -- boutique de reference (revendeur
generaliste jeux/figurines/TCG, confirmee legitime par Justok le
24/08/2026), mais son ampleur (457 641 produits au total sur son sitemap,
verifie le 24/08/2026) la rend incompatible avec la strategie generique de
connecteur_prestashop_sitemap.py, qui filtre les URLs par NOM+NUMERO de
carte -- ici on cherche des produits SCELLES sans numero connu a l'avance,
et visiter 457k pages une a une n'est pas envisageable.

Sa page categorie Pokemon (/fr/212-pokemon) charge ses produits via
JavaScript (verifie le 24/08/2026, cf. session avec Justok) -- pas de HTML
brut scrapable, contrairement aux autres boutiques PrestaShop du projet.

Strategie retenue (2 etapes, cout reseau maitrise) :
  1. Sitemap XML classique (reutilise ConnecteurPrestaShopSitemap, qui EST
     scrapable -- c'est juste la page categorie qui ne l'est pas) : filtre
     LOCAL (en memoire, sans requete reseau supplementaire) des URLs sur le
     mot-cle "pokemon" -- ~938 URLs sur 457 641 au moment de la verification
     du 24/08/2026.
  2. Visite individuelle de CHAQUE url filtree (necessaire : le sitemap ne
     donne que l'URL, jamais le titre ni la disponibilite) pour en extraire
     titre/description/stock (JSON-LD puis repli microdata, EXACTEMENT
     comme connecteur_prestashop_sitemap.py), puis application des memes
     criteres que le radar generique (precommande_generique.py) : mention
     Pokemon + precommande (FR) + type de produit scelle + aucune autre
     franchise.

Cout reseau reel : ~940 requetes par cycle (1 sitemap + ~938 pages
produit filtrees) -- nettement plus qu'une boutique normale (dizaines de
produits), d'ou un WORKFLOW SEPARE avec sa propre cadence (moins frequente,
cf. scan_precommandes_philibert.yml) et son propre budget de temps, pour ne
jamais entamer la marge des autres workflows de scan.
"""
from __future__ import annotations

import time
from datetime import datetime, timezone

import requests

from connecteur_prestashop_sitemap import (
    ConnecteurPrestaShopSitemap,
    _extraire_jsonld_produit,
    _extraire_microdata_produit,
    _stock_indisponible_selon_dom,
)
from connecteur_shopify import HEADERS_HTML, TIMEOUT
from precommande_generique import determiner_categorie_produit, produit_est_candidat_precommande

DOMAINE = "philibertnet.com"
DELAI_ENTRE_PAGES_PRODUIT = 0.3  # politesse -- ~940 requetes sur un site tiers, jamais en rafale


def _horodatage() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def lister_urls_pokemon_sitemap(connecteur: ConnecteurPrestaShopSitemap | None = None) -> list[str]:
    """Sitemap XML complet, filtre LOCALEMENT (aucune requete reseau
    supplementaire au-dela du sitemap lui-meme) sur le mot-cle "pokemon"
    dans l'URL -- meme heuristique grossiere que le repli WooCommerce de
    decouverte_boutiques.py (slug d'URL, pas de titre exploitable sans
    visiter chaque page)."""
    connecteur = connecteur or ConnecteurPrestaShopSitemap(DOMAINE)
    sitemaps = connecteur._decouvrir_sitemaps_racine()
    urls: list[str] = []
    for sm in sitemaps:
        urls.extend(connecteur._lister_urls_recursif(sm))
    return [u for u in urls if "pokemon" in u.lower()]


def _extraire_produit(url: str) -> dict | None:
    """Recupere une page produit et en extrait titre/description/stock.
    None si la page est inaccessible ou sans donnees structurees
    exploitables (JSON-LD Product ni microdata) -- ignoree, jamais une
    exception qui interromprait le cycle complet."""
    try:
        r = requests.get(url, headers=HEADERS_HTML, timeout=TIMEOUT)
        if r.status_code != 200:
            return None
        html = r.text
    except requests.exceptions.RequestException:
        return None

    jsonld = _extraire_jsonld_produit(html)
    if jsonld is not None:
        offres = jsonld.get("offers")
        if isinstance(offres, list):
            offres = offres[0] if offres else {}
        offres = offres if isinstance(offres, dict) else {}
        titre = jsonld.get("name", "") or ""
        description = jsonld.get("description", "") or ""
        en_stock = offres.get("availability", "") in (
            "https://schema.org/InStock", "https://schema.org/LimitedAvailability",
        )
        prix = offres.get("price")
    else:
        micro = _extraire_microdata_produit(html)
        if micro is None:
            return None
        titre = micro.get("titre", "")
        description = ""
        en_stock = micro.get("en_stock", False)
        prix = micro.get("prix")

    # Le signal RENDU (DOM) prime toujours sur le signal STRUCTURE
    # (microdata/JSON-LD) quand ils se contredisent -- meme piege deja
    # documente pour les autres boutiques PrestaShop (cf.
    # connecteur_prestashop_sitemap.py, investcollect.com).
    if _stock_indisponible_selon_dom(html):
        en_stock = False

    try:
        prix = float(prix) if prix is not None else None
    except (TypeError, ValueError):
        prix = None

    return {"titre": titre, "description": description, "en_stock": en_stock, "prix": prix}


def scanner_philibert_precommandes_generiques(
    urls: list[str] | None = None, connecteur: ConnecteurPrestaShopSitemap | None = None
) -> list[dict]:
    """Retourne les produits CANDIDATS a une precommande Pokemon TCG
    generique trouves parmi les URLs filtrees du sitemap philibertnet.com
    -- pas encore filtres contre la memoire (fait par
    detecter_nouvelles_precommandes_generiques, reutilisee telle quelle
    depuis radar_precommande_generique.py)."""
    urls = urls if urls is not None else lister_urls_pokemon_sitemap(connecteur)

    candidats = []
    for i, url in enumerate(urls):
        produit = _extraire_produit(url)
        if i < len(urls) - 1:
            time.sleep(DELAI_ENTRE_PAGES_PRODUIT)
        if produit is None:
            continue

        ok, raison = produit_est_candidat_precommande(produit["titre"], produit["description"])
        if not ok:
            continue

        candidats.append({
            "domaine": DOMAINE,
            "slug": url,  # cle memoire stable, pas de handle court cote PrestaShop
            "titre": produit["titre"],
            "url_produit": url,
            "prix": produit["prix"],
            "en_stock": produit["en_stock"],
            "raison": raison,
            "categorie": determiner_categorie_produit(produit["titre"], produit["description"]),
            "horodatage": _horodatage(),
        })
    return candidats
