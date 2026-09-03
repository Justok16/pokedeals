"""
Orchestrateur du radar de verification -- cf. verification_alertes.py pour la
logique de verification par plateforme. Fonctionnalite INDEPENDANTE du reste
du scraper (nouveau fichier, aucune modification des connecteurs/
orchestrateurs existants).

Usage :
  python verifier_alertes_watchlist.py
"""

import logging
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from verification_alertes import (  # noqa: E402
    DELAI_ENTRE_VERIFICATIONS,
    enregistrer_verification,
    lister_alertes_recentes,
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

    alertes = lister_alertes_recentes(supabase_url, supabase_key)
    print(f"{len(alertes)} alerte(s) récente(s) à revérifier\n")

    verifiees = 0
    disponibles = 0
    indisponibles = 0
    non_verifiables = 0

    for i, alerte in enumerate(alertes):
        resultat = verifier_une_alerte(alerte["url"])
        if resultat is None:
            non_verifiables += 1
        else:
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
