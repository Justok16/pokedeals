"""
Notifications personnalisees (push navigateur + email) pour les utilisateurs
du SaaS (saas/), envoyees pour toute alerte watchlist_alerts dont au moins
un canal n'est pas encore marque livre (push_envoye/email_envoye) -- cf.
connecteur_supabase.lister_alertes_a_notifier(). Chaque canal est marque
envoye INDIVIDUELLEMENT apres un succes (ou une situation "rien a livrer" :
pas d'abonnement push, email desactive par l'utilisateur), jamais les deux
ensemble -- corrige un bug reel trouve lors d'un audit externe du 30/08/2026 :
avant, seules les alertes fraichement inserees etaient notifiees ; si push
ET email echouaient tous les deux au meme cycle, l'alerte restait enregistree
en base mais n'etait plus jamais retentee.

Systeme optionnel et non bloquant, meme philosophie que
verification_photo.py/connecteur_supabase.py : chaque canal (push, email)
est actif independamment selon les secrets configures ; absent -> ce canal
est simplement saute. Toute erreur reseau/API est avalee (log + skip), ne
doit jamais faire echouer un cycle de scan.

Push : protocole Web Push (RFC 8291 chiffrement + RFC 8292 VAPID) via
pywebpush -- seule dependance ajoutee a requirements.txt pour cette
fonctionnalite. Contrairement aux autres modules de ce projet (qui evitent
les SDK au profit de requests brut, cf. verification_photo.py), reimplementer
ce chiffrement a la main serait un risque reel (protocole cryptographique,
erreur facile et silencieuse) -- pywebpush est la bibliotheque de reference,
largement utilisee, pas une dependance ajoutee a la legere.
Email : API HTTP SendGrid (https://docs.sendgrid.com/api-reference/mail-send/mail-send),
requete brute via requests, pas de SDK necessaire. Migre de Resend le
04/09/2026 : le compte Resend n'avait aucun domaine verifie (aucun nom de
domaine disponible cote Justok), donc tournait en mode sandbox
(onboarding@resend.dev) -- Resend restreint alors la livraison au seul email
du proprietaire du compte, expliquant pourquoi Justok recevait ses propres
alertes mais aucun autre utilisateur PokeDeals/PokePrecoms ne recevait quoi
que ce soit (confirme via les logs Resend : 403 Forbidden sur chaque
destinataire autre que Justok). SendGrid permet une verification "Single
Sender" gratuite sans domaine, avec une delivrabilite correcte (alignement
SPF/DKIM plus faible qu'un domaine verifie, mais fonctionnelle) -- solution
choisie par Justok en attendant un eventuel nom de domaine.
"""
from __future__ import annotations

import json
import logging

import requests

from telegram_utils import echapper_html, echapper_url_html

log = logging.getLogger("pokedeals.notifications_saas")

TIMEOUT = 10


def _headers(service_role_key: str) -> dict:
    return {"apikey": service_role_key, "Authorization": f"Bearer {service_role_key}"}


def _lister_abonnements_push(supabase_url: str, service_role_key: str, user_ids: list[str]) -> list[dict] | None:
    """Retourne les abonnements push (endpoint/p256dh/auth) des utilisateurs
    donnes. [] si aucun user_id, secrets absents, ou lecture reussie mais
    aucun abonnement -- None si la lecture a reellement echoue (reseau/API).

    Distinction ajoutee le 05/09/2026 (audit externe multi-IA, confirme par
    relecture directe du code) : avant, une panne reseau renvoyait aussi [],
    strictement indiscernable d'un "aucun abonnement" legitime cote appelant
    (notifier_alertes_en_attente() traite alors uid not in abonnements_par_
    utilisateur comme "rien a livrer, pas un echec" et marque le push comme
    envoye) -- un utilisateur ayant reellement un abonnement actif au moment
    d'une panne Supabase se voyait donc son push marque livre a tort, sans
    qu'aucun envoi n'ait eu lieu, et sans plus jamais etre retente. Meme
    classe de bug que le canari email Resend (cf. CLAUDE.md, "verification
    doit avoir un pouvoir de discrimination reel") mais cote lecture au lieu
    d'envoi."""
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
        return None


def _preferences_email(supabase_url: str, service_role_key: str, user_ids: list[str]) -> dict[str, bool] | None:
    """Retourne {user_id: notif_email actif}. Un utilisateur absent de la
    table (pas encore de préférence enregistrée) est considéré actif par
    défaut -- l'appelant doit donc faire .get(user_id, True), jamais un
    accès direct qui traiterait une absence comme désactivé. {} si aucun
    user_id/secrets absents ou lecture reussie sans aucune ligne -- None si
    la lecture a reellement echoue (meme distinction que
    _lister_abonnements_push() ci-dessus, meme raison : sans elle, une panne
    reseau pendant la lecture des préférences fait ignorer un opt-out email
    reel pour ce cycle)."""
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
        return None


def _email_utilisateur(supabase_url: str, service_role_key: str, user_id: str) -> str | None:
    """Récupère l'adresse email d'un utilisateur via l'API Admin Supabase
    (auth.users n'est jamais exposé via l'API REST standard, seulement via
    l'API Admin -- réservée à la clé service_role)."""
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
    """Purge un abonnement push expiré/révoqué côté navigateur (réponse 404/410
    du service de push) -- évite de le retenter indéfiniment à chaque alerte."""
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
) -> bool:
    """Retourne True si le push est "termine" pour cet utilisateur (livre
    avec succes sur tous les abonnements, et/ou abonnements expires purges),
    False si AU MOINS UN abonnement a echoue pour une raison transitoire --
    dans ce cas l'appelant ne doit PAS marquer le canal comme envoye, pour
    que le prochain cycle retente (cf. connecteur_supabase.marquer_notification_envoyee)."""
    from pywebpush import WebPushException, webpush

    payload = json.dumps({"title": titre, "body": corps, "url": url})
    echec_transitoire = False
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
                # Abonnement expiré/révoqué côté navigateur -- purge définitive,
                # jamais retenté (sinon échec silencieux répété à chaque cycle).
                _supprimer_abonnement_push(supabase_url, service_role_key, sub["endpoint"])
            else:
                log.warning("Envoi push échoué (%s) -- retenté au prochain cycle", e)
                echec_transitoire = True
    return not echec_transitoire


def _envoyer_email(
    sendgrid_api_key: str, sendgrid_from: str, destinataire: str, titre: str, corps: str, url: str,
    custom_args: dict[str, str] | None = None,
) -> bool:
    """Retourne True si l'email a bien été envoyé (accepté par SendGrid,
    202 -- pas de corps de réponse, cf. r.raise_for_status() qui ne lève
    que sur 4xx/5xx), False sinon -- l'appelant ne doit alors PAS marquer
    le canal comme envoyé, pour que le prochain cycle retente.

    `custom_args` (ajouté le 05/09/2026, cf. webhook SendGrid côté
    pokedeals-saas) : échoué tel quel par SendGrid dans chaque événement de
    livraison (delivered/bounce/spamreport/...) -- permet de corréler un
    événement reçu par le webhook à l'alerte/canari précis qui l'a déclenché,
    plutôt que de seulement savoir que l'appel API a été accepté. Valeurs
    OBLIGATOIREMENT des chaînes (contrainte SendGrid)."""
    payload = {
        "personalizations": [{"to": [{"email": destinataire}]}],
        "from": {"email": sendgrid_from},
        "subject": titre,
        "content": [
            {"type": "text/plain", "value": f"{corps}\n\nVoir l'annonce : {url}"},
            {"type": "text/html", "value": f"<p>{echapper_html(corps)}</p><p><a href=\"{echapper_url_html(url)}\">Voir l'annonce</a></p>"},
        ],
    }
    if custom_args:
        payload["custom_args"] = custom_args
    try:
        r = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={
                "Authorization": f"Bearer {sendgrid_api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return True
    except requests.RequestException as e:
        log.warning("Envoi email échoué (%s) -- retenté au prochain cycle", e)
        return False


def notifier_alertes_en_attente(secrets: dict, alertes_en_attente: list[dict]) -> None:
    """Point d'entrée unique, appelé avec connecteur_supabase.lister_alertes_a_notifier()
    -- TOUTES les alertes dont au moins un canal n'est pas encore livré, pas
    seulement celles insérées ce cycle (corrige un bug réel trouvé lors d'un
    audit externe du 30/08/2026 : si push ET email échouaient tous les deux
    au même cycle, l'alerte n'était plus jamais retentée, cf. docstring de
    connecteur_supabase.lister_alertes_a_notifier). Chaque alerte porte
    `push_envoye`/`email_envoye` : un canal déjà livré est sauté, jamais
    renvoyé une deuxième fois. Après un envoi réussi (ou déterminé sans
    objet -- pas d'abonnement push, email désactivé par l'utilisateur), le
    canal est marqué envoyé via connecteur_supabase.marquer_notification_envoyee()."""
    if not alertes_en_attente:
        return

    supabase_url = secrets.get("SUPABASE_URL", "")
    service_role_key = secrets.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not supabase_url or not service_role_key:
        return

    vapid_private_key = secrets.get("VAPID_PRIVATE_KEY", "")
    vapid_claim_email = secrets.get("VAPID_CLAIM_EMAIL", "")
    sendgrid_api_key = secrets.get("SENDGRID_API_KEY", "")
    sendgrid_from = secrets.get("SENDGRID_FROM_EMAIL", "")

    push_actif = bool(vapid_private_key and vapid_claim_email)
    email_actif = bool(sendgrid_api_key and sendgrid_from)
    if not push_actif and not email_actif:
        return

    # Import tardif : connecteur_supabase importe deja notifications_saas
    # ailleurs dans le pipeline (watchlist_saas.py) -- eviter tout risque
    # d'import circulaire au chargement du module.
    from connecteur_supabase import marquer_notification_envoyee

    user_ids = sorted({a["user_id"] for a in alertes_en_attente})

    # push_lecture_ok/email_lecture_ok distinguent une lecture reussie (meme
    # vide) d'une lecture ratee (None, cf. docstrings de _lister_abonnements_
    # push()/_preferences_email()) -- une lecture ratee desactive le canal
    # pour ce cycle SANS rien marquer envoye, pour que l'alerte soit retentee
    # au prochain cycle (cf. lister_alertes_a_notifier) plutot que consideree
    # a tort comme "rien a livrer".
    abonnements_par_utilisateur: dict[str, list[dict]] = {}
    push_lecture_ok = True
    if push_actif:
        resultat_push = _lister_abonnements_push(supabase_url, service_role_key, user_ids)
        if resultat_push is None:
            push_lecture_ok = False
        else:
            for sub in resultat_push:
                abonnements_par_utilisateur.setdefault(sub["user_id"], []).append(sub)

    prefs_email: dict[str, bool] = {}
    email_lecture_ok = True
    if email_actif:
        resultat_prefs = _preferences_email(supabase_url, service_role_key, user_ids)
        if resultat_prefs is None:
            email_lecture_ok = False
        else:
            prefs_email = resultat_prefs

    emails_cache: dict[str, str | None] = {}

    for alerte in alertes_en_attente:
        uid = alerte["user_id"]
        titre_notif = f"Bonne affaire PokéDeals : {alerte.get('titre', 'une carte')[:80]}"
        corps = f"{float(alerte['prix']):.2f}€"
        if alerte.get("plateforme"):
            corps += f" sur {alerte['plateforme']}"

        if push_actif and push_lecture_ok and not alerte.get("push_envoye"):
            if uid in abonnements_par_utilisateur:
                reussi = _envoyer_push(
                    supabase_url, service_role_key, vapid_private_key, vapid_claim_email,
                    abonnements_par_utilisateur[uid], titre_notif, corps, alerte["url"],
                )
            else:
                reussi = True  # aucun abonnement push -- rien a livrer, pas un echec
            if reussi:
                marquer_notification_envoyee(supabase_url, service_role_key, alerte["id"], "push")

        if email_actif and email_lecture_ok and not alerte.get("email_envoye"):
            if not prefs_email.get(uid, True):
                # Notifications email desactivees par l'utilisateur -- rien a
                # livrer par choix de l'utilisateur, pas un echec.
                marquer_notification_envoyee(supabase_url, service_role_key, alerte["id"], "email")
            else:
                if uid not in emails_cache:
                    emails_cache[uid] = _email_utilisateur(supabase_url, service_role_key, uid)
                email = emails_cache[uid]
                if email and _envoyer_email(
                    sendgrid_api_key, sendgrid_from, email, titre_notif, corps, alerte["url"],
                    custom_args={"produit": "pokedeals", "type_notification": "alerte", "reference_id": str(alerte["id"])},
                ):
                    marquer_notification_envoyee(supabase_url, service_role_key, alerte["id"], "email")


def notifier_transition_verification(secrets: dict, user_id: str, titre_notif: str, corps: str, url: str) -> None:
    """Envoie une notification push+email PONCTUELLE à UN utilisateur, pour
    un événement de VÉRIFICATION périodique (03/09/2026, cf.
    verification_alertes.detecter_transition()/verifier_alertes_watchlist.py) --
    pas une nouvelle bonne affaire (notifier_alertes_en_attente() ci-dessus).

    Différence volontaire avec notifier_alertes_en_attente() : PAS de
    colonnes `push_envoye`/`email_envoye` équivalentes ici -- watchlist_alerts
    n'a rien de tel pour cet événement, et n'en a pas besoin : c'est
    detecter_transition() (comparaison à l'état PRÉCÉDENT de la ligne) qui
    garantit qu'une même transition n'est détectée qu'une seule fois, pas un
    mécanisme de retry basé sur une colonne "livré". Un échec d'envoi ici
    (secret absent, réseau, abonnement expiré...) n'est donc PAS retenté au
    prochain cycle -- best-effort, jamais bloquant, même philosophie que
    tout le reste de ce module et de verification_alertes.py (cf. leurs
    docstrings) : une notification manquée n'empêche jamais le radar de
    continuer, et ne fait jamais échouer le cycle."""
    if not user_id:
        return

    supabase_url = secrets.get("SUPABASE_URL", "")
    service_role_key = secrets.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not supabase_url or not service_role_key:
        return

    vapid_private_key = secrets.get("VAPID_PRIVATE_KEY", "")
    vapid_claim_email = secrets.get("VAPID_CLAIM_EMAIL", "")
    sendgrid_api_key = secrets.get("SENDGRID_API_KEY", "")
    sendgrid_from = secrets.get("SENDGRID_FROM_EMAIL", "")

    push_actif = bool(vapid_private_key and vapid_claim_email)
    email_actif = bool(sendgrid_api_key and sendgrid_from)
    if not push_actif and not email_actif:
        return

    if push_actif:
        abonnements = _lister_abonnements_push(supabase_url, service_role_key, [user_id])
        if abonnements:
            _envoyer_push(
                supabase_url, service_role_key, vapid_private_key, vapid_claim_email,
                abonnements, titre_notif, corps, url,
            )

    if email_actif:
        prefs = _preferences_email(supabase_url, service_role_key, [user_id])
        if (prefs or {}).get(user_id, True):
            email = _email_utilisateur(supabase_url, service_role_key, user_id)
            if email:
                _envoyer_email(
                    sendgrid_api_key, sendgrid_from, email, titre_notif, corps, url,
                    custom_args={"produit": "pokedeals", "type_notification": "verification"},
                )
