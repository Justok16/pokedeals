"""
Utilitaires HTTP partagés par les connecteurs de PokéDeals (eBay, Vinted,
Leboncoin...) : rotation de User-Agent + requête avec retry/backoff sur 429.

Extrait de main.py le 17/08/2026 (cinquième étape du découpage progressif,
cf. SESSION_NOTES.md) — bloc pur, sans état partagé ni dépendance vers le
reste de main.py, nécessaire pour permettre l'extraction du connecteur
Leboncoin (connecteur_leboncoin.py) sans import circulaire : main.py garde
ses propres usages (ebay_rechercher, vinted_rechercher...) via un
ré-import, comme pour json_utils.py.
"""
from __future__ import annotations

import logging
import random
import time

import requests

log = logging.getLogger("pokedeals.http_utils")


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
]


def user_agent() -> str:
    return random.choice(USER_AGENTS)


def requete_avec_retry(methode, url, tentatives: int = 3, **kwargs):
    """Requête HTTP avec 3 tentatives et attente progressive.

    Retente sur 429 (rate-limit) ET sur les erreurs serveur temporaires
    (5xx, 408 Request Timeout) -- audit externe du 17/08/2026 (cf.
    SESSION_NOTES.md) : avant, un 503 ponctuel d'eBay/Vinted/Cardtrader
    (fréquent sur des API publiques) était retourné tel quel sans
    nouvelle tentative, alors qu'un simple retry quelques secondes plus
    tard aurait souvent suffi. Les codes 4xx autres que 408/429 restent
    retournés immédiatement (une vraie erreur client ne se corrige pas
    en réessayant)."""
    CODES_A_RETENTER = {408, 429}
    derniere_erreur = None
    r = None
    for i in range(tentatives):
        try:
            r = methode(url, **kwargs)
            if r.status_code in CODES_A_RETENTER or r.status_code >= 500:
                attente = (2 ** (i + 1)) + random.uniform(0, 2)
                log.info("%d reçu, pause de %.1fs", r.status_code, attente)
                time.sleep(attente)
                continue
            return r
        except requests.RequestException as e:
            derniere_erreur = e
            time.sleep((2 ** i) + random.uniform(0, 1))
    if derniere_erreur:
        raise derniere_erreur
    return r
