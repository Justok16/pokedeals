"""
Pont scraper -> Supabase PokePrecoms (depot separe justok16/pokeprecoms) :
enregistre les precommandes generiques reellement detectees (transition
"pas en stock" -> "en stock", cf. radar_precommande_generique.py) dans la
table `precommande_alerts`, et notifie TOUS les abonnes PokePrecoms actifs
(modele BROADCAST -- pas de watchlist personnalisee cote PokePrecoms,
contrairement a connecteur_supabase.py/watchlist_saas.py cote PokeDeals :
chaque abonne actif recoit TOUTES les alertes, pas de correspondance a
calculer).

Systeme optionnel et non bloquant, meme philosophie que connecteur_supabase.py/
notifications_saas.py : actif uniquement si POKEPRECOMS_SUPABASE_URL/
POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY sont configures -- secrets DISTINCTS de
SUPABASE_URL/SUPABASE_SERVICE_ROLE_KEY (qui pointent vers le projet Supabase
de pokedeals-saas, un projet DIFFERENT). Toute erreur reseau/API est avalee
(log + no-op), ne doit jamais faire echouer un cycle de scan.

Notifications push/email : reutilisent VAPID_PRIVATE_KEY/VAPID_CLAIM_EMAIL/
RESEND_API_KEY/RESEND_FROM_EMAIL -- MEMES secrets que notifications_saas.py
(meme paire de cles VAPID et meme compte Resend reutilises entre les deux
produits, decision explicite de Justok le 23/08/2026 pour eviter de gerer
deux jeux de credentials en parallele -- changeable plus tard si besoin
d'isoler les deux identites push/email).
"""
from __future__ import annotations

import json
import logging

import requests

log = logging.getLogger("pokedeals.connecteur_supabase_precoms")

TIMEOUT = 10


def _headers(service_role_key: str) -> dict:
    return {"apikey": service_role_key, "Authorization": f"Bearer {service_role_key}"}


def enregistrer_precommande_alertes(
    supabase_url: str, service_role_key: str, evenements: list[dict]
) -> list[dict]:
    """Insere les evenements de precommande detectes dans `precommande_alerts`.
    Deduplique sur `url_produit` (contrainte unique cote base, cf. migration
    0005_precommande_alerts_unique_url.sql du depot pokeprecoms -- une meme
    fiche produit ne peut jamais generer 2 lignes, meme si ce pont est appele
    deux fois sur le meme evenement). Retourne UNIQUEMENT les lignes
    reellement inserees (return=representation + resolution=ignore-duplicates)
    -- utilise par notifier_abonnes_precoms() pour ne notifier qu'une fois
    par alerte reellement nouvelle."""
    if not evenements or not supabase_url or not service_role_key:
        return []
    lignes = [
        {
            "titre_produit": e["titre"][:500],
            "boutique": e["domaine"],
            "url_produit": e["url_produit"],
            "prix": e.get("prix"),
        }
        for e in evenements
    ]
    try:
        r = requests.post(
            f"{supabase_url.rstrip('/')}/rest/v1/precommande_alerts",
            params={"on_conflict": "url_produit"},
            json=lignes,
            headers={
                **_headers(service_role_key),
                "Content-Type": "application/json",
                "Prefer": "return=representation,resolution=ignore-duplicates",
            },
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        nouvelles = r.json()
        log.info("[Supabase PokePrecoms] %d précommande(s) enregistrée(s)", len(nouvelles))
        return nouvelles
    except requests.RequestException as e:
        log.warning("Écriture precommande_alerts échouée (%s) -- ignorée ce cycle", e)
        return []


def _lister_abonnes_actifs(supabase_url: str, service_role_key: str) -> list[str]:
    """user_id de tous les abonnements Stripe actifs (`subscriptions.status`
    in ('active', 'trialing')) -- modele broadcast, TOUS les abonnes actifs
    recoivent TOUTES les alertes."""
    if not supabase_url or not service_role_key:
        return []
    try:
        r = requests.get(
            f"{supabase_url.rstrip('/')}/rest/v1/subscriptions",
            params={"select": "user_id", "status": "in.(active,trialing)"},
            headers=_headers(service_role_key),
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return [row["user_id"] for row in r.json()]
    except requests.RequestException as e:
        log.warning("Lecture des abonnés actifs échouée (%s) -- ignorée ce cycle", e)
        return []


def _lister_abonnements_push(supabase_url: str, service_role_key: str, user_ids: list[str]) -> list[dict]:
    if not user_ids or not supabase_url or not service_role_key:
        return []
    try:
        r = requests.get(
            f"{supabase_url.rstrip('/')}/rest/v1/push_subscriptions",
            params={
                "select": "user_id,endpoint,p256dh,auth",
                "user_id": f"in.({','.join(user_ids)})",
            },
            headers=_headers(service_role_key),
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        log.warning("Lecture des abonnements push échouée (%s) -- ignorée ce cycle", e)
        return []


def _preferences_email(supabase_url: str, service_role_key: str, user_ids: list[str]) -> dict[str, bool]:
    """Retourne {user_id: notif_email actif}. Un utilisateur absent de la
    table (pas encore de preference enregistree) est considere actif par
    defaut -- l'appelant doit donc faire .get(user_id, True)."""
    if not user_ids or not supabase_url or not service_role_key:
        return {}
    try:
        r = requests.get(
            f"{supabase_url.rstrip('/')}/rest/v1/user_preferences",
            params={
                "select": "user_id,notif_email",
                "user_id": f"in.({','.join(user_ids)})",
            },
            headers=_headers(service_role_key),
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return {row["user_id"]: row["notif_email"] for row in r.json()}
    except requests.RequestException as e:
        log.warning("Lecture des préférences email échouée (%s) -- ignorée ce cycle", e)
        return {}


def _email_utilisateur(supabase_url: str, service_role_key: str, user_id: str) -> str | None:
    """Récupère l'adresse email d'un utilisateur via l'API Admin Supabase
    (auth.users n'est jamais exposé via l'API REST standard)."""
    try:
        r = requests.get(
            f"{supabase_url.rstrip('/')}/auth/v1/admin/users/{user_id}",
            headers=_headers(service_role_key),
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return r.json().get("email")
    except requests.RequestException as e:
        log.warning("Récupération de l'email utilisateur échouée (%s)", e)
        return None


def _supprimer_abonnement_push(supabase_url: str, service_role_key: str, endpoint: str) -> None:
    """Purge un abonnement push expiré/révoqué côté navigateur (réponse
    404/410 du service de push) -- évite de le retenter indéfiniment."""
    try:
        requests.delete(
            f"{supabase_url.rstrip('/')}/rest/v1/push_subscriptions",
            params={"endpoint": f"eq.{endpoint}"},
            headers=_headers(service_role_key),
            timeout=TIMEOUT,
        )
    except requests.RequestException as e:
        log.warning("Purge d'un abonnement push expiré échouée (%s)", e)


def _envoyer_push(
    supabase_url: str,
    service_role_key: str,
    vapid_private_key: str,
    vapid_claim_email: str,
    abonnements: list[dict],
    titre: str,
    corps: str,
    url: str,
) -> None:
    from pywebpush import WebPushException, webpush

    payload = json.dumps({"title": titre, "body": corps, "url": url})
    for sub in abonnements:
        try:
            webpush(
                subscription_info={
                    "endpoint": sub["endpoint"],
                    "keys": {"p256dh": sub["p256dh"], "auth": sub["auth"]},
                },
                data=payload,
                vapid_private_key=vapid_private_key,
                vapid_claims={"sub": f"mailto:{vapid_claim_email}"},
                timeout=TIMEOUT,
            )
        except WebPushException as e:
            statut = e.response.status_code if e.response is not None else None
            if statut in (404, 410):
                _supprimer_abonnement_push(supabase_url, service_role_key, sub["endpoint"])
            else:
                log.warning("Envoi push échoué (%s) -- ignoré ce cycle", e)


def _envoyer_email(resend_api_key: str, resend_from: str, destinataire: str, titre: str, corps: str, url: str) -> None:
    from telegram_utils import echapper_html, echapper_url_html

    try:
        r = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {resend_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "from": resend_from,
                "to": [destinataire],
                "subject": titre,
                "text": f"{corps}\n\nVoir la fiche produit : {url}",
                "html": f"<p>{echapper_html(corps)}</p><p><a href=\"{echapper_url_html(url)}\">Voir la fiche produit</a></p>",
            },
            timeout=TIMEOUT,
        )
        r.raise_for_status()
    except requests.RequestException as e:
        log.warning("Envoi email échoué (%s) -- ignoré ce cycle", e)


def notifier_abonnes_precoms(secrets: dict, nouvelles_precommandes: list[dict]) -> None:
    """Point d'entrée unique, appelé juste après enregistrer_precommande_alertes()
    avec UNIQUEMENT les lignes qu'elle a retournées (les nouvelles, jamais les
    doublons déjà connus). Notifie TOUS les abonnés PokePrécoms actifs par
    push (si abonné) et/ou email (si activé, actif par défaut) -- modèle
    broadcast, pas de correspondance individuelle à calculer."""
    if not nouvelles_precommandes:
        return

    supabase_url = secrets.get("POKEPRECOMS_SUPABASE_URL", "")
    service_role_key = secrets.get("POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY", "")
    if not supabase_url or not service_role_key:
        return

    vapid_private_key = secrets.get("VAPID_PRIVATE_KEY", "")
    vapid_claim_email = secrets.get("VAPID_CLAIM_EMAIL", "")
    resend_api_key = secrets.get("RESEND_API_KEY", "")
    resend_from = secrets.get("RESEND_FROM_EMAIL", "")

    push_actif = bool(vapid_private_key and vapid_claim_email)
    email_actif = bool(resend_api_key and resend_from)
    if not push_actif and not email_actif:
        return

    user_ids = _lister_abonnes_actifs(supabase_url, service_role_key)
    if not user_ids:
        return

    abonnements_par_utilisateur: dict[str, list[dict]] = {}
    if push_actif:
        for sub in _lister_abonnements_push(supabase_url, service_role_key, user_ids):
            abonnements_par_utilisateur.setdefault(sub["user_id"], []).append(sub)

    prefs_email = _preferences_email(supabase_url, service_role_key, user_ids) if email_actif else {}
    emails_cache: dict[str, str | None] = {}

    for precommande in nouvelles_precommandes:
        titre_notif = "Nouvelle précommande Pokémon TCG disponible !"
        corps = precommande.get("titre_produit", "un produit")
        if precommande.get("boutique"):
            corps += f" sur {precommande['boutique']}"
        url = precommande.get("url_produit", "")

        for uid in user_ids:
            if push_actif and uid in abonnements_par_utilisateur:
                _envoyer_push(
                    supabase_url, service_role_key, vapid_private_key, vapid_claim_email,
                    abonnements_par_utilisateur[uid], titre_notif, corps, url,
                )

            if email_actif and prefs_email.get(uid, True):
                if uid not in emails_cache:
                    emails_cache[uid] = _email_utilisateur(supabase_url, service_role_key, uid)
                email = emails_cache[uid]
                if email:
                    _envoyer_email(resend_api_key, resend_from, email, titre_notif, corps, url)
