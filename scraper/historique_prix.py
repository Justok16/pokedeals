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

# Sources de taux de change GRATUITES et SANS CLE, verifiees en direct le
# 13/08/2026 -- frankfurter.dev (Banque Centrale Europeenne) en priorite,
# open.er-api.com en repli si la 1ere echoue. Conversion appliquee
# UNIQUEMENT a L'AFFICHAGE (Telegram) -- jamais aux donnees stockees ni au
# calcul de tendance, qui reste en devise d'origine (un ecart en % entre
# 2 valeurs USD est mathematiquement valide sans conversion prealable).

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


def _requete_pokemonpricetracker(carte: CarteTendance, cle_api: str, avec_set: bool) -> list | None:
    """Un seul appel a /cards. `avec_set=False` : repli sans le parametre
    "set" (recherche texte libre seule), utilise si la recherche avec set
    ne renvoie rien -- cas reel constate le 12/08/2026 (Oricorio ex 111,
    set "MEGA Dream ex" : total=1 cote API mais data=[] avec le set
    precise, cause exacte non confirmee)."""
    params = {
        "language": "japanese" if carte.langue in ("jp", "kr") else "chinese",
        "search": f"{carte.nom_anglais} {carte.numero}",
        "includeEbay": "true",
        "limit": 1,
    }
    if avec_set:
        params["set"] = carte.set_jp
    r = requests.get(
        f"{POKEMONPRICETRACKER_BASE_URL}/cards",
        headers={**HEADERS, "Authorization": f"Bearer {cle_api}"},
        params=params,
        timeout=TIMEOUT,
    )
    if r.status_code != 200:
        print(f"[pokemonpricetracker] {carte.nom_affichage} (avec_set={avec_set}) : HTTP {r.status_code} — {r.text[:300]}", file=sys.stderr)
        return None
    data = r.json()
    resultats = data.get("data") or data.get("cards") or data.get("results") or ([data] if data.get("name") else [])
    if not resultats:
        print(f"[pokemonpricetracker] {carte.nom_affichage} (avec_set={avec_set}) : aucun resultat — "
              f"reponse brute : {str(data)[:400]}", file=sys.stderr)
    return resultats


def _pokemonpricetracker_prix(carte: CarteTendance, cle_api: str) -> dict | None:
    """Interroge PokemonPriceTracker pour le prix marche actuel d'une carte
    japonaise, best-effort. Essaie d'abord avec "set" (plus precis), puis
    sans si rien n'est trouve (cf. _requete_pokemonpricetracker).

    Retourne None si la carte n'est pas trouvee, si l'API echoue, ou si la
    cle n'est pas configuree -- jamais bloquant pour le reste du script."""
    if not cle_api:
        return None
    try:
        resultats = _requete_pokemonpricetracker(carte, cle_api, avec_set=True)
        if not resultats:
            resultats = _requete_pokemonpricetracker(carte, cle_api, avec_set=False)
        if not resultats:
            return None

        carte_trouvee = resultats[0]
        # V3 : on logue TOUJOURS le resultat brut (succes inclus) tant que
        # la structure exacte de reponse n'est pas totalement stabilisee --
        # notamment pour confirmer la DEVISE (PokemonPriceTracker agrege
        # TCGPlayer, tres probablement des prix en USD, jamais confirme
        # avec certitude) et reperer d'autres champs utiles (volume de
        # ventes sur carte brute, pas seulement gradee PSA10).
        print(f"[pokemonpricetracker] {carte.nom_affichage} : resultat brut — {str(carte_trouvee)[:500]}")

        prix = (carte_trouvee.get("prices") or {}).get("market") or carte_trouvee.get("marketPrice") or carte_trouvee.get("price")
        devise = (carte_trouvee.get("prices") or {}).get("currency") or carte_trouvee.get("currency")
        ventes_psa10 = ((carte_trouvee.get("ebay") or {}).get("psa10") or {}).get("avg")
        if prix is None:
            print(f"[pokemonpricetracker] {carte.nom_affichage} : resultat trouve mais champ prix introuvable "
                  f"— resultat brut : {str(carte_trouvee)[:400]}", file=sys.stderr)
            return None
        return {
            "prix_marche": float(prix),
            "devise": devise or "USD",  # USD par defaut si absent -- hypothese la plus probable (agregateur TCGPlayer), a confirmer
            "prix_gradee_psa10": float(ventes_psa10) if ventes_psa10 else None,
        }
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
        "devise_pokemonpricetracker": donnees_ppt.get("devise") if donnees_ppt else None,
        "prix_gradee_psa10": donnees_ppt.get("prix_gradee_psa10") if donnees_ppt else None,
        "cote_pokedeals": cote_locale,  # toujours en EUR (source PokeDeals/eBay)
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


def _devise_reference(point: dict) -> str:
    """Devise correspondant au prix retourne par _prix_reference -- pour
    ne jamais afficher un montant sans dire dans quelle monnaie il est
    (PokemonPriceTracker = tres probablement USD, PokeDeals = toujours EUR)."""
    if point.get("prix_pokemonpricetracker") is not None:
        return point.get("devise_pokemonpricetracker") or "USD"
    return "EUR"


_cache_taux_change: dict[str, float | None] = {}


def taux_change_vers_eur(devise: str) -> float | None:
    """Taux de change actuel devise -> EUR (combien vaut 1 unite de `devise`
    en euros), source gratuite sans cle. Mis en cache pour la duree du
    script (un seul appel reseau par execution, meme si plusieurs cartes
    sont dans une devise etrangere). Retourne None si aucune des 2 sources
    ne repond -- jamais bloquant, l'appelant doit gerer ce cas (affichage
    du montant en devise d'origine uniquement)."""
    if devise == "EUR":
        return 1.0
    if devise in _cache_taux_change:
        return _cache_taux_change[devise]

    taux = None
    try:
        r = requests.get(
            "https://api.frankfurter.dev/v1/latest",
            params={"from": devise, "to": "EUR"},
            timeout=TIMEOUT,
        )
        if r.status_code == 200:
            taux = float(r.json()["rates"]["EUR"])
    except (requests.exceptions.RequestException, ValueError, KeyError, TypeError) as e:
        print(f"[taux_change] frankfurter.dev echec pour {devise} : {e}", file=sys.stderr)

    if taux is None:
        try:
            r = requests.get(f"https://open.er-api.com/v6/latest/{devise}", timeout=TIMEOUT)
            if r.status_code == 200:
                taux = float(r.json()["rates"]["EUR"])
        except (requests.exceptions.RequestException, ValueError, KeyError, TypeError) as e:
            print(f"[taux_change] open.er-api.com echec pour {devise} : {e}", file=sys.stderr)

    _cache_taux_change[devise] = taux
    return taux


def analyser_tendance(points: list[dict]) -> dict | None:
    """Calcule un signal simple : prix le plus recent vs moyenne des
    `FENETRE_MOYENNE_JOURS` derniers jours DISPONIBLES (pas forcement
    calendaires -- le script ne tourne qu'une fois par jour, donc "derniers
    N points" = "derniers N jours" en pratique).

    Retourne None tant que MIN_POINTS_POUR_SIGNAL n'est pas atteint --
    comparer a une moyenne calculee sur trop peu de points n'a pas de sens
    statistique (meme logique que alerte_stock.py : pas de conclusion sur
    une premiere donnee).

    Audit externe du 18/08/2026 (verifie contre les vraies donnees
    accumulees avant correction -- les 3 cartes suivies n'avaient encore
    QUE des points PokemonPriceTracker/USD au moment de la verification,
    donc le bug ne s'etait pas encore materialise, mais restait latent) :
    `_prix_reference()` bascule silencieusement, jour par jour, entre
    PokemonPriceTracker (USD la plupart du temps) et `cote_pokedeals`
    (TOUJOURS EUR) selon la source disponible CE jour-la -- rien ne
    garantissait que tous les points d'une meme fenetre de calcul soient
    dans la MEME devise. Un simple echec ponctuel de l'API PokemonPriceTracker
    un jour donne (panne, rate-limit) aurait fait tomber ce jour-la sur la
    cote PokeDeals en EUR, melangeant silencieusement USD et EUR dans le
    calcul de moyenne -- contrairement a l'hypothese documentee dans
    CLAUDE.md ("un ecart en % entre 2 valeurs USD est deja correct sans
    conversion"), vraie UNIQUEMENT si toute la serie comparee est dans la
    MEME devise. Corrige en ne retenant, pour le calcul, QUE les points
    dans la MEME devise que le point le plus recent -- reste fidele au
    principe "pas de conversion dans le calcul, uniquement a l'affichage"
    (cf. module docstring) plutot que de convertir a la volee."""
    valeurs = [(_prix_reference(p), p["date"], _devise_reference(p)) for p in points if _prix_reference(p) is not None]
    if not valeurs:
        return {"signal": "pas_assez_de_donnees", "nb_points": 0,
                "points_manquants": MIN_POINTS_POUR_SIGNAL}

    devise_actuelle = valeurs[-1][2]
    valeurs_meme_devise = [(v, d) for v, d, dev in valeurs if dev == devise_actuelle]

    if len(valeurs_meme_devise) < MIN_POINTS_POUR_SIGNAL:
        return {"signal": "pas_assez_de_donnees", "nb_points": len(valeurs_meme_devise),
                "points_manquants": MIN_POINTS_POUR_SIGNAL - len(valeurs_meme_devise)}

    fenetre = valeurs_meme_devise[-FENETRE_MOYENNE_JOURS:]
    prix_actuel, date_actuelle = valeurs_meme_devise[-1]
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
        "devise": devise_actuelle,
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
    devise = tendance.get("devise", "EUR")
    lignes = [
        f"📈 <b>Tendance prix — {carte.nom_affichage}</b>",
        _LIBELLES_SIGNAL.get(tendance["signal"], tendance["signal"]),
        "",
    ]

    # Conversion EUR uniquement pour l'AFFICHAGE -- le signal/ecart_pct ci-dessus
    # a deja ete calcule en devise d'origine (correct : un ecart en % ne depend
    # pas de la devise). Best-effort : si le taux echoue, on affiche quand meme
    # le montant en devise d'origine plutot que de bloquer toute l'alerte.
    taux = taux_change_vers_eur(devise) if devise != "EUR" else 1.0
    if taux is not None:
        prix_eur = tendance["prix_actuel"] * taux
        moyenne_eur = tendance["moyenne_recente"] * taux
        if devise == "EUR":
            lignes.append(f"Prix actuel ({tendance['date_actuelle']}) : <b>{prix_eur:.2f}€</b>")
            lignes.append(f"Moyenne des {tendance['nb_points_fenetre']} derniers points : {moyenne_eur:.2f}€")
        else:
            lignes.append(f"Prix actuel ({tendance['date_actuelle']}) : <b>≈{prix_eur:.2f}€</b> ({tendance['prix_actuel']:.2f} {devise})")
            lignes.append(f"Moyenne des {tendance['nb_points_fenetre']} derniers points : ≈{moyenne_eur:.2f}€ ({tendance['moyenne_recente']:.2f} {devise})")
    else:
        lignes.append(f"Prix actuel ({tendance['date_actuelle']}) : <b>{tendance['prix_actuel']:.2f} {devise}</b> (conversion € indisponible aujourd'hui)")
        lignes.append(f"Moyenne des {tendance['nb_points_fenetre']} derniers points : {tendance['moyenne_recente']:.2f} {devise}")

    lignes.append(f"Écart : <b>{tendance['ecart_pct']:+.1f}%</b>")
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
                    print("  -> alerte envoyee (changement de signal)")
            else:
                print("  -> signal inchange depuis la derniere alerte, silence")

    sauvegarder_historique(historique)
    print(f"\nHistorique sauvegarde dans {FICHIER_HISTORIQUE}")
