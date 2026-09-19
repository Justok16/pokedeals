"""Interrupteur maitre pour les notifications PERSONNELLES de Justok
(Telegram + email), ajoute le 19/09/2026 a sa demande explicite : plus
besoin de notifications sur son Telegram ni sur justokseize@gmail.com
"jusqu'a preuve du contraire" (periode calme apres les 30 ans de
Pokemon) -- MAIS les utilisateurs PokeDeals SaaS et PokePrecoms doivent
continuer a recevoir les leurs normalement.

Cet interrupteur s'appuie sur les cles `notifications.telegram`/
`notifications.email` de config.yaml -- deja presentes dans le fichier
depuis un moment mais jamais reellement lues par le code jusqu'ici (pur
commentaire documentaire). Il ne touche JAMAIS :
- aux canaux SaaS (push/email des utilisateurs, notifications_saas.py,
  connecteur_supabase*.py) : entierement independants, ne lisent pas
  config.yaml pour decider d'envoyer ou non ;
- a la lecture des alertes email Leboncoin par IMAP dans
  connecteur_leboncoin.py (GMAIL_APP_PASSWORD y sert a CONSULTER des
  emails, pas a en envoyer a Justok) ;
- aux envois de test des canaris (verification_email_canari.py /
  verification_push_canari.py) : seule leur ALERTE Telegram en cas
  d'echec (destinee a Justok) est coupee par cet interrupteur, jamais le
  test lui-meme, qui continue de verifier la livraison reelle cote SaaS.

Les fonctions d'envoi existantes traitent deja un token/mot de passe vide
comme "secret absent -> no-op silencieux" (comportement documente dans
CLAUDE.md, ex. `notifications_historique.envoyer_telegram`). Reutiliser
ce chemin deja teste, plutot que d'ajouter une condition dans chacune des
~13 fonctions d'envoi, est le moyen le plus sur de couper TOUS les
canaux personnels d'un coup sans risquer d'en oublier un.
"""

from __future__ import annotations

import os
from pathlib import Path

import yaml

CHEMIN_CONFIG_DEFAUT = Path(__file__).parent / "config.yaml"


def _notifications_perso_actives(cle: str, chemin: Path | None = None) -> bool:
    """Lit `notifications.<cle>` dans config.yaml. Absent -> True (actif
    par defaut, comme avant l'existence de cet interrupteur).

    `chemin=None` (plutot qu'un defaut `= CHEMIN_CONFIG_DEFAUT`, evalue
    une seule fois a la definition de la fonction) resout CHEMIN_CONFIG_DEFAUT
    a CHAQUE appel -- indispensable pour que les tests puissent le
    monkeypatcher (`monkeypatch.setattr(notifications_perso,
    "CHEMIN_CONFIG_DEFAUT", ...)`), sans quoi la reaffectation du module
    resterait invisible ici (piege classique des arguments par defaut)."""
    if chemin is None:
        chemin = CHEMIN_CONFIG_DEFAUT
    with open(chemin, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return bool((cfg or {}).get("notifications", {}).get(cle, True))


def token_telegram_perso() -> str:
    """TELEGRAM_BOT_TOKEN, ou "" (no-op silencieux en aval) si
    notifications.telegram est desactive dans config.yaml."""
    if not _notifications_perso_actives("telegram"):
        return ""
    return os.environ.get("TELEGRAM_BOT_TOKEN", "")


def mdp_email_perso() -> str:
    """GMAIL_APP_PASSWORD, ou "" (no-op silencieux en aval) si
    notifications.email est desactive dans config.yaml."""
    if not _notifications_perso_actives("email"):
        return ""
    return os.environ.get("GMAIL_APP_PASSWORD", "")
