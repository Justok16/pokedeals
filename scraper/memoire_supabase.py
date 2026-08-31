"""
Memoire persistante partagee (Supabase) -- remplace le stockage historique
data/*.json + commit Git pour les fichiers memoire a ROTATION RAPIDE (mis a
jour a chaque cycle de scan, plusieurs fois par heure). Ajoute le 24/08/2026
(chantier "Git comme base de donnees", suite a l'audit externe qui signalait
la croissance illimitee de l'historique Git comme fragilite structurelle --
53 Mo / 4106 commits mesures ce jour-la, dont l'ecrasante majorite de
commits automatiques "maj memoire ...").

PREMIERE ETAPE d'une migration progressive et prudente (un fichier memoire
a la fois, meme principe que le decoupage progressif de main.py documente
plus haut dans ce fichier) : cible ici UNIQUEMENT data/stock_boutiques_tcg*.json
(3 fichiers, les plus gros -- 1,1 Mo cumules -- et les plus souvent reecrits,
3 workflows toutes les 30 min). Les autres familles de memoire (precommandes,
decouverte, systeme historique main.py) restent sur disque/Git pour
l'instant -- migration future, un fichier a la fois.

Contrairement aux autres ponts Supabase du projet (connecteur_supabase.py,
notifications_saas.py, connecteur_supabase_precoms.py...), CE module n'est
PAS "optionnel et non bloquant" : la memoire de deduplication est au coeur
de la logique d'alerte -- une lecture ratee qui renverrait silencieusement
{} ferait perdre tout l'etat connu et rejouerait une alerte "retour en
stock" pour CHAQUE produit deja en stock. charger_memoire_supabase()
distingue donc explicitement 2 cas (meme principe que vinted_description()
dans main.py) :
  - dict (potentiellement vide {}) : lecture reussie, {} = vraiment aucun
    historique pour cette cle (premiere execution).
  - None : Supabase injoignable/erreur -- l'appelant DOIT abandonner le
    cycle de detection stock pour cette memoire plutot que de continuer
    avec un dict vide (cf. scan_boutique*.py, sys.exit(1) sur None).

Table Supabase requise (projet pokedeals-saas -- meme projet que
connecteur_supabase.py, migration a appliquer manuellement via le SQL editor
Supabase, ce depot n'ayant pas acces au depot prive pokedeals-saas) :

    create table scraper_memoire (
      cle text primary key,
      donnees jsonb not null default '{}'::jsonb,
      maj_le timestamptz not null default now()
    );
    alter table scraper_memoire enable row level security;
    -- Aucune policy anon/authenticated : accessible uniquement via la cle
    -- service_role (deja utilisee par tous les autres ponts scraper -> SaaS
    -- de ce projet), qui contourne RLS.

Reutilise les MEMES secrets SUPABASE_URL/SUPABASE_SERVICE_ROLE_KEY que
connecteur_supabase.py (deja presents dans scan_boutique*.py) -- pas de
nouveau secret GitHub Actions a ajouter.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone

import requests

from http_utils import requete_avec_retry

log = logging.getLogger("pokedeals.memoire_supabase")

TIMEOUT = 20


def charger_memoire_supabase(cle: str, supabase_url: str, service_role_key: str) -> dict | None:
    """Retourne le dict memoire associe a `cle`, {} si la cle n'existe pas
    encore (premiere execution), ou None si Supabase est injoignable/en
    erreur -- l'appelant doit alors ABANDONNER le cycle pour cette memoire
    plutot que de continuer avec un dict vide (cf. docstring du module)."""
    if not supabase_url or not service_role_key:
        return None
    try:
        # Audit du 31/08/2026 (signale par Justok) : un seul essai, aucun
        # retry -- un simple timeout reseau transitoire (deja observe en
        # prod, 20s depassees une fois) abandonnait tout le cycle de scan
        # pour rien (cf. docstring du module : ce module n'est PAS
        # optionnel, contrairement aux autres ponts Supabase de ce depot).
        # requete_avec_retry() (http_utils.py, deja utilise pour eBay/
        # Vinted/Cardtrader) retente jusqu'a 3 fois avec backoff sur toute
        # erreur reseau (timeout, connexion, 5xx, 429) avant d'abandonner
        # reellement -- le sys.exit(1) cote appelant ne se declenche
        # desormais que si la panne persiste sur les 3 tentatives.
        r = requete_avec_retry(
            requests.get,
            f"{supabase_url.rstrip('/')}/rest/v1/scraper_memoire",
            params={"select": "donnees", "cle": f"eq.{cle}"},
            headers={"apikey": service_role_key, "Authorization": f"Bearer {service_role_key}"},
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        lignes = r.json()
        return lignes[0]["donnees"] if lignes else {}
    except (requests.RequestException, ValueError, KeyError, IndexError) as e:
        log.error("[memoire_supabase] Lecture de '%s' échouée : %s", cle, e)
        return None


def sauvegarder_memoire_supabase(memoire: dict, cle: str, supabase_url: str, service_role_key: str) -> bool:
    """Ecrit (upsert) le dict memoire complet sous `cle`. Retourne False en
    cas d'echec (reseau, erreur API) -- l'appelant doit alors le signaler
    clairement (l'etat de ce cycle est perdu, contrairement a une ecriture
    fichier atomique qui ne pouvait qu'echouer entierement ou reussir
    entierement au niveau du disque local)."""
    if not supabase_url or not service_role_key:
        return False
    try:
        # Audit du 31/08/2026 : meme retry qu'en lecture (cf. plus haut) --
        # sans danger ici malgre l'ecriture, puisque c'est un UPSERT
        # (on_conflict=cle) : retenter le meme envoi ne cree jamais de
        # doublon, juste une re-ecriture identique de la meme ligne.
        r = requete_avec_retry(
            requests.post,
            f"{supabase_url.rstrip('/')}/rest/v1/scraper_memoire",
            params={"on_conflict": "cle"},
            json={
                "cle": cle,
                "donnees": memoire,
                "maj_le": datetime.now(timezone.utc).isoformat(),
            },
            headers={
                "apikey": service_role_key,
                "Authorization": f"Bearer {service_role_key}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates",
            },
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return True
    except requests.RequestException as e:
        log.error("[memoire_supabase] Écriture de '%s' échouée : %s", cle, e)
        return False
