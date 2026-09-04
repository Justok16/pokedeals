"""Script de verification manuelle : envoie un vrai email via SendGrid, avec
les MEMES secrets que la production (SENDGRID_API_KEY/SENDGRID_FROM_EMAIL,
partages entre PokeDeals et PokePrecoms, cf. CLAUDE.md), pour confirmer que
la config email fonctionne reellement -- independant de toute detection de
deal/precommande.

Contrairement a `_envoyer_email` dans notifications_saas.py/
connecteur_supabase_precoms.py (qui avale les erreurs, comportement
optionnel et non bloquant voulu en prod), ce script affiche explicitement
le succes/l'echec avec le detail de l'erreur -- c'est tout l'interet d'un
outil de verification manuelle.

Usage : python envoyer_email_test.py destinataire@example.com
Necessite SENDGRID_API_KEY et SENDGRID_FROM_EMAIL en variables d'environnement.
"""
from __future__ import annotations

import sys

import requests


def envoyer_email_test(destinataire: str, sendgrid_api_key: str, sendgrid_from: str) -> bool:
    reponse = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": f"Bearer {sendgrid_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "personalizations": [{"to": [{"email": destinataire}]}],
            "from": {"email": sendgrid_from},
            "subject": "Email de test PokéDeals / PokéPrécoms",
            "content": [
                {
                    "type": "text/plain",
                    "value": (
                        "Ceci est un email de test envoye manuellement pour verifier "
                        "que la configuration SendGrid fonctionne. Si tu recois ce "
                        "message, les alertes email de PokeDeals et PokePrecoms "
                        "fonctionnent bien (memes secrets partages entre les deux)."
                    ),
                },
                {
                    "type": "text/html",
                    "value": (
                        "<p>Ceci est un email de test envoyé manuellement pour vérifier "
                        "que la configuration SendGrid fonctionne.</p>"
                        "<p>Si tu reçois ce message, les alertes email de <strong>PokéDeals</strong> "
                        "et <strong>PokéPrécoms</strong> fonctionnent bien (mêmes secrets partagés "
                        "entre les deux).</p>"
                    ),
                },
            ],
        },
        timeout=15,
    )
    if reponse.ok:
        # SendGrid renvoie 202 sans corps de réponse (contrairement à Resend
        # qui renvoyait un id JSON) -- l'identifiant du message est dans
        # l'en-tête X-Message-Id.
        print(f"OK -- email envoyé à {destinataire} (id SendGrid : {reponse.headers.get('X-Message-Id')})")
        return True
    print(f"ÉCHEC -- statut HTTP {reponse.status_code} : {reponse.text}")
    return False


if __name__ == "__main__":
    import os

    if len(sys.argv) != 2:
        print("Usage : python envoyer_email_test.py destinataire@example.com")
        sys.exit(1)

    cle = os.environ.get("SENDGRID_API_KEY", "")
    expediteur = os.environ.get("SENDGRID_FROM_EMAIL", "")
    if not cle or not expediteur:
        print("SENDGRID_API_KEY et/ou SENDGRID_FROM_EMAIL absents de l'environnement.")
        sys.exit(1)

    succes = envoyer_email_test(sys.argv[1], cle, expediteur)
    sys.exit(0 if succes else 1)
