"""Canari de livraison push -- verification periodique que le pipeline Web
Push (VAPID + pywebpush + service de push du navigateur) fonctionne
reellement, symetrique a verification_email_canari.py.

Ajoute le 05/09/2026, suite a un audit approfondi demande par Justok apres
le bug Resend (aucun canari n'existait pour le push, seulement pour
l'email -- angle mort symetrique). Contrairement au canari email, qui
envoie vers un destinataire DISTINCT du compte d'envoi (le point precis qui
avait revele le bug Resend en sandbox), un canari push n'a pas cet
equivalent : un abonnement push appartient forcement a UN navigateur/
appareil precis, deja associe a UN compte utilisateur. Le pouvoir de
discrimination ici est different mais reel : verifier PERIODIQUEMENT et
AUTOMATIQUEMENT qu'un push arrive encore a etre accepte par le service de
push (VAPID valide, secrets corrects, pywebpush fonctionnel) sans attendre
qu'un vrai utilisateur reçoive une vraie alerte -- utile precisement parce
que l'usage reel est encore faible (peu d'alertes generees), donc peu
d'occasions de detecter une regression silencieuse (ex. VAPID_PRIVATE_KEY
mal renseigne apres une rotation de secret) autrement qu'en attendant
qu'un utilisateur signale ne rien recevoir.

Reutilise LITTERALEMENT `_envoyer_push`/`_lister_abonnements_push` de
notifications_saas.py (pas une reimplementation), meme raison que le
canari email : exercer le meme chemin de code que la production.

Piege connu et gere explicitement : `_envoyer_push()` retourne True a la
fois pour "livre avec succes" ET pour "abonnement expire, purge" (cf. sa
docstring) -- un abonnement canari qui se desabonne silencieusement (ex.
Justok change de navigateur) ne doit PAS se traduire par un "succes"
indefiniment. Corrige ici en verifiant D'ABORD qu'un abonnement existe
encore pour l'utilisateur canari avant d'envoyer -- son absence est traitee
comme un echec (canari casse), distinct de secrets absents (canari non
configure, cf. verifier_livraison -> None)."""
from __future__ import annotations

import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memoire_supabase import charger_memoire_supabase, sauvegarder_memoire_supabase
from notifications_saas import _envoyer_push, _lister_abonnements_push
from watchdog_workflows import envoyer_telegram

log = logging.getLogger("pokedeals.verification_push_canari")

CLE_MEMOIRE = "push_canari_etat"
TITRE_CANARI = "Canari PokéDeals -- vérification push"
CORPS_CANARI = (
    "Envoyé automatiquement toutes les quelques heures pour vérifier que "
    "les notifications push fonctionnent réellement. Si tu reçois ce "
    "message à intervalles réguliers, tout va bien, rien à faire."
)
URL_CANARI = "https://pokedeals.app"


def verifier_livraison(
    supabase_url: str, service_role_key: str, vapid_private_key: str, vapid_claim_email: str, user_id: str
) -> bool | None:
    """Retourne True/False (succès/échec réel), ou None si le canari n'est
    pas configuré (secrets absents) -- distinct d'un échec, pour ne jamais
    alerter à tort quand le système est simplement inactif."""
    if not supabase_url or not service_role_key or not vapid_private_key or not vapid_claim_email or not user_id:
        return None

    abonnements = _lister_abonnements_push(supabase_url, service_role_key, [user_id])
    if abonnements is None:
        # Lecture ratee (reseau/API) -- inconnu ce cycle, pas un echec de
        # livraison avere. Meme None que "canari non configure" cote
        # verifier_livraison : main() ne modifie alors rien a l'etat, ce
        # cycle est simplement ignore (pas de fausse resolution/alerte).
        return None
    if not abonnements:
        # Le canari doit avoir un abonnement actif en permanence -- son
        # absence (jamais souscrit, ou desabonnement depuis) est un echec
        # reel : plus rien n'est testé, aucune alerte push ne peut se
        # comparer.
        return False

    return _envoyer_push(
        supabase_url, service_role_key, vapid_private_key, vapid_claim_email,
        abonnements, TITRE_CANARI, CORPS_CANARI, URL_CANARI,
    )


def main() -> None:
    supabase_url = os.environ.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    vapid_private_key = os.environ.get("VAPID_PRIVATE_KEY", "")
    vapid_claim_email = os.environ.get("VAPID_CLAIM_EMAIL", "")
    user_id = os.environ.get("PUSH_CANARI_USER_ID", "")
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID", "1245330032")

    resultat = verifier_livraison(supabase_url, supabase_key, vapid_private_key, vapid_claim_email, user_id)
    if resultat is None:
        print("[verification_push_canari] SUPABASE_URL/SUPABASE_SERVICE_ROLE_KEY/VAPID_PRIVATE_KEY/"
              "VAPID_CLAIM_EMAIL/PUSH_CANARI_USER_ID absent(s) -- canari inactif.")
        return

    etat = charger_memoire_supabase(CLE_MEMOIRE, supabase_url, supabase_key)
    if etat is None:
        print("[verification_push_canari] Supabase injoignable pour l'état d'alerte -- "
              "poursuite avec un état vide (pire cas : une alerte en double, jamais une alerte manquée).")
        etat = {}
    deja_alerte = etat.get("echec", False)
    etat_modifie = False

    if not resultat and not deja_alerte:
        texte = (
            "🚨 <b>Canari push PokéDeals</b>\n\n"
            "Le push de test n'a pas pu être livré (ou l'abonnement canari a disparu) -- "
            "les notifications push des utilisateurs PokéDeals/PokéPrécoms sont probablement "
            "toutes en échec en ce moment."
        )
        envoyer_telegram(texte, telegram_chat_id, telegram_token)
        etat["echec"] = True
        etat_modifie = True
        print("[verification_push_canari] ALERTE : échec de livraison push")
    elif resultat and deja_alerte:
        texte = "✅ <b>Canari push PokéDeals</b>\n\nLa livraison push est revenue au vert."
        envoyer_telegram(texte, telegram_chat_id, telegram_token)
        etat["echec"] = False
        etat_modifie = True
        print("[verification_push_canari] RÉSOLU : livraison de nouveau fonctionnelle")
    else:
        print(f"[verification_push_canari] OK : push {'réussi' if resultat else 'toujours en échec (déjà alerté)'}")

    if etat_modifie:
        if not sauvegarder_memoire_supabase(etat, CLE_MEMOIRE, supabase_url, supabase_key):
            print("[verification_push_canari] ATTENTION : échec de sauvegarde de l'état d'alerte sur Supabase "
                  "-- une alerte déjà envoyée pourrait être renvoyée au prochain passage.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
