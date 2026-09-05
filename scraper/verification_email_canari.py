"""Canari de livraison email -- verification de bout en bout que les emails
SendGrid arrivent reellement chez un destinataire AUTRE que le proprietaire
du compte, pas seulement que l'appel API reussit.

Systeme ajoute le 04/09/2026, suite a un bug reel decouvert le meme jour :
le compte Resend (fournisseur precedent, cf. notifications_saas.py) tournait
en mode sandbox (aucun domaine verifie) -- Resend acceptait alors les appels
API et les logs cote scraper montraient un succes, mais ne livrait en
realite qu'au SEUL email du proprietaire du compte, silencieusement
(403 Forbidden pour tout autre destinataire, jamais remonte jusqu'ici car
`_envoyer_email` avale les erreurs par conception -- systeme optionnel et
non bloquant, cf. sa docstring). Ni les audits de code precedents (relecture
de `_envoyer_email`, verification de la gestion des flags email_envoye...)
ni les tests unitaires (qui mockent l'appel HTTP) ne pouvaient detecter ce
genre de probleme -- seule une verification de livraison REELLE vers une
adresse distincte de celle de l'expediteur/proprietaire peut le faire.

Reutilise LITTERALEMENT `_envoyer_email` de notifications_saas.py (pas une
reimplementation) : le canari doit exercer exactement le meme chemin de code
que la production, sinon un futur bug dans `_envoyer_email` lui-meme
passerait inapercu.

Meme philosophie anti-spam que watchdog_workflows.py : etat "deja alerte"
persiste dans Supabase (memoire_supabase.py, cle CLE_MEMOIRE, meme projet
pokedeals-saas) pour n'alerter qu'au changement d'etat (echec -> pas de
nouvelle alerte tant que ca reste en echec ; retour au vert -> message de
resolution), pas a chaque passage.
"""
from __future__ import annotations

import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memoire_supabase import charger_memoire_supabase, sauvegarder_memoire_supabase
from notifications_saas import _envoyer_email
from watchdog_workflows import envoyer_telegram

log = logging.getLogger("pokedeals.verification_email_canari")

CLE_MEMOIRE = "email_canari_etat"
TITRE_CANARI = "Canari PokéDeals -- vérification automatique de livraison"
URL_CANARI = "https://pokedeals.app"


def corps_canari() -> str:
    return (
        "Cet email est envoyé automatiquement toutes les quelques heures pour "
        "vérifier que la livraison email fonctionne réellement pour un "
        "destinataire différent du compte d'envoi -- pas seulement pour "
        "Justok. Si tu reçois ce message à intervalles réguliers, tout va "
        "bien, rien à faire."
    )


def verifier_livraison(sendgrid_api_key: str, sendgrid_from: str, destinataire: str) -> bool | None:
    """Retourne True/False (succès/échec réel de l'envoi), ou None si le
    canari n'est pas configuré (secrets absents) -- distinct d'un échec,
    pour ne jamais alerter à tort quand le système est simplement inactif."""
    if not sendgrid_api_key or not sendgrid_from or not destinataire:
        return None
    return _envoyer_email(
        sendgrid_api_key, sendgrid_from, destinataire, TITRE_CANARI, corps_canari(), URL_CANARI,
        custom_args={"produit": "pokedeals", "type_notification": "canari"},
    )


def main() -> None:
    sendgrid_api_key = os.environ.get("SENDGRID_API_KEY", "")
    sendgrid_from = os.environ.get("SENDGRID_FROM_EMAIL", "")
    destinataire = os.environ.get("EMAIL_CANARI_DESTINATAIRE", "")
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID", "1245330032")
    supabase_url = os.environ.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

    resultat = verifier_livraison(sendgrid_api_key, sendgrid_from, destinataire)
    if resultat is None:
        print("[verification_email_canari] SENDGRID_API_KEY/SENDGRID_FROM_EMAIL/EMAIL_CANARI_DESTINATAIRE "
              "absent(s) -- canari inactif (comportement identique aux autres ponts optionnels de ce dépôt).")
        return

    etat = charger_memoire_supabase(CLE_MEMOIRE, supabase_url, supabase_key) if (supabase_url and supabase_key) else {}
    if etat is None:
        print("[verification_email_canari] Supabase injoignable pour l'état d'alerte -- "
              "poursuite avec un état vide (pire cas : une alerte en double, jamais une alerte manquée).")
        etat = {}
    deja_alerte = etat.get("echec", False)
    etat_modifie = False

    if not resultat and not deja_alerte:
        texte = (
            f"🚨 <b>Canari email PokéDeals</b>\n\n"
            f"L'email de test n'a PAS pu être envoyé à {destinataire} via SendGrid -- "
            f"les alertes email des utilisateurs PokéDeals/PokéPrécoms sont probablement "
            f"toutes en échec en ce moment (pas juste ce destinataire de test)."
        )
        envoyer_telegram(texte, telegram_chat_id, telegram_token)
        etat["echec"] = True
        etat_modifie = True
        print(f"[verification_email_canari] ALERTE : échec d'envoi à {destinataire}")
    elif resultat and deja_alerte:
        texte = "✅ <b>Canari email PokéDeals</b>\n\nLa livraison email est revenue au vert."
        envoyer_telegram(texte, telegram_chat_id, telegram_token)
        etat["echec"] = False
        etat_modifie = True
        print("[verification_email_canari] RÉSOLU : livraison de nouveau fonctionnelle")
    else:
        print(f"[verification_email_canari] OK : envoi à {destinataire} {'réussi' if resultat else 'toujours en échec (déjà alerté)'}")

    if etat_modifie and supabase_url and supabase_key:
        if not sauvegarder_memoire_supabase(etat, CLE_MEMOIRE, supabase_url, supabase_key):
            print("[verification_email_canari] ATTENTION : échec de sauvegarde de l'état d'alerte sur Supabase "
                  "-- une alerte déjà envoyée pourrait être renvoyée au prochain passage.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
