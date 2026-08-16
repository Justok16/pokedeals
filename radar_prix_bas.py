"""
Radar de prix bas quotidien -- systeme INDEPENDANT (nouveau fichier, ne
modifie aucun connecteur/orchestrateur/watchlist existant), pour les 4
cartes de watchlist_prix_bas.py, suivies dans les 4 langues qui interessent
Justok (FR/JP/KR/CN).

Objectif : chaque jour a 11h (heure de Paris), reperer le prix le PLUS BAS
actuellement disponible pour chaque carte -- tous sites/plateformes/langues
confondus -- et confirmer sa disponibilite au moment de l'envoi. Envoye sur
Telegram MEME si aucune bonne affaire n'est detectee (contrairement a
bonne_affaire_shopify.py/main.py, qui n'alertent QUE sous la cote) : c'est
un etat des lieux quotidien, pas une alerte de deal.

Les alertes IMMEDIATES "des qu'un prix passe sous la cote" pour ces memes 4
cartes restent gerees par les systemes EXISTANTS (main.py pour eBay/Vinted/
Leboncoin, bonne_affaire_shopify.py pour les 83 boutiques TCG), via les
entrees FR/JP/KR/CN deja presentes dans config.yaml -- ce fichier ne
duplique PAS cette logique, il vient en complement (etat des lieux, pas
detection de deal).

Sources couvertes : eBay + Vinted (reutilise main.py) + 83 boutiques TCG
Shopify/PrestaShop/WooCommerce + boutiques auto-decouvertes (reutilise les
connecteurs existants tels quels, meme esprit que radar_precommandes.py).
Volontairement HORS perimetre (cf. session du 13/08/2026) : Leboncoin
(bloque par anti-bot, fonctionne uniquement via alertes email pre-
configurees, pas de recherche a la demande possible), Cardmarket (API
fermee + scraping quotidien interdit par leurs CGU), TCGplayer (marche
quasi exclusivement americain, peu pertinent pour un filtre "vendeur en
France").
"""

import os
import re
import sys
import time

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import main as pokedeals
from bonne_affaire_shopify import _est_carte_gradee, _etat_refuse
from boutiques_decouvertes import BOUTIQUES_SHOPIFY_AUTO, BOUTIQUES_WOOCOMMERCE_AUTO
from boutiques_prestashop import BOUTIQUES_PRESTASHOP_REPLI_HTML, BOUTIQUES_PRESTASHOP_SITEMAP
from boutiques_shopify import BOUTIQUES_SHOPIFY
from boutiques_woocommerce import (
    BOUTIQUES_WOOCOMMERCE_REPLI_API_REST,
    BOUTIQUES_WOOCOMMERCE_SITEMAP,
)
from connecteur_prestashop_sitemap import ConnecteurPrestaShopSitemap
from connecteur_shopify import ConnecteurShopify
from connecteur_woocommerce import ConnecteurWooCommerce
from telegram_utils import echapper_html, echapper_url_html
from watchlist_prix_bas import FAMILLES_PRIX_BAS
from watchlist_shopify import charger_watchlist_config, detecter_qualificatif_titre

TELEGRAM_CHAT_ID = "1245330032"
DELAI_ENTRE_BOUTIQUES = 2.0  # meme politesse que scan_boutique*.py
LABEL_LANGUE = {"fr": "FR", "jp": "JP", "kr": "KR", "cn": "CN"}


# =====================================================================
# eBay + Vinted -- reutilise main.py tel quel (ebay_rechercher,
# vinted_rechercher, annonce_pertinente), sans rien y modifier.
# =====================================================================

def _rechercher_ebay_vinted(nom_config: str, langue: str, alias: str,
                            secrets: dict, cfg_regles: dict) -> list[dict]:
    resultats = []

    try:
        annonces_ebay = pokedeals.ebay_rechercher(nom_config, langue, secrets, 40, cfg_regles, alias)
    except Exception as e:  # noqa: BLE001 -- une source en echec ne doit jamais bloquer les autres
        print(f"    [eBay] erreur pour '{nom_config}' ({langue}) : {e}")
        annonces_ebay = []
    for a in annonces_ebay:
        pertinent, _ = pokedeals.annonce_pertinente(a["titre"], nom_config, langue, alias, a.get("plateforme", ""))
        if not pertinent:
            continue
        resultats.append({
            "plateforme": a["plateforme"],
            "prix": a["prix"] + (a.get("port") or 0),
            "url": a["url"],
            "titre": a["titre"],
        })

    try:
        annonces_vinted = pokedeals.vinted_rechercher(nom_config, langue, 30)
    except Exception as e:  # noqa: BLE001
        print(f"    [Vinted] erreur pour '{nom_config}' ({langue}) : {e}")
        annonces_vinted = []
    for a in annonces_vinted:
        pertinent, _ = pokedeals.annonce_pertinente(a["titre"], nom_config, langue, alias, "Vinted")
        if not pertinent:
            continue
        resultats.append({
            "plateforme": "Vinted",
            "prix": a["prix"] + (a.get("port") or 0),
            "url": a["url"],
            "titre": a["titre"],
        })

    return resultats


# =====================================================================
# Boutiques TCG -- reutilise les connecteurs Shopify/PrestaShop/WooCommerce
# EXISTANTS (meme mecanique que scan_boutique*.py), mais retourne les
# ResultatRecherche BRUTS (prix/stock/url) au lieu de les faire passer par
# detecter_bonnes_affaires/detecter_retours_en_stock -- ce radar veut le
# prix le plus bas du jour, pas seulement les deals sous cote.
# =====================================================================

def _fusionner(cible: dict, source: dict) -> None:
    for cle, liste in source.items():
        cible.setdefault(cle, []).extend(liste)


def _scanner_boutiques(criteres: list[tuple[str, str | None]]) -> dict:
    """dict[(nom, numero)] -> list[ResultatRecherche], sur toutes les
    boutiques actives, pour les seuls `criteres` demandes (pas la
    watchlist complete -- beaucoup plus rapide qu'un scan_boutique*.py
    normal, qui cherche ~194 criteres au lieu d'une quinzaine ici)."""
    resultats: dict = {}

    boutiques_shopify = list(BOUTIQUES_SHOPIFY) + list(BOUTIQUES_SHOPIFY_AUTO)
    print(f"  Shopify : {len(boutiques_shopify)} boutique(s)")
    for domaine in boutiques_shopify:
        try:
            connecteur = ConnecteurShopify(domaine)
            catalogue = connecteur.recuperer_tout_le_catalogue()
            _fusionner(resultats, connecteur.rechercher_dans_catalogue(catalogue, criteres))
        except Exception as e:  # noqa: BLE001 -- une boutique en echec ne bloque pas les autres
            print(f"    [Shopify] {domaine} : echec ({e})")
        time.sleep(DELAI_ENTRE_BOUTIQUES)

    print(f"  PrestaShop (sitemap) : {len(BOUTIQUES_PRESTASHOP_SITEMAP)} boutique(s)")
    for domaine in BOUTIQUES_PRESTASHOP_SITEMAP:
        try:
            connecteur = ConnecteurPrestaShopSitemap(domaine)
            urls = connecteur.recuperer_toutes_les_urls_produits()
            _fusionner(resultats, connecteur.rechercher_dans_catalogue(urls, criteres))
        except Exception as e:  # noqa: BLE001
            print(f"    [PrestaShop] {domaine} : echec ({e})")
        time.sleep(DELAI_ENTRE_BOUTIQUES)

    print(f"  PrestaShop (repli HTML) : {len(BOUTIQUES_PRESTASHOP_REPLI_HTML)} boutique(s)")
    for domaine in BOUTIQUES_PRESTASHOP_REPLI_HTML:
        try:
            connecteur = ConnecteurPrestaShopSitemap(domaine)
            _fusionner(resultats, connecteur.rechercher_via_recherche_html(criteres))
        except Exception as e:  # noqa: BLE001
            print(f"    [PrestaShop repli] {domaine} : echec ({e})")
        time.sleep(DELAI_ENTRE_BOUTIQUES)

    boutiques_woo = list(BOUTIQUES_WOOCOMMERCE_SITEMAP) + list(BOUTIQUES_WOOCOMMERCE_AUTO)
    repli_api_rest = set(BOUTIQUES_WOOCOMMERCE_REPLI_API_REST)
    print(f"  WooCommerce : {len(boutiques_woo)} boutique(s)")
    for domaine in boutiques_woo:
        try:
            connecteur = ConnecteurWooCommerce(domaine)
            if domaine in repli_api_rest:
                resultats_boutique = connecteur.rechercher_via_api_rest(criteres)
            else:
                urls = connecteur.recuperer_toutes_les_urls_produits()
                resultats_boutique = connecteur.rechercher_dans_catalogue(urls, criteres)
            _fusionner(resultats, resultats_boutique)
        except Exception as e:  # noqa: BLE001
            print(f"    [WooCommerce] {domaine} : echec ({e})")
        time.sleep(DELAI_ENTRE_BOUTIQUES)

    return resultats


# =====================================================================
# Analyse : meilleur prix par famille, tous sites/langues confondus.
# =====================================================================

def _resultat_boutique_fiable(res, carte) -> bool:
    """Memes garde-fous, dans le meme ordre, que bonne_affaire_shopify.py/
    alerte_stock.py (gradee -> etat -> langue -> qualificatif) -- ce radar
    reutilise les MEMES ResultatRecherche mais avait jusqu'ici son propre
    filtre "confiance forte + en stock" SANS ces garde-fous, ce qui laissait
    passer des cartes homonymes non-ex/gradees/langue incoherente. Cas reel
    (14/08/2026) : "Plumeline ex 024" (config) confondu avec "Plumeline 24
    Sun & Moon REVERSE" (1,50€, meme nom+numero, pas "ex") sur kyoriyu.fr --
    exactement le piege deja documente et corrige ailleurs, mais jamais ici."""
    if _est_carte_gradee(res.titre):
        return False
    if _etat_refuse(res.etat_detecte):
        return False
    if res.langue_detectee == "jp_ou_kr":
        if carte.langue not in ("jp", "kr"):
            return False
    elif res.langue_detectee is not None and res.langue_detectee != carte.langue:
        return False
    if carte.qualificatif:
        if not re.search(rf"\b{re.escape(carte.qualificatif)}\b", res.titre.lower()):
            return False
    elif detecter_qualificatif_titre(res.titre, carte.numero) is not None:
        return False
    return True


def analyser_famille(famille, entrees_brutes: dict, secrets: dict, cfg_regles: dict,
                     resultats_boutiques: dict, cartes_boutiques_par_nom_config: dict) -> dict | None:
    """Retourne le meilleur (prix le plus bas, en stock, confiance forte
    pour les boutiques) resultat trouve pour une famille de carte, ou None
    si rien de fiable n'a ete trouve nulle part aujourd'hui."""
    meilleur = None

    for variante in famille.variantes:
        entree = entrees_brutes.get((variante.nom_config, variante.langue), {})
        alias = entree.get("alias", "")

        for r in _rechercher_ebay_vinted(variante.nom_config, variante.langue, alias, secrets, cfg_regles):
            if meilleur is None or r["prix"] < meilleur["prix"]:
                meilleur = {**r, "langue": variante.langue}

        for carte in cartes_boutiques_par_nom_config.get(variante.nom_config, []):
            # Le meme nom_config est parfois partage entre plusieurs langues
            # (ex. JP/KR/CN-T qui reprennent le meme numero/code de set) :
            # sans ce filtre, un resultat coreen trouve pendant l'iteration
            # "jp" se serait vu etiquete a tort "langue: jp" plus bas (bug
            # reel trouve le 16/08/2026, revele en corrigeant l'entree CN de
            # Carapuce -- meme nom_config que JP/KR depuis ce correctif).
            if carte.langue != variante.langue:
                continue
            for res in resultats_boutiques.get(carte.cle_recherche, []):
                if res.confiance != "forte" or not res.en_stock:
                    continue
                if not _resultat_boutique_fiable(res, carte):
                    continue
                if meilleur is None or res.prix < meilleur["prix"]:
                    meilleur = {
                        "plateforme": res.boutique,
                        "prix": res.prix,
                        "url": res.url_produit,
                        "titre": res.titre,
                        "langue": variante.langue,
                    }

    return meilleur


# =====================================================================
# Telegram
# =====================================================================

def _texte_ligne(famille, meilleur: dict | None) -> str:
    if meilleur is None:
        return (f"❔ <b>{echapper_html(famille.nom_affichage)}</b>\n"
                f"Aucune annonce fiable trouvée aujourd'hui, toutes langues et sources confondues.")
    langue_label = LABEL_LANGUE.get(meilleur["langue"], meilleur["langue"].upper())
    return (
        f"🏷️ <b>{echapper_html(famille.nom_affichage)}</b>\n"
        f"💶 <b>{meilleur['prix']:.2f}€</b> ({langue_label}) — {echapper_html(meilleur['plateforme'])}\n"
        f"✅ Disponible (vérifié à l'instant)\n"
        f"👉 <a href=\"{echapper_url_html(meilleur['url'])}\">Voir l'annonce</a>"
    )


def envoyer_telegram(lignes: list[str], chat_id: str, token: str) -> bool:
    if not token or not chat_id:
        print("[radar_prix_bas] Telegram non configuré : rapport non envoyé.")
        return False
    texte = "📊 <b>Prix du jour — cartes suivies</b>\n\n" + "\n\n".join(lignes)
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        r = requests.post(url, json={
            "chat_id": chat_id, "text": texte, "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }, timeout=15)
        r.raise_for_status()
        return True
    except Exception as e:  # noqa: BLE001
        print(f"[radar_prix_bas] envoi Telegram échoué : {e}")
        return False


# =====================================================================
# Orchestration
# =====================================================================

def main() -> int:
    debut = time.time()
    cfg = pokedeals.charger_config()
    secrets = pokedeals.secrets_env()

    voulues = {(v.nom_config, v.langue) for f in FAMILLES_PRIX_BAS for v in f.variantes}
    entrees_brutes = {(e["nom"], e["langue"]): e for e in cfg["watchlist"] if (e["nom"], e["langue"]) in voulues}

    nom_configs = {v.nom_config for f in FAMILLES_PRIX_BAS for v in f.variantes}
    cartes_boutiques = [c for c in charger_watchlist_config() if c.nom_config in nom_configs]
    cartes_boutiques_par_nom_config: dict[str, list] = {}
    for c in cartes_boutiques:
        cartes_boutiques_par_nom_config.setdefault(c.nom_config, []).append(c)

    criteres = list({c.cle_recherche for c in cartes_boutiques})
    print(f"{len(FAMILLES_PRIX_BAS)} famille(s) de cartes, {len(criteres)} critère(s) de recherche boutiques\n")

    print("Scan des boutiques TCG...")
    resultats_boutiques = _scanner_boutiques(criteres)
    print()

    lignes = []
    for famille in FAMILLES_PRIX_BAS:
        print(f"=== {famille.nom_affichage} ===")
        meilleur = analyser_famille(famille, entrees_brutes, secrets, cfg["regles"],
                                    resultats_boutiques, cartes_boutiques_par_nom_config)
        if meilleur:
            print(f"  -> {meilleur['prix']:.2f}€ ({meilleur['langue'].upper()}) sur {meilleur['plateforme']}")
        else:
            print("  -> aucune annonce fiable trouvée")
        lignes.append(_texte_ligne(famille, meilleur))

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    envoyer_telegram(lignes, TELEGRAM_CHAT_ID, token)

    duree = time.time() - debut
    print(f"\nDurée totale : {duree:.1f}s ({duree / 60:.1f} min)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
