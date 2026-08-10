"""
Connecteur PrestaShop (strategie SITEMAP) pour PokeDeals.

Contrairement a Shopify (endpoint JSON /products.json unique et standard),
les boutiques PrestaShop n'exposent pas d'API produit uniforme, et leurs
themes varient enormement (verifie sur 3 boutiques de reference : classes
CSS totalement differentes selon le theme -- classic, custom PS1.6,
Elementor). En revanche, la plupart exposent :

  1. Un SITEMAP XML (natif /sitemap.xml, ou via un module tiers courant
     accessible a /1_index_sitemap.xml, parfois declare dans robots.txt)
     -- donne une liste d'URLs produits sans avoir a deviner l'URL de
     recherche.
  2. Des donnees structurees JSON-LD (schema.org Product/Offer) sur CHAQUE
     page produit -- prix, devise (code ISO fiable, ex "EUR"/"JPY"), et
     statut de stock, independamment du theme visuel utilise.

Strategie (V1, volontairement etroite -- PAS de repli "recherche HTML") :
  1. Decouvrir le/les sitemap(s) racine (robots.txt puis chemins standards).
  2. Lister toutes les URLs produits (recursion sur sitemapindex).
  3. Filtrer ces URLs par nom+numero (matching sur le slug, insensible aux
     accents/tirets) -- ne retient qu'une poignee de candidats.
  4. Pour chaque candidat retenu, recuperer sa page et en extraire le
     JSON-LD (prix/devise/stock). Si la devise n'est PAS EUR, le resultat
     est marque a confiance faible / necessite_verification_manuelle=True
     (pas de conversion de change, juste un garde-fou).
  5. Si aucun JSON-LD Product n'est trouve sur une page candidate, elle est
     ignoree (pas de repli regex sur le HTML brut dans cette V1).

Retourne les MEMES structures que connecteur_shopify.py (ResultatRecherche,
CritereRecherche) pour rester compatible avec bonne_affaire_shopify.py et
alerte_stock.py SANS AUCUNE MODIFICATION -- ces deux modules ne referencent
jamais ConnecteurShopify directement, uniquement ces structures de donnees
partagees (verifie a la lecture de leur code : ils sont deja generiques).
"""

import json
import re
import sys
import time
import unicodedata
import xml.etree.ElementTree as ET

import requests

from connecteur_shopify import (
    HEADERS,
    TIMEOUT,
    CritereRecherche,
    ResultatRecherche,
    _regex_numero_sans_denominateur,
    detecter_langue,
)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DELAI_ENTRE_PAGES_PRODUIT = 0.5  # meme politesse que Shopify
LIMITE_CANDIDATS_PAR_CRITERE = 15  # garde-fou si un critere sans numero matche trop large

# Chemins de sitemap standards a tenter si rien n'est declare dans robots.txt.
CHEMINS_SITEMAP_CANDIDATS = ["/sitemap.xml", "/1_index_sitemap.xml", "/sitemap_index.xml"]

# Segments d'URL clairement non-produits, exclus du filtrage (reduit le
# volume de candidats sans avoir a classifier finement chaque URL).
SEGMENTS_EXCLUS = (
    "/content/", "/cms/", "/module/", "/panier", "/connexion", "/mon-compte",
    "/nous-contacter", "/recherche", "/commande", "/meilleures-ventes",
)

# Statuts schema.org consideres comme "achetable maintenant".
DISPONIBILITES_EN_STOCK = {
    "https://schema.org/InStock",
    "https://schema.org/LimitedAvailability",
}


def _normaliser_texte(texte: str) -> str:
    """Minuscule, accents retires, tout separateur non-alphanumerique
    remplace par un espace -- pour comparer un nom de config.yaml (accents,
    espaces) a un slug d'URL (sans accents, tirets)."""
    sans_accents = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", sans_accents.lower()).strip()


def _slug_correspond(url: str, critere: CritereRecherche) -> bool:
    """Meme regles de matching que connecteur_shopify._titre_correspond
    (nom ET numero obligatoires des qu'un numero existe), appliquees au
    slug de l'URL apres normalisation (accents/tirets neutralises)."""
    texte = _normaliser_texte(url)

    if _normaliser_texte(critere.nom) not in texte:
        return False
    if critere.numero is None:
        return True

    if "/" in critere.numero:
        # "199/165" -> normalise "199 165" (le "/" devient un espace, comme le "-" du slug)
        return _normaliser_texte(critere.numero) in texte

    return bool(_regex_numero_sans_denominateur(critere.numero).search(texte))


def _est_xml_valide(contenu: bytes) -> bool:
    debut = contenu.lstrip()[:200].lower()
    return debut.startswith(b"<?xml") or debut.startswith(b"<urlset") or debut.startswith(b"<sitemapindex")


def _extraire_jsonld_produit(html: str) -> dict | None:
    """Extrait le premier bloc JSON-LD de type Product (schema.org) d'une
    page produit. Gere le wrapper /* <![CDATA[ ... ]]> */ que certains
    themes (ex: nin-nin-game.com) ajoutent autour du JSON."""
    for bloc in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        corps = re.sub(r"/\*\s*<!\[CDATA\[\s*\*/", "", bloc)
        corps = re.sub(r"/\*\s*\]\]>\s*\*/", "", corps)
        try:
            donnees = json.loads(corps)
        except (json.JSONDecodeError, ValueError):
            continue
        candidats = donnees if isinstance(donnees, list) else [donnees]
        for d in candidats:
            if isinstance(d, dict) and d.get("@type") == "Product":
                return d
    return None


def _analyser_offre(produit_jsonld: dict) -> dict:
    """Extrait prix/devise/disponibilite depuis le champ offers (dict OU liste selon les themes)."""
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
        "en_stock": offres.get("availability", "") in DISPONIBILITES_EN_STOCK,
    }


class ConnecteurPrestaShopSitemap:
    """Connecteur PrestaShop generique base sur le sitemap XML + JSON-LD des pages produit."""

    def __init__(self, domaine: str, nom_affiche: str | None = None):
        self.domaine = domaine.strip().rstrip("/")
        self.nom_affiche = nom_affiche or domaine
        self.base_url = f"https://{self.domaine}"
        self.session = requests.Session()

    def _decouvrir_sitemaps_racine(self) -> list[str]:
        """Trouve le(s) sitemap(s) racine : d'abord via robots.txt (Sitemap:),
        sinon en tentant les chemins standards -- en validant a chaque fois
        que la reponse est bien du XML (et pas une page HTML de secours,
        cas frequent : plusieurs boutiques renvoient un 200 sur un chemin
        de sitemap absent, avec la page d'accueil comme contenu)."""
        try:
            r = self.session.get(f"{self.base_url}/robots.txt", headers=HEADERS, timeout=TIMEOUT)
            if r.status_code == 200:
                declares = re.findall(r"(?im)^sitemap:\s*(\S+)", r.text)
                declares = [u if u.startswith("http") else f"{self.base_url}{u}" for u in declares]
                if declares:
                    return declares
        except requests.exceptions.RequestException:
            pass

        for chemin in CHEMINS_SITEMAP_CANDIDATS:
            try:
                r = self.session.get(f"{self.base_url}{chemin}", headers=HEADERS, timeout=TIMEOUT)
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
            r = self.session.get(sitemap_url, headers=HEADERS, timeout=TIMEOUT)
            r.raise_for_status()
            if not _est_xml_valide(r.content):
                return []
            racine = ET.fromstring(r.content)
        except (requests.exceptions.RequestException, ET.ParseError):
            return []

        tag = racine.tag.split("}")[-1]  # ignore le namespace XML
        if tag == "sitemapindex":
            urls = []
            sous_sitemaps = [
                loc.text.strip() for loc in racine.iter()
                if loc.tag.split("}")[-1] == "loc" and loc.text
            ]
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
        """Decouvre et liste toutes les URLs du sitemap, moins les segments
        clairement non-produits (categories techniques, CMS, panier...)."""
        racines = self._decouvrir_sitemaps_racine()
        toutes_urls: list[str] = []
        for racine in racines:
            toutes_urls.extend(self._lister_urls_recursif(racine))

        toutes_urls = list(dict.fromkeys(toutes_urls))  # dedupe en gardant l'ordre
        return [u for u in toutes_urls if not any(seg in u for seg in SEGMENTS_EXCLUS)]

    def rechercher_dans_catalogue(
        self, urls_produits: list[str], criteres: list[tuple[str, str | None]]
    ) -> dict[tuple[str, str | None], list[ResultatRecherche]]:
        """Filtre les URLs par critere (slug), puis recupere le JSON-LD de
        chaque page candidate. Meme structure de retour que
        ConnecteurShopify.rechercher_dans_catalogue."""
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
                try:
                    r = self.session.get(url, headers=HEADERS, timeout=TIMEOUT)
                    r.raise_for_status()
                except requests.exceptions.RequestException:
                    continue
                finally:
                    time.sleep(DELAI_ENTRE_PAGES_PRODUIT)

                produit = _extraire_jsonld_produit(r.text)
                if produit is None:
                    continue  # pas de JSON-LD exploitable -> ignore (V1 volontairement etroite)

                offre = _analyser_offre(produit)
                if offre["prix"] is None:
                    continue

                devise = (offre["devise"] or "").upper()
                devise_ok = devise == "EUR"
                confiance = confiance_base if devise_ok else "faible"
                necessite_verif = (numero is None) or not devise_ok

                image = produit.get("image")
                if isinstance(image, list):
                    image = image[0] if image else None

                resultats_par_critere[(nom, numero)].append(ResultatRecherche(
                    boutique=self.nom_affiche,
                    titre=produit.get("name", ""),
                    prix=offre["prix"],
                    en_stock=offre["en_stock"],
                    url_produit=url,
                    variante_titre="",
                    image_url=image,
                    langue_detectee=detecter_langue(produit.get("name", "")),
                    confiance=confiance,
                    necessite_verification_manuelle=necessite_verif,
                ))

        return resultats_par_critere

    def rechercher_par_mots_cles(
        self, criteres: list[tuple[str, str | None]]
    ) -> dict[tuple[str, str | None], list[ResultatRecherche]]:
        """Raccourci standalone : decouvre le sitemap PUIS cherche dedans."""
        urls_produits = self.recuperer_toutes_les_urls_produits()
        return self.rechercher_dans_catalogue(urls_produits, criteres)


if __name__ == "__main__":
    from watchlist_shopify import ECHANTILLON_CONFIG

    boutiques = ["blazingtail.fr", "nin-nin-game.com", "nordikards.com"]
    criteres = [c.cle_recherche for c in ECHANTILLON_CONFIG]

    for domaine in boutiques:
        print(f"\n{'=' * 70}")
        print(f"Boutique : {domaine}")
        print("=" * 70)

        connecteur = ConnecteurPrestaShopSitemap(domaine)
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
