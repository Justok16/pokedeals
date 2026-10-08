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
    chaque URL, exigeant AU MOINS UN mot-cle du groupe EDITION *ET* AU
    MOINS UN du groupe TYPE (meme double exigence que la verification
    finale, appliquee tot pour limiter le nombre de pages a recuperer --
    cf. _slug_est_candidat), avant de charger la page complete (titre +
    texte) pour la verification finale (mots-cles edition+type ET date).
  - PrestaShop/WooCommerce (repli recherche HTML/API REST, boutiques sans
    sitemap) : une recherche par mot-cle "type" (ETB, UPC, mentali...) via
    le mecanisme de decouverte deja existant, meme filtrage final.
"""

import os
import html as html_module
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from connecteur_shopify import HEADERS_HTML, TIMEOUT
from connecteur_prestashop_sitemap import (
    ConnecteurPrestaShopSitemap,
    _analyser_offre,
    _extraire_jsonld_produit,
    _extraire_microdata_produit,
    _stock_indisponible_selon_dom as _rupture_dom_prestashop,
)
from connecteur_woocommerce import (
    ConnecteurWooCommerce,
    _attente_sans_panier_selon_dom,
    _stock_indisponible_selon_dom as _rupture_dom_woocommerce,
)
from precommandes_watchlist import ProduitSurveille, evaluer_correspondance

import requests

from http_radar_poli import rendre_poli

DELAI_ENTRE_PAGES = 1.0


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


def _candidat(domaine, produit, titre, texte_desc, url, prix=None, en_stock=None, texte_exclusions=None):
    confiance, raison = evaluer_correspondance(titre, texte_desc, produit, texte_exclusions)
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
        "prioritaire": produit.prioritaire,
        "alerte_disponibilite": produit.alerte_disponibilite,
        "horodatage": _horodatage(),
    }


# --- Shopify : catalogue complet deja recupere, aucune requete supplementaire ---

def scanner_shopify(domaine: str, produits: list[ProduitSurveille], connecteur=None) -> list[dict]:
    from connecteur_shopify import ConnecteurShopify
    connecteur = rendre_poli(connecteur or ConnecteurShopify(domaine))
    catalogue = connecteur.recuperer_tout_le_catalogue()

    candidats = []
    for p in catalogue:
        titre = p.get("title", "")
        description = re.sub(r"<[^>]+>", " ", p.get("body_html") or "")
        handle = p.get("handle", "")
        url = f"{connecteur.base_url}/products/{handle}"
        variants = p.get("variants") or []
        for produit in produits:
            # 08/10/2026 : une fiche UPC peut reunir Mentali ET Noctali.
            # Le stock d'une variante ne prouve jamais celui de l'autre,
            # meme si la description commune mentionne les deux personnages.
            # On conserve une seule observation par produit/fiche pour la
            # memoire existante, avec prix et lien de la variante retenue.
            observations = []
            personnages = {"mentali", "espeon", "noctali", "umbreon", "nymphali", "sylveon"}
            discriminants = produit.mots_cles_type & personnages
            discriminants |= frozenset(
                mot for groupe in produit.mots_cles_supplementaires
                for mot in groupe if mot in personnages
            )
            variantes_personnage = any(
                any(mot in _normaliser_slug(v.get("title") or "") for mot in personnages)
                for v in variants
            )
            for v in variants or [{}]:
                titre_variante = v.get("title") or ""
                if discriminants and variantes_personnage and not any(
                    mot in _normaliser_slug(titre_variante) for mot in discriminants
                ):
                    continue
                titre_complet = titre if titre_variante in ("", "Default Title") else f"{titre} — {titre_variante}"
                try:
                    prix = float(v.get("price"))
                except (TypeError, ValueError):
                    prix = None
                disponible = v.get("available")
                en_stock = disponible if isinstance(disponible, bool) else None
                lien = f"{url}?variant={v['id']}" if v.get("id") else url
                c = _candidat(domaine, produit, titre_complet, description, lien, prix, en_stock)
                if c:
                    observations.append(c)
            if observations:
                # Priorite a une variante commandable et son prix reel.
                # L'absence de champ available reste INDETERMINEE.
                disponibles = [c for c in observations if c["en_stock"] is True]
                choix = disponibles or [c for c in observations if c["en_stock"] is None] or observations
                candidats.append(min(choix, key=lambda c: c["prix"] if c["prix"] is not None else float("inf")))

    return candidats


# --- PrestaShop/WooCommerce : sitemap (prefiltre slug) + repli recherche HTML ---
# Une seule fonction de recuperation de page partagee : la logique (requete,
# extraction titre/texte, evaluation) ne depend d'aucune specificite de
# plateforme -- seul le TYPE de connecteur differe (duck typing sur
# .session/.nom_affiche, presents sur les deux classes). Fusionnee le
# 11/08/2026 (etait dupliquee a l'identique entre les deux plateformes).

def _extraire_prix_et_stock(html: str, plateforme: str) -> tuple[float | None, bool | None]:
    """Statut de stock reel de la page, meme strategie que
    ConnecteurPrestaShopSitemap/ConnecteurWooCommerce (JSON-LD -> repli
    microdata -> override DOM de rupture) -- AVANT ce premier fix
    (25/08/2026, signale par l'utilisateur : alerte "precommande detectee"
    recue pour un produit affichant 0,00€ et "rupture de stock" sur
    plazatcg.com), cette fonction ne lisait QUE le titre+texte brut de la
    page, sans jamais determiner le stock reel : `en_stock` restait
    toujours None ("indetermine"), donc `stock_vient_de_souvrir`
    (alerte_precommande.py) ne se declenchait jamais et l'alerte partait
    uniquement sur la confiance "forte" (date de sortie confirmee sur la
    page) -- meme si le produit n'etait pas reellement commandable.

    `plateforme` ("prestashop" ou "woocommerce") choisit le bon override
    DOM : bug reel DISTINCT trouve le meme jour (golden-poke.fr, WooCommerce)
    -- ce premier fix avait applique tel quel l'override PrestaShop
    (`_stock_indisponible_selon_dom` de connecteur_prestashop_sitemap.py,
    cible un span id="product-availability" absent de toute page
    WooCommerce) aux DEUX plateformes, donc l'override ne pouvait jamais se
    declencher sur une page WooCommerce (liste d'attente affichee, JSON-LD
    pourtant "commandable"). Le signal DOM (rupture explicite) prime
    toujours sur le signal structure (JSON-LD/microdata) en cas de
    contradiction, jamais l'inverse -- meme regle que les connecteurs
    principaux.

    2e override WooCommerce ajoute le 26/08/2026 (`_attente_sans_panier_selon_dom`,
    cf. sa docstring) : le premier override ci-dessus ne se declenche que si
    la boutique a explicitement marque le produit outofstock/onbackorder --
    inoperant si la classe native reste "instock" par defaut (produit publie
    a l'avance, stock jamais mis a jour) alors que l'UI reelle n'affiche
    qu'un formulaire "prevenez-moi", sans bouton d'achat. Meme cas reel
    (golden-poke.fr) qui a motive le premier override WooCommerce, mais
    resurgit sous une forme que celui-ci ne couvrait pas."""
    produit_jsonld = _extraire_jsonld_produit(html)
    if produit_jsonld:
        offre = _analyser_offre(produit_jsonld)
        prix, en_stock = offre["prix"], offre["en_stock"]
    else:
        microdata = _extraire_microdata_produit(html)
        prix, en_stock = (microdata["prix"], microdata["en_stock"]) if microdata else (None, None)

    rupture_dom = _rupture_dom_woocommerce if plateforme == "woocommerce" else _rupture_dom_prestashop
    if rupture_dom(html):
        en_stock = False
    if plateforme == "woocommerce" and _attente_sans_panier_selon_dom(html):
        en_stock = False

    return prix, en_stock


def _evaluer_page(connecteur, url: str, produits: list[ProduitSurveille]) -> list[dict]:
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
    # Audit externe du 18/08/2026 (verifie contre le code reel) : la
    # troncature a 5000 caracteres coupait potentiellement AVANT la date de
    # sortie sur un theme avec beaucoup de contenu avant la description
    # produit (nav, en-tete, fil d'ariane, widget panier...) -- l'hypothese
    # "5000 caracteres suffisent pour mots-cles + date" n'etait pas verifiee.
    # Consequence reelle limitee (le radar V54 alerte quand meme sur une
    # transition de stock, meme sans date confirmee) mais peut retarder/
    # empecher la confiance "forte" et l'alerte immediate correspondante
    # (V53). scanner_shopify() (meme fichier) n'a AUCUNE troncature
    # equivalente sur body_html -- retiree ici par coherence, le cout de
    # traitement d'un texte de page web complet est negligeable.
    # Texte VISIBLE seulement : sans <script>/<style>. Bug reel du 08/10/2026
    # (missplaybros.com) : le "priceValidUntil" 2027-12-31 du JSON-LD etait
    # lu comme une date de sortie incompatible -> ETB 30e Anniversaire rejete.
    texte = re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S | re.I))
    plateforme = "woocommerce" if isinstance(connecteur, ConnecteurWooCommerce) else "prestashop"
    prix, en_stock = _extraire_prix_et_stock(html, plateforme)
    # Mots exclus ("japonais", "coreen"...) cherches dans la description
    # PROPRE au produit quand la fiche en a une (JSON-LD), pas dans la page
    # entiere ou figurent d'autres produits (cf. evaluer_correspondance).
    produit_jsonld = _extraire_jsonld_produit(html)
    description = produit_jsonld.get("description") if produit_jsonld else None
    texte_exclusions = (re.sub(r"<[^>]+>", " ", html_module.unescape(description))
                        if isinstance(description, str) and description.strip() else None)

    candidats = []
    for produit in produits:
        c = _candidat(connecteur.nom_affiche, produit, titre, texte, url, prix, en_stock, texte_exclusions)
        if c:
            candidats.append(c)
    return candidats


def scanner_prestashop_sitemap(domaine: str, produits: list[ProduitSurveille]) -> list[dict]:
    connecteur = rendre_poli(ConnecteurPrestaShopSitemap(domaine))
    urls = connecteur.recuperer_toutes_les_urls_produits()

    candidats_urls = {
        u for u in urls
        if any(_slug_est_candidat(u, p) for p in produits)
    }

    resultats = []
    for url in candidats_urls:
        resultats.extend(_evaluer_page(connecteur, url, produits))
    return resultats


def scanner_prestashop_repli_html(domaine: str, produits: list[ProduitSurveille]) -> list[dict]:
    connecteur = rendre_poli(ConnecteurPrestaShopSitemap(domaine))
    urls_vues = set()
    for produit in produits:
        for mot in produit.mots_cles_type:
            urls_vues.update(connecteur._decouvrir_candidats_recherche(mot))
            time.sleep(DELAI_ENTRE_PAGES)

    resultats = []
    for url in urls_vues:
        resultats.extend(_evaluer_page(connecteur, url, produits))
    return resultats


def scanner_woocommerce_sitemap(domaine: str, produits: list[ProduitSurveille]) -> list[dict]:
    connecteur = rendre_poli(ConnecteurWooCommerce(domaine))
    urls = connecteur.recuperer_toutes_les_urls_produits()

    candidats_urls = {
        u for u in urls
        if any(_slug_est_candidat(u, p) for p in produits)
    }

    resultats = []
    for url in candidats_urls:
        resultats.extend(_evaluer_page(connecteur, url, produits))
    return resultats


def scanner_woocommerce_repli_html(domaine: str, produits: list[ProduitSurveille]) -> list[dict]:
    connecteur = rendre_poli(ConnecteurWooCommerce(domaine))
    urls_vues = set()
    for produit in produits:
        for mot in produit.mots_cles_type:
            urls_vues.update(connecteur._decouvrir_candidats_recherche(mot))
            time.sleep(DELAI_ENTRE_PAGES)

    resultats = []
    for url in urls_vues:
        resultats.extend(_evaluer_page(connecteur, url, produits))
    return resultats


def scanner_woocommerce_api_rest(domaine: str, produits: list[ProduitSurveille]) -> list[dict]:
    """Audit externe du 18/08/2026 (verifie contre le code reel, cf.
    SESSION_NOTES.md) : appelait auparavant `_decouvrir_produits_api_rest()`
    directement, une fois par (produit, mot-cle type) -- jusqu'a 12 appels
    (4 produits x ~3 mots-cles chacun) sans AUCUN coupe-circuit, alors que
    `_decouvrir_produits_api_rest()` documente explicitement que
    `rechercher_via_api_rest()` s'appuie sur son retour `ok` pour un
    coupe-circuit (SEUIL_ECHECS_CONSECUTIFS_API_REST). La boutique qui a
    motive ce repli API REST (mymesis.fr) est justement celle deja connue
    pour etre lente/instable (cf. le coupe-circuit du connecteur principal,
    16/08/2026) -- une boutique bloquee ici pouvait consommer jusqu'a
    12 x timeout avant de passer a la suivante, sans aucune protection.
    Meme logique de coupe-circuit que rechercher_via_api_rest() reprise ici
    (mots-cles differents des criteres carte, mais meme principe : apres N
    echecs D'AFFILEE, on arrete d'interroger cette boutique pour ce cycle)."""
    connecteur = rendre_poli(ConnecteurWooCommerce(domaine))
    candidats = []
    vus_ids = set()
    echecs_consecutifs = 0
    api_abandonnee = False
    for produit in produits:
        if api_abandonnee:
            break
        for mot in produit.mots_cles_type:
            if api_abandonnee:
                break
            produits_api, ok = connecteur._decouvrir_produits_api_rest(mot)
            if ok:
                echecs_consecutifs = 0
            else:
                echecs_consecutifs += 1
                if echecs_consecutifs >= connecteur.SEUIL_ECHECS_CONSECUTIFS_API_REST:
                    api_abandonnee = True
                    print(f"[{domaine}] API REST precommandes : {echecs_consecutifs} "
                          f"echecs consecutifs -- abandon pour ce cycle")
            for p in produits_api:
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
                # Une recherche peut renvoyer plusieurs produits suivis.
                # Ne pas marquer l'ID vu apres l'avoir compare a UN SEUL
                # produit : un Noctali trouve par la recherche Mentali
                # serait ensuite saute par la recherche Noctali.
                stock = p.get("is_in_stock")
                en_stock = stock if isinstance(stock, bool) else None
                if p.get("is_purchasable") is False:
                    en_stock = False
                for produit_a_evaluer in produits:
                    c = _candidat(domaine, produit_a_evaluer, titre, description, url, prix, en_stock)
                    if c:
                        candidats.append(c)
            time.sleep(DELAI_ENTRE_PAGES)
    return candidats


# --- E.Leclerc (08/10/2026) : plateforme maison, recherche + fiche JSON-LD ---

# Recherches lancees a chaque cycle (une page de resultats chacune) : couvrent
# les 6 produits des 30 ans suivis par Justok, en noms francais.
REQUETES_LECLERC = (
    "pokemon 30e anniversaire",
    "pokemon me05.5",   # Leclerc nomme ses produits par code d'extension
    "coffret dresseur d'elite 30e anniversaire",
    "pokemon lot de boosters 30e anniversaire",
    "pokemon mini tin 30e anniversaire",
    "pokebox nymphali",
    "collection ultra premium noctali",
    "collection ultra premium mentali",
)


def _titre_est_candidat(titre: str, produit: ProduitSurveille) -> bool:
    """Meme double exigence (edition ET type) que _slug_est_candidat, sur le
    titre d'un resultat de recherche -- evite de charger des fiches inutiles."""
    norm = _normaliser_slug(titre)
    return (any(_normaliser_slug(m) in norm for m in produit.mots_cles_edition)
            and any(_normaliser_slug(m) in norm for m in produit.mots_cles_type))


def _scanner_enseigne(domaine: str, produits: list[ProduitSurveille], connecteur, requetes,
                      urls_directes: tuple[str, ...] = ()) -> list[dict]:
    """Logique commune aux grandes enseignes a plateforme maison (Leclerc,
    Auchan...) : quelques recherches, dedoublonnage par URL (sans parametres),
    filtre edition + type sur le titre, puis evaluation complete. Si le
    connecteur sait lire une fiche (`lire_fiche`), prix/stock/description en
    viennent ; sinon ceux de la carte de recherche sont utilises. Une erreur
    sur une RECHERCHE remonte (boutique en echec ce cycle, rien n'est ecrit en
    memoire) ; une fiche illisible est simplement ignoree.

    `urls_directes` : fiches lues meme si la recherche ne les remonte pas
    (EAN connus, cf. EANS_30E) ; une fiche absente (404) est ignoree, une
    fiche presente passe par le meme filtre edition + type que les resultats
    de recherche (son titre fait foi)."""
    connecteur = rendre_poli(connecteur)
    vus: dict[str, dict] = {}
    for requete in requetes:
        for r in connecteur.rechercher(requete):
            vus.setdefault(r["url"].split("?")[0], r)
    fiches_lues: dict[str, dict] = {}
    for url in urls_directes:
        try:
            fiche = connecteur.lire_fiche(url)
        except requests.RequestException:
            continue
        if fiche is None:
            continue
        url_finale = fiche.get("url") or url
        fiches_lues[url_finale] = fiche
        vus.setdefault(url_finale, {"titre": fiche["titre"], "url": url_finale})

    lire_fiche = getattr(connecteur, "lire_fiche", None)
    candidats = []
    for url, r in vus.items():
        concernes = [p for p in produits if _titre_est_candidat(r["titre"], p)]
        if not concernes:
            continue
        if url in fiches_lues:
            fiche = fiches_lues[url]
        elif lire_fiche:
            try:
                fiche = lire_fiche(r["url"])
            except requests.RequestException:
                continue
            if fiche is None:
                continue
        else:
            fiche = {"titre": r["titre"], "description": "", "prix": r.get("prix"), "en_stock": r.get("en_stock")}
        titre = fiche["titre"] or r["titre"]
        # Descriptions de ces enseignes en francais mais souvent sans les
        # mots-indices de langue_non_francaise() (verifie le 08/10/2026 :
        # "Les Mini Tins Pokemon, appelees aussi mini-boites..."). Sites
        # francais vendant des versions francaises : indice explicite ajoute ;
        # un marqueur d'une autre langue dans le TITRE ("- EN", "japonais"...)
        # reste rejete.
        description = f"{fiche['description']} (site francais {domaine})"
        for produit in concernes:
            c = _candidat(domaine, produit, titre, description, url,
                          prix=fiche["prix"], en_stock=fiche["en_stock"])
            if c:
                candidats.append(c)
    return candidats


# EAN des produits des 30 ans VERIFIES sur des fiches reelles (08/10/2026) :
# ETB et Bundle sur ultrajeux.com (EAN affiche sur la fiche), Bundle aussi
# sur lagranderecre.fr, Mini Tin sur e.leclerc. Le rapport Gemini donnait a
# tort l'EAN de l'ETB pour les deux UPC, et 0196214147102 est le COFFRET
# 4 boosters Nymphali (ultrajeux.com), pas la Pokebox.
EANS_30E = {
    "0196214144835": "Coffret Dresseur d'Elite 30e anniversaire",
    "0196214145221": "Lot de 6 boosters (Bundle) 30e anniversaire",
    "0196214146297": "Mini Tin 30e anniversaire",
    # Donnes concordants par deux rapports independants (Grok, puis l'audit
    # de la PR #147 recoupe sur les catalogues CLD), pas encore vus sur une
    # fiche Leclerc (404 le 08/10/2026) : une fiche absente ne coute qu'une
    # requete sans effet, une fiche presente repasse le filtre edition + type.
    "0196214146976": "Pokebox Nymphali-ex 30e anniversaire",
    "0196214155398": "Collection Ultra Premium Noctali-ex (Soiree)",
    "0196214155336": "Collection Ultra Premium Mentali-ex (Journee)",
}


def scanner_leclerc(domaine: str, produits: list[ProduitSurveille], connecteur=None) -> list[dict]:
    """Recherche + fiches lues directement par EAN (la recherche Leclerc ne
    remonte pas les produits "Pokemon 30A", cf. connecteur_leclerc)."""
    from connecteur_leclerc import ConnecteurLeclerc, url_fiche_par_ean
    return _scanner_enseigne(domaine, produits, connecteur or ConnecteurLeclerc(), REQUETES_LECLERC,
                             urls_directes=tuple(url_fiche_par_ean(e) for e in EANS_30E))


def scanner_auchan(domaine: str, produits: list[ProduitSurveille], connecteur=None) -> list[dict]:
    """Auchan (08/10/2026) : prix et disponibilite directement sur la carte de
    recherche (microdonnees schema.org), aucune fiche a charger."""
    from connecteur_auchan import ConnecteurAuchan
    return _scanner_enseigne(domaine, produits, connecteur or ConnecteurAuchan(), REQUETES_LECLERC)


def scanner_ultrajeux(domaine: str, produits: list[ProduitSurveille], connecteur=None) -> list[dict]:
    """Ultrajeux (08/10/2026) : pages categorie lisibles (nouveautes en tete),
    prix et disponibilite en ligne sur chaque carte, aucune fiche a charger."""
    from connecteur_ultrajeux import CATEGORIES, ConnecteurUltrajeux
    return _scanner_enseigne(domaine, produits, connecteur or ConnecteurUltrajeux(), list(CATEGORIES))
