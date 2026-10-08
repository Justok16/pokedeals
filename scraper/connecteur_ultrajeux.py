"""
Connecteur Ultrajeux (ultrajeux.com), ajoute le 08/10/2026 (piste venue du
rapport Gemini demande par Justok, verifiee a la main) : boutique TCG
francaise historique, plateforme maison rendue cote serveur.

La recherche (search3.php) renvoie une page vide sans JavaScript, mais les
pages CATEGORIE sont lisibles et listent les nouveautes en tete (verifie le
08/10/2026 : ETB 30e, Bundle 30e et les 10 Mini Tins 30e y figurent) :
  https://www.ultrajeux.com/cat-1-4-<id>-x.html  (le slug est ignore)
Une carte = <div class="block_produit"> avec :
  - titre complet dans l'attribut alt de l'image `produit_scan`
    ("Mini-Tin Pokemon 30e Anniversaire - Noctali (Version Nuit)") ;
  - drapeau de langue /images/pays/<code>.png (fr, gb...) ;
  - <p class="prix"> et <p class="disponibilite"> ;
  - <p class="selecteur"> : bouton "Ajouter" = commandable en ligne,
    bouton "Alertez-moi !" = non commandable (y compris "Disponible en
    Magasin", stock des boutiques parisiennes seulement).

Pages en Windows-1252. Politesse : quelques pages par cycle, pause
DELAI_ENTRE_REQUETES entre deux requetes, une seule session HTTP.
"""
from __future__ import annotations

import html as html_module
import re
import time
from urllib.parse import urljoin

import requests

from connecteur_shopify import HEADERS_HTML, TIMEOUT

DOMAINE = "ultrajeux.com"
BASE = "https://www.ultrajeux.com/"
DELAI_ENTRE_REQUETES = 1.0

# Categories Pokemon a lire (id Ultrajeux -> libelle), plus la page Pokemon
# generale ou les nouveautes de toutes categories apparaissent en tete.
CATEGORIES = {
    "cat-1-4-x.html": "Pokemon (nouveautes)",
    "cat-1-4-505-x.html": "ETB / Coffret Dresseur d'Elite",
    "cat-1-4-523-x.html": "Bundle de 6 boosters",
    "cat-1-4-488-x.html": "Mini Tin",
    "cat-1-4-81-x.html": "Pokebox",
    "cat-1-4-522-x.html": "Collection Ultra Premium",
}

_RE_TITRE = re.compile(r'alt="([^"]*)"[^>]*class="produit_scan"')
_RE_LIEN = re.compile(r'<p class="titre"><a href="([^"]+)"')
_RE_DRAPEAU = re.compile(r'/images/pays/([a-z]+)\.png')
_RE_PRIX = re.compile(r'<span class="prix">\s*([\d\s.,]+)')
_RE_SELECTEUR = re.compile(r'<p class="selecteur">(.*?)</p>', re.S)


def _prix(brut: str | None) -> float | None:
    if not brut:
        return None
    try:
        return float(brut.replace("\xa0", "").replace(" ", "").replace(",", "."))
    except ValueError:
        return None


def analyser_categorie(page: str) -> list[dict]:
    """[{titre, url, en_stock, prix}] des cartes en FRANCAIS d'une page
    categorie (les cartes d'une autre langue sont ignorees)."""
    resultats = []
    for carte in page.split('<div class="block_produit">')[1:]:
        titre, lien = _RE_TITRE.search(carte), _RE_LIEN.search(carte)
        if not titre or not lien:
            continue
        drapeau = _RE_DRAPEAU.search(carte)
        if drapeau and drapeau.group(1) != "fr":
            continue
        selecteur = _RE_SELECTEUR.search(carte)
        commandable = bool(selecteur) and 'type="submit"' in selecteur.group(1) and "Alertez" not in selecteur.group(1)
        prix = _RE_PRIX.search(carte)
        resultats.append({
            "titre": html_module.unescape(titre.group(1)).strip(),
            "url": urljoin(BASE, html_module.unescape(lien.group(1))),
            "en_stock": commandable,
            "prix": _prix(prix.group(1) if prix else None),
        })
    return resultats


class ConnecteurUltrajeux:
    def __init__(self):
        self.session = requests.Session()
        self._derniere_requete = 0.0

    def rechercher(self, categorie: str) -> list[dict]:
        """`categorie` = chemin d'une page categorie (cf. CATEGORIES)."""
        attente = DELAI_ENTRE_REQUETES - (time.monotonic() - self._derniere_requete)
        if attente > 0:
            time.sleep(attente)
        try:
            r = self.session.get(urljoin(BASE, categorie), headers=HEADERS_HTML, timeout=TIMEOUT)
        finally:
            self._derniere_requete = time.monotonic()
        r.raise_for_status()
        return analyser_categorie(r.content.decode("cp1252", errors="replace"))
