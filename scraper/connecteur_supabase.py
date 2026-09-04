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
    qu'echouer sur tout, cf. philosophie non-bloquante du module).

    Tri explicite par created_at croissant (03/09/2026, signale par Justok :
    "je ne recois jamais d'alerte eBay/Vinted pour mes cartes coreennes") --
    sans ORDER BY, l'ordre de retour de PostgREST n'est PAS garanti, et
    watchlist_saas._grouper_par_carte() s'appuie sur cet ordre pour
    departager les egalites (nb_utilisateurs identique) et decider
    quelles cartes passent le plafond MAX_CARTES_SAAS_EBAY cote eBay/Vinted
    -- sans tri explicite, quelles cartes tombent sous le plafond aurait pu
    changer silencieusement d'un cycle a l'autre selon l'ordre de scan
    physique de Postgres."""
    if not supabase_url or not service_role_key:
        return []
    items: list[dict] = []
    offset = 0
    while True:
        try:
            r = requests.get(
                f"{supabase_url.rstrip('/')}/rest/v1/watchlist_items",
                params={"select": "id,user_id,nom_carte,langue,prix_seuil,actif", "order": "created_at.asc"},
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
    watchlist_alerts.

    Indexé par (nom_norm, langue) -- audit externe du 30/08/2026 : la version
    précédente comparait chaque item à CHAQUE deal (boucle imbriquée), un coût
    O(items × deals) qui grossit avec le nombre d'utilisateurs même si le
    nombre de deals par cycle reste petit. Regrouper les items par clé une
    seule fois ramène le travail par deal à ses seuls items réellement
    candidats (même nom + même langue), sans changer aucun résultat."""
    if not deals or not items:
        return []
    items_par_cle: dict[tuple[str, str], list[dict]] = {}
    for item in items:
        nom_norm = normaliser(item.get("nom_carte", ""))
        if not nom_norm:
            continue
        langue = (item.get("langue") or "fr").lower()
        try:
            seuil = float(item.get("prix_seuil", 0))
        except (TypeError, ValueError):
            continue
        items_par_cle.setdefault((nom_norm, langue), []).append({**item, "prix_seuil": seuil})

    alertes = []
    for deal in deals:
        cle = (normaliser(deal.get("carte", "")), (deal.get("langue") or "fr").lower())
        candidats = items_par_cle.get(cle)
        if not candidats:
            continue
        total = float(deal.get("total", 0))
        for item in candidats:
            if total > item["prix_seuil"]:
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
    n'apparaissent pas dans la réponse `return=representation`) -- ne PAS
    utiliser cette valeur pour decider qui notifier (cf. piege corrige le
    30/08/2026 ci-dessous) : appeler lister_alertes_a_notifier() juste apres
    pour ca.

    `on_conflict` est OBLIGATOIRE pour que PostgREST sache sur QUELLE
    contrainte appliquer `resolution=ignore-duplicates` -- sans lui (bug reel
    trouve le 31/08/2026, jamais signale par l'audit externe : la contrainte
    est bien creee cote base, cf. migration 0002_watchlist_alerts.sql du
    depot pokedeals-saas, mais jamais nommee ici), PostgREST tente une
    insertion normale et renvoie une vraie 409 Conflict des qu'une alerte
    deja connue revient (une carte boutique qui reste sous le seuil sur
    PLUSIEURS cycles consecutifs, cas courant cote boutiques TCG qui n'ont
    pas de dedup amont equivalente a `vues`/seen.json cote eBay/Vinted) --
    toute la requete echoue alors (une seule requete HTTP pour tout le lot),
    entrainant la PERTE des alertes vraiment nouvelles du meme cycle si
    elles etaient regroupees dans le meme appel. Meme parametre deja present
    et correct dans connecteur_supabase_precoms.enregistrer_precommande_alertes()
    -- oubli specifique a cette fonction-ci."""
    if not alertes or not supabase_url or not service_role_key:
        return []
    try:
        r = requests.post(
            f"{supabase_url.rstrip('/')}/rest/v1/watchlist_alerts",
            params={"on_conflict": "watchlist_item_id,url"},
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


CHAMPS_ALERTE_NOTIFICATION = "id,user_id,titre,prix,url,plateforme,push_envoye,email_envoye"


def lister_alertes_a_notifier(supabase_url: str, service_role_key: str) -> list[dict]:
    """Retourne TOUTES les alertes dont AU MOINS UN canal (push/email) n'a
    pas encore ete livre avec succes -- pas seulement celles inserees ce
    cycle. Corrige un bug reel trouve lors d'un audit externe du 30/08/2026 :
    enregistrer_alertes() ne renvoyait QUE les lignes fraichement inserees
    (resolution=ignore-duplicates), et notifications_saas.py n'etait appele
    qu'avec celles-ci -- si push ET email echouaient tous les deux au meme
    cycle (ex. panne SendGrid/service Web Push), la ligne restait en base mais
    n'etait plus JAMAIS retentee (les cycles suivants la voient comme un
    doublon deja connu). Necessite les colonnes push_envoye/email_envoye
    (cf. migration 0009 du depot pokedeals-saas) -- absentes -> la requete
    echoue proprement (log + liste vide), comme tout le reste du module."""
    if not supabase_url or not service_role_key:
        return []
    alertes: list[dict] = []
    offset = 0
    while True:
        try:
            r = requests.get(
                f"{supabase_url.rstrip('/')}/rest/v1/watchlist_alerts",
                params={
                    "select": CHAMPS_ALERTE_NOTIFICATION,
                    "or": "(push_envoye.eq.false,email_envoye.eq.false)",
                },
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
            log.warning("Lecture des alertes en attente de notification échouée (%s) -- %d déjà récupérée(s), le reste ignoré ce cycle",
                        e, len(alertes))
            break
        alertes.extend(page)
        if len(page) < TAILLE_PAGE_WATCHLIST:
            break
        offset += TAILLE_PAGE_WATCHLIST
    return alertes


def marquer_notification_envoyee(supabase_url: str, service_role_key: str, alerte_id: str, canal: str) -> None:
    """Marque UN canal ("push" ou "email") comme livre avec succes pour une
    alerte -- appele par notifications_saas.py apres chaque envoi reussi (ou
    determine sans objet, ex. aucun abonnement push). Erreur reseau : loguee
    et ignoree, la ligne restera simplement retentee au prochain cycle
    (comportement sur, jamais pire qu'avant ce correctif)."""
    if not supabase_url or not service_role_key or canal not in ("push", "email"):
        return
    try:
        r = requests.patch(
            f"{supabase_url.rstrip('/')}/rest/v1/watchlist_alerts",
            params={"id": f"eq.{alerte_id}"},
            json={f"{canal}_envoye": True},
            headers={
                "apikey": service_role_key,
                "Authorization": f"Bearer {service_role_key}",
                "Content-Type": "application/json",
            },
            timeout=TIMEOUT,
        )
        r.raise_for_status()
    except requests.RequestException as e:
        log.warning("Marquage de la notification %s comme envoyée échoué pour l'alerte %s (%s) -- retentée au prochain cycle",
                    canal, alerte_id, e)


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
