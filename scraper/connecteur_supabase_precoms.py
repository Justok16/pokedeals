"""
Pont scraper -> Supabase PokePrecoms (depot separe justok16/pokeprecoms) :
enregistre les precommandes generiques reellement detectees (transition
"pas en stock" -> "en stock", cf. radar_precommande_generique.py) dans la
table `precommande_alerts`, et notifie TOUS les utilisateurs PokePrecoms
inscrits -- service 100% gratuit et illimite depuis le 28/08/2026 (decision
de Justok, plus d'abonnement payant du tout), modele BROADCAST (pas de
watchlist personnalisee cote PokePrecoms, contrairement a
connecteur_supabase.py/watchlist_saas.py cote PokeDeals : chaque utilisateur
inscrit recoit TOUTES les alertes, pas de correspondance a calculer).

Systeme optionnel et non bloquant, meme philosophie que connecteur_supabase.py/
notifications_saas.py : actif uniquement si POKEPRECOMS_SUPABASE_URL/
POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY sont configures -- secrets DISTINCTS de
SUPABASE_URL/SUPABASE_SERVICE_ROLE_KEY (qui pointent vers le projet Supabase
de pokedeals-saas, un projet DIFFERENT). Toute erreur reseau/API est avalee
(log + no-op), ne doit jamais faire echouer un cycle de scan.

Notifications push/email : reutilisent VAPID_PRIVATE_KEY/VAPID_CLAIM_EMAIL/
SENDGRID_API_KEY/SENDGRID_FROM_EMAIL -- MEMES secrets que notifications_saas.py
(meme paire de cles VAPID et meme compte SendGrid reutilises entre les deux
produits, decision explicite de Justok le 23/08/2026 pour eviter de gerer
deux jeux de credentials en parallele -- changeable plus tard si besoin
d'isoler les deux identites push/email). Migre de Resend a SendGrid le
04/09/2026, cf. docstring de notifications_saas.py pour le detail du bug
corrige (mode sandbox Resend sans domaine verifie -> emails livres au seul
proprietaire du compte, pas aux autres utilisateurs).
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
) -> list[dict] | None:
    """Insere les evenements de precommande detectes dans `precommande_alerts`.
    Deduplique sur `url_produit` (contrainte unique cote base, cf. migration
    0005_precommande_alerts_unique_url.sql du depot pokeprecoms -- une meme
    fiche produit ne peut jamais generer 2 lignes, meme si ce pont est appele
    deux fois sur le meme evenement). Retourne UNIQUEMENT les lignes
    reellement inserees (return=representation + resolution=ignore-duplicates)
    -- ne PAS utiliser cette valeur pour decider quoi diffuser (cf. piege
    corrige le 30/08/2026, meme bug que watchlist_alerts cote PokeDeals) :
    appeler lister_precommandes_a_diffuser() juste apres pour ca.

    Distingue explicitement (meme idiome que memoire_supabase.charger_memoire_supabase)
    un ECHEC REEL (retourne `None`) d'un NO-OP LEGITIME (`[]` -- secrets absents,
    aucun evenement a inserer, ou insertion reussie sans aucune ligne nouvelle
    car tout etait deja connu cote base) : corrige un bug reel trouve le
    31/08/2026 (signalement direct de Justok, "j'ai recu des alertes Telegram
    mais rien sur mon Dashboard") ou une erreur reseau ici (retournait `[]`,
    indistinguable d'un no-op) survenant le MEME cycle qu'un envoi Telegram
    reussi laissait l'appelant (scan_precommandes_generique.py/
    scan_precommandes_philibert.py) commiter quand meme l'evenement dans la
    memoire locale de deduplication (via envoyer_telegram_precommandes_generiques) --
    empechant alors DEFINITIVEMENT toute nouvelle tentative d'ecriture Supabase
    pour cet evenement precis (la transition "pas en stock -> en stock" ne se
    reproduit jamais une 2e fois pour le meme produit). L'appelant doit
    utiliser `None` pour annuler le commit memoire de Telegram sur les
    evenements concernes, afin qu'ils soient redetectes et retentes (les deux
    canaux, doublon Telegram accepte) au prochain cycle."""
    if not evenements or not supabase_url or not service_role_key:
        return []
    lignes = [
        {
            "titre_produit": e["titre"][:500],
            "boutique": e["domaine"],
            "url_produit": e["url_produit"],
            "prix": e.get("prix"),
            "categorie": e.get("categorie"),
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
        log.warning("Écriture precommande_alerts échouée (%s) -- retentée au prochain cycle", e)
        return None


CHAMPS_PRECOMMANDE_DIFFUSION = "id,titre_produit,boutique,url_produit,push_diffuse,email_diffuse"
TAILLE_PAGE_DIFFUSION = 1000  # limite par defaut de PostgREST/Supabase par requete


def lister_precommandes_a_diffuser(supabase_url: str, service_role_key: str) -> list[dict]:
    """Retourne TOUTES les precommandes dont AU MOINS UN canal (push/email)
    n'a pas encore ete diffuse avec succes a tous les abonnes -- pas
    seulement celles inserees ce cycle. Corrige un bug reel trouve lors d'un
    audit externe du 30/08/2026 (meme bug que celui deja corrige cote
    watchlist_alerts/PokeDeals) : si push ET email echouaient tous les deux
    au meme cycle, la precommande n'etait plus jamais rediffusee. Necessite
    les colonnes push_diffuse/email_diffuse (cf. migration 0007 du depot
    pokeprecoms) -- absentes -> la requete echoue proprement (log + liste
    vide)."""
    if not supabase_url or not service_role_key:
        return []
    precommandes: list[dict] = []
    offset = 0
    while True:
        try:
            r = requests.get(
                f"{supabase_url.rstrip('/')}/rest/v1/precommande_alerts",
                params={
                    "select": CHAMPS_PRECOMMANDE_DIFFUSION,
                    "or": "(push_diffuse.eq.false,email_diffuse.eq.false)",
                },
                headers={
                    **_headers(service_role_key),
                    "Range": f"{offset}-{offset + TAILLE_PAGE_DIFFUSION - 1}",
                },
                timeout=TIMEOUT,
            )
            r.raise_for_status()
            page = r.json()
        except requests.RequestException as e:
            log.warning("Lecture des précommandes en attente de diffusion échouée (%s) -- %d déjà récupérée(s), le reste ignoré ce cycle",
                        e, len(precommandes))
            break
        precommandes.extend(page)
        if len(page) < TAILLE_PAGE_DIFFUSION:
            break
        offset += TAILLE_PAGE_DIFFUSION
    return precommandes


def marquer_diffusion_terminee(supabase_url: str, service_role_key: str, precommande_id: str, canal: str) -> None:
    """Marque UN canal ("push" ou "email") comme diffuse avec succes pour une
    precommande -- appele par notifier_abonnes_precoms() une fois que TOUS
    les envois de ce canal ont reussi pour ce cycle (modele broadcast, cf.
    migration 0007). Erreur reseau : loguee et ignoree, la ligne sera
    simplement retentee au prochain cycle."""
    if not supabase_url or not service_role_key or canal not in ("push", "email"):
        return
    try:
        r = requests.patch(
            f"{supabase_url.rstrip('/')}/rest/v1/precommande_alerts",
            params={"id": f"eq.{precommande_id}"},
            json={f"{canal}_diffuse": True},
            headers={
                **_headers(service_role_key),
                "Content-Type": "application/json",
            },
            timeout=TIMEOUT,
        )
        r.raise_for_status()
    except requests.RequestException as e:
        log.warning("Marquage de la diffusion %s comme terminée échoué pour la précommande %s (%s) -- retentée au prochain cycle",
                    canal, precommande_id, e)


def _lister_tous_utilisateurs(supabase_url: str, service_role_key: str) -> list[str]:
    """user_id de TOUS les comptes inscrits, via l'API Admin Supabase paginee
    (`auth.users` n'est jamais expose par l'API REST standard). Service
    100% gratuit et illimite (28/08/2026) -- modele broadcast, chaque
    utilisateur inscrit recoit TOUTES les alertes, plus de notion
    d'abonnement actif a filtrer."""
    if not supabase_url or not service_role_key:
        return []
    user_ids: list[str] = []
    page = 1
    try:
        while True:
            r = requests.get(
                f"{supabase_url.rstrip('/')}/auth/v1/admin/users",
                params={"page": page, "per_page": 1000},
                headers=_headers(service_role_key),
                timeout=TIMEOUT,
            )
            r.raise_for_status()
            lot = r.json().get("users", [])
            if not lot:
                break
            user_ids.extend(u["id"] for u in lot)
            if len(lot) < 1000:
                break
            page += 1
        return user_ids
    except requests.RequestException as e:
        log.warning("Lecture des utilisateurs inscrits échouée (%s) -- ignorée ce cycle", e)
        return []


def _lister_abonnements_push(supabase_url: str, service_role_key: str, user_ids: list[str]) -> list[dict] | None:
    """[] si aucun user_id/secrets absents ou lecture reussie sans abonnement
    -- None si la lecture a reellement echoue (reseau/API). Distinction
    ajoutee le 05/09/2026 (audit externe multi-IA) : sans elle, une panne au
    moment de cette lecture faisait passer TOUS les user_ids pour "sans
    abonnement" dans diffuser_precommande_a_tous() ci-dessous -- aucun push
    n'etait alors tente pour PERSONNE, mais le canal push du broadcast entier
    etait quand meme marque diffuse (echec_push jamais mis a True puisque
    aucun envoi n'etait meme tente), empechant tout retry au cycle suivant.
    Meme correctif applique en parallele a notifications_saas.py
    (justok16/pokedeals, meme audit)."""
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
    table (pas encore de preference enregistree) est considere actif par
    defaut -- l'appelant doit donc faire .get(user_id, True). {} si aucun
    user_id/secrets absents ou lecture reussie sans aucune ligne -- None si
    la lecture a reellement echoue (meme raison que _lister_abonnements_push()
    ci-dessus)."""
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
) -> bool:
    """Retourne True si AUCUN abonnement n'a echoue pour une raison
    transitoire (succes et/ou purge d'abonnements expires uniquement) --
    False si au moins un echec transitoire, pour que l'appelant sache qu'il
    ne doit pas marquer le canal comme diffuse (cf. marquer_diffusion_terminee)."""
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
                _supprimer_abonnement_push(supabase_url, service_role_key, sub["endpoint"])
            else:
                log.warning("Envoi push échoué (%s) -- retenté au prochain cycle", e)
                echec_transitoire = True
    return not echec_transitoire


def _envoyer_email(
    sendgrid_api_key: str, sendgrid_from: str, destinataire: str, titre: str, corps: str, url: str,
    custom_args: dict[str, str] | None = None,
) -> bool:
    """Retourne True si l'email a été accepté par SendGrid (202, pas de
    corps de réponse), False sinon.

    `custom_args` (ajouté le 05/09/2026, cf. webhook SendGrid côté
    pokedeals-saas, même correctif que notifications_saas.py) : échoué tel
    quel par SendGrid dans chaque événement de livraison -- permet de
    corréler un événement reçu par le webhook à la précommande précise qui
    l'a déclenché. Valeurs OBLIGATOIREMENT des chaînes (contrainte SendGrid)."""
    from telegram_utils import echapper_html, echapper_url_html

    payload = {
        "personalizations": [{"to": [{"email": destinataire}]}],
        "from": {"email": sendgrid_from},
        "subject": titre,
        "content": [
            {"type": "text/plain", "value": f"{corps}\n\nVoir la fiche produit : {url}"},
            {"type": "text/html", "value": f"<p>{echapper_html(corps)}</p><p><a href=\"{echapper_url_html(url)}\">Voir la fiche produit</a></p>"},
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


def notifier_abonnes_precoms(secrets: dict, precommandes_a_diffuser: list[dict]) -> None:
    """Point d'entrée unique, appelé avec lister_precommandes_a_diffuser() --
    TOUTES les précommandes dont au moins un canal n'est pas encore diffusé,
    pas seulement celles insérées ce cycle (corrige un bug réel trouvé lors
    d'un audit externe du 30/08/2026, même bug que celui déjà corrigé côté
    watchlist_alerts/PokéDeals). Notifie TOUS les utilisateurs PokéPrécoms
    inscrits par push (si abonné) et/ou email (si activé, actif par défaut)
    -- modèle broadcast, pas de correspondance individuelle à calculer, plus
    de notion d'abonnement payant (service gratuit et illimité depuis le
    28/08/2026). Un canal n'est marqué diffusé (via marquer_diffusion_terminee)
    que si AUCUN envoi de ce canal n'a échoué pour ce cycle -- un seul échec
    individuel fait retenter tout le canal au prochain cycle (modèle broadcast,
    cf. docstring de la migration : plus simple qu'un suivi par utilisateur,
    au prix d'un risque de doublon plutôt que d'une alerte jamais reçue)."""
    if not precommandes_a_diffuser:
        return

    supabase_url = secrets.get("POKEPRECOMS_SUPABASE_URL", "")
    service_role_key = secrets.get("POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY", "")
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

    user_ids = _lister_tous_utilisateurs(supabase_url, service_role_key)
    if not user_ids:
        return

    # push_lecture_ok/email_lecture_ok distinguent une lecture reussie (meme
    # vide) d'une lecture ratee (None) -- une lecture ratee desactive le
    # canal pour ce cycle SANS jamais appeler marquer_diffusion_terminee,
    # pour que le broadcast entier soit retente au prochain cycle plutot que
    # declare diffuse a tort (cf. docstrings de _lister_abonnements_push()/
    # _preferences_email() ci-dessus).
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

    for precommande in precommandes_a_diffuser:
        titre_notif = "Nouvelle précommande Pokémon TCG disponible !"
        corps = precommande.get("titre_produit", "un produit")
        if precommande.get("boutique"):
            corps += f" sur {precommande['boutique']}"
        url = precommande.get("url_produit", "")

        if push_actif and push_lecture_ok and not precommande.get("push_diffuse"):
            echec_push = False
            for uid in user_ids:
                if uid in abonnements_par_utilisateur:
                    if not _envoyer_push(
                        supabase_url, service_role_key, vapid_private_key, vapid_claim_email,
                        abonnements_par_utilisateur[uid], titre_notif, corps, url,
                    ):
                        echec_push = True
            if not echec_push:
                marquer_diffusion_terminee(supabase_url, service_role_key, precommande["id"], "push")

        if email_actif and email_lecture_ok and not precommande.get("email_diffuse"):
            echec_email = False
            for uid in user_ids:
                if prefs_email.get(uid, True):
                    if uid not in emails_cache:
                        emails_cache[uid] = _email_utilisateur(supabase_url, service_role_key, uid)
                    email = emails_cache[uid]
                    if email and not _envoyer_email(
                        sendgrid_api_key, sendgrid_from, email, titre_notif, corps, url,
                        custom_args={"produit": "pokeprecoms", "type_notification": "precommande", "reference_id": str(precommande["id"])},
                    ):
                        echec_email = True
            if not echec_email:
                marquer_diffusion_terminee(supabase_url, service_role_key, precommande["id"], "email")
