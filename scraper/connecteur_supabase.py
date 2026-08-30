"""
Connecteur optionnel vers la base Supabase du SaaS (saas/) : lit les
watchlists personnalisées des utilisateurs et y enregistre les deals qui
matchent, pour affichage dans le dashboard (saas/app/dashboard).

Système ENTIÈREMENT additif et non-bloquant, même philosophie que
verification_photo.py : n'intervient qu'APRÈS qu'un deal a déjà été détecté
et validé par le système historique (nouveaux_deals dans main.py), jamais
dans la détection elle-même. Actif uniquement si les secrets SUPABASE_URL/
SUPABASE_SERVICE_ROLE_KEY sont configurés ; absents -> no-op silencieux.
Toute erreur réseau/API est avalée (log + liste vide), ne doit jamais faire
échouer un cycle de scan pour une fonctionnalité annexe.

Le matching réutilise le nom EXACT (normalisé) de la carte tel que défini
dans config.yaml (watchlist) / saisi par l'utilisateur dans le dashboard
(même format attendu, ex. "Dracaufeu ex 199/165") -- pas de recherche eBay
dédiée par utilisateur : ça multiplierait les appels sur une API déjà
sujette au rate-limit 429 documenté dans CLAUDE.md/SESSION_NOTES.md.
"""
from __future__ import annotations

import logging

import requests

from filtre_annonces import normaliser

log = logging.getLogger("pokedeals.connecteur_supabase")

TIMEOUT = 10


TAILLE_PAGE_WATCHLIST = 1000  # limite par defaut de PostgREST/Supabase par requete


def lister_watchlist_items(supabase_url: str, service_role_key: str) -> list[dict]:
    """Récupère TOUTES les watchlists de tous les utilisateurs (clé service_role,
    contourne volontairement les policies RLS -- c'est le scraper, pas un
    utilisateur), en paginant par blocs de TAILLE_PAGE_WATCHLIST -- Supabase/
    PostgREST plafonne une requête a 1000 lignes par defaut (audit externe du
    30/08/2026) : sans pagination, les utilisateurs au-dela de la 1000e ligne
    etaient silencieusement absents du scan (jamais d'erreur, juste une liste
    tronquee). Retourne [] si les secrets sont absents ; une page en erreur
    reseau arrete la pagination et renvoie ce qui a deja ete recupere (mieux
    qu'echouer sur tout, cf. philosophie non-bloquante du module)."""
    if not supabase_url or not service_role_key:
        return []
    items: list[dict] = []
    offset = 0
    while True:
        try:
            r = requests.get(
                f"{supabase_url.rstrip('/')}/rest/v1/watchlist_items",
                params={"select": "id,user_id,nom_carte,langue,prix_seuil"},
                headers={
                    "apikey": service_role_key,
                    "Authorization": f"Bearer {service_role_key}",
                    "Range": f"{offset}-{offset + TAILLE_PAGE_WATCHLIST - 1}",
                },
                timeout=TIMEOUT,
            )
            r.raise_for_status()
            page = r.json()
        except requests.RequestException as e:
            log.warning("Lecture des watchlists Supabase échouée (%s) -- %d ligne(s) déjà récupérée(s), le reste ignoré ce cycle",
                        e, len(items))
            break
        items.extend(page)
        if len(page) < TAILLE_PAGE_WATCHLIST:
            break
        offset += TAILLE_PAGE_WATCHLIST
    return items


def trouver_correspondances(deals: list[dict], items: list[dict]) -> list[dict]:
    """Compare chaque deal déjà validé aux watchlists utilisateur (nom normalisé
    + langue + seuil de prix). Retourne les lignes prêtes à insérer dans
    watchlist_alerts."""
    if not deals or not items:
        return []
    alertes = []
    for item in items:
        nom_norm = normaliser(item.get("nom_carte", ""))
        if not nom_norm:
            continue
        langue = (item.get("langue") or "fr").lower()
        try:
            seuil = float(item.get("prix_seuil", 0))
        except (TypeError, ValueError):
            continue
        for deal in deals:
            if normaliser(deal.get("carte", "")) != nom_norm:
                continue
            if (deal.get("langue") or "fr").lower() != langue:
                continue
            total = float(deal.get("total", 0))
            if total > seuil:
                continue
            alertes.append({
                "user_id": item["user_id"],
                "watchlist_item_id": item["id"],
                "titre": deal.get("titre", "")[:500],
                "prix": total,
                "url": deal.get("url", ""),
                "plateforme": deal.get("plateforme", ""),
            })
    return alertes


def enregistrer_alertes(supabase_url: str, service_role_key: str, alertes: list[dict]) -> list[dict]:
    """Insère les correspondances trouvées. Une même alerte (même carte
    surveillée + même annonce) n'est jamais dupliquée : contrainte unique
    (watchlist_item_id, url) côté base + `resolution=ignore-duplicates`.

    Retourne UNIQUEMENT les lignes réellement insérées (les doublons ignorés
    n'apparaissent pas dans la réponse `return=representation`) -- utilisé par
    notifications_saas.py pour ne notifier (push/email) qu'une seule fois par
    alerte réellement NOUVELLE, jamais à chaque cycle sur les mêmes deals déjà
    connus."""
    if not alertes or not supabase_url or not service_role_key:
        return []
    try:
        r = requests.post(
            f"{supabase_url.rstrip('/')}/rest/v1/watchlist_alerts",
            json=alertes,
            headers={
                "apikey": service_role_key,
                "Authorization": f"Bearer {service_role_key}",
                "Content-Type": "application/json",
                "Prefer": "return=representation,resolution=ignore-duplicates",
            },
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        nouvelles = r.json()
        log.info("[Supabase] %d alerte(s) watchlist enregistrée(s) pour le dashboard SaaS",
                  len(nouvelles))
        return nouvelles
    except requests.RequestException as e:
        log.warning("Écriture des alertes watchlist Supabase échouée (%s) -- ignorée ce cycle", e)
        return []


def enregistrer_cotes_marche(supabase_url: str, service_role_key: str, cotes: list[dict]) -> None:
    """Upsert des cotes (prix de référence marché) calculées ce cycle, pour
    affichage d'un "prix marché" dans le dashboard SaaS. `cotes` :
    [{"nom_norm", "langue", "cote", "confiance"}, ...] -- une entrée par
    carte scannée ce cycle (config.yaml + watchlist SaaS confondues, cf.
    main.py). Clé (nom_norm, langue) : une carte déjà connue est mise à
    jour, jamais dupliquée (contrainte unique côté base + resolution=
    merge-duplicates)."""
    if not cotes or not supabase_url or not service_role_key:
        return
    # Deduplique par (nom_norm, langue) -- deux entrees de cfg["watchlist"]
    # (config.yaml et/ou watchlist SaaS) peuvent se normaliser sur la meme
    # cle. PostgREST/Postgres rejette un upsert avec deux lignes en conflit
    # DANS LE MEME LOT (erreur 500 "ON CONFLICT DO UPDATE command cannot
    # affect row a second time"), donc un seul POST par cle -- la derniere
    # cote calculee ce cycle l'emporte.
    dedupliquees = {(c["nom_norm"], c["langue"]): c for c in cotes}
    cotes = list(dedupliquees.values())
    try:
        r = requests.post(
            f"{supabase_url.rstrip('/')}/rest/v1/market_cotes",
            json=cotes,
            headers={
                "apikey": service_role_key,
                "Authorization": f"Bearer {service_role_key}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates",
            },
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        log.info("[Supabase] %d cote(s) marché enregistrée(s)/mise(s) à jour pour le dashboard SaaS",
                  len(cotes))
    except requests.RequestException as e:
        log.warning("Écriture des cotes marché Supabase échouée (%s) -- ignorée ce cycle", e)
