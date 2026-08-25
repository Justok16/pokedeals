"""
Connecteur WooCommerce (strategie SITEMAP + double extraction) pour PokeDeals.

Meme squelette que connecteur_prestashop_sitemap.py : decouverte du
sitemap XML, filtrage des URLs candidates par nom+numero (slug normalise),
puis recuperation de chaque page candidate pour en extraire prix/devise/stock.

Deux differences constatees a l'inspection (3 boutiques de reference :
mgs-shop.fr, pokestock.fr, cardshunter.fr) :

  1. Sitemap : WooCommerce (via le plugin SEO, generalement Yoast) genere
     un index /sitemap_index.xml listant des sous-sitemaps nommes
     "product-sitemap.xml", "product-sitemap2.xml", etc. -- bien
     distincts des sous-sitemaps de taxonomie ("product_cat-sitemap.xml",
     "product_tag-sitemap.xml"...). Convention plus propre et plus
     uniforme que sur PrestaShop.

  2. JSON-LD : PAS garanti present partout, contrairement a l'hypothese de
     depart. mgs-shop.fr et pokestock.fr exposent un schema Product/Offer
     complet (via Yoast, souvent enveloppe dans un objet "@graph" -- prise
     en charge ici). cardshunter.fr n'expose AUCUN schema Product (juste
     WebPage/BreadcrumbList generiques) alors qu'il tourne bien sur
     WooCommerce -- d'ou un REPLI HTML sur les classes CSS natives de
     WooCommerce (pas du theme, du coeur du plugin, donc stables d'un site
     a l'autre) :
       - prix + symbole de devise : <span class="woocommerce-Price-amount">
         ... <bdi>12,34&nbsp;<span class="woocommerce-Price-currencySymbol">€</span>
       - stock : classe "instock" / "outofstock" / "onbackorder" sur le
         conteneur produit (<div class="product ... instock ...">)

Garde-fou devise identique a PrestaShop : un prix dont la devise n'est PAS
EUR (symbole OU code ISO) est marque confiance faible /
necessite_verification_manuelle=True plutot que converti.

Retourne la MEME structure que les deux autres connecteurs
(ResultatRecherche/CritereRecherche) -- bonne_affaire_shopify.py et
alerte_stock.py restent utilisables SANS AUCUNE MODIFICATION.
"""

import html as html_module
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from urllib.parse import quote

import requests

from connecteur_shopify import (
    HEADERS_HTML,
    TIMEOUT,
    CritereRecherche,
    ResultatRecherche,
    _est_xml_valide,
    _slug_correspond,
    _titre_correspond,
    detecter_etat,
    detecter_langue,
)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DELAI_ENTRE_PAGES_PRODUIT = 0.5
LIMITE_CANDIDATS_PAR_CRITERE = 15

CHEMINS_SITEMAP_CANDIDATS = ["/sitemap_index.xml", "/wp-sitemap.xml", "/sitemap.xml"]

# Un sous-sitemap est retenu s'il contient "product" (WooCommerce/Yoast ou
# sitemaps natifs WordPress) MAIS PAS un des suffixes de taxonomie
# ci-dessous (categories, tags, marques -- pas des pages produit).
SEGMENTS_TAXONOMIE_EXCLUS = (
    "product_cat", "product-cat", "product_tag", "product-tag",
    "product_brand", "product-brand", "product-category", "product_type",
)

SEGMENTS_URL_EXCLUS = (
    "/panier", "/mon-compte", "/checkout", "/cart", "/my-account",
    "/nous-contacter", "/contact",
)

# Segments a exclure des liens trouves sur une page de RESULTATS DE RECHERCHE
# (repli sans sitemap) -- plus larges que SEGMENTS_URL_EXCLUS car une page de
# recherche contient aussi des liens de nav/pagination/tri absents d'un sitemap.
SEGMENTS_RECHERCHE_EXCLUS = SEGMENTS_URL_EXCLUS + (
    "/page/", "/categorie-produit/", "/product-category/", "/product-tag/",
    "/wp-content/", "/wp-json/", "/wp-admin/", "?s=", "?add-to-cart=",
    ".css", ".js", ".jpg", ".jpeg", ".png", ".webp", ".svg", ".ico",
    "/feed/", "/feed", "xmlrpc.php", "/a-propos", "/about", "/professionnels",
    "/vendre-mes-cartes", "/blog/", "/faq", "/mentions-legales",
    "/conditions-generales", "/politique-de-confidentialite", "/livraison",
    "/cgv", "/nos-services",
)

DISPONIBILITES_JSONLD_EN_STOCK = {
    "https://schema.org/InStock",
    "https://schema.org/LimitedAvailability",
}

# Symbole -> code ISO, pour le repli HTML (JSON-LD donne deja le code ISO
# directement quand il est present).
SYMBOLES_DEVISE = {
    "€": "EUR",
    "$": "USD",
    "£": "GBP",
    "¥": "JPY",
}


# _normaliser_texte, _slug_correspond et _est_xml_valide sont partagees
# avec connecteur_prestashop_sitemap.py -- factorisees dans
# connecteur_shopify.py le 11/08/2026 (code strictement identique dans les
# deux fichiers avant ca).


def _est_racine_boutique(url: str) -> bool:
    """True si `url` est EXACTEMENT la page racine de la categorie boutique
    (ex. ".../boutique/"), jamais un vrai produit.

    Audit du 18/08/2026 : cette exclusion vivait auparavant dans
    SEGMENTS_URL_EXCLUS sous la forme du segment "/boutique/</loc>" -- cense
    filtrer la racine boutique quand elle apparait dans le sitemap, mais qui
    ne pouvait JAMAIS matcher : les URLs testees viennent soit du texte deja
    PARSE par ElementTree (`loc.text`, qui ne contient plus aucune balise
    XML), soit d'un `href="..."` extrait par regex -- aucune des deux ne
    contient jamais le texte litteral "</loc>". Un simple "/boutique/" en
    substring exclusion aurait ete pire : c'est aussi le PREFIXE commun a
    TOUTE vraie URL produit sous ce chemin (".../boutique/pikachu-151/"),
    qu'un simple `in` aurait exclue a tort dans son integralite -- d'ou cette
    verification par SUFFIXE EXACT, apres avoir retire un `/` de fin
    eventuel."""
    return url.rstrip("/").endswith("/boutique")


def _est_sous_sitemap_produit(url: str) -> bool:
    u = url.lower()
    if "product" not in u:
        return False
    return not any(seg in u for seg in SEGMENTS_TAXONOMIE_EXCLUS)


def _chercher_product_jsonld(noeud):
    """Cherche recursivement un objet {"@type": "Product", ...} dans un
    JSON-LD -- gere le cas ou le bloc est un dict simple, une liste de
    blocs, OU un dict avec une cle "@graph" (convention Yoast SEO)."""
    if isinstance(noeud, dict):
        if noeud.get("@type") == "Product":
            return noeud
        if "@graph" in noeud:
            return _chercher_product_jsonld(noeud["@graph"])
        return None
    if isinstance(noeud, list):
        for element in noeud:
            trouve = _chercher_product_jsonld(element)
            if trouve:
                return trouve
    return None


def _extraire_jsonld_produit(html: str) -> dict | None:
    for bloc in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        corps = re.sub(r"/\*\s*<!\[CDATA\[\s*\*/", "", bloc)
        corps = re.sub(r"/\*\s*\]\]>\s*\*/", "", corps)
        try:
            donnees = json.loads(corps)
        except (json.JSONDecodeError, ValueError):
            continue
        produit = _chercher_product_jsonld(donnees)
        if produit:
            return produit
    return None


def _analyser_offre_jsonld(produit_jsonld: dict) -> dict:
    offres = produit_jsonld.get("offers")
    if isinstance(offres, list):
        offres = offres[0] if offres else {}
    if not isinstance(offres, dict):
        offres = {}

    try:
        prix = float(offres.get("price"))
    except (TypeError, ValueError):
        prix = None

    return {
        "prix": prix,
        "devise": offres.get("priceCurrency"),
        "en_stock": offres.get("availability", "") in DISPONIBILITES_JSONLD_EN_STOCK,
    }


def _extraire_variations(html: str) -> list[dict]:
    """Extrait le tableau JSON data-product_variations d'une fiche produit
    WooCommerce variable (present des qu'une carte a un attribut "etat" --
    la quasi-totalite des fiches carte a l'unite sur WooCommerce, meme
    quand une SEULE condition est proposee). Retourne [] si absent/invalide."""
    m = re.search(r'data-product_variations="([^"]+)"', html)
    if not m:
        return []
    try:
        return json.loads(html_module.unescape(m.group(1)))
    except (json.JSONDecodeError, ValueError):
        return []


def _offre_depuis_variation(variation: dict) -> dict | None:
    """Convertit UNE entree du tableau data-product_variations en
    prix/stock, en lisant le "availability_html" (le VRAI statut affiche a
    l'utilisateur -- rendu cote serveur au chargement de la page) plutot
    que de se fier a un flag booleen separe qui peut etre desynchronise."""
    try:
        prix = float(variation.get("display_price"))
    except (TypeError, ValueError):
        return None
    dispo_html = (variation.get("availability_html") or "").lower()
    en_stock = "in-stock" in dispo_html and "out-of-stock" not in dispo_html
    return {"prix": prix, "en_stock": en_stock}


def _stock_indisponible_selon_dom(html: str) -> bool:
    """True si la classe CSS coeur WooCommerce (pas du theme -- rendue cote
    serveur par le plugin lui-meme, donc stable d'un site a l'autre) annonce
    explicitement outofstock/onbackorder sur le conteneur produit -- a
    utiliser pour FORCER en_stock=False meme si le JSON-LD/microdata annonce
    le contraire (jamais l'inverse : une classe "instock" ou absente ne
    prouve pas la disponibilite, juste l'absence d'un signal de rupture).

    Extrait le 25/08/2026 (bug reel : golden-poke.fr affichait une liste
    d'attente "Rejoindre la liste d'attente" -- pas de bouton ajouter au
    panier -- alors que le JSON-LD annoncait la precommande comme
    commandable) pour etre reutilisable par radar_precommandes.py, qui
    n'appliquait jusque-la QUE l'override DOM PrestaShop
    (_stock_indisponible_selon_dom de connecteur_prestashop_sitemap.py,
    cible un span id="product-availability" absent de toute page
    WooCommerce) meme sur les pages WooCommerce -- l'override ne pouvait
    donc jamais se declencher pour cette plateforme."""
    m = re.search(r'class="product[^"]*\b(instock|outofstock|onbackorder)\b[^"]*"', html)
    return bool(m and m.group(1) != "instock")


def _extraire_html_woocommerce(html: str) -> dict | None:
    """Repli quand aucun JSON-LD Product n'est trouve : lit directement les
    classes CSS natives de WooCommerce (coeur du plugin, pas du theme).

    IMPORTANT : on isole d'abord le bloc <p class="price">...</p> (prix de
    LA fiche produit elle-meme) avant d'y chercher le montant. Sans ca, un
    simple re.search sur "woocommerce-Price-amount" tombe sur le premier
    element du genre trouve sur la page -- qui peut etre un widget de
    comparaison/mini-panier affichant un "0,00€" de remplissage AVANT le
    vrai prix dans le HTML (constate sur cardshunter.fr : 2 faux "0,00€"
    precedent le vrai prix). Le template WooCommerce du produit unique
    utilise <p class="price">, celui des widgets/listes utilise <span
    class="price"> -- distinction fiable pour cibler le bon bloc."""
    m_bloc = re.search(r'<p class="price">(.*?)</p>', html, re.S)
    if not m_bloc:
        return None

    m_prix = re.search(
        r'woocommerce-Price-amount[^>]*>\s*<bdi>\s*([\d.,]+)\s*(?:&nbsp;|\s)*'
        r'<span class="woocommerce-Price-currencySymbol"[^>]*>([^<]+)</span>',
        m_bloc.group(1),
    )
    if not m_prix:
        return None

    prix_texte = m_prix.group(1).replace(",", ".").replace(" ", "")
    # Un prix a la fois un point ET une virgule dans le texte original
    # (ex: format "1.234,56") n'est pas gere ici -- cas rare pour des
    # cartes a l'unite, laisse tel quel (echec propre plutot que faux calcul).
    try:
        prix = float(prix_texte)
    except ValueError:
        return None

    symbole = html_module.unescape(m_prix.group(2).strip())  # ex: "&euro;" -> "€"
    devise = SYMBOLES_DEVISE.get(symbole)  # None si symbole inconnu -> traite comme non-EUR par prudence

    m_stock = re.search(r'class="product[^"]*\b(instock|outofstock|onbackorder)\b[^"]*"', html)
    en_stock = bool(m_stock and m_stock.group(1) == "instock")

    titre = ""
    m_titre = re.search(r'<h1[^>]*\bproduct_title\b[^>]*>(.*?)</h1>', html, re.S)
    if m_titre:
        titre = html_module.unescape(re.sub(r"<[^>]+>", "", m_titre.group(1))).strip()

    return {"prix": prix, "devise": devise, "en_stock": en_stock, "titre": titre}


class ConnecteurWooCommerce:
    """Connecteur WooCommerce generique base sur le sitemap XML, avec
    extraction JSON-LD prioritaire et repli sur les classes CSS natives
    WooCommerce si le JSON-LD Product est absent."""

    def __init__(self, domaine: str, nom_affiche: str | None = None):
        self.domaine = domaine.strip().rstrip("/")
        self.nom_affiche = nom_affiche or domaine
        self.base_url = f"https://{self.domaine}"
        self.session = requests.Session()

    def _decouvrir_sitemaps_racine(self) -> list[str]:
        try:
            r = self.session.get(f"{self.base_url}/robots.txt", headers=HEADERS_HTML, timeout=TIMEOUT)
            if r.status_code == 200:
                declares = re.findall(r"(?im)^sitemap:\s*(\S+)", r.text)
                declares = [u if u.startswith("http") else f"{self.base_url}{u}" for u in declares]
                if declares:
                    return declares
        except requests.exceptions.RequestException:
            pass

        for chemin in CHEMINS_SITEMAP_CANDIDATS:
            try:
                r = self.session.get(f"{self.base_url}{chemin}", headers=HEADERS_HTML, timeout=TIMEOUT)
                if r.status_code == 200 and _est_xml_valide(r.content):
                    return [r.url]
            except requests.exceptions.RequestException:
                continue
        return []

    def _lister_urls_recursif(self, sitemap_url: str, profondeur: int = 0, vus: set | None = None) -> list[str]:
        if vus is None:
            vus = set()
        if sitemap_url in vus or profondeur > 3:
            return []
        vus.add(sitemap_url)

        try:
            r = self.session.get(sitemap_url, headers=HEADERS_HTML, timeout=TIMEOUT)
            r.raise_for_status()
            if not _est_xml_valide(r.content):
                return []
            # .lstrip() : certains serveurs (constate sur pokemoms.fr) renvoient
            # une ligne vide AVANT la declaration <?xml ...?>, ce qui est invalide
            # au sens strict XML et fait echouer ElementTree ("XML or text
            # declaration not at start of entity") alors que le contenu est
            # par ailleurs exploitable.
            racine = ET.fromstring(r.content.lstrip())
        except (requests.exceptions.RequestException, ET.ParseError):
            return []

        tag = racine.tag.split("}")[-1]
        if tag == "sitemapindex":
            urls = []
            sous_sitemaps = [
                loc.text.strip() for loc in racine.iter()
                if loc.tag.split("}")[-1] == "loc" and loc.text
            ]
            # Au premier niveau (profondeur 0), ne descend QUE dans les
            # sous-sitemaps produits -- evite de recuperer les milliers
            # d'URLs de pages/categories/tags/articles inutiles.
            if profondeur == 0:
                candidats_produits = [u for u in sous_sitemaps if _est_sous_sitemap_produit(u)]
                sous_sitemaps = candidats_produits or sous_sitemaps
            for sous_url in sous_sitemaps:
                urls.extend(self._lister_urls_recursif(sous_url, profondeur + 1, vus))
            return urls
        if tag == "urlset":
            return [
                loc.text.strip() for loc in racine.iter()
                if loc.tag.split("}")[-1] == "loc" and loc.text
            ]
        return []

    def recuperer_toutes_les_urls_produits(self) -> list[str]:
        """Audit du 18/08/2026 (meme cause racine que connecteur_shopify.py
        et connecteur_prestashop_sitemap.py, cf. leurs commentaires) : un
        echec TOTAL de decouverte du sitemap renvoyait auparavant une liste
        vide, indiscernable d'un sitemap reellement vide -- fausses alertes
        📦 en consequence (alerte_stock.py). N'est appelee QUE pour les
        boutiques SANS repli_api_rest (cf. scan_boutique_woocommerce.py),
        donc une liste vide ici est TOUJOURS anormale. On leve seulement si
        le resultat AVANT filtre des segments exclus est vide -- un resultat
        vide APRES filtre (boutique fraichement enregistree) reste legitime."""
        racines = self._decouvrir_sitemaps_racine()
        toutes_urls: list[str] = []
        for racine in racines:
            toutes_urls.extend(self._lister_urls_recursif(racine))

        if not toutes_urls:
            raise RuntimeError(
                f"aucune URL produit recuperee pour {self.domaine} (sitemap introuvable ou en echec)"
            )

        toutes_urls = list(dict.fromkeys(toutes_urls))
        return [
            u for u in toutes_urls
            if not any(seg in u for seg in SEGMENTS_URL_EXCLUS) and not _est_racine_boutique(u)
        ]

    def _evaluer_url(
        self, url: str, nom: str, numero: str | None, confiance_base: str
    ) -> ResultatRecherche | None:
        """Recupere UNE page produit et en extrait un ResultatRecherche
        (JSON-LD prioritaire, repli HTML natif WooCommerce sinon). Factorise
        pour etre utilisee aussi bien par la strategie sitemap que par le
        repli recherche HTML (meme extraction, seule la decouverte differe)."""
        try:
            r = self.session.get(url, headers=HEADERS_HTML, timeout=TIMEOUT)
            r.raise_for_status()
        except requests.exceptions.RequestException:
            return None
        finally:
            time.sleep(DELAI_ENTRE_PAGES_PRODUIT)

        # Decodage UTF-8 explicite plutot que r.text : plusieurs boutiques
        # WordPress ne declarent pas le charset dans leur en-tete
        # Content-Type ("text/html" sans "; charset=..."), ce qui fait
        # retomber requests sur ISO-8859-1 par defaut (RFC 2616) alors que
        # le contenu reel est en UTF-8 -- constate sur mgs-shop.fr (titres
        # illisibles : "RÃ¨gne" au lieu de "Règne"). WordPress sert
        # quasi-systematiquement de l'UTF-8, donc on decode directement
        # plutot que de deviner.
        html = r.content.decode("utf-8", errors="replace")
        produit_jsonld = _extraire_jsonld_produit(html)
        if produit_jsonld is not None:
            offre = _analyser_offre_jsonld(produit_jsonld)
            titre = produit_jsonld.get("name", "")
            image = produit_jsonld.get("image")
            if isinstance(image, list):
                image = image[0] if image else None
        else:
            offre = _extraire_html_woocommerce(html)
            if offre is None:
                return None  # ni JSON-LD ni repli HTML exploitable -> ignore cette page
            titre = offre.get("titre", "")
            image = None

        if offre["prix"] is None:
            return None

        # Cross-validation via data-product_variations, present des qu'une
        # carte a un attribut "etat" (near-mint, excellent...) -- la quasi-
        # totalite des fiches carte a l'unite sur WooCommerce, meme avec une
        # SEULE condition proposee. Bug reel corrige : sur fuji-store.fr, le
        # JSON-LD annoncait "InStock" alors que l'UNIQUE variation portait
        # elle-meme "En rupture de stock" dans son availability_html (rendu
        # serveur, donc plus fiable qu'un schema JSON-LD potentiellement en
        # cache/perime). Avec une seule variation, pas d'ambiguite : on lui
        # fait confiance. Avec plusieurs, on ne peut pas savoir laquelle
        # correspond au prix capte -> confiance abaissee plutot que de deviner.
        variations = _extraire_variations(html)
        ambigu_plusieurs_variations = False
        if len(variations) == 1:
            offre_variation = _offre_depuis_variation(variations[0])
            if offre_variation is not None:
                offre["en_stock"] = offre_variation["en_stock"]
        elif len(variations) > 1:
            ambigu_plusieurs_variations = True

        devise = (offre["devise"] or "").upper()
        devise_ok = devise == "EUR"
        confiance = confiance_base if (devise_ok and not ambigu_plusieurs_variations) else "faible"
        necessite_verif = (numero is None) or not devise_ok or ambigu_plusieurs_variations

        return ResultatRecherche(
            boutique=self.nom_affiche,
            titre=titre or url,
            prix=offre["prix"],
            en_stock=offre["en_stock"],
            url_produit=url,
            variante_titre="",
            image_url=image,
            langue_detectee=detecter_langue(titre or ""),
            confiance=confiance,
            necessite_verification_manuelle=necessite_verif,
            etat_detecte=detecter_etat(html),
        )

    def rechercher_dans_catalogue(
        self, urls_produits: list[str], criteres: list[tuple[str, str | None]]
    ) -> dict[tuple[str, str | None], list[ResultatRecherche]]:
        resultats_par_critere: dict[tuple[str, str | None], list[ResultatRecherche]] = {
            (nom, numero): [] for nom, numero in criteres
        }

        for nom, numero in criteres:
            critere = CritereRecherche(nom=nom, numero=numero)
            confiance_base = "forte" if numero is not None else "faible"

            candidats = [u for u in urls_produits if _slug_correspond(u, critere)]
            if len(candidats) > LIMITE_CANDIDATS_PAR_CRITERE:
                candidats = candidats[:LIMITE_CANDIDATS_PAR_CRITERE]

            for url in candidats:
                resultat = self._evaluer_url(url, nom, numero, confiance_base)
                if resultat:
                    resultats_par_critere[(nom, numero)].append(resultat)

        return resultats_par_critere

    def _decouvrir_candidats_recherche(self, nom: str) -> list[str]:
        """Repli quand aucun sitemap n'est exploitable : utilise la
        recherche WordPress native (?s=) pour trouver des URLs candidates.
        Recherche sur le NOM SEUL -- inclure le numero de carte degrade la
        pertinence de la recherche native sur les boutiques testees
        (0 resultat des qu'un "/" ou un nombre isole est ajoute a la
        requete) ; le filtrage nom+numero se fait ensuite normalement via
        _slug_correspond sur les URLs candidates trouvees.

        Detection par DOMAINE + exclusions plutot que par classe CSS : la
        classe de lien produit WooCommerce standard
        ("woocommerce-loop-product__link") fonctionne sur certains themes
        (kiokutcg.fr) mais pas d'autres (nexthobby.fr n'a aucune classe de
        ce type sur ses liens produit, meme constat que sur PrestaShop) --
        on recupere donc tous les liens internes du domaine et on exclut
        les segments clairement non-produits, plus fiable d'un theme a l'autre."""
        try:
            url = f"{self.base_url}/?s={quote(nom)}&post_type=product"
            r = self.session.get(url, headers=HEADERS_HTML, timeout=TIMEOUT)
            r.raise_for_status()
        except requests.exceptions.RequestException:
            return []
        html = r.content.decode("utf-8", errors="replace")

        domaine_nu = self.domaine.removeprefix("www.")
        candidats = re.findall(rf'href="(https?://(?:www\.)?{re.escape(domaine_nu)}/[^"]+)"', html)
        candidats = [
            u for u in candidats
            if not any(seg in u for seg in SEGMENTS_RECHERCHE_EXCLUS) and not _est_racine_boutique(u)
        ]
        return list(dict.fromkeys(candidats))

    def rechercher_via_recherche_html(
        self, criteres: list[tuple[str, str | None]]
    ) -> dict[tuple[str, str | None], list[ResultatRecherche]]:
        """Repli SANS sitemap : decouverte via la recherche native WordPress
        (?s=) plutot que le sitemap XML. A utiliser uniquement pour les
        boutiques ou aucun sitemap exploitable n'a ete trouve."""
        resultats_par_critere: dict[tuple[str, str | None], list[ResultatRecherche]] = {
            (nom, numero): [] for nom, numero in criteres
        }
        candidats_par_nom: dict[str, list[str]] = {}

        for nom, numero in criteres:
            critere = CritereRecherche(nom=nom, numero=numero)
            confiance_base = "forte" if numero is not None else "faible"

            if nom not in candidats_par_nom:
                candidats_par_nom[nom] = self._decouvrir_candidats_recherche(nom)
                time.sleep(DELAI_ENTRE_PAGES_PRODUIT)
            candidats_bruts = candidats_par_nom[nom]

            candidats = [u for u in candidats_bruts if _slug_correspond(u, critere)]
            if len(candidats) > LIMITE_CANDIDATS_PAR_CRITERE:
                candidats = candidats[:LIMITE_CANDIDATS_PAR_CRITERE]

            for url in candidats:
                resultat = self._evaluer_url(url, nom, numero, confiance_base)
                if resultat:
                    resultats_par_critere[(nom, numero)].append(resultat)

        return resultats_par_critere

    def _decouvrir_produits_api_rest(self, nom: str) -> tuple[list[dict], bool]:
        """Repli via l'API REST WooCommerce "Store API"
        (wp-json/wc/store/v1/products), publique et documentee -- PAS un
        contournement, c'est l'API officielle destinee aux vitrines
        headless, activee par defaut sur la plupart des installations
        WooCommerce. Alternative au repli recherche HTML pour les
        boutiques dont la recherche visible est pilotee par JS/AJAX cote
        client (constate sur mymesis.fr : widget Elementor "Jet Search",
        une requete GET statique sur "?s=" ne renvoie pas de resultats
        filtres) -- l'API REST, elle, applique un vrai filtrage cote
        serveur independant du widget de recherche du theme.

        Renvoie (produits, ok) : ok=False si la requete a echoue
        (timeout/erreur reseau/reponse invalide), a distinguer d'une
        recherche reussie qui ne renvoie simplement aucun produit -- cf.
        rechercher_via_api_rest() qui s'appuie dessus pour son coupe-circuit."""
        try:
            url = f"{self.base_url}/wp-json/wc/store/v1/products?search={quote(nom)}&per_page=50"
            r = self.session.get(url, headers=HEADERS_HTML, timeout=TIMEOUT)
            r.raise_for_status()
            produits = r.json()
        except (requests.exceptions.RequestException, ValueError):
            return [], False
        return (produits if isinstance(produits, list) else []), True

    # Nombre d'echecs CONSECUTIFS (timeout/erreur reseau) au-dela duquel on
    # suppose l'API distante en panne/rate-limitee pour ce cycle et on
    # arrete d'insister -- plutot que de consommer, dans le pire cas, ~15s
    # (TIMEOUT) par nom de carte restant (~100+ noms uniques dans la
    # watchlist). Cas reel (16/08/2026) : mymesis.fr bloque 7+ min sans
    # jamais finir dans scan_lot_a (deja tendu par cardshunter.fr/
    # hamacards.com), job tue par son propre timeout -- cf. SESSION_NOTES.md.
    SEUIL_ECHECS_CONSECUTIFS_API_REST = 3

    def rechercher_via_api_rest(
        self, criteres: list[tuple[str, str | None]]
    ) -> dict[tuple[str, str | None], list[ResultatRecherche]]:
        """Repli via l'API REST WooCommerce -- a utiliser pour les
        boutiques dont le repli recherche HTML echoue faute de recherche
        cote serveur exploitable (cf. _decouvrir_produits_api_rest)."""
        resultats_par_critere: dict[tuple[str, str | None], list[ResultatRecherche]] = {
            (nom, numero): [] for nom, numero in criteres
        }
        produits_par_nom: dict[str, list[dict]] = {}
        echecs_consecutifs = 0
        api_abandonnee = False

        for nom, numero in criteres:
            critere = CritereRecherche(nom=nom, numero=numero)
            confiance_base = "forte" if numero is not None else "faible"

            if nom not in produits_par_nom:
                if api_abandonnee:
                    produits_par_nom[nom] = []
                else:
                    produits, ok = self._decouvrir_produits_api_rest(nom)
                    produits_par_nom[nom] = produits
                    if ok:
                        echecs_consecutifs = 0
                    else:
                        echecs_consecutifs += 1
                        if echecs_consecutifs >= self.SEUIL_ECHECS_CONSECUTIFS_API_REST:
                            api_abandonnee = True
                            print(f"[{self.nom_affiche}] API REST : {echecs_consecutifs} "
                                  f"echecs consecutifs -- abandon pour ce cycle "
                                  f"({len(criteres)} criteres au total, arret sur '{nom}')")
                    time.sleep(DELAI_ENTRE_PAGES_PRODUIT)

            for produit in produits_par_nom[nom]:
                titre = produit.get("name", "")
                if not _titre_correspond(titre, critere):
                    continue

                prix_info = produit.get("prices") or {}
                try:
                    unite_min = int(prix_info.get("currency_minor_unit", 2))
                    prix = float(prix_info["price"]) / (10 ** unite_min)
                except (KeyError, TypeError, ValueError):
                    continue

                devise = (prix_info.get("currency_code") or "").upper()
                devise_ok = devise == "EUR"
                confiance = confiance_base if devise_ok else "faible"
                images = produit.get("images") or []
                # Store API : pas de page HTML recuperee ici, mais les champs
                # description/short_description exposent le meme texte.
                texte_description = f"{produit.get('short_description', '')} {produit.get('description', '')}"

                resultats_par_critere[(nom, numero)].append(ResultatRecherche(
                    boutique=self.nom_affiche,
                    titre=titre,
                    prix=prix,
                    en_stock=bool(produit.get("is_in_stock")),
                    url_produit=produit.get("permalink", ""),
                    variante_titre="",
                    image_url=images[0].get("src") if images else None,
                    langue_detectee=detecter_langue(titre),
                    confiance=confiance,
                    necessite_verification_manuelle=(numero is None) or not devise_ok,
                    etat_detecte=detecter_etat(texte_description),
                ))

        return resultats_par_critere

    def rechercher_par_mots_cles(
        self, criteres: list[tuple[str, str | None]]
    ) -> dict[tuple[str, str | None], list[ResultatRecherche]]:
        urls_produits = self.recuperer_toutes_les_urls_produits()
        return self.rechercher_dans_catalogue(urls_produits, criteres)


if __name__ == "__main__":
    from watchlist_shopify import ECHANTILLON_CONFIG

    boutiques = ["mgs-shop.fr", "pokestock.fr", "cardshunter.fr"]
    criteres = [c.cle_recherche for c in ECHANTILLON_CONFIG]

    for domaine in boutiques:
        print(f"\n{'=' * 70}")
        print(f"Boutique : {domaine}")
        print("=" * 70)

        connecteur = ConnecteurWooCommerce(domaine)
        urls = connecteur.recuperer_toutes_les_urls_produits()
        print(f"{len(urls)} URLs produits trouvees via le sitemap")

        resultats_par_critere = connecteur.rechercher_dans_catalogue(urls, criteres)

        for (nom, numero), resultats in resultats_par_critere.items():
            libelle = f"{nom} {numero}" if numero else f"{nom} (sans numero)"
            print(f"\n--- {libelle} ---")
            if not resultats:
                print("  Non trouve.")
                continue
            resultats.sort(key=lambda r: r.prix)
            for r in resultats:
                statut = "EN STOCK" if r.en_stock else "RUPTURE "
                verif = " ⚠ A VERIFIER" if r.necessite_verification_manuelle else ""
                print(f"  [{statut}] ({r.confiance}){verif} {r.titre} — {r.prix:.2f} — {r.url_produit}")
