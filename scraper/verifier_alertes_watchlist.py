"""
Orchestrateur du radar de verification -- cf. verification_alertes.py pour la
logique de verification par plateforme. Fonctionnalite INDEPENDANTE du reste
du scraper (nouveau fichier, aucune modification des connecteurs/
orchestrateurs existants).

Notification sur transition (03/09/2026) : detecter_transition() est appelee
AVANT enregistrer_verification() pour chaque alerte (qui ecrase l'etat
precedent) -- cf. docstring de verification_alertes.py pour le detail des 2
transitions notifiees. Secrets VAPID_*/RESEND_* optionnels comme partout
ailleurs dans le SaaS (notifications_saas.py) : absents -> ce cycle continue
de mettre a jour disponible/prix_verifie, juste sans notification.

Usage :
  python verifier_alertes_watchlist.py
"""

import logging
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from notifications_saas import notifier_transition_verification  # noqa: E402
from verification_alertes import (  # noqa: E402
    DELAI_ENTRE_VERIFICATIONS,
    detecter_transition,
    enregistrer_verification,
    lister_alertes_recentes,
    message_transition,
    verifier_une_alerte,
)

# cf. scan_boutique.py pour le detail de ce correctif (31/08/2026) : sans
# ceci, les log.info()/log.warning() du module de verification restent
# invisibles dans les logs GitHub Actions.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)

if __name__ == "__main__":
    supabase_url = os.environ.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

    if not supabase_url or not supabase_key:
        print("SUPABASE_URL/SUPABASE_SERVICE_ROLE_KEY absents -- rien à faire, ce radar est optionnel.")
        sys.exit(0)

    # 03/09/2026 : secrets de notification -- optionnels (cf. docstring du
    # module), réutilisés tels quels par notifier_transition_verification()
    # (même secrets que le reste des notifications SaaS, cf. CLAUDE.md).
    secrets_notif = {
        "SUPABASE_URL": supabase_url,
        "SUPABASE_SERVICE_ROLE_KEY": supabase_key,
        "VAPID_PRIVATE_KEY": os.environ.get("VAPID_PRIVATE_KEY", ""),
        "VAPID_CLAIM_EMAIL": os.environ.get("VAPID_CLAIM_EMAIL", ""),
        "RESEND_API_KEY": os.environ.get("RESEND_API_KEY", ""),
        "RESEND_FROM_EMAIL": os.environ.get("RESEND_FROM_EMAIL", ""),
    }

    alertes = lister_alertes_recentes(supabase_url, supabase_key)
    print(f"{len(alertes)} alerte(s) récente(s) à revérifier\n")

    verifiees = 0
    disponibles = 0
    indisponibles = 0
    non_verifiables = 0
    notifiees = 0

    for i, alerte in enumerate(alertes):
        resultat = verifier_une_alerte(alerte["url"])
        if resultat is None:
            non_verifiables += 1
        else:
            # 03/09/2026 : la transition se détecte contre l'état PRÉCÉDENT
            # (`alerte`, tel que lu par lister_alertes_recentes()) --
            # TOUJOURS avant enregistrer_verification() ci-dessous, qui
            # écrase cet état. cf. verification_alertes.detecter_transition().
            transition = detecter_transition(alerte, resultat)
            if transition and alerte.get("user_id"):
                titre_notif, corps = message_transition(alerte, resultat, transition)
                notifier_transition_verification(
                    secrets_notif, alerte["user_id"], titre_notif, corps, alerte["url"],
                )
                notifiees += 1

            enregistrer_verification(supabase_url, supabase_key, alerte["id"], resultat)
            verifiees += 1
            if resultat["disponible"]:
                disponibles += 1
            else:
                indisponibles += 1

        if i < len(alertes) - 1:
            time.sleep(DELAI_ENTRE_VERIFICATIONS)

    print(f"\n{'=' * 70}")
    print("RÉSUMÉ DU CYCLE DE VÉRIFICATION")
    print("=" * 70)
    print(f"Vérifiées      : {verifiees}/{len(alertes)}")
    print(f"  - toujours disponibles : {disponibles}")
    print(f"  - indisponibles/vendues : {indisponibles}")
    print(f"Non vérifiables (eBay/Vinted/Leboncoin, ou boutique non couverte) : {non_verifiables}")
    print(f"Notifications de transition envoyées (vendu/baisse de prix) : {notifiees}")
