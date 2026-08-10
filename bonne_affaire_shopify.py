"""
Detection des "bonnes affaires" sur les boutiques Shopify pour PokeDeals.

Systeme d'alerte INDEPENDANT de celui du retour en stock (alerte_stock.py) :
celui-ci compare le prix affiche a la cote connue de la carte (data/cotes.json)
selon les memes regles que la logique eBay/Vinted/Cardtrader deja en place
dans main.py de PokeDeals (marge_achat, cote_min, profit_min,
prix_plancher_ratio) -- reimplementee ici sous une forme simplifiee car
/products.json Shopify ne donne PAS de frais de port : le "total" utilise
ici est donc le prix affiche SEUL (pas de port a ajouter, contrairement aux
annonces eBay/Vinted). A reviser si les boutiques Shopify integrees plus
tard exposent un frais de port exploitable.

Seuls les resultats a CONFIANCE FORTE (nom+numero) et EN STOCK alimentent ce
systeme : les resultats a confiance faible (repli nom seul) sont trop peu
fiables pour declencher une alerte financiere, et un article en rupture ne
peut de toute facon pas etre achete.
"""

import json
import re
from pathlib import Path

import requests
import yaml

from watchlist_shopify import CarteWatchlist, detecter_qualificatif_titre

# Chemins relatifs au repo (ce fichier vit a la racine, a cote de main.py,
# config.yaml et data/) -- indispensable pour tourner sur le runner GitHub
# Actions (Ubuntu), pas seulement en local sur Windows.
CHEMIN_COTES_DEFAUT = Path(__file__).parent / "data" / "cotes.json"
CHEMIN_CONFIG_DEFAUT = Path(__file__).parent / "config.yaml"


def charger_cotes(chemin: Path = CHEMIN_COTES_DEFAUT) -> dict:
    if not chemin.exists():
        return {}
    with open(chemin, "r", encoding="utf-8") as f:
        return json.load(f)


def derniere_cote(cotes: dict, cle_cotes: str) -> float | None:
    """Cote la plus RECENTE (par timestamp) pour une cle "nom_config|langue"."""
    historique = cotes.get(cle_cotes)
    if not historique:
        return None
    plus_recente = max(historique, key=lambda entree: entree.get("ts", 0))
    return float(plus_recente["cote"])


def charger_regles(chemin: Path = CHEMIN_CONFIG_DEFAUT) -> dict:
    """Charge les regles d'achat/revente globales depuis config.yaml
    (memes cles que celles utilisees par main.py : marge_achat, cote_min,
    profit_min, marge_revente, frais_revente_estimes, prix_plancher_ratio)."""
    with open(chemin, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg.get("regles", {})


def evaluer_deal(
    resultat, carte: CarteWatchlist, cotes: dict, regles: dict
) -> tuple[dict | None, str]:
    """Applique les regles de bonne affaire a un ResultatRecherche donne.
    Retourne (deal, raison) -- deal est None si ce n'est pas une affaire,
    auquel cas `raison` explique pourquoi (pour du log/debug)."""

    if not resultat.en_stock:
        return None, "rupture de stock"

    # Coherence de langue : une carte FR ne s'achete pas comme si elle etait
    # japonaise/chinoise/coreenne, meme numero et meme nom -- les cotes
    # different fortement d'une langue a l'autre (cf. main.py, protection
    # equivalente cote eBay : _localisation_incoherente). On ne rejette que
    # si une AUTRE langue est explicitement detectee dans le titre ; si rien
    # n'est detecte (langue_detectee=None), on laisse passer (risque residuel
    # documente : aucun mot de langue ET aucun code de set reconnu dans le titre).
    #
    # "jp_ou_kr" (cf. connecteur_shopify.detecter_langue) : code de set
    # partage entre impressions japonaises et coreennes (meme numerotation,
    # config.yaml a souvent les deux entrees jp/kr pour le meme numero) --
    # incompatible avec une carte configuree en fr, mais compatible avec jp
    # OU kr puisqu'on ne peut pas trancher lequel des deux a partir du seul
    # code de set.
    if resultat.langue_detectee == "jp_ou_kr":
        if carte.langue not in ("jp", "kr"):
            return None, f"langue incoherente (jp_ou_kr != {carte.langue})"
    elif resultat.langue_detectee is not None and resultat.langue_detectee != carte.langue:
        return None, f"langue incoherente ({resultat.langue_detectee} != {carte.langue})"

    # Qualificatif ("ex"/"gx"/"v"/"vmax"/"vstar") : rejette une carte
    # HOMONYME (meme nom+numero) mais d'une edition differente. Bug reel
    # corrige : "Plumeline ex 024" (config.yaml) et "Plumeline 24 Sun & Moon
    # REVERSE" (carte plus ancienne, non-ex) partagent le meme nom+numero --
    # sans ce filtre, le mauvais Plumeline (1,50€) matchait a la place du bon
    # (28€), declenchant une fausse alerte via le seuil fixe.
    if carte.qualificatif and not re.search(rf"\b{re.escape(carte.qualificatif)}\b", resultat.titre.lower()):
        # \b...\b (limites de mot) et pas un simple "in" : le qualificatif
        # "v" en substring nu matcherait quasiment tous les titres (ex:
        # "Evoli" contient un "v").
        return None, f"qualificatif manquant (\"{carte.qualificatif}\" absent du titre)"

    # Sens INVERSE (symetrique) : une carte configuree SANS qualificatif ne
    # doit pas non plus matcher un titre qui en porte un -- sinon une carte
    # de base ("Bulbizarre 166/165") pourrait matcher a tort une version
    # "ex"/"GX"/"V" homonyme (meme nom+numero, carte differente en realite).
    if carte.qualificatif is None:
        qualificatif_titre = detecter_qualificatif_titre(resultat.titre)
        if qualificatif_titre is not None:
            return None, f"qualificatif inattendu (\"{qualificatif_titre}\" present dans le titre, absent de la config)"

    prix = resultat.prix

    # V45 (portee de main.py) : seuil de prix fixe par carte, independant de
    # la cote.
    if carte.prix_max_fixe:
        if prix <= 0 or prix > float(carte.prix_max_fixe):
            return None, f"prix ({prix:.2f}€) au-dessus du seuil fixe ({carte.prix_max_fixe:.2f}€)"
        return {
            "boutique": resultat.boutique,
            "nom": carte.nom_config,
            "titre_produit": resultat.titre,
            "url_produit": resultat.url_produit,
            "prix": round(prix, 2),
            "cote": float(carte.prix_max_fixe),
            "decote_pct": 0.0,
            "prix_revente_conseille": 0.0,
            "profit_net_estime": 0.0,
            "confiance": 100,
        }, "DEAL (seuil fixe)"

    cote = derniere_cote(cotes, carte.cle_cotes)
    if cote is None or cote <= 0:
        return None, "cote indisponible"

    cote_min = float(regles.get("cote_min", 5.0))
    if cote < cote_min:
        return None, f"cote trop faible ({cote:.2f}€ < {cote_min:.2f}€)"

    marge_achat = float(regles.get("marge_achat", 0.10))
    seuil_achat = cote * (1 - marge_achat)
    if prix > seuil_achat:
        return None, f"pas assez sous la cote ({prix:.2f}€ > seuil {seuil_achat:.2f}€)"

    # Garde-fou "trop beau pour etre vrai" (meme logique que main.py V22.8).
    seuil_absurde = float(regles.get("prix_plancher_ratio", 0.15))
    if prix < cote * seuil_absurde:
        return None, (f"prix suspect ({prix:.2f}€ = {prix / cote * 100:.0f}% de la "
                       f"cote {cote:.2f}€, seuil {seuil_absurde * 100:.0f}%)")

    marge_revente = float(regles.get("marge_revente", 0.10))
    frais_revente = min(float(regles.get("frais_revente_estimes", 0.13)), 0.99)
    prix_revente = cote * (1 + marge_revente) / (1 - frais_revente)
    profit_net = cote * (1 + marge_revente) - prix

    profit_min = float(regles.get("profit_min", 0) or 0)
    if profit_net < max(profit_min, 0.01):
        return None, f"profit trop faible ({profit_net:.2f}€ < {profit_min:.2f}€ minimum)"

    return {
        "boutique": resultat.boutique,
        "nom": carte.nom_config,
        "titre_produit": resultat.titre,
        "url_produit": resultat.url_produit,
        "prix": round(prix, 2),
        "cote": round(cote, 2),
        "decote_pct": round((1 - prix / cote) * 100, 1),
        "prix_revente_conseille": round(prix_revente, 2),
        "profit_net_estime": round(profit_net, 2),
        "confiance": 0,
    }, "DEAL"


def detecter_bonnes_affaires(
    resultats_par_critere: dict,
    cartes_par_critere: dict[tuple, CarteWatchlist],
    cotes: dict,
    regles: dict,
) -> list[dict]:
    """Parcourt les resultats (deja recuperes, partages avec la logique de
    retour en stock) et retourne la liste des bonnes affaires detectees.

    Ne considere que les resultats a confiance forte (nom+numero) -- les
    resultats a confiance faible (repli nom seul) sont ignores, exactement
    comme pour la logique de retour en stock.

    Dedoublonne par (boutique, url_produit) : une carte cherchee via son nom
    principal ET son alias peut faire remonter deux fois le MEME produit."""
    deals = []
    urls_deja_vues: set[tuple[str, str]] = set()

    for cle, resultats in resultats_par_critere.items():
        carte = cartes_par_critere.get(cle)
        if carte is None or carte.numero is None:
            continue  # pas de carte associee, ou confiance faible -> hors perimetre

        for resultat in resultats:
            if resultat.confiance != "forte":
                continue
            deal, _raison = evaluer_deal(resultat, carte, cotes, regles)
            if not deal:
                continue
            cle_dedup = (deal["boutique"], deal["url_produit"])
            if cle_dedup in urls_deja_vues:
                continue
            urls_deja_vues.add(cle_dedup)
            deals.append(deal)

    return deals


# --- Notification Telegram (style proche de l'alerte eBay existante : 🔥) ---

def _echapper_html(texte) -> str:
    return str(texte).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _echapper_url_html(url: str) -> str:
    return str(url).replace("&", "&amp;")


def _texte_bonne_affaire(d: dict) -> str:
    if d.get("confiance") == 100:
        return (
            f"🎯 <b>{_echapper_html(d['nom'])}</b>\n"
            f"🏪 {_echapper_html(d['boutique'])} — <b>{d['prix']:.2f}€</b> "
            f"(seuil fixe : {d['cote']:.2f}€)\n"
            f"👉 <a href=\"{_echapper_url_html(d['url_produit'])}\">Voir le produit</a>"
        )
    # Meme garde-fou que main.py (cote eBay) : une decote extreme n'est pas
    # forcement une bonne nouvelle plus grande -- ca peut etre une erreur de
    # prix, un produit factice, ou (pour Shopify specifiquement) une variante
    # mal identifiee (mauvaise langue/edition). On avertit sans bloquer
    # l'alerte : la decision finale reste a l'humain.
    avertissement = ""
    if d.get("decote_pct", 0) and float(d["decote_pct"]) >= 30:
        avertissement = (
            "\n⚠️ <b>Écart important avec la cote — vérifie la fiche produit avant "
            "d'acheter</b> (variante, édition ou langue potentiellement mal identifiée).")
    return (
        f"🔥 <b>{_echapper_html(d['nom'])}</b>\n"
        f"🏪 {_echapper_html(d['boutique'])} — <b>{d['prix']:.2f}€</b>\n"
        f"📊 Cote : {d['cote']:.2f}€ (<b>-{d['decote_pct']}%</b>)\n"
        f"💶 Revente conseillée : {d['prix_revente_conseille']:.2f}€\n"
        f"✅ Profit net estimé : <b>+{d['profit_net_estime']:.2f}€</b>"
        f"{avertissement}\n"
        f"👉 <a href=\"{_echapper_url_html(d['url_produit'])}\">Voir le produit</a>"
    )


def envoyer_telegram_bonnes_affaires(deals: list[dict], chat_id: str, token: str) -> bool:
    if not deals:
        return True
    if not token or not chat_id:
        print("[bonne_affaire_shopify] Telegram non configure : deals non envoyes.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    ok = True
    for d in deals:
        try:
            r = requests.post(
                url,
                json={"chat_id": chat_id, "text": _texte_bonne_affaire(d), "parse_mode": "HTML"},
                timeout=20,
            )
            if r.status_code != 200:
                print(f"[bonne_affaire_shopify] Telegram a refuse le deal ({r.status_code}) : {r.text[:200]}")
                ok = False
        except Exception as ex:  # noqa: BLE001
            print(f"[bonne_affaire_shopify] Echec envoi Telegram : {ex}")
            ok = False
    return ok
