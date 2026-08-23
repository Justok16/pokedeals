"""
Orchestrateur du radar de precommandes GENERIQUE (PokePrecoms) -- cf.
precommande_generique.py / radar_precommande_generique.py. Fonctionnalite
INDEPENDANTE de scan_precommandes.py (radar a produits fixes du systeme
PokeDeals historique), qu'elle ne modifie ni n'appelle.

SHOPIFY UNIQUEMENT pour l'instant (cf. docstring de
radar_precommande_generique.py) -- concu pour tourner comme une ETAPE
SUPPLEMENTAIRE dans le workflow scan_shopify.yml existant (meme cadence),
sans creer de nouveau workflow separe, exactement comme scan_precommandes.py
pour le radar a produits fixes.

Usage :
  python scan_precommandes_generique.py [boutique1 boutique2 ...]
Sans boutique(s) en argument : scanne toutes les boutiques Shopify actives
(cartes + precommande-seulement + decouvertes automatiquement).
"""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memoire_json import charger_memoire, sauvegarder_memoire
from radar_precommande_generique import (
    detecter_nouvelles_precommandes_generiques,
    envoyer_telegram_precommandes_generiques,
    scanner_shopify_precommandes_generiques,
)

DELAI_ENTRE_BOUTIQUES = 2.5
TELEGRAM_CHAT_ID = "1245330032"
FICHIER_MEMOIRE = Path(__file__).parent / "data" / "precommandes_generiques_shopify.json"


def _boutiques_shopify_actives() -> list[str]:
    from boutiques_decouvertes import BOUTIQUES_SHOPIFY_AUTO, BOUTIQUES_SHOPIFY_AUTO_PRECOMMANDE_SEULEMENT
    from boutiques_shopify import BOUTIQUES_SHOPIFY, BOUTIQUES_SHOPIFY_PRECOMMANDE_SEULEMENT
    return (list(BOUTIQUES_SHOPIFY) + list(BOUTIQUES_SHOPIFY_PRECOMMANDE_SEULEMENT)
            + list(BOUTIQUES_SHOPIFY_AUTO) + list(BOUTIQUES_SHOPIFY_AUTO_PRECOMMANDE_SEULEMENT))


def scanner_plusieurs_boutiques(boutiques: list[str], memoire: dict) -> dict:
    debut = time.monotonic()
    tous_les_evenements: list[dict] = []
    boutiques_ok: list[str] = []
    boutiques_echec: list[dict] = []

    for i, domaine in enumerate(boutiques):
        try:
            candidats = scanner_shopify_precommandes_generiques(domaine)
            evenements = detecter_nouvelles_precommandes_generiques(candidats, memoire)
            tous_les_evenements.extend(evenements)
            boutiques_ok.append(domaine)
            print(f"[{i + 1}/{len(boutiques)}] {domaine} : OK — {len(candidats)} candidat(s), {len(evenements)} nouvelle(s) alerte(s)")
        except Exception as e:  # noqa: BLE001 -- une boutique en echec ne doit jamais arreter le cycle
            raison = f"{type(e).__name__}: {e}"
            boutiques_echec.append({"domaine": domaine, "raison": raison})
            print(f"[{i + 1}/{len(boutiques)}] {domaine} : ECHEC — {raison}")

        if i < len(boutiques) - 1:
            time.sleep(DELAI_ENTRE_BOUTIQUES)

    duree = time.monotonic() - debut
    return {
        "evenements": tous_les_evenements,
        "boutiques_ok": boutiques_ok,
        "boutiques_echec": boutiques_echec,
        "duree_secondes": duree,
    }


if __name__ == "__main__":
    boutiques = sys.argv[1:] if len(sys.argv) > 1 else _boutiques_shopify_actives()
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")

    print(f"{len(boutiques)} boutique(s) Shopify à scanner (radar précommandes générique)")
    print(f"Telegram : {'configuré' if token else 'NON configuré (TELEGRAM_BOT_TOKEN absent -- envoi désactivé)'}\n")

    memoire = charger_memoire(FICHIER_MEMOIRE)
    resume = scanner_plusieurs_boutiques(boutiques, memoire)
    # Meme raison que scan_precommandes.py (V57) : sauvegarde APRES la
    # tentative d'envoi Telegram, qui commite elle-meme l'etat des
    # evenements alertes dans `memoire` uniquement pour ceux envoyes avec
    # succes -- evite de figer "deja alerté" en memoire pour un envoi qui
    # a echoué (perte définitive de l'événement sinon).
    envoyer_telegram_precommandes_generiques(resume["evenements"], TELEGRAM_CHAT_ID, token, memoire)
    sauvegarder_memoire(memoire, FICHIER_MEMOIRE)

    print(f"\n{'=' * 70}")
    print("RÉSUMÉ DU CYCLE PRÉCOMMANDES GÉNÉRIQUE")
    print("=" * 70)
    print(f"Boutiques OK      : {len(resume['boutiques_ok'])}/{len(boutiques)}")
    print(f"Boutiques en échec: {len(resume['boutiques_echec'])}/{len(boutiques)}")
    for e in resume["boutiques_echec"]:
        print(f"  - {e['domaine']} : {e['raison']}")
    print(f"Nouvelles alertes précommande : {len(resume['evenements'])}")
    for e in resume["evenements"]:
        print(f"  🎉 {e['domaine']} — {e['titre']}")
    print(f"Durée totale du cycle : {resume['duree_secondes']:.1f}s ({resume['duree_secondes'] / 60:.1f} min)")
