"""
Scanner + memoire + alerte pour le radar de precommandes GENERIQUE
(PokePrecoms) -- utilise precommande_generique.py (matching SANS produit
connu a l'avance) sur le catalogue d'une boutique.

Demarre volontairement SHOPIFY UNIQUEMENT : son catalogue complet (titre +
description) est deja recupere en un seul appel HTTP (/products.json, cf.
ConnecteurShopify.recuperer_tout_le_catalogue), donc ce radar est GRATUIT en
requetes reseau supplementaires -- meme raisonnement que cartes_watchlist_saas()
(watchlist_saas.py). PrestaShop/WooCommerce necessiteraient une requete PAR
PAGE PRODUIT (contrairement a precommandes_watchlist.py, il n'y a pas de
mot-cle EDITION fixe propre a un produit pour prefiltrer le sitemap comme le
fait radar_precommandes._slug_est_candidat) -- risque documente de timeout
(cf. CLAUDE.md, piege "Prefiltre de decouverte de candidats trop laxiste")
si fait a la legere. A etendre a ces plateformes dans une etape ulterieure,
une fois ce premier radar valide en conditions reelles.

Memoire et logique d'alerte : MEME philosophie que alerte_stock.py/
alerte_precommande.py -- la premiere apparition d'un produit CANDIDAT
etablit une base silencieuse (jamais d'alerte), pour ne pas spammer tout le
catalogue existant au premier lancement du radar sur une boutique. Une
alerte n'est declenchee QUE quand un produit deja connu passe de
"pas en stock" a "en stock" (demande explicite : "faire en sorte qu'il y
ait bien du stock, sinon inutile") -- jamais sur la simple apparition d'une
page, contrairement au radar a produits fixes qui peut alerter des la
premiere detection si une date de sortie est confirmee (aucun equivalent
ici, il n'y a pas de date attendue a confirmer pour un produit inconnu
a l'avance).
"""
from __future__ import annotations

import re
from datetime import datetime, timezone

import requests

from precommande_generique import produit_est_candidat_precommande
from telegram_utils import echapper_html, echapper_url_html


def _horodatage() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# --- Scan (Shopify uniquement, cf. docstring du module) ---

def scanner_shopify_precommandes_generiques(domaine: str, connecteur=None) -> list[dict]:
    """Retourne les produits CANDIDATS a une precommande Pokemon TCG
    generique trouves sur le catalogue Shopify de `domaine` -- pas encore
    filtres contre la memoire (fait par detecter_nouvelles_precommandes_generiques)."""
    from connecteur_shopify import ConnecteurShopify
    connecteur = connecteur or ConnecteurShopify(domaine)
    catalogue = connecteur.recuperer_tout_le_catalogue()

    candidats = []
    for p in catalogue:
        titre = p.get("title", "")
        description = re.sub(r"<[^>]+>", " ", p.get("body_html") or "")
        ok, raison = produit_est_candidat_precommande(titre, description)
        if not ok:
            continue

        handle = p.get("handle", "")
        variants = p.get("variants") or []
        en_stock = any(v.get("available") for v in variants) if variants else False
        prix = None
        if variants:
            try:
                prix = float(variants[0].get("price"))
            except (TypeError, ValueError):
                pass

        candidats.append({
            "domaine": domaine,
            "slug": handle,
            "titre": titre,
            "url_produit": f"{connecteur.base_url}/products/{handle}",
            "prix": prix,
            "en_stock": en_stock,
            "raison": raison,
            "horodatage": _horodatage(),
        })
    return candidats


# --- Memoire et detection de nouveaute (meme principe que alerte_stock.py) ---

def _cle_memoire(domaine: str, slug: str) -> str:
    return f"{domaine}|{slug}"


def detecter_nouvelles_precommandes_generiques(candidats: list[dict], memoire: dict) -> list[dict]:
    """N'alerte JAMAIS sur la toute premiere detection d'un (domaine, slug)
    -- etablit une base silencieuse, meme si deja en stock a ce moment (evite
    de spammer tout le catalogue existant des l'activation du radar sur une
    boutique, meme principe que alerte_stock.py/alerte_precommande.py).

    Alerte ENSUITE une seule fois, quand un produit deja connu passe de
    "pas en stock" (False/indetermine) a "en stock" (True) -- c'est le seul
    evenement pertinent ici : une precommande existante mais indisponible
    n'est pas actionnable.

    ECRITURE MEMOIRE DIFFEREE (meme pattern V57 que alerte_precommande.py) :
    pour un candidat qui declenche une alerte, l'etat n'est PAS ecrit ici --
    attache a l'evenement (`_cle_memoire`/`_nouvel_etat`), commite seulement
    apres confirmation d'envoi Telegram reussi par
    envoyer_telegram_precommandes_generiques(). Pour un candidat qui
    n'alerte pas, l'ecriture reste immediate (rien n'est du a l'utilisateur,
    aucune perte possible)."""
    evenements = []

    for c in candidats:
        cle = _cle_memoire(c["domaine"], c["slug"])
        etat_precedent = memoire.get(cle)
        premiere_fois = etat_precedent is None
        stock_vient_de_souvrir = (
            etat_precedent is not None
            and etat_precedent.get("en_stock") is not True
            and c.get("en_stock") is True
        )

        nouvel_etat = {
            "titre_produit": c["titre"],
            "url_produit": c["url_produit"],
            "prix": c.get("prix"),
            "en_stock": c.get("en_stock"),
            "derniere_verification": c["horodatage"],
        }

        if not premiere_fois and stock_vient_de_souvrir:
            c["_cle_memoire"] = cle
            c["_nouvel_etat"] = nouvel_etat
            evenements.append(c)
        else:
            memoire[cle] = nouvel_etat

    return evenements


# --- Notification Telegram ---

def _texte_precommande_generique(e: dict) -> str:
    prix_ligne = f"💰 {e['prix']:.2f}€\n" if e.get("prix") else ""
    return (
        f"🎉 <b>Précommande Pokémon TCG détectée !</b>\n"
        f"🏪 {echapper_html(e['domaine'])}\n"
        f"📦 En stock / commandable\n"
        f"{prix_ligne}"
        f"📝 {echapper_html(e['titre'])}\n"
        f"👉 <a href=\"{echapper_url_html(e['url_produit'])}\">Voir le produit</a>"
    )


def envoyer_telegram_precommandes_generiques(
    evenements: list[dict], chat_id: str, token: str, memoire: dict | None = None
) -> bool:
    """`memoire`, si fourni : l'etat differe de
    detecter_nouvelles_precommandes_generiques() n'est commite dans
    `memoire` QU'APRES confirmation d'envoi reussi pour CET evenement precis
    -- un echec (Telegram indisponible, token invalide...) laisse `memoire`
    intacte, pour que l'evenement soit redetecte et retente au prochain
    cycle plutot que perdu definitivement."""
    if not evenements:
        return True
    if not token or not chat_id:
        print("[radar_precommande_generique] Telegram non configure : alertes non envoyees.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    ok = True
    for e in evenements:
        succes = False
        try:
            r = requests.post(
                url,
                json={"chat_id": chat_id, "text": _texte_precommande_generique(e), "parse_mode": "HTML"},
                timeout=20,
            )
            if r.status_code == 200:
                succes = True
            else:
                print(f"[radar_precommande_generique] Telegram a refusé l'alerte ({r.status_code}) : {r.text[:200]}")
        except Exception as ex:  # noqa: BLE001
            print(f"[radar_precommande_generique] Échec envoi Telegram : {ex}")

        if succes:
            if memoire is not None and "_cle_memoire" in e:
                memoire[e["_cle_memoire"]] = e["_nouvel_etat"]
        else:
            ok = False
    return ok
