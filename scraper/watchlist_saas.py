"""
Etend la watchlist scraper avec les cartes ajoutees par les utilisateurs du
SaaS (saas/, table watchlist_items), en plus de la watchlist curee a la
main dans config.yaml. Systeme ENTIEREMENT additif : ne modifie jamais
config.yaml (ni sur disque ni en memoire), ne touche pas a son parsing
existant -- reutilise watchlist_shopify.extraire_nom_et_numero() pour
convertir chaque carte SaaS au meme format que les entrees curees.

Deux usages distincts, avec des couts reseau tres differents :
- scan_boutique*.py (Shopify/PrestaShop/WooCommerce) : le catalogue ENTIER
  d'une boutique est deja recupere en un seul appel reseau, quel que soit
  le nombre de cartes recherchees (cf. scan_boutique.py,
  ConnecteurShopify.recuperer_tout_le_catalogue). Ajouter des cartes SaaS
  ici est donc GRATUIT en requetes HTTP, seulement un peu plus de matching
  local -- aucune limite (cartes_watchlist_saas()).
- main.py (eBay/Vinted/Leboncoin, via collecter()) : UNE recherche reseau
  PAR carte -- rate-limit 429 deja documente (CLAUDE.md/SESSION_NOTES.md,
  coupe-circuit connecteur_ebay). Chaque carte SaaS ajoutee ici a un cout
  reseau reel : plafonne a MAX_CARTES_SAAS_EBAY, priorisees par nombre
  d'utilisateurs qui la surveillent (dict_watchlist_saas(max_cartes=...)).

Absent de secrets Supabase ou erreur reseau -> liste vide (cf.
connecteur_supabase.lister_watchlist_items, deja no-op silencieux) :
aucun de ces deux usages ne peut donc echouer a cause de ce module.
"""
from __future__ import annotations

import connecteur_supabase
import notifications_saas
from connecteur_supabase import lister_watchlist_items
from filtre_annonces import normaliser
from watchlist_shopify import CarteWatchlist, extraire_nom_et_numero

# Releve de 20 a 30 le 03/09/2026 (signale par Justok) : 24 cartes SaaS
# existaient deja au moment du releve (tous utilisateurs confondus), 4 d'entre
# elles (les plus recemment ajoutees, cf. tri par created_at desormais
# explicite dans connecteur_supabase.lister_watchlist_items) ne passaient
# jamais le plafond -- jamais recherchees sur eBay/Vinted, silencieusement.
# 30 laisse une marge sur les 24 actuelles sans faire exploser le budget
# reseau de main.py (marge mesuree ~2-3x sur son timeout de 15 min, cf.
# SESSION_NOTES.md).
MAX_CARTES_SAAS_EBAY = 30


def _grouper_par_carte(items: list[dict]) -> list[dict]:
    """Deduplique les watchlist_items (potentiellement un par utilisateur
    qui surveille la meme carte) en une entree par carte (nom normalise +
    langue). prix_max_fixe = le seuil le PLUS HAUT parmi les utilisateurs
    qui la surveillent -- chaque utilisateur est ensuite refiltre
    individuellement contre SON PROPRE seuil par
    connecteur_supabase.trouver_correspondances() (deja appele plus loin
    dans main.py sur les deals detectes), donc elargir le seuil ici ne cree
    jamais de fausse alerte, seulement une detection plus large en amont.
    `nb_utilisateurs` sert a prioriser en cas de plafond (MAX_CARTES_SAAS_EBAY).

    Correctif du 04/09/2026 (audit externe, confirme par relecture directe du
    code) : une carte mise en pause par l'utilisateur cote dashboard SaaS
    (watchlist_items.actif = false, cf. migration 0013 du depot
    pokedeals-saas) continuait d'etre scannee ici -- le bouton "Mettre en
    pause" du dashboard ne faisait rien cote scraper, contrairement a ce que
    l'utilisateur croit. item.get("actif", True) : une ligne SANS la colonne
    (ancien schema, ou valeur NULL improbable vu le NOT NULL DEFAULT true de
    la migration) est traitee comme active, jamais comme un rejet silencieux
    par defaut."""
    groupes: dict[tuple[str, str], dict] = {}
    for item in items:
        if item.get("actif", True) is False:
            continue
        nom_carte = (item.get("nom_carte") or "").strip()
        nom_norm = normaliser(nom_carte)
        if not nom_norm:
            continue
        langue = (item.get("langue") or "fr").lower()
        try:
            seuil = float(item.get("prix_seuil", 0))
        except (TypeError, ValueError):
            continue
        if seuil <= 0:
            continue
        cle = (nom_norm, langue)
        if cle not in groupes:
            groupes[cle] = {"nom": nom_carte, "langue": langue, "prix_max_fixe": seuil, "nb_utilisateurs": 1}
        else:
            groupes[cle]["prix_max_fixe"] = max(groupes[cle]["prix_max_fixe"], seuil)
            groupes[cle]["nb_utilisateurs"] += 1
    return sorted(groupes.values(), key=lambda g: g["nb_utilisateurs"], reverse=True)


def dict_watchlist_saas(
    supabase_url: str, service_role_key: str, max_cartes: int | None = None
) -> list[dict]:
    """Cartes SaaS distinctes, au meme format que les entrees de
    cfg["watchlist"] (config.yaml) : [{"nom", "langue", "prix_max_fixe"}, ...].
    `max_cartes` limite le nombre d'entrees retournees (les plus
    demandees en premier) -- a utiliser pour main.py, jamais pour les
    scanners boutiques (cf. docstring du module)."""
    items = lister_watchlist_items(supabase_url, service_role_key)
    cartes = _grouper_par_carte(items)
    if max_cartes is not None:
        cartes = cartes[:max_cartes]
    return [
        {"nom": c["nom"], "langue": c["langue"], "prix_max_fixe": c["prix_max_fixe"]}
        for c in cartes
    ]


def cartes_watchlist_saas(supabase_url: str, service_role_key: str) -> list[CarteWatchlist]:
    """Cartes SaaS distinctes converties en CarteWatchlist, pretes pour les
    scanners boutiques (scan_boutique*.py) -- AUCUNE limite de nombre (cf.
    docstring du module : gratuit en requetes HTTP pour ces scanners)."""
    cartes: list[CarteWatchlist] = []
    for entree in dict_watchlist_saas(supabase_url, service_role_key):
        nom_recherche, numero, qualificatif = extraire_nom_et_numero(entree["nom"])
        cartes.append(CarteWatchlist(
            nom_recherche, numero, entree["langue"], entree["nom"], entree["prix_max_fixe"], qualificatif
        ))
    return cartes


def notifier_deals_boutique_saas(secrets: dict, deals_boutique: list[dict]) -> None:
    """Fait correspondre les deals detectes par les scanners boutiques
    (scan_boutique*.py, format bonne_affaire_shopify.evaluer_deal --
    nom/langue/prix/titre_produit/url_produit/boutique) aux watchlists
    personnalisees des utilisateurs SaaS, enregistre les alertes et notifie
    (push/email) uniquement les nouvelles -- meme pipeline que main.py pour
    eBay/Vinted, jusqu'ici applique aux boutiques SEULEMENT pour le scan
    (cartes_watchlist_saas ci-dessus), jamais pour l'alerte elle-meme.
    Entierement additif et non-bloquant (memes garanties que
    connecteur_supabase.py : secrets absents ou erreur reseau -> no-op)."""
    supabase_url = secrets.get("SUPABASE_URL", "")
    service_role_key = secrets.get("SUPABASE_SERVICE_ROLE_KEY", "")
    watchlist_items = connecteur_supabase.lister_watchlist_items(supabase_url, service_role_key)
    if not watchlist_items:
        return

    deals_normalises = [
        {
            "carte": d["nom"],
            "langue": d["langue"],
            "total": d["prix"],
            "titre": d["titre_produit"],
            "url": d["url_produit"],
            "plateforme": d["boutique"],
        }
        for d in deals_boutique
    ]
    alertes = connecteur_supabase.trouver_correspondances(deals_normalises, watchlist_items)
    connecteur_supabase.enregistrer_alertes(supabase_url, service_role_key, alertes)
    # Notifie TOUTES les alertes en attente d'au moins un canal, pas
    # seulement celles inserees ce cycle (cf. connecteur_supabase.
    # lister_alertes_a_notifier, audit du 30/08/2026) -- meme pipeline que
    # main.py. Ce module et main.py peuvent chacun retenter la meme alerte
    # en attente lors d'un cycle proche dans le temps (workflows
    # independants) ; le pire cas est une notification envoyee deux fois de
    # suite a un utilisateur, jamais une alerte perdue -- compromis
    # deliberement accepte plutot qu'un verrouillage distribue, hors de
    # portee de ce correctif.
    alertes_a_notifier = connecteur_supabase.lister_alertes_a_notifier(supabase_url, service_role_key)
    notifications_saas.notifier_alertes_en_attente(secrets, alertes_a_notifier)
