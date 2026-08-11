"""
Scanners par plateforme pour le radar de precommandes (cf.
precommandes_watchlist.py / alerte_precommande.py) -- fonctionnalite
INDEPENDANTE des scans existants (scan_boutique.py / scan_boutique_prestashop.py /
scan_boutique_woocommerce.py), qu'elle ne modifie ni n'appelle.

Reutilise les CONNECTEURS existants (Shopify catalogue complet, PrestaShop/
WooCommerce sitemap + replis recherche HTML/API REST deja en place) sans
les modifier -- seule la logique de MATCHING differe (mots-cles libres +
date, cf. precommandes_watchlist.py, au lieu de nom+numero de carte).

Strategie par plateforme :
  - Shopify : le catalogue complet (deja recupere par /products.json) donne
    directement titre ET description (body_html) de chaque produit -- pas
    de requete supplementaire necessaire.
  - PrestaShop/WooCommerce (sitemap) : filtrage LEGER sur le slug de
    chaque URL (mots-cles TYPE seulement -- "etb"/"upc"/personnage --
    plus discriminant qu'un mot d'edition generique comme "anniversaire",
    limite le nombre de pages a recuperer) avant de charger la page
    complete (titre + texte) pour la verification finale (mots-cles
    edition+type ET date).
  - PrestaShop/WooCommerce (repli recherche HTML/API REST, boutiques sans
    sitemap) : une recherche par mot-cle "type" (ETB, UPC, mentali...) via
    le mecanisme de decouverte deja existant, meme filtrage final.
"""

import os
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from connecteur_shopify import HEADERS_HTML, TIMEOUT
from connecteur_prestashop_sitemap import ConnecteurPrestaShopSitemap
from connecteur_woocommerce import ConnecteurWooCommerce
from precommandes_watchlist import ProduitSurveille, evaluer_correspondance

import requests

DELAI_ENTRE_PAGES = 0.5


def _horodatage() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _normaliser_slug(texte: str) -> str:
    sans_accents = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", sans_accents.lower()).strip()


# Extensions d'assets (images, feuilles de style...) presentes dans
# certains sitemaps PrestaShop/WooCommerce combines (sitemap produit +
# sitemap images) -- jamais des pages produit, a exclure du prefiltre
# AVANT tout, sinon chaque candidat image compte pour une requete gaspillee.
_EXTENSIONS_MEDIA = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".ico", ".css", ".js")


def _slug_est_candidat(url: str, produit: ProduitSurveille) -> bool:
    """Prefiltre LEGER (pas de requete reseau) : le slug de l'URL contient
    au moins un mot-cle du groupe EDITION *ET* au moins un du groupe TYPE
    (meme double exigence que evaluer_correspondance, appliquee tot pour
    limiter le nombre de pages recuperees).

    Bug reel corrige le 11/08/2026 : un premier prefiltre ne verifiait que
    le groupe TYPE ("etb"/"upc"/nom de personnage), des mots bien trop
    courants (N'IMPORTE QUEL set a un ETB) -- sur
    blazingtail.fr seul, ca remontait 251 candidats (dont des URLs
    d'IMAGES .jpg, jamais filtrees), chacun necessitant une requete +
    delai de politesse -> timeout du job GitHub Actions (25-30 min
    depasses). Exiger les DEUX groupes des le prefiltre (comme le fait
    deja evaluer_correspondance sur le texte complet de la page) reduit
    drastiquement le nombre de pages a recuperer, sans perte de rappel
    constatee : les vrais matches trouves jusqu'ici (Shopify) contenaient
    tous les deux groupes dans leur slug/titre (ex "elite-trainer-box-30th-
    celebration-francais", "etb-pokemon-me06-regne-delta-francais")."""
    if url.lower().endswith(_EXTENSIONS_MEDIA):
        return False
    slug_norm = _normaliser_slug(url)
    a_edition = any(_normaliser_slug(mot) in slug_norm for mot in produit.mots_cles_edition)
    a_type = any(_normaliser_slug(mot) in slug_norm for mot in produit.mots_cles_type)
    return a_edition and a_type


def _candidat(domaine, produit, titre, texte_desc, url, prix=None, en_stock=None):
    confiance, raison = evaluer_correspondance(titre, texte_desc, produit)
    if confiance is None:
        return None
    return {
        "domaine": domaine,
        "nom_produit": produit.nom,
        "confiance": confiance,
        "raison": raison,
        "titre": titre,
        "url_produit": url,
        "prix": prix,
        "en_stock": en_stock,
        "horodatage": _horodatage(),
    }


# --- Shopify : catalogue complet deja recupere, aucune requete supplementaire ---

def scanner_shopify(domaine: str, produits: list[ProduitSurveille], connecteur=None) -> list[dict]:
    from connecteur_shopify import ConnecteurShopify
    connecteur = connecteur or ConnecteurShopify(domaine)
    catalogue = connecteur.recuperer_tout_le_catalogue()

    candidats = []
    for p in catalogue:
        titre = p.get("title", "")
        description = re.sub(r"<[^>]+>", " ", p.get("body_html") or "")
        handle = p.get("handle", "")
        url = f"{connecteur.base_url}/products/{handle}"
        prix = None
        en_stock = None
        variants = p.get("variants") or []
        if variants:
            try:
                prix = float(variants[0].get("price"))
            except (TypeError, ValueError):
                pass
            en_stock = any(v.get("available") for v in variants)

        for produit in produits:
            c = _candidat(domaine, produit, titre, description, url, prix, en_stock)
            if c:
                candidats.append(c)

    return candidats


# --- PrestaShop : sitemap (prefiltre slug) + repli recherche HTML (par mot-cle type) ---

def _evaluer_page_prestashop(connecteur: ConnecteurPrestaShopSitemap, url: str, produits: list[ProduitSurveille]) -> list[dict]:
    try:
        r = connecteur.session.get(url, headers=HEADERS_HTML, timeout=TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.RequestException:
        return []
    finally:
        time.sleep(DELAI_ENTRE_PAGES)

    html = r.content.decode("utf-8", errors="replace")
    m_titre = re.search(r"<title[^>]*>([^<]*)</title>", html, re.IGNORECASE)
    titre = m_titre.group(1).strip() if m_titre else ""
    texte = re.sub(r"<[^>]+>", " ", html)[:5000]  # texte brut, suffisant pour mots-cles + date

    candidats = []
    for produit in produits:
        c = _candidat(connecteur.nom_affiche, produit, titre, texte, url)
        if c:
            candidats.append(c)
    return candidats


def scanner_prestashop_sitemap(domaine: str, produits: list[ProduitSurveille]) -> list[dict]:
    connecteur = ConnecteurPrestaShopSitemap(domaine)
    urls = connecteur.recuperer_toutes_les_urls_produits()

    candidats_urls = {
        u for u in urls
        if any(_slug_est_candidat(u, p) for p in produits)
    }

    resultats = []
    for url in candidats_urls:
        resultats.extend(_evaluer_page_prestashop(connecteur, url, produits))
    return resultats


def scanner_prestashop_repli_html(domaine: str, produits: list[ProduitSurveille]) -> list[dict]:
    connecteur = ConnecteurPrestaShopSitemap(domaine)
    urls_vues = set()
    for produit in produits:
        for mot in produit.mots_cles_type:
            urls_vues.update(connecteur._decouvrir_candidats_recherche(mot))
            time.sleep(DELAI_ENTRE_PAGES)

    resultats = []
    for url in urls_vues:
        resultats.extend(_evaluer_page_prestashop(connecteur, url, produits))
    return resultats


# --- WooCommerce : sitemap (prefiltre slug) + repli recherche HTML / API REST ---

def _evaluer_page_woocommerce(connecteur: ConnecteurWooCommerce, url: str, produits: list[ProduitSurveille]) -> list[dict]:
    try:
        r = connecteur.session.get(url, headers=HEADERS_HTML, timeout=TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.RequestException:
        return []
    finally:
        time.sleep(DELAI_ENTRE_PAGES)

    html = r.content.decode("utf-8", errors="replace")
    m_titre = re.search(r"<title[^>]*>([^<]*)</title>", html, re.IGNORECASE)
    titre = m_titre.group(1).strip() if m_titre else ""
    texte = re.sub(r"<[^>]+>", " ", html)[:5000]

    candidats = []
    for produit in produits:
        c = _candidat(connecteur.nom_affiche, produit, titre, texte, url)
        if c:
            candidats.append(c)
    return candidats


def scanner_woocommerce_sitemap(domaine: str, produits: list[ProduitSurveille]) -> list[dict]:
    connecteur = ConnecteurWooCommerce(domaine)
    urls = connecteur.recuperer_toutes_les_urls_produits()

    candidats_urls = {
        u for u in urls
        if any(_slug_est_candidat(u, p) for p in produits)
    }

    resultats = []
    for url in candidats_urls:
        resultats.extend(_evaluer_page_woocommerce(connecteur, url, produits))
    return resultats


def scanner_woocommerce_repli_html(domaine: str, produits: list[ProduitSurveille]) -> list[dict]:
    connecteur = ConnecteurWooCommerce(domaine)
    urls_vues = set()
    for produit in produits:
        for mot in produit.mots_cles_type:
            urls_vues.update(connecteur._decouvrir_candidats_recherche(mot))
            time.sleep(DELAI_ENTRE_PAGES)

    resultats = []
    for url in urls_vues:
        resultats.extend(_evaluer_page_woocommerce(connecteur, url, produits))
    return resultats


def scanner_woocommerce_api_rest(domaine: str, produits: list[ProduitSurveille]) -> list[dict]:
    connecteur = ConnecteurWooCommerce(domaine)
    candidats = []
    vus_ids = set()
    for produit in produits:
        for mot in produit.mots_cles_type:
            for p in connecteur._decouvrir_produits_api_rest(mot):
                if p.get("id") in vus_ids:
                    continue
                vus_ids.add(p.get("id"))
                titre = p.get("name", "")
                description = re.sub(r"<[^>]+>", " ", p.get("description") or p.get("short_description") or "")
                url = p.get("permalink", "")
                prix = None
                try:
                    unite_min = int((p.get("prices") or {}).get("currency_minor_unit", 2))
                    prix = float(p["prices"]["price"]) / (10 ** unite_min)
                except (KeyError, TypeError, ValueError):
                    pass
                c = _candidat(domaine, produit, titre, description, url, prix, p.get("is_in_stock"))
                if c:
                    candidats.append(c)
            time.sleep(DELAI_ENTRE_PAGES)
    return candidats
