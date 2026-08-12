"""
Accumulateur de prix long terme + indicateur de tendance, pour repondre a
"est-ce un bon moment pour acheter CETTE carte precise ?" (demande de
Justok, 12/08/2026, pour un petit nombre de cartes JP/KR/CN precises --
cf. watchlist_tendance.py).

Pourquoi un fichier separe de main.py/data/cotes.json :
  - cotes.json est plafonne a 5 points par carte (HISTORIQUE_MAX) et purge
    entierement a chaque changement de version de la logique de cote
    (PURGE_VERSION) -- concu pour du lissage court terme, pas un historique
    long terme. Ce fichier-ci n'est NI plafonne a 5 NI purge : il grossit
    indefiniment (jusqu'a LIMITE_POINTS_PAR_CARTE, tres large).
  - Aucun "nombre d'achats" (volume de ventes reelles) n'existe gratuitement
    pour eBay (Marketplace Insights API fermee aux nouveaux comptes, deja
    verifie pour PokeDeals). PokemonPriceTracker (pokemonpricetracker.com)
    comble partiellement ce manque : GRATUIT, couvre les cartes japonaises,
    et fournit un historique de VENTES EBAY REELLES -- mais UNIQUEMENT pour
    les copies GRADEES (PSA/CGC). Pour les cartes brutes (la plupart des
    JP/KR/CN suivies ici), seul un prix de marche est disponible, pas de
    volume -- meme limite qu'ailleurs, honnetement documentee.

Ce module ne decide JAMAIS d'acheter a la place de Justok -- il calcule un
signal de tendance simple (prix actuel vs moyenne recente accumulee) et le
rapporte. Aucune donnee retroactive sur 1 an n'existe : le signal ne devient
significatif qu'apres plusieurs semaines/mois d'accumulation reelle.
"""

import os
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from connecteur_shopify import HEADERS, TIMEOUT  # User-Agent + timeout partages
from memoire_json import charger_memoire, sauvegarder_memoire
from watchlist_tendance import CARTES_TENDANCE, CarteTendance

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FICHIER_HISTORIQUE = Path(__file__).parent / "data" / "historique_prix_tendance.json"
FICHIER_COTES = Path(__file__).parent / "data" / "cotes.json"

POKEMONPRICETRACKER_BASE_URL = "https://www.pokemonpricetracker.com/api/v2"

# Large mais pas illimite -- ~3 ans de points quotidiens, garde-fou contre
# une croissance infinie du fichier si le script tourne pendant des annees.
LIMITE_POINTS_PAR_CARTE = 1200

# Nombre minimum de points accumules avant de calculer un signal de
# tendance -- avec moins, comparer "aujourd'hui" a "la moyenne des 3
# derniers jours" n'a aucun sens statistique. Meme philosophie que
# alerte_stock.py (pas d'alerte sur la toute premiere donnee).
MIN_POINTS_POUR_SIGNAL = 14

# Fenetre de la moyenne "recente" utilisee comme reference pour le signal.
FENETRE_MOYENNE_JOURS = 30

# Ecart (en %) par rapport a la moyenne recente pour classer un signal
# comme "bon moment pour acheter" / "prix eleve, pas le bon moment".
SEUIL_SIGNAL_PCT = 10.0


def _cle_historique(carte: CarteTendance) -> str:
    return f"{carte.nom_config}|{carte.langue}"


def _pokemonpricetracker_prix(carte: CarteTendance, cle_api: str) -> dict | None:
    """Interroge PokemonPriceTracker pour le prix marche actuel d'une carte
    japonaise, best-effort.

    V2 (12/08/2026, apres le tout premier run reel) : "name"/"number" ne
    sont PAS des parametres acceptes par l'API (HTTP 400, confirme en
    prod) -- les seuls parametres documentes sont search/set/setId/
    tcgPlayerId/etc. On combine donc nom + numero dans "search" (recherche
    texte libre), avec "set" pour restreindre. La structure exacte de la
    reponse JSON n'est TOUJOURS PAS confirmee (pas encore eu de 200 avec
    resultat) -- le parsing ci-dessous reste best-effort, avec le JSON brut
    logué en cas d'echec pour ajuster au prochain run.

    Retourne None si la carte n'est pas trouvee, si l'API echoue, ou si la
    cle n'est pas configuree -- jamais bloquant pour le reste du script."""
    if not cle_api:
        return None
    try:
        r = requests.get(
            f"{POKEMONPRICETRACKER_BASE_URL}/cards",
            headers={**HEADERS, "Authorization": f"Bearer {cle_api}"},
            params={
                "language": "japanese" if carte.langue in ("jp", "kr") else "chinese",
                "search": f"{carte.nom_anglais} {carte.numero}",
                "set": carte.set_jp,
                "includeEbay": "true",
                "limit": 1,
            },
            timeout=TIMEOUT,
        )
        if r.status_code != 200:
            print(f"[pokemonpricetracker] {carte.nom_affichage} : HTTP {r.status_code} — {r.text[:300]}", file=sys.stderr)
            return None
        data = r.json()
        resultats = data.get("data") or data.get("cards") or data.get("results") or ([data] if data.get("name") else [])
        if not resultats:
            print(f"[pokemonpricetracker] {carte.nom_affichage} : aucun resultat — reponse brute : {str(data)[:400]}", file=sys.stderr)
            return None
        carte_trouvee = resultats[0]
        prix = (carte_trouvee.get("prices") or {}).get("market") or carte_trouvee.get("marketPrice") or carte_trouvee.get("price")
        ventes_psa10 = ((carte_trouvee.get("ebay") or {}).get("psa10") or {}).get("avg")
        if prix is None:
            print(f"[pokemonpricetracker] {carte.nom_affichage} : resultat trouve mais champ prix introuvable "
                  f"— resultat brut : {str(carte_trouvee)[:400]}", file=sys.stderr)
            return None
        return {"prix_marche": float(prix), "prix_gradee_psa10": float(ventes_psa10) if ventes_psa10 else None}
    except (requests.exceptions.RequestException, ValueError, KeyError, TypeError) as e:
        print(f"[pokemonpricetracker] {carte.nom_affichage} : echec — {e}", file=sys.stderr)
        return None


def _derniere_cote_locale(carte: CarteTendance) -> float | None:
    """Cote la plus recente deja connue de PokeDeals (data/cotes.json), si
    elle existe pour cette carte -- purement informatif, en complement du
    prix PokemonPriceTracker (cotes.json n'a que 5 points glissants, cf.
    docstring du module)."""
    if not FICHIER_COTES.exists():
        return None
    try:
        import json
        cotes = json.loads(FICHIER_COTES.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    historique = cotes.get(_cle_historique(carte))
    if not historique:
        return None
    plus_recente = max(historique, key=lambda e: e.get("ts", 0))
    return float(plus_recente.get("cote")) if plus_recente.get("cote") else None


def enregistrer_point_du_jour(carte: CarteTendance, historique: dict, cle_api_ppt: str) -> dict | None:
    """Ajoute le point du jour pour une carte si pas deja fait aujourd'hui
    (idempotent -- le script peut tourner plusieurs fois le meme jour sans
    dupliquer). Retourne le point ajoute, ou None si rien de nouveau."""
    cle = _cle_historique(carte)
    points = historique.setdefault(cle, [])

    aujourdhui = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if points and points[-1].get("date") == aujourdhui:
        return None  # deja enregistre aujourd'hui

    donnees_ppt = _pokemonpricetracker_prix(carte, cle_api_ppt)
    cote_locale = _derniere_cote_locale(carte)

    if donnees_ppt is None and cote_locale is None:
        return None  # aucune source n'a rien donne aujourd'hui -- rien a enregistrer

    point = {
        "date": aujourdhui,
        "prix_pokemonpricetracker": donnees_ppt["prix_marche"] if donnees_ppt else None,
        "prix_gradee_psa10": donnees_ppt.get("prix_gradee_psa10") if donnees_ppt else None,
        "cote_pokedeals": cote_locale,
    }
    points.append(point)
    if len(points) > LIMITE_POINTS_PAR_CARTE:
        del points[: len(points) - LIMITE_POINTS_PAR_CARTE]
    return point


def _prix_reference(point: dict) -> float | None:
    """Le prix a utiliser pour le calcul de tendance : PokemonPriceTracker
    en priorite (couvre reellement le marche JP/KR/CN vise), la cote
    PokeDeals (eBay, souvent absente pour ces langues) en repli."""
    return point.get("prix_pokemonpricetracker") or point.get("cote_pokedeals")


def analyser_tendance(points: list[dict]) -> dict | None:
    """Calcule un signal simple : prix le plus recent vs moyenne des
    `FENETRE_MOYENNE_JOURS` derniers jours DISPONIBLES (pas forcement
    calendaires -- le script ne tourne qu'une fois par jour, donc "derniers
    N points" = "derniers N jours" en pratique).

    Retourne None tant que MIN_POINTS_POUR_SIGNAL n'est pas atteint --
    comparer a une moyenne calculee sur trop peu de points n'a pas de sens
    statistique (meme logique que alerte_stock.py : pas de conclusion sur
    une premiere donnee)."""
    valeurs = [(_prix_reference(p), p["date"]) for p in points if _prix_reference(p) is not None]
    if len(valeurs) < MIN_POINTS_POUR_SIGNAL:
        return {"signal": "pas_assez_de_donnees", "nb_points": len(valeurs),
                "points_manquants": MIN_POINTS_POUR_SIGNAL - len(valeurs)}

    fenetre = valeurs[-FENETRE_MOYENNE_JOURS:]
    prix_actuel, date_actuelle = valeurs[-1]
    moyenne_recente = statistics.mean(v for v, _ in fenetre)
    ecart_pct = (prix_actuel - moyenne_recente) / moyenne_recente * 100

    if ecart_pct <= -SEUIL_SIGNAL_PCT:
        signal = "bon_moment_achat"
    elif ecart_pct >= SEUIL_SIGNAL_PCT:
        signal = "prix_eleve"
    else:
        signal = "stable"

    return {
        "signal": signal,
        "prix_actuel": round(prix_actuel, 2),
        "date_actuelle": date_actuelle,
        "moyenne_recente": round(moyenne_recente, 2),
        "ecart_pct": round(ecart_pct, 1),
        "nb_points_fenetre": len(fenetre),
        "nb_points_total": len(valeurs),
    }


def charger_historique() -> dict:
    return charger_memoire(FICHIER_HISTORIQUE)


def sauvegarder_historique(historique: dict) -> None:
    sauvegarder_memoire(historique, FICHIER_HISTORIQUE)


_LIBELLES_SIGNAL = {
    "bon_moment_achat": "🟢 BON MOMENT POUR ACHETER",
    "prix_eleve": "🔴 PRIX ÉLEVÉ, PAS LE MOMENT",
    "stable": "⚪ PRIX STABLE",
}


def _texte_telegram_tendance(carte: CarteTendance, tendance: dict) -> str:
    lignes = [
        f"📈 <b>Tendance prix — {carte.nom_affichage}</b>",
        _LIBELLES_SIGNAL.get(tendance["signal"], tendance["signal"]),
        "",
        f"Prix actuel ({tendance['date_actuelle']}) : <b>{tendance['prix_actuel']:.2f}€</b>",
        f"Moyenne des {tendance['nb_points_fenetre']} derniers points : {tendance['moyenne_recente']:.2f}€",
        f"Écart : <b>{tendance['ecart_pct']:+.1f}%</b>",
    ]
    return "\n".join(lignes)


def envoyer_telegram_tendance(carte: CarteTendance, tendance: dict, chat_id: str, token: str) -> bool:
    """Envoie une notification UNIQUEMENT quand le signal vient de CHANGER
    par rapport au dernier signal notifié (meme anti-spam que alerte_stock.py
    / alerte_precommande.py) -- sinon un "prix stable" quotidien spammerait
    inutilement. Le changement est detecte par l'appelant (main), cette
    fonction envoie seulement."""
    if not token or not chat_id:
        print(f"[historique_prix] Telegram non configure : signal '{tendance['signal']}' pour {carte.nom_affichage} non envoye.")
        return False
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": _texte_telegram_tendance(carte, tendance), "parse_mode": "HTML"},
            timeout=TIMEOUT,
        )
        if not r.ok:
            print(f"[historique_prix] Telegram a refuse ({r.status_code}) : {r.text[:200]}", file=sys.stderr)
            return False
        return True
    except requests.exceptions.RequestException as e:
        print(f"[historique_prix] echec envoi Telegram : {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    cle_api_ppt = os.environ.get("POKEMONPRICETRACKER_API_KEY", "")
    token_tg = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id_tg = os.environ.get("TELEGRAM_CHAT_ID", "1245330032")  # meme chat que le reste de PokeDeals
    print(f"PokemonPriceTracker : {'configure' if cle_api_ppt else 'NON configure (POKEMONPRICETRACKER_API_KEY absent -- prix PokeDeals seul utilise)'}")
    print(f"Telegram : {'configure' if token_tg else 'NON configure'}\n")

    historique = charger_historique()
    derniers_signaux = historique.setdefault("_derniers_signaux_notifies", {})

    for carte in CARTES_TENDANCE:
        point = enregistrer_point_du_jour(carte, historique, cle_api_ppt)
        cle = _cle_historique(carte)
        if point:
            print(f"[{carte.nom_affichage}] point ajoute : {point}")
        else:
            print(f"[{carte.nom_affichage}] rien de nouveau aujourd'hui (deja fait, ou aucune source disponible)")

        tendance = analyser_tendance(historique.get(cle, []))
        print(f"  -> {tendance}")

        if tendance["signal"] in ("bon_moment_achat", "prix_eleve", "stable"):
            if derniers_signaux.get(cle) != tendance["signal"]:
                if envoyer_telegram_tendance(carte, tendance, chat_id_tg, token_tg):
                    derniers_signaux[cle] = tendance["signal"]
                    print(f"  -> alerte envoyee (changement de signal)")
            else:
                print(f"  -> signal inchange depuis la derniere alerte, silence")

    sauvegarder_historique(historique)
    print(f"\nHistorique sauvegarde dans {FICHIER_HISTORIQUE}")
