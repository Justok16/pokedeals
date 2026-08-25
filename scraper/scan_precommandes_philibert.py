"""
Orchestrateur du radar de precommandes generique DEDIE a philibertnet.com
(cf. connecteur_philibert.py pour le detail de la strategie -- sitemap
filtre par mot-cle, ~940 requetes/cycle). Fonctionnalite INDEPENDANTE de
scan_precommandes_generique.py (radar Shopify multi-boutiques), qu'elle ne
modifie ni n'appelle -- mais reutilise TELLE QUELLE sa logique de
memoire/detection/notification (detecter_nouvelles_precommandes_generiques,
envoyer_telegram_precommandes_generiques), le format de candidat produit
par connecteur_philibert.py etant identique.

Usage :
  python scan_precommandes_philibert.py
"""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from connecteur_philibert import scanner_philibert_precommandes_generiques
from connecteur_supabase_precoms import enregistrer_precommande_alertes, notifier_abonnes_precoms
from memoire_json import charger_memoire, sauvegarder_memoire
from memoire_supabase import charger_memoire_supabase, sauvegarder_memoire_supabase
from radar_precommande_generique import (
    detecter_nouvelles_precommandes_generiques,
    envoyer_telegram_precommandes_generiques,
)

TELEGRAM_CHAT_ID = "1245330032"
FICHIER_MEMOIRE = Path(__file__).parent / "data" / "precommandes_generique_philibert.json"
# Cle Supabase equivalente (cf. memoire_supabase.py) -- migration du 25/08/2026.
CLE_MEMOIRE = "precommandes_generique_philibert"


if __name__ == "__main__":
    debut = time.monotonic()
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    pont_precoms_configure = bool(
        os.environ.get("POKEPRECOMS_SUPABASE_URL") and os.environ.get("POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY")
    )

    print("Scan précommandes génériques -- philibertnet.com")
    print(f"Telegram : {'configuré' if token else 'NON configuré (TELEGRAM_BOT_TOKEN absent -- envoi désactivé)'}")
    print(
        f"Pont Supabase PokéPrécoms : {'configuré' if pont_precoms_configure else 'NON configuré (POKEPRECOMS_SUPABASE_URL/_SERVICE_ROLE_KEY absents -- écriture désactivée)'}\n"
    )

    supabase_url = os.environ.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    memoire_via_supabase = bool(supabase_url and supabase_key)
    if memoire_via_supabase:
        memoire = charger_memoire_supabase(CLE_MEMOIRE, supabase_url, supabase_key)
        if memoire is None:
            print("[scan_precommandes_philibert] Supabase injoignable : mémoire illisible, "
                  "cycle ABANDONNÉ (évite de rejouer une alerte pour chaque précommande déjà connue).")
            sys.exit(1)
    else:
        memoire = charger_memoire(FICHIER_MEMOIRE)

    try:
        candidats = scanner_philibert_precommandes_generiques()
        print(f"{len(candidats)} candidat(s) précommande trouvé(s) parmi les URLs Pokémon du sitemap")
    except Exception as e:  # noqa: BLE001 -- un echec complet ne doit jamais planter le workflow
        print(f"ÉCHEC du scan : {type(e).__name__}: {e}")
        candidats = []

    evenements = detecter_nouvelles_precommandes_generiques(candidats, memoire)

    # Meme raison que scan_precommandes_generique.py (V57) : sauvegarde
    # APRES la tentative d'envoi Telegram, qui commite elle-meme l'etat des
    # evenements alertes dans `memoire` uniquement pour ceux envoyes avec
    # succes -- evite de figer "deja alerté" en memoire pour un envoi qui a
    # echoué (perte définitive de l'événement sinon).
    envoyer_telegram_precommandes_generiques(evenements, TELEGRAM_CHAT_ID, token, memoire)
    if memoire_via_supabase:
        if not sauvegarder_memoire_supabase(memoire, CLE_MEMOIRE, supabase_url, supabase_key):
            print("[scan_precommandes_philibert] ATTENTION : échec de sauvegarde de la mémoire sur Supabase "
                  "-- l'état de ce cycle est perdu, les événements détectés ce cycle-ci pourront se rejouer au prochain.")
    else:
        sauvegarder_memoire(memoire, FICHIER_MEMOIRE)

    # Pont PokePrecoms (optionnel/non bloquant), independant du succes
    # Telegram ci-dessus -- la dedup se fait cote base (contrainte unique
    # sur url_produit), pas via `memoire`.
    secrets = {
        "POKEPRECOMS_SUPABASE_URL": os.environ.get("POKEPRECOMS_SUPABASE_URL", ""),
        "POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY": os.environ.get("POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY", ""),
        "VAPID_PRIVATE_KEY": os.environ.get("VAPID_PRIVATE_KEY", ""),
        "VAPID_CLAIM_EMAIL": os.environ.get("VAPID_CLAIM_EMAIL", ""),
        "RESEND_API_KEY": os.environ.get("RESEND_API_KEY", ""),
        "RESEND_FROM_EMAIL": os.environ.get("RESEND_FROM_EMAIL", ""),
    }
    nouvelles_precommandes = enregistrer_precommande_alertes(
        secrets["POKEPRECOMS_SUPABASE_URL"], secrets["POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY"], evenements,
    )
    notifier_abonnes_precoms(secrets, nouvelles_precommandes)

    duree = time.monotonic() - debut
    print(f"\n{'=' * 70}")
    print("RÉSUMÉ DU CYCLE PRÉCOMMANDES PHILIBERT")
    print("=" * 70)
    print(f"Nouvelles alertes précommande : {len(evenements)}")
    for e in evenements:
        print(f"  🎉 {e['titre']}")
    print(f"Durée totale du cycle : {duree:.1f}s ({duree / 60:.1f} min)")
