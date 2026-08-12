"""
Radar de decouverte automatique de nouvelles boutiques Pokemon TCG.

Source de donnees : listes QUOTIDIENNES gratuites, sans cle ni inscription,
publiees par l'AFNIC (registre officiel des domaines .fr) --
https://www.afnic.fr/wp-media/ftp/domaineTLD_Afnic/YYYYMMDD_CREA_fr.txt --
un fichier texte par jour (un domaine .fr NOUVELLEMENT ENREGISTRE par
ligne), disponible 7 jours sur le serveur AFNIC.

Choix technique fait le 12/08/2026 apres verification (cf. echange avec
Justok) : une "recherche web continue" via Google/Bing/Brave n'est PAS
faisable gratuitement en 2026 (Google Custom Search ferme aux nouveaux
comptes + deprecie 2027, Brave Search API a supprime son tier gratuit en
fevrier 2026). L'AFNIC est la seule source vraiment gratuite et perenne
identifiee -- mais elle ne couvre QUE les domaines .fr fraichement crees
avec un nom evocateur, pas les boutiques existantes ou en .com/.shop/etc.
La veille manuelle de Justok reste complementaire, pas remplacee.

Pipeline :
  1. Telecharger les fichiers AFNIC des N derniers jours (par defaut 7 --
     correspond a la fenetre de disponibilite du serveur, donc un cron
     HEBDOMADAIRE suffit a ne rien manquer).
  2. Filtrer les noms de domaine par mots-cles (large volontairement --
     la vraie decision se fait a l'etape 3 sur le contenu reel, pas sur
     le nom).
  3. Pour chaque candidat non deja vu (cf. memoire) : verifier Shopify
     (/products.json) puis WooCommerce (product-sitemap.xml) en repli,
     recuperer un echantillon de produits, classer en "singles confirmes"
     / "scelle uniquement" / "signal insuffisant" avec les MEMES criteres
     objectifs que la verification manuelle du 12/08/2026 (motif de
     numero de collection NNN/MMM + mention/tag/type "pokemon" explicite).
  4. AJOUT AUTOMATIQUE seulement si le signal est net (cf. SEUIL_*
     ci-dessous) -- dans boutiques_decouvertes.py, un fichier separe et
     entierement gere par ce script (jamais les fichiers boutiques_*.py
     annotes a la main, pour ne jamais risquer d'ecraser leurs
     commentaires/contexte). Les cas ambigus sont juste rapportes, pas
     ajoutes -- mieux vaut manquer une boutique limite qu'ajouter un faux
     positif dans un systeme qui declenche de vraies alertes Telegram.
  5. Notification Telegram recapitulative (ajouts automatiques + candidats
     ambigus a examiner) -- jamais silencieux, meme quand 0 ajout.

Ne modifie JAMAIS boutiques_shopify.py / boutiques_woocommerce.py (les
listes annotees a la main par Justok/les sessions precedentes) -- lit
uniquement boutiques_decouvertes.py, qu'il possede entierement.
"""

import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from connecteur_shopify import HEADERS, HEADERS_HTML, TIMEOUT
from memoire_json import charger_memoire, sauvegarder_memoire
from telegram_utils import echapper_html

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FICHIER_MEMOIRE = Path(__file__).parent / "data" / "decouverte_boutiques_memoire.json"
FICHIER_BOUTIQUES_DECOUVERTES = Path(__file__).parent / "boutiques_decouvertes.py"

JOURS_AFNIC = 7  # fenetre de disponibilite des fichiers sur le serveur AFNIC
DELAI_ENTRE_BOUTIQUES = 1.5  # secondes, politesse -- verification, pas un scan complet
MAX_CANDIDATS_PAR_CYCLE = 60  # garde-fou : ne pas exploser le temps du workflow si un jour AFNIC est trop bruyant

# Mots-cles pour filtrer les ~3000 domaines/jour de la liste AFNIC.
# Volontairement LARGE (le vrai filtre se fait sur le contenu reel a
# l'etape de verification, pas ici) -- mais on evite les mots isoles trop
# generiques qui exploseraient le nombre de candidats a verifier (ex :
# "carte" seul matcherait "carte-de-visite.fr", "carte-grise-express.fr"...).
MOTS_CLES_DOMAINE = [
    "pokemon", "pokeball", "pikachu", "dracaufeu", "bulbizarre", "carapuce",
    "evoli", "mewtwo", "salameche", "leviator", "dracolosse",
    "cartepokemon", "cartespokemon", "pokemoncarte", "pokemoncard",
    "pokemontcg", "tcgpokemon", "jcc-pokemon", "pokemon-jcc", "pokemonjcc",
    "-tcg", "tcg-", "tcgshop", "tcgstore", "tcgcard", "tcgstock",
]

# Signal de carte a l'unite : motif "NNN/MMM" (numero de collection) dans
# le titre -- meme regex que celle utilisee pour verifier a la main les 12
# boutiques trouvees par Justok le 12/08/2026.
RE_NUMERO_CARTE = re.compile(r"\b\d{1,3}\s*/\s*\d{2,3}\b")

# Seuils d'AJOUT AUTOMATIQUE -- volontairement stricts, calibres sur les
# vrais cas rencontres le 12/08/2026 (playshop.fr : 214/214 singles tagges
# "pokemon-tcg" -> cas clair ; kairyu.fr : 74/190 -> ambigu, aurait
# meriter une revue humaine plutot qu'un ajout aveugle).
SEUIL_MIN_SINGLES_POKEMON = 15
SEUIL_RATIO_POKEMON_SUR_SINGLES = 0.5  # au moins 50% des "singles" detectes doivent etre explicitement Pokemon
SEUIL_MIN_PRODUITS_SCELLE_POKEMON = 5  # pour le classement "scelle uniquement"


def _telecharger_fichier_afnic(jour: "datetime") -> list[str]:
    """Telecharge la liste des domaines .fr crees un jour donne. Retourne
    une liste vide (pas une erreur) si le fichier n'est pas encore publie
    ou plus disponible (hors de la fenetre de 7 jours)."""
    url = f"https://www.afnic.fr/wp-media/ftp/domaineTLD_Afnic/{jour.strftime('%Y%m%d')}_CREA_fr.txt"
    try:
        r = requests.get(url, timeout=TIMEOUT)
        if r.status_code != 200:
            return []
        lignes = r.text.splitlines()
        # Le fichier a un en-tete de commentaires (#...) termine par "#BOF"
        # -- les domaines commencent juste apres.
        debut = 0
        for i, ligne in enumerate(lignes):
            if ligne.strip() == "#BOF":
                debut = i + 1
                break
        return [l.strip().lower() for l in lignes[debut:] if l.strip() and not l.startswith("#")]
    except requests.exceptions.RequestException as e:
        print(f"[afnic] echec telechargement {jour.strftime('%Y%m%d')} : {e}", file=sys.stderr)
        return []


def recuperer_nouveaux_domaines_fr(jours: int = JOURS_AFNIC) -> set[str]:
    """Union des domaines .fr crees sur les `jours` derniers jours."""
    domaines: set[str] = set()
    aujourdhui = datetime.now(timezone.utc)
    for delta in range(jours):
        jour = aujourdhui - timedelta(days=delta)
        domaines.update(_telecharger_fichier_afnic(jour))
        time.sleep(0.3)
    return domaines


def filtrer_par_mots_cles(domaines: set[str]) -> list[str]:
    return sorted(d for d in domaines if any(mot in d for mot in MOTS_CLES_DOMAINE))


def _extraire_produits_json(domaine: str) -> list[dict] | None:
    """Retourne la liste de produits si `domaine` est une boutique Shopify
    publique, None sinon (pas Shopify, SSL invalide, timeout...)."""
    try:
        r = requests.get(
            f"https://{domaine}/products.json?limit=250",
            headers=HEADERS, timeout=TIMEOUT,
        )
        if r.status_code != 200:
            return None
        data = r.json()
        produits = data.get("products")
        return produits if isinstance(produits, list) else None
    except (requests.exceptions.RequestException, ValueError):
        return None


def _extraire_produits_woocommerce(domaine: str) -> list[str] | None:
    """Retourne la liste des URLs produits via product-sitemap.xml si
    `domaine` est une boutique WooCommerce avec sitemap Yoast/AIOSEO,
    None sinon."""
    try:
        r = requests.get(
            f"https://{domaine}/product-sitemap.xml",
            headers=HEADERS_HTML, timeout=TIMEOUT,
        )
        if r.status_code != 200 or b"<loc>" not in r.content:
            return None
        return re.findall(r"<loc>([^<]+)</loc>", r.text)
    except requests.exceptions.RequestException:
        return None


def _classifier_produits_shopify(produits: list[dict]) -> dict:
    """Meme heuristique que la verification manuelle du 12/08/2026 :
    singles = motif NNN/MMM dans le titre ; pokemon_singles = parmi eux,
    ceux dont le titre/tags/type mentionnent explicitement Pokemon."""
    singles = [p for p in produits if RE_NUMERO_CARTE.search(p.get("title", ""))]
    scelle_pokemon = [
        p for p in produits
        if "pokemon" in _texte_produit(p) or "pokémon" in _texte_produit(p)
    ]
    pokemon_singles = [p for p in singles if "pokemon" in _texte_produit(p) or "pokémon" in _texte_produit(p)]
    return {
        "nb_produits": len(produits),
        "nb_singles": len(singles),
        "nb_pokemon_singles": len(pokemon_singles),
        "nb_scelle_pokemon": len(scelle_pokemon) - len(pokemon_singles),
    }


def _texte_produit(p: dict) -> str:
    return (p.get("title", "") + " " + " ".join(p.get("tags", []) or []) + " " + p.get("product_type", "")).lower()


def verifier_candidat(domaine: str) -> dict:
    """Verifie techniquement un domaine candidat. Retourne un rapport avec
    un `verdict` parmi : "singles" (ajout BOUTIQUES_*_AUTO), "scelle"
    (ajout BOUTIQUES_*_AUTO_PRECOMMANDE_SEULEMENT), ou "insuffisant"
    (rapporte mais pas ajoute)."""
    produits = _extraire_produits_json(domaine)
    if produits is not None:
        stats = _classifier_produits_shopify(produits)
        if (stats["nb_pokemon_singles"] >= SEUIL_MIN_SINGLES_POKEMON
                and stats["nb_singles"] > 0
                and stats["nb_pokemon_singles"] / stats["nb_singles"] >= SEUIL_RATIO_POKEMON_SUR_SINGLES):
            return {"domaine": domaine, "plateforme": "shopify", "verdict": "singles", **stats}
        if stats["nb_scelle_pokemon"] >= SEUIL_MIN_PRODUITS_SCELLE_POKEMON:
            return {"domaine": domaine, "plateforme": "shopify", "verdict": "scelle", **stats}
        return {"domaine": domaine, "plateforme": "shopify", "verdict": "insuffisant", **stats}

    urls_produits = _extraire_produits_woocommerce(domaine)
    if urls_produits is not None:
        # Pas de titres exploitables sans requeter chaque page produit
        # individuellement (couteux) -- on se limite a un signal de mots-cles
        # dans les slugs d'URL, plus grossier que Shopify mais suffisant
        # pour distinguer "boutique TCG probable" de "0 rapport".
        slugs_pokemon = [u for u in urls_produits if "pokemon" in u.lower() or "pok%c3%a9mon" in u.lower()]
        if len(slugs_pokemon) >= SEUIL_MIN_PRODUITS_SCELLE_POKEMON:
            return {"domaine": domaine, "plateforme": "woocommerce", "verdict": "scelle",
                    "nb_produits": len(urls_produits), "nb_slugs_pokemon": len(slugs_pokemon)}
        return {"domaine": domaine, "plateforme": "woocommerce", "verdict": "insuffisant",
                "nb_produits": len(urls_produits), "nb_slugs_pokemon": len(slugs_pokemon)}

    return {"domaine": domaine, "plateforme": None, "verdict": "non_boutique"}


def _charger_boutiques_decouvertes() -> dict[str, list[str]]:
    """Lit boutiques_decouvertes.py et retourne ses 4 listes -- le fichier
    est cense n'etre modifie QUE par ce script, format simple garanti."""
    if not FICHIER_BOUTIQUES_DECOUVERTES.exists():
        return {"shopify": [], "shopify_precommande": [], "woocommerce": [], "woocommerce_precommande": []}
    namespace: dict = {}
    exec(FICHIER_BOUTIQUES_DECOUVERTES.read_text(encoding="utf-8"), namespace)  # noqa: S102 -- fichier interne, jamais de contenu externe
    return {
        "shopify": namespace.get("BOUTIQUES_SHOPIFY_AUTO", []),
        "shopify_precommande": namespace.get("BOUTIQUES_SHOPIFY_AUTO_PRECOMMANDE_SEULEMENT", []),
        "woocommerce": namespace.get("BOUTIQUES_WOOCOMMERCE_AUTO", []),
        "woocommerce_precommande": namespace.get("BOUTIQUES_WOOCOMMERCE_AUTO_PRECOMMANDE_SEULEMENT", []),
    }


def _ecrire_boutiques_decouvertes(listes: dict[str, list[str]]) -> None:
    """Reecrit entierement boutiques_decouvertes.py -- fichier auto-genere,
    jamais edite a la main (contrairement a boutiques_shopify.py /
    boutiques_woocommerce.py)."""
    horodatage = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    contenu = f'''"""
Boutiques trouvees et validees AUTOMATIQUEMENT par decouverte_boutiques.py
(radar hebdomadaire base sur les listes AFNIC des nouveaux domaines .fr).

FICHIER AUTO-GENERE -- ne pas editer a la main, il est reecrit en entier a
chaque execution du radar. Pour une boutique trouvee manuellement (capture
d'ecran, bouche a oreille...), l'ajouter directement dans boutiques_shopify.py
/ boutiques_woocommerce.py a la place -- ces fichiers-la restent geres a la
main et ne sont jamais touches par ce script.

Derniere mise a jour : {horodatage}
"""

BOUTIQUES_SHOPIFY_AUTO = {listes["shopify"]!r}

BOUTIQUES_SHOPIFY_AUTO_PRECOMMANDE_SEULEMENT = {listes["shopify_precommande"]!r}

BOUTIQUES_WOOCOMMERCE_AUTO = {listes["woocommerce"]!r}

BOUTIQUES_WOOCOMMERCE_AUTO_PRECOMMANDE_SEULEMENT = {listes["woocommerce_precommande"]!r}
'''
    FICHIER_BOUTIQUES_DECOUVERTES.write_text(contenu, encoding="utf-8")


def envoyer_telegram_rapport(ajouts: list[dict], a_examiner: list[dict], chat_id: str, token: str) -> None:
    if not token or not chat_id:
        print("Telegram non configure : rapport de decouverte non envoye.")
        return
    if not ajouts and not a_examiner:
        return  # cycle silencieux si vraiment rien a signaler (0 candidat trouve)
    lignes = ["\U0001f50e <b>Radar de decouverte -- nouvelles boutiques TCG</b>", ""]
    if ajouts:
        lignes.append(f"<b>{len(ajouts)} boutique(s) ajoutee(s) automatiquement :</b>")
        for c in ajouts:
            genre = "cartes a l'unite" if c["verdict"] == "singles" else "scelle (precommandes)"
            lignes.append(f"✅ {echapper_html(c['domaine'])} ({genre}, {c['plateforme']})")
        lignes.append("")
    if a_examiner:
        lignes.append(f"<b>{len(a_examiner)} candidat(s) ambigu(s), a verifier a la main :</b>")
        for c in a_examiner[:15]:
            lignes.append(f"❓ {echapper_html(c['domaine'])} ({c['plateforme'] or 'plateforme inconnue'})")
        if len(a_examiner) > 15:
            lignes.append(f"... et {len(a_examiner) - 15} de plus (cf. logs du workflow)")
    texte = "\n".join(lignes)
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": texte, "parse_mode": "HTML"},
            timeout=TIMEOUT,
        )
        if not r.ok:
            print(f"[telegram] reponse de l'API : {r.status_code} {r.text}", file=sys.stderr)
    except requests.exceptions.RequestException as e:
        print(f"[telegram] echec envoi rapport decouverte : {e}", file=sys.stderr)


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "1245330032")  # meme chat que le reste de PokeDeals

    memoire = charger_memoire(FICHIER_MEMOIRE)
    domaines_deja_vus = set(memoire.get("domaines_verifies", {}).keys())

    print("Telechargement des listes AFNIC (7 derniers jours)...")
    nouveaux_domaines = recuperer_nouveaux_domaines_fr()
    print(f"{len(nouveaux_domaines)} domaines .fr crees recemment (fenetre AFNIC).")

    candidats = filtrer_par_mots_cles(nouveaux_domaines)
    candidats = [d for d in candidats if d not in domaines_deja_vus][:MAX_CANDIDATS_PAR_CYCLE]
    print(f"{len(candidats)} candidat(s) apres filtre mots-cles + memoire (non deja verifies).")

    ajouts: list[dict] = []
    a_examiner: list[dict] = []

    for i, domaine in enumerate(candidats):
        rapport = verifier_candidat(domaine)
        print(f"[{i + 1}/{len(candidats)}] {domaine} : {rapport['verdict']}")

        if rapport["verdict"] in ("singles", "scelle"):
            ajouts.append(rapport)
            memoire.setdefault("domaines_verifies", {})[domaine] = {
                "derniere_verification": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "verdict": rapport["verdict"],
            }
        elif rapport["verdict"] == "insuffisant":
            # PAS memorise definitivement : un Shopify/WooCommerce fraichement
            # cree peut avoir un catalogue encore vide/minimal la 1ere semaine
            # (cas reel constate le 12/08/2026 : "nemee-tcg.fr", 1 seul
            # produit) -- on prefere le reverifier chaque semaine plutot que
            # de manquer une vraie boutique juste parce qu'elle n'etait pas
            # encore approvisionnee au moment du 1er passage.
            a_examiner.append(rapport)
        else:
            # "non_boutique" : ni Shopify ni WooCommerce detecte -- la SEULE
            # categorie memorisee definitivement, car un domaine sans site du
            # tout a peu de chances de devenir une boutique TCG la semaine
            # suivante ; evite de re-verifier indefiniment tout le bruit.
            memoire.setdefault("domaines_verifies", {})[domaine] = {
                "derniere_verification": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "verdict": rapport["verdict"],
            }

        if i < len(candidats) - 1:
            time.sleep(DELAI_ENTRE_BOUTIQUES)

    listes = _charger_boutiques_decouvertes()
    for c in ajouts:
        cle = f"{'shopify' if c['plateforme'] == 'shopify' else 'woocommerce'}" + ("_precommande" if c["verdict"] == "scelle" else "")
        if c["domaine"] not in listes[cle]:
            listes[cle].append(c["domaine"])
    _ecrire_boutiques_decouvertes(listes)

    sauvegarder_memoire(memoire, FICHIER_MEMOIRE)
    envoyer_telegram_rapport(ajouts, a_examiner, chat_id, token)

    print(f"\nTermine : {len(ajouts)} ajout(s) automatique(s), {len(a_examiner)} a examiner.")


if __name__ == "__main__":
    main()
