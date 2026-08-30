"""
Watchdog de sante des workflows GitHub Actions programmes de PokeDeals.

Systeme INDEPENDANT ajoute le 30/08/2026 (audit externe du compte GitHub) :
jusqu'ici, un workflow de scan qui echoue silencieusement a chaque cycle
(bug de code, secret expire, API tierce cassee) ne generait AUCUNE alerte --
seul un examen manuel de l'onglet Actions du repo l'aurait revele. Ce
watchdog interroge l'API GitHub Actions (lecture seule, GITHUB_TOKEN standard
du workflow, aucun nouveau secret) pour les 9 workflows de scan programmes
(cf. tableau CLAUDE.md) et alerte sur Telegram si l'un d'eux a echoue
SEUIL_ECHECS_CONSECUTIFS fois de suite (pas juste une fois -- un echec isole
est courant et deja tolere par la conception de chaque scanner, ex. une
boutique HS ne fait pas echouer tout le job).

Anti-spam : l'etat "deja alerte" par workflow est persiste dans Supabase
(memoire_supabase.py, cle "watchdog_workflows_etat", meme projet
pokedeals-saas que les autres ponts Supabase du scraper) pour ne pas
re-notifier a chaque execution du watchdog tant que le probleme n'est pas
resolu -- et pour envoyer un message de "retour a la normale" une fois le
workflow de nouveau vert. Contrairement a memoire_supabase.py pour le stock
boutiques (etape 1 de la migration), cet etat n'est PAS critique : une
lecture ratee degrade au pire vers une alerte en double, jamais vers une
alerte manquee -- donc pas de sys.exit(1) ici, juste un repli sur un etat
vide en cas d'erreur Supabase.
"""
from __future__ import annotations

import logging
import os
import sys

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memoire_supabase import charger_memoire_supabase, sauvegarder_memoire_supabase

log = logging.getLogger("pokedeals.watchdog_workflows")

TIMEOUT = 15
CLE_MEMOIRE = "watchdog_workflows_etat"
SEUIL_ECHECS_CONSECUTIFS = 3
NB_EXECUTIONS_EXAMINEES = 5

# Les 9 workflows de scan programmes (cf. tableau "CI/deploiement" de
# CLAUDE.md) -- exclut volontairement tests.yml (pas un scanner, se
# declenche sur push/PR) et les workflows manuels/de test
# (verifier_candidats_manuels.yml, test_notification_email.yml,
# test_verification_photo.yml).
WORKFLOWS_SURVEILLES = [
    "pokedeals.yml",
    "scan_shopify.yml",
    "scan_prestashop.yml",
    "scan_woocommerce.yml",
    "decouverte_boutiques.yml",
    "tendance_prix.yml",
    "prix_bas_quotidien.yml",
    "scan_precommandes_generique.yml",
    "scan_precommandes_philibert.yml",
]


def dernieres_conclusions(owner: str, repo: str, token: str, fichier_workflow: str,
                           n: int = NB_EXECUTIONS_EXAMINEES) -> list[str]:
    """Retourne les conclusions (\"success\"/\"failure\"/...) des n dernieres
    executions TERMINEES d'un workflow, la plus recente en premier. Liste
    vide si l'appel echoue ou si le workflow n'a encore jamais tourne --
    dans les deux cas, aucune conclusion connue ne doit jamais etre traitee
    comme un echec (repli silencieux, cf. echecs_consecutifs())."""
    try:
        r = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{fichier_workflow}/runs",
            params={"per_page": n, "status": "completed"},
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
            },
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        runs = r.json().get("workflow_runs", [])
        return [run["conclusion"] for run in runs]
    except requests.RequestException as e:
        log.warning("Lecture des exécutions de %s échouée (%s) -- ignoré ce passage", fichier_workflow, e)
        return []


def echecs_consecutifs(conclusions: list[str]) -> int:
    """Compte les echecs ("failure") consecutifs depuis la PLUS RECENTE
    execution -- s'arrete au premier "success" rencontre, ou a la fin de la
    liste. "cancelled"/"skipped"/None (execution annulee manuellement, pas
    un vrai echec du code) sont ignores : ils ne comptent ni comme un echec
    ni comme un succes qui reinitialiserait le compteur, pour ne pas
    masquer une vraie serie d'echecs par une annulation manuelle isolee."""
    compte = 0
    for conclusion in conclusions:
        if conclusion == "success":
            break
        if conclusion == "failure":
            compte += 1
        # "cancelled"/"skipped"/"timed_out"/None : ignore, ni +1 ni arret.
        # NB : timed_out est traite comme neutre ici par prudence (peut
        # venir d'une charge ponctuelle du runner GitHub, pas forcement un
        # bug du code) -- a revoir si ca masque un vrai probleme recurrent.
    return compte


def dernier_lien_execution(owner: str, repo: str, fichier_workflow: str) -> str:
    return f"https://github.com/{owner}/{repo}/actions/workflows/{fichier_workflow}"


def envoyer_telegram(texte: str, chat_id: str, token: str) -> bool:
    if not token or not chat_id:
        log.error("Telegram non configuré : message watchdog non envoyé")
        return False
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": texte, "parse_mode": "HTML"},
            timeout=TIMEOUT,
        )
        return r.status_code == 200
    except requests.RequestException as e:
        log.warning("Envoi Telegram watchdog échoué (%s)", e)
        return False


def verifier_sante(owner: str, repo: str, token: str) -> dict[str, int]:
    """Retourne {fichier_workflow: nb_echecs_consecutifs} pour tous les
    workflows surveilles."""
    return {
        fichier: echecs_consecutifs(dernieres_conclusions(owner, repo, token, fichier))
        for fichier in WORKFLOWS_SURVEILLES
    }


def main() -> None:
    owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "")
    repo_complet = os.environ.get("GITHUB_REPOSITORY", "")
    repo = repo_complet.split("/")[-1] if repo_complet else ""
    github_token = os.environ.get("GITHUB_TOKEN", "")
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID", "1245330032")
    supabase_url = os.environ.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

    if not owner or not repo or not github_token:
        print("[watchdog_workflows] GITHUB_REPOSITORY/GITHUB_TOKEN absents -- abandon (ne devrait arriver qu'hors CI).")
        return

    etat = charger_memoire_supabase(CLE_MEMOIRE, supabase_url, supabase_key) if (supabase_url and supabase_key) else {}
    if etat is None:
        print("[watchdog_workflows] Supabase injoignable pour l'état d'alerte -- "
              "poursuite avec un état vide (pire cas : une alerte en double, jamais une alerte manquée).")
        etat = {}

    sante = verifier_sante(owner, repo, github_token)
    etat_modifie = False

    for fichier, echecs in sante.items():
        deja_alerte = etat.get(fichier, False)
        lien = dernier_lien_execution(owner, repo, fichier)

        if echecs >= SEUIL_ECHECS_CONSECUTIFS and not deja_alerte:
            texte = (
                f"🚨 <b>Watchdog PokéDeals</b>\n\n"
                f"Le workflow <b>{fichier}</b> a échoué {echecs} fois de suite.\n"
                f"🔗 <a href=\"{lien}\">Voir les exécutions</a>"
            )
            envoyer_telegram(texte, telegram_chat_id, telegram_token)
            etat[fichier] = True
            etat_modifie = True
            print(f"[watchdog_workflows] ALERTE : {fichier} -- {echecs} échec(s) consécutif(s)")
        elif echecs == 0 and deja_alerte:
            texte = f"✅ <b>Watchdog PokéDeals</b>\n\nLe workflow <b>{fichier}</b> est revenu au vert."
            envoyer_telegram(texte, telegram_chat_id, telegram_token)
            etat[fichier] = False
            etat_modifie = True
            print(f"[watchdog_workflows] RÉSOLU : {fichier}")
        else:
            print(f"[watchdog_workflows] OK : {fichier} -- {echecs} échec(s) consécutif(s) (seuil {SEUIL_ECHECS_CONSECUTIFS})")

    if etat_modifie and supabase_url and supabase_key:
        if not sauvegarder_memoire_supabase(etat, CLE_MEMOIRE, supabase_url, supabase_key):
            print("[watchdog_workflows] ATTENTION : échec de sauvegarde de l'état d'alerte sur Supabase "
                  "-- une alerte déjà envoyée pourrait être renvoyée au prochain passage.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
