"""
Detection d'OUVERTURE de precommande pour des produits scelles surveilles
(cf. precommandes_watchlist.py) -- systeme d'alerte INDEPENDANT de
bonne_affaire_shopify.py (seuil de prix sur cartes deja catalogues) et
alerte_stock.py (retour en stock d'un produit deja catalogue).

Contrairement a alerte_stock.py qui compare un etat "en_stock" avant/apres
pour un produit deja connu, ici on detecte l'APPARITION du produit
LUI-MEME sur une boutique (precommande qui n'existait pas avant -> existe
maintenant), en stock ou non -- la simple presence d'une page produit
correspondante suffit a declencher l'alerte (une seule fois par produit x
boutique, memorisee pour ne jamais re-alerter deux fois).
"""

import json
from pathlib import Path

import requests

FICHIER_MEMOIRE = Path(__file__).parent / "data" / "precommandes_anniversaire.json"


def _cle_memoire(domaine: str, nom_produit: str) -> str:
    return f"{domaine}|{nom_produit}"


def charger_memoire(chemin: Path = FICHIER_MEMOIRE) -> dict:
    if not chemin.exists():
        return {}
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def sauvegarder_memoire(memoire: dict, chemin: Path = FICHIER_MEMOIRE) -> None:
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(memoire, f, indent=2, ensure_ascii=False)


def detecter_nouvelles_precommandes(
    domaine: str,
    candidats: list[dict],
    memoire: dict,
) -> list[dict]:
    """`candidats` : liste de dicts {nom_produit, confiance, raison, titre,
    url_produit, prix, en_stock} deja filtres/evalues par
    precommandes_watchlist.evaluer_correspondance (confiance != None).

    Alerte UNE SEULE FOIS par (domaine, nom_produit) -- meme principe que
    alerte_stock.py pour ne pas spammer a chaque cycle. Si un match a
    confiance "moyenne" est deja memorise et qu'un match "forte" est
    trouve ensuite (date confirmee apres coup), une SECONDE alerte est
    envoyee pour signaler la confirmation -- utile (l'info "date
    confirmee" a une vraie valeur), pas juste du bruit."""
    evenements = []

    for c in candidats:
        cle_mem = _cle_memoire(domaine, c["nom_produit"])
        etat_precedent = memoire.get(cle_mem)

        deja_alerte_a_ce_niveau = (
            etat_precedent is not None
            and etat_precedent.get("confiance") == c["confiance"]
        )
        # Ne re-alerte pas si deja vu a confiance EGALE OU SUPERIEURE
        # (une fois "forte" alertee, un nouveau match "moyenne" sur la
        # meme page ne doit pas redeclencher).
        deja_confirme_mieux = (
            etat_precedent is not None
            and etat_precedent.get("confiance") == "forte"
        )

        if not deja_alerte_a_ce_niveau and not deja_confirme_mieux:
            evenements.append(c)

        memoire[cle_mem] = {
            "confiance": c["confiance"],
            "raison": c["raison"],
            "titre_produit": c["titre"],
            "url_produit": c["url_produit"],
            "derniere_verification": c.get("horodatage", ""),
        }

    return evenements


# --- Notification Telegram (visuellement distincte des 2 autres alertes) ---

def _echapper_html(texte) -> str:
    return str(texte).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _echapper_url_html(url: str) -> str:
    return str(url).replace("&", "&amp;")


def _texte_precommande(e: dict) -> str:
    niveau = "🟢 confirmée (date de sortie détectée)" if e["confiance"] == "forte" else "🟡 probable (mots-clés seuls)"
    prix_ligne = f"💰 {e['prix']:.2f}€\n" if e.get("prix") else ""
    lien_ligne = f"👉 <a href=\"{_echapper_url_html(e['url_produit'])}\">Voir le produit</a>" if e.get("url_produit") else ""
    return (
        f"🎉 <b>Précommande détectée !</b>\n"
        f"📦 <b>{_echapper_html(e['nom_produit'])}</b>\n"
        f"🏪 {_echapper_html(e['domaine'])}\n"
        f"🔎 Confiance : {niveau}\n"
        f"{prix_ligne}"
        f"📝 {_echapper_html(e['titre'])}\n"
        f"{lien_ligne}"
    )


def envoyer_telegram_precommandes(evenements: list[dict], chat_id: str, token: str) -> bool:
    if not evenements:
        return True
    if not token or not chat_id:
        print("[alerte_precommande] Telegram non configure : alertes precommande non envoyees.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    ok = True
    for e in evenements:
        try:
            r = requests.post(
                url,
                json={"chat_id": chat_id, "text": _texte_precommande(e), "parse_mode": "HTML"},
                timeout=20,
            )
            if r.status_code != 200:
                print(f"[alerte_precommande] Telegram a refuse l'alerte ({r.status_code}) : {r.text[:200]}")
                ok = False
        except Exception as ex:  # noqa: BLE001
            print(f"[alerte_precommande] Echec envoi Telegram : {ex}")
            ok = False
    return ok
