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

import logging
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from connecteur_philibert import scanner_philibert_precommandes_generiques
from connecteur_supabase_precoms import (
    enregistrer_precommande_alertes,
    lister_precommandes_a_diffuser,
    notifier_abonnes_precoms,
)
from memoire_json import charger_memoire, sauvegarder_memoire
from memoire_supabase import charger_memoire_supabase, sauvegarder_memoire_supabase
from radar_precommande_generique import (
    detecter_nouvelles_precommandes_generiques,
    envoyer_telegram_precommandes_generiques,
)

# cf. scan_boutique.py pour le detail de ce correctif (31/08/2026) : sans
# ceci, les log.info()/log.warning() du pont PokePrecoms restaient
# invisibles dans les logs GitHub Actions.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
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

    # Pont PokePrecoms (optionnel/non bloquant, cf. connecteur_supabase_precoms.py) :
    # appele AVANT l'envoi Telegram (et son commit memoire), pas apres --
    # corrige un bug reel signale par Justok le 31/08/2026 ("j'ai recu des
    # alertes Telegram mais rien sur mon Dashboard"), meme correctif que
    # scan_precommandes_generique.py : si Telegram commitait `memoire` en
    # premier puis que cette ecriture Supabase echouait sur le MEME cycle,
    # l'evenement ne pouvait plus jamais etre redetecte (la transition "pas
    # en stock -> en stock" ne se reproduit qu'une fois) -- perte DEFINITIVE
    # cote Supabase/Dashboard malgre l'alerte Telegram recue.
    # `enregistrer_precommande_alertes()` retourne maintenant `None` sur un
    # echec reel (pas `[]`, reserve au no-op legitime) : on retire alors
    # `_cle_memoire`/`_nouvel_etat` des evenements concernes AVANT l'appel
    # Telegram, pour que son commit memoire ne les fige pas -- ils seront
    # redetectes et retentes (les deux canaux, doublon Telegram accepte) au
    # prochain cycle plutot que perdus.
    secrets = {
        "POKEPRECOMS_SUPABASE_URL": os.environ.get("POKEPRECOMS_SUPABASE_URL", ""),
        "POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY": os.environ.get("POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY", ""),
        "VAPID_PRIVATE_KEY": os.environ.get("VAPID_PRIVATE_KEY", ""),
        "VAPID_CLAIM_EMAIL": os.environ.get("VAPID_CLAIM_EMAIL", ""),
        "SENDGRID_API_KEY": os.environ.get("SENDGRID_API_KEY", ""),
        "SENDGRID_FROM_EMAIL": os.environ.get("SENDGRID_FROM_EMAIL", ""),
    }
    if enregistrer_precommande_alertes(
        secrets["POKEPRECOMS_SUPABASE_URL"], secrets["POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY"], evenements,
    ) is None:
        print("[scan_precommandes_philibert] ATTENTION : échec d'écriture Supabase PokéPrécoms -- "
              "les événements de ce cycle ne seront pas marqués comme alertés, pour être retentés au prochain cycle.")
        for e in evenements:
            e.pop("_cle_memoire", None)
            e.pop("_nouvel_etat", None)

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

    precommandes_a_diffuser = lister_precommandes_a_diffuser(
        secrets["POKEPRECOMS_SUPABASE_URL"], secrets["POKEPRECOMS_SUPABASE_SERVICE_ROLE_KEY"],
    )
    notifier_abonnes_precoms(secrets, precommandes_a_diffuser)

    duree = time.monotonic() - debut
    print(f"\n{'=' * 70}")
    print("RÉSUMÉ DU CYCLE PRÉCOMMANDES PHILIBERT")
    print("=" * 70)
    print(f"Nouvelles alertes précommande : {len(evenements)}")
    for e in evenements:
        print(f"  🎉 {e['titre']}")
    print(f"Durée totale du cycle : {duree:.1f}s ({duree / 60:.1f} min)")
