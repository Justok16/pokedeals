"""Script de verification manuelle : envoie un vrai email via Resend, avec
les MEMES secrets que la production (RESEND_API_KEY/RESEND_FROM_EMAIL,
partages entre PokeDeals et PokePrecoms, cf. CLAUDE.md), pour confirmer que
la config email fonctionne reellement -- independant de toute detection de
deal/precommande.

Contrairement a `_envoyer_email` dans notifications_saas.py/
connecteur_supabase_precoms.py (qui avale les erreurs, comportement
optionnel et non bloquant voulu en prod), ce script affiche explicitement
le succes/l'echec avec le detail de l'erreur -- c'est tout l'interet d'un
outil de verification manuelle.

Usage : python envoyer_email_test.py destinataire@example.com
Necessite RESEND_API_KEY et RESEND_FROM_EMAIL en variables d'environnement.
"""
from __future__ import annotations

import sys

import requests


def envoyer_email_test(destinataire: str, resend_api_key: str, resend_from: str) -> bool:
    reponse = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {resend_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "from": resend_from,
            "to": [destinataire],
            "subject": "Email de test PokéDeals / PokéPrécoms",
            "text": (
                "Ceci est un email de test envoye manuellement pour verifier "
                "que la configuration Resend fonctionne. Si tu recois ce "
                "message, les alertes email de PokeDeals et PokePrecoms "
                "fonctionnent bien (memes secrets partages entre les deux)."
            ),
            "html": (
                "<p>Ceci est un email de test envoyé manuellement pour vérifier "
                "que la configuration Resend fonctionne.</p>"
                "<p>Si tu reçois ce message, les alertes email de <strong>PokéDeals</strong> "
                "et <strong>PokéPrécoms</strong> fonctionnent bien (mêmes secrets partagés "
                "entre les deux).</p>"
            ),
        },
        timeout=15,
    )
    if reponse.ok:
        print(f"OK -- email envoyé à {destinataire} (id Resend : {reponse.json().get('id')})")
        return True
    print(f"ÉCHEC -- statut HTTP {reponse.status_code} : {reponse.text}")
    return False


if __name__ == "__main__":
    import os

    if len(sys.argv) != 2:
        print("Usage : python envoyer_email_test.py destinataire@example.com")
        sys.exit(1)

    cle = os.environ.get("RESEND_API_KEY", "")
    expediteur = os.environ.get("RESEND_FROM_EMAIL", "")
    if not cle or not expediteur:
        print("RESEND_API_KEY et/ou RESEND_FROM_EMAIL absents de l'environnement.")
        sys.exit(1)

    succes = envoyer_email_test(sys.argv[1], cle, expediteur)
    sys.exit(0 if succes else 1)
