"""
Detection des retours en stock sur les boutiques Shopify pour PokeDeals.

Systeme d'alerte INDEPENDANT de celui des bonnes affaires (seuil de prix,
cf. main.py de PokeDeals) : celui-ci se declenche uniquement sur une
transition rupture -> stock, quel que soit le prix affiche. Les deux
systemes tournent en parallele sans interference.

Utilise ConnecteurShopify (connecteur_shopify.py) pour interroger les
boutiques, et un fichier memoire JSON (data/stock_boutiques_tcg.json) pour
detecter les changements d'un scan a l'autre -- meme principe que
data/anciennete_annonces.json dans le PokeDeals existant.

Seuls les resultats a CONFIANCE FORTE (nom+numero) alimentent ce systeme :
les resultats a confiance faible (repli nom seul, cf. connecteur_shopify.py)
sont trop peu fiables pour declencher une alerte de retour en stock.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bonne_affaire_shopify import _est_carte_gradee  # noqa: E402
from connecteur_shopify import ConnecteurShopify  # noqa: E402
from memoire_json import charger_memoire as _charger_memoire_generique, sauvegarder_memoire as _sauvegarder_memoire_generique  # noqa: E402
from telegram_utils import echapper_html as _echapper_html, echapper_url_html as _echapper_url_html  # noqa: E402
from watchlist_shopify import detecter_qualificatif_titre  # noqa: E402

FICHIER_MEMOIRE = Path(__file__).parent / "data" / "stock_boutiques_tcg.json"


def _cle_memoire(domaine: str, nom_config: str) -> str:
    """Cle unique carte x boutique, basee sur l'identite CANONIQUE de la
    carte (nom_config, ex: "Dracaufeu ex 199/165"), pas sur le nom/alias
    utilise pour la recherche -- sinon une carte trouvee via son alias et
    via son nom principal produirait deux entrees memoire distinctes pour
    la MEME carte physique."""
    return f"{domaine}|{nom_config}"


def charger_memoire(chemin: Path = FICHIER_MEMOIRE) -> dict:
    return _charger_memoire_generique(chemin)


def sauvegarder_memoire(memoire: dict, chemin: Path = FICHIER_MEMOIRE) -> None:
    _sauvegarder_memoire_generique(memoire, chemin)


def detecter_retours_en_stock(
    domaine: str,
    resultats_par_critere: dict,
    cartes_par_critere: dict,
    memoire: dict,
) -> list[dict]:
    """Compare le statut en_stock actuel (issu d'un scan) a celui memorise
    et retourne la liste des evenements "retour en stock" a notifier.

    `cartes_par_critere` associe chaque cle (nom_recherche, numero) a son
    CarteWatchlist d'origine (cf. watchlist_shopify.py) -- necessaire pour
    regrouper par identite CANONIQUE de carte (nom_config), car une meme
    carte peut avoir plusieurs criteres de recherche (nom principal + alias).

    Regles :
      - Seuls les criteres AVEC numero (confiance forte) sont pris en
        compte ; les criteres sans numero (confiance faible) sont ignores
        pour ce systeme d'alerte.
      - Une carte x boutique jamais vue avant est ajoutee a la memoire mais
        NE DECLENCHE PAS d'alerte (evite le spam massif au premier lancement).
      - Une alerte n'est declenchee QUE sur une vraie transition
        False -> True (rupture -> stock).
      - La memoire est mise a jour pour CHAQUE combinaison carte x boutique
        a chaque appel, qu'elle soit en stock ou non a ce cycle -- sinon les
        transitions futures ne peuvent plus etre detectees correctement.
    """
    evenements = []
    maintenant = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # Regroupement par identite canonique (nom_config) : consolide les
    # variantes nom principal / alias qui pointent vers la MEME carte.
    resultats_fiables_par_carte: dict[str, list] = {}
    for cle, resultats in resultats_par_critere.items():
        carte = cartes_par_critere.get(cle)
        if carte is None or carte.numero is None:
            continue  # confiance faible (repli nom seul) : hors perimetre

        candidats = [r for r in resultats if r.confiance == "forte"]

        # V47 (13/08/2026) : exclusion des cartes GRADEES, meme garde-fou
        # que bonne_affaire_shopify.py (evaluer_deal) -- une carte gradee
        # (PSA/CGC/BGS...) qui revient en stock n'est pas la meme chose
        # qu'un retour en stock de la carte BRUTE suivie ; sans ce filtre,
        # une annonce gradee homonyme declenche une alerte trompeuse.
        candidats = [r for r in candidats if not _est_carte_gradee(r.titre)]

        # Coherence de langue -- meme garde-fou que bonne_affaire_shopify.py
        # (evaluer_deal), jusqu'ici absent ici : une carte FR ne doit pas
        # matcher un retour en stock d'une carte homonyme explicitement
        # detectee dans une AUTRE langue (nom+numero identiques, edition
        # differente). "jp_ou_kr" reste compatible avec une carte configuree
        # jp OU kr (numerotation partagee, cf. connecteur_shopify.detecter_langue).
        def _langue_coherente(r):
            if r.langue_detectee == "jp_ou_kr":
                return carte.langue in ("jp", "kr")
            return r.langue_detectee is None or r.langue_detectee == carte.langue

        candidats = [r for r in candidats if _langue_coherente(r)]

        if carte.qualificatif:
            # Rejette une carte HOMONYME (meme nom+numero, edition
            # differente) sans le qualificatif attendu ("ex"/"gx"/"v"/...)
            # dans son titre -- meme bug/correctif que bonne_affaire_shopify.py
            # (cf. "Plumeline ex 024" vs "Plumeline 24 Sun & Moon REVERSE").
            motif = re.compile(rf"\b{re.escape(carte.qualificatif)}\b")
            candidats = [r for r in candidats if motif.search(r.titre.lower())]
        else:
            # Sens INVERSE (symetrique) : une carte configuree SANS
            # qualificatif ne doit pas matcher un titre qui en porte un
            # (carte "ex"/"GX"/"V" homonyme, en realite differente).
            candidats = [r for r in candidats if detecter_qualificatif_titre(r.titre, carte.numero) is None]

        resultats_fiables_par_carte.setdefault(carte.nom_config, []).extend(candidats)

    for nom_config, resultats_fiables in resultats_fiables_par_carte.items():
        en_stock_actuel = any(r.en_stock for r in resultats_fiables)

        cle_mem = _cle_memoire(domaine, nom_config)
        etat_precedent = memoire.get(cle_mem)
        etait_en_stock = etat_precedent["en_stock"] if etat_precedent else None

        # Alerte uniquement si un etat precedent existait DEJA (pas au premier
        # passage) ET que ce precedent etait "rupture" ET que c'est maintenant "stock".
        if etait_en_stock is False and en_stock_actuel is True:
            meilleur = min((r for r in resultats_fiables if r.en_stock), key=lambda r: r.prix)
            evenements.append({
                "boutique": domaine,
                "nom": nom_config,
                "prix": meilleur.prix,
                "titre_produit": meilleur.titre,
                "url_produit": meilleur.url_produit,
            })

        memoire[cle_mem] = {
            "en_stock": en_stock_actuel,
            "derniere_verification": maintenant,
        }

    return evenements


# --- Notification Telegram (visuellement distincte de l'alerte "bonne affaire") ---
# _echapper_html/_echapper_url_html : cf. telegram_utils.py (import en tete
# de fichier).


def _texte_retour_stock(e: dict) -> str:
    return (
        f"📦 <b>De retour en stock !</b>\n"
        f"🎴 <b>{_echapper_html(e['nom'])}</b>\n"
        f"🏪 {_echapper_html(e['boutique'])} — <b>{e['prix']:.2f}€</b>\n"
        f"📝 {_echapper_html(e['titre_produit'])}\n"
        f"👉 <a href=\"{_echapper_url_html(e['url_produit'])}\">Voir le produit</a>"
    )


def envoyer_telegram_retours_stock(evenements: list[dict], chat_id: str, token: str) -> bool:
    """Envoie une alerte Telegram par retour en stock detecte.

    Format volontairement different de l'alerte "bonne affaire" existante
    (📦 + "De retour en stock !" au lieu de 🔥/💰 + cote/decote/profit) pour
    etre reconnaissable d'un coup d'oeil."""
    if not evenements:
        return True
    if not token or not chat_id:
        print("[alerte_stock] Telegram non configure : alertes retour en stock non envoyees.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    ok = True
    for e in evenements:
        try:
            r = requests.post(
                url,
                json={"chat_id": chat_id, "text": _texte_retour_stock(e), "parse_mode": "HTML"},
                timeout=20,
            )
            if r.status_code != 200:
                print(f"[alerte_stock] Telegram a refuse l'alerte ({r.status_code}) : {r.text[:200]}")
                ok = False
        except Exception as ex:  # noqa: BLE001
            print(f"[alerte_stock] Echec envoi Telegram : {ex}")
            ok = False
    return ok


if __name__ == "__main__":
    from watchlist_shopify import ECHANTILLON_CONFIG

    boutiques = ["questcorner.fr", "kyoriyu.fr"]
    cartes_par_critere = {c.cle_recherche: c for c in ECHANTILLON_CONFIG}
    criteres = list(cartes_par_critere.keys())

    # Fichier memoire de test isole (ne touche pas un eventuel fichier de prod).
    fichier_test = Path(__file__).parent / "data" / "stock_boutiques_tcg_TEST.json"
    if fichier_test.exists():
        fichier_test.unlink()  # repart d'une memoire vide pour un test reproductible

    for passage in (1, 2):
        print(f"\n{'=' * 70}")
        print(f"PASSAGE {passage} — {'premier scan (memoire vide attendue)' if passage == 1 else 'second scan (aucun changement attendu)'}")
        print("=" * 70)

        memoire = charger_memoire(fichier_test)
        total_evenements = []

        for domaine in boutiques:
            connecteur = ConnecteurShopify(domaine)
            resultats_par_critere = connecteur.rechercher_par_mots_cles(criteres)
            evenements = detecter_retours_en_stock(domaine, resultats_par_critere, cartes_par_critere, memoire)
            total_evenements.extend(evenements)
            print(f"\n{domaine} : {len(evenements)} evenement(s) 'retour en stock' detecte(s)")
            for e in evenements:
                print(f"  📦 {e['nom']} — {e['prix']:.2f}€ — {e['url_produit']}")

        sauvegarder_memoire(memoire, fichier_test)

        print(f"\n>>> Total passage {passage} : {len(total_evenements)} alerte(s) qui seraient envoyees.")
        # Mode test : on n'envoie PAS de vrai message Telegram (pas de token
        # fourni volontairement) -- on verifie juste que le compte est a 0.
        envoyer_telegram_retours_stock(total_evenements, chat_id="", token="")

    print(f"\nMemoire de test ecrite dans : {fichier_test}")
    print("Contenu :")
    print(json.dumps(charger_memoire(fichier_test), indent=2, ensure_ascii=False))
