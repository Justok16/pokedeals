"""
Veille EXPRESS des produits des 30 ans (08/10/2026, choix de Justok :
toutes les 5 minutes, en plus du radar complet de 15-20 min).

Pourquoi : un restock peut s'epuiser en 2-3 minutes ; avec un passage toutes
les 15-20 min, le radar complet en rate la plupart. La veille express ne
redecouvre rien : elle relit seulement les fiches DEJA reperees par le radar
(memoires precommandes_anniversaire_*), plus les enseignes dont le scan
complet ne coute que quelques requetes (Leclerc, Auchan, Ultrajeux).

  - Shopify : /products/<handle>.js (une requete par fiche, variante exacte
    si l'URL memorisee porte ?variant=).
  - WooCommerce / PrestaShop : relecture de la fiche (_evaluer_page, memes
    regles de correspondance que le radar).
  - Leclerc / Auchan / Ultrajeux : scanner complet (quelques requetes).

Memoire PROPRE (cle "veille_express_30e"), jamais celle du radar : aucune
course d'ecriture entre les deux systemes. Anti-doublon par horodatage :
l'etat "precedent" d'une fiche est l'observation la plus RECENTE des deux
systemes ; le radar fait la meme verification de son cote (cf.
deja_alerte_par_la_veille_express, appelee par scan_precommandes.py).

Politesse : SessionRadarPolie (une requete par seconde maximum par site),
User-Agent honnete, aucun contournement.
"""
from __future__ import annotations

import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alerte_precommande import _consolider_suivi_disponibilite, envoyer_telegram_precommandes
from http_radar_poli import SessionRadarPolie, rendre_poli
from memoire_json import charger_memoire as charger_json, sauvegarder_memoire as sauvegarder_json
from memoire_supabase import charger_memoire_supabase, sauvegarder_memoire_supabase
import re

from precommandes_watchlist import evaluer_correspondance, produits_actifs

CLE_MEMOIRE_EXPRESS = "veille_express_30e"
FICHIER_MEMOIRE_EXPRESS = Path(__file__).parent / "data" / "veille_express_30e.json"
PLATEFORMES_FICHES = ("shopify", "woocommerce", "prestashop")
ENSEIGNES = {"leclerc": "e.leclerc", "auchan": "auchan.fr", "ultrajeux": "ultrajeux.com"}
PARALLELISME = 8
TIMEOUT = 15


def _maintenant() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def cles_memoires_radar() -> dict[str, str]:
    """{cle Supabase: plateforme} des 12 memoires du radar (2 perimetres)."""
    from scan_precommandes import CLE_MEMOIRE_PAR_PLATEFORME, SUFFIXE_MEMOIRE_COMPLEMENT
    cles = {}
    for plateforme, cle in CLE_MEMOIRE_PAR_PLATEFORME.items():
        cles[cle] = plateforme
        cles[cle + SUFFIXE_MEMOIRE_COMPLEMENT] = plateforme
    return cles


def fiches_a_surveiller(memoires: dict[str, dict], plateformes: dict[str, str], noms_suivis: set[str]) -> list[dict]:
    """Fiches connues des produits suivis : [{plateforme, domaine, nom_produit,
    url, titre}] pour les plateformes a fiche relisible (Shopify/Woo/Presta)."""
    fiches, vues = [], set()
    for cle, memoire in memoires.items():
        plateforme = plateformes[cle]
        if plateforme not in PLATEFORMES_FICHES:
            continue
        for cle_entree, etat in memoire.items():
            if cle_entree.startswith("__") or "|" not in cle_entree or not isinstance(etat, dict):
                continue
            domaine, nom = cle_entree.split("|", 1)
            url = etat.get("url_produit")
            if nom not in noms_suivis or not url or (domaine, nom) in vues:
                continue
            vues.add((domaine, nom))
            fiches.append({"plateforme": plateforme, "domaine": domaine, "nom_produit": nom,
                           "url": url, "titre": etat.get("titre_produit") or ""})
    return fiches


def etat_radar(memoires: dict[str, dict]) -> dict[str, dict]:
    """{"domaine|produit": etat le plus recent} toutes memoires du radar confondues."""
    fusion: dict[str, dict] = {}
    for memoire in memoires.values():
        for cle, etat in memoire.items():
            if cle.startswith("__") or not isinstance(etat, dict):
                continue
            if (etat.get("derniere_verification") or "") >= (fusion.get(cle, {}).get("derniere_verification") or ""):
                fusion[cle] = etat
    return fusion


def observer_fiche_shopify(session: requests.Session, fiche: dict, produit) -> dict | None:
    """Etat d'une fiche Shopify via /products/<handle>.js (prix en centimes)."""
    morceaux = urlsplit(fiche["url"])
    if "/products/" not in morceaux.path:
        return None
    handle = morceaux.path.split("/products/", 1)[1].strip("/")
    r = session.get(f"{morceaux.scheme}://{morceaux.netloc}/products/{handle}.js",
                    headers={"Accept": "application/json"}, timeout=TIMEOUT)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    donnees = r.json()
    variantes = donnees.get("variants") or []
    voulue = (parse_qs(morceaux.query).get("variant") or [None])[0]
    if voulue:
        variantes = [v for v in variantes if str(v.get("id")) == voulue] or variantes
    # 10/10/2026 : une fiche reste en memoire du radar meme si une regle
    # ajoutee depuis l'exclut (pack en chinois traditionnel de poke-geek.fr,
    # UPC « -en » de pokemael.com, lots kwilytcg.com...) : on rejoue la regle
    # du radar sur le titre et la description du jour, sinon un retour en
    # stock declencherait une fausse alerte « Disponible ».
    description = re.sub(r"<[^>]+>", " ", donnees.get("description") or "")
    titre = donnees.get("title") or fiche["titre"]
    if voulue and len(variantes) == 1 and variantes[0].get("title") not in (None, "", "Default Title"):
        titre = f"{titre} — {variantes[0]['title']}"
    if evaluer_correspondance(titre, description, produit)[0] is None:
        return None
    dispo = [v for v in variantes if v.get("available") is True]
    choix = dispo or variantes
    prix = None
    if choix:
        try:
            prix = min(float(v.get("price")) / 100 for v in choix if v.get("price") is not None)
        except ValueError:
            prix = None
    return {
        "domaine": fiche["domaine"], "nom_produit": fiche["nom_produit"], "confiance": "moyenne",
        "raison": "veille express (fiche connue)", "titre": donnees.get("title") or fiche["titre"],
        "url_produit": fiche["url"], "prix": prix, "en_stock": bool(dispo),
        "prioritaire": produit.prioritaire, "alerte_disponibilite": True, "horodatage": _maintenant(),
    }


def _observer_domaine(plateforme: str, domaine: str, fiches: list[dict], produits_par_nom: dict) -> list[dict]:
    """Observations d'un domaine (sequentiel : une boutique n'est jamais
    sollicitee par deux fils a la fois). Une fiche illisible est ignoree."""
    from radar_precommandes import _evaluer_page
    observations = []
    if plateforme == "shopify":
        session = SessionRadarPolie()
        for f in fiches:
            try:
                o = observer_fiche_shopify(session, f, produits_par_nom[f["nom_produit"]])
            except (requests.RequestException, ValueError):
                continue
            if o:
                observations.append(o)
        return observations
    from connecteur_prestashop_sitemap import ConnecteurPrestaShopSitemap
    from connecteur_woocommerce import ConnecteurWooCommerce
    classe = ConnecteurWooCommerce if plateforme == "woocommerce" else ConnecteurPrestaShopSitemap
    connecteur = rendre_poli(classe(domaine))
    for f in fiches:
        for c in _evaluer_page(connecteur, f["url"], [produits_par_nom[f["nom_produit"]]]):
            c["domaine"] = domaine
            observations.append(c)
    return observations


def _observer_enseigne(plateforme: str, produits: list) -> list[dict]:
    from scan_precommandes import scanner_une_boutique
    return scanner_une_boutique(plateforme, ENSEIGNES[plateforme], None, produits)


def evenements_express(observations: list[dict], memoire_express: dict, radar: dict) -> list[dict]:
    """Met a jour `memoire_express` (sauf alertes : ecriture differee apres
    envoi Telegram reussi, cf. envoyer_telegram_precommandes) et retourne les
    evenements a envoyer. Precedent = observation la plus RECENTE entre la
    veille et le radar ; aucune observation precedente = reference silencieuse."""
    evenements = []
    par_domaine: dict[str, list[dict]] = {}
    for o in observations:
        par_domaine.setdefault(o["domaine"], []).append(o)
    for domaine, obs in par_domaine.items():
        for o in _consolider_suivi_disponibilite(obs):
            cle = f"{domaine}|{o['nom_produit']}"
            precedents = [e for e in (memoire_express.get(cle), radar.get(cle)) if e]
            precedent = max(precedents, key=lambda e: e.get("verifie") or e.get("derniere_verification") or "",
                            default=None)
            nouvel_etat = {"en_stock": o.get("en_stock"), "verifie": o.get("horodatage") or _maintenant(),
                           "url_produit": o.get("url_produit"), "prix": o.get("prix")}
            if precedent is not None and precedent.get("en_stock") is not True and o.get("en_stock") is True:
                nouvel_etat["alerte"] = nouvel_etat["verifie"]
                o["_cle_memoire"], o["_nouvel_etat"] = cle, nouvel_etat
                evenements.append(o)
            else:
                memoire_express[cle] = nouvel_etat
    return evenements


def deja_alerte_par_la_veille_express(evenement: dict, memoire_express: dict, etat_radar_precedent: dict | None) -> bool:
    """Pour le radar : la veille express a-t-elle deja signale CE passage en
    stock (vu commandable APRES la derniere observation du radar) ?"""
    express = memoire_express.get(evenement.get("_cle_memoire", ""))
    if not express or express.get("en_stock") is not True or not express.get("alerte"):
        return False
    vu_par_radar = (etat_radar_precedent or {}).get("derniere_verification") or ""
    return (express.get("verifie") or "") > vu_par_radar


def main() -> int:
    produits = [p for p in produits_actifs() if p.alerte_disponibilite]
    if not produits:
        print("Aucun produit en suivi de disponibilite actif -- rien a faire.")
        return 0
    produits_par_nom = {p.nom: p for p in produits}
    url, cle_service = os.environ.get("SUPABASE_URL", ""), os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    via_supabase = bool(url and cle_service)

    plateformes = cles_memoires_radar()
    memoires = {}
    for cle in plateformes:
        if via_supabase:
            m = charger_memoire_supabase(cle, url, cle_service)
            if m is None:
                print(f"[veille_express] Supabase injoignable ({cle}) : cycle abandonne.")
                return 1
        else:
            m = charger_json(Path(__file__).parent / "data" / f"{cle}.json")
        memoires[cle] = m
    memoire_express = (charger_memoire_supabase(CLE_MEMOIRE_EXPRESS, url, cle_service) if via_supabase
                       else charger_json(FICHIER_MEMOIRE_EXPRESS))
    if memoire_express is None:
        print("[veille_express] Supabase injoignable (memoire express) : cycle abandonne.")
        return 1

    fiches = fiches_a_surveiller(memoires, plateformes, set(produits_par_nom))
    groupes: dict[tuple[str, str], list[dict]] = {}
    for f in fiches:
        groupes.setdefault((f["plateforme"], f["domaine"]), []).append(f)
    print(f"{len(fiches)} fiche(s) connue(s) sur {len(groupes)} boutique(s) + {len(ENSEIGNES)} enseigne(s)")

    def tache(t):
        try:
            if t[0] == "enseigne":
                return _observer_enseigne(t[1], produits)
            return _observer_domaine(t[0], t[1], groupes[t], produits_par_nom)
        except Exception as e:  # noqa: BLE001 -- une boutique en echec n'arrete pas la veille
            print(f"[veille_express] {t[1]} : ECHEC {type(e).__name__}: {e}")
            return []

    taches = [("enseigne", p) for p in ENSEIGNES] + list(groupes)
    with ThreadPoolExecutor(max_workers=PARALLELISME) as pool:
        observations = [o for lot in pool.map(tache, taches) for o in lot]

    evenements = evenements_express(observations, memoire_express, etat_radar(memoires))
    print(f"{len(observations)} observation(s), {len(evenements)} passage(s) en stock")
    for e in evenements:
        print(f"  🔔 {e['nom_produit']} — {e['domaine']} — {e.get('prix')} — {e['url_produit']}")
    from scan_precommandes import TELEGRAM_CHAT_ID
    envoyer_telegram_precommandes(evenements, TELEGRAM_CHAT_ID, os.environ.get("TELEGRAM_BOT_TOKEN", ""), memoire_express)

    if via_supabase:
        if not sauvegarder_memoire_supabase(memoire_express, CLE_MEMOIRE_EXPRESS, url, cle_service):
            print("[veille_express] ATTENTION : echec de sauvegarde de la memoire express.")
            return 1
    else:
        sauvegarder_json(memoire_express, FICHIER_MEMOIRE_EXPRESS)
    return 0


def boucle(passages: int, intervalle: float) -> int:
    """`passages` veilles espacees de `intervalle` secondes (debut a debut).
    08/10/2026 : le cron GitHub "*/5" ne se declenche jamais en pratique ;
    la veille est donc lancee a la fin de chaque scan_complement (lui-meme
    declenche ~toutes les 20 min par cron-job.org) et couvre l'intervalle
    en 4 passages. Chaque passage relit les memoires (etat a jour). Code de
    sortie : le pire des passages."""
    pire = 0
    for i in range(passages):
        debut = time.monotonic()
        print(f"--- Passage {i + 1}/{passages} ({_maintenant()}) ---")
        pire = max(pire, main())
        if i < passages - 1:
            time.sleep(max(0.0, intervalle - (time.monotonic() - debut)))
    return pire


if __name__ == "__main__":
    sys.exit(boucle(int(os.environ.get("VEILLE_PASSAGES", "1")),
                    float(os.environ.get("VEILLE_INTERVALLE", "300"))))
