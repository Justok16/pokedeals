"""
Connecteur Leboncoin pour PokéDeals : recherche via l'API publique (bloquée
sur ce sandbox de dev mais fonctionnelle en prod) + extraction des annonces
depuis les emails d'alerte Leboncoin (repli utilisé en continu, l'API étant
protégée par anti-bot).

Extrait de main.py le 17/08/2026 (sixième module du découpage progressif,
cf. SESSION_NOTES.md). Extraction en deux points non contigus dans
main.py (lbc_rechercher d'un côté, lbc_extraire_annonces_email/
lbc_relever_alertes_email de l'autre, séparés par le moteur de cote/
historique qui reste dans main.py) — recollés ici en un seul module.

Deux dépendances qui auraient créé un import circulaire si laissées telles
quelles dans main.py ont été extraites en amont dans des modules dédiés :
- http_utils.py (user_agent, requete_avec_retry) : encore utilisé par
  ebay_rechercher/vinted_rechercher dans main.py, qui restent sur place.
- stats_fiabilite.py (_stats_fiabilite) : dict partagé avec
  vinted_rechercher (main.py), jamais réassigné en bloc (seulement muté
  clé par clé), donc un simple import par nom suffit ici comme côté
  main.py -- pas besoin d'accès qualifié (contrairement à _ct_cache dans
  connecteur_cardtrader.py).
"""
from __future__ import annotations

import email as email_lib
import imaplib
import logging
import re

import requests

from filtre_annonces import SUFFIXES_LANGUE
from http_utils import requete_avec_retry, user_agent
from stats_fiabilite import _stats_fiabilite

log = logging.getLogger("pokedeals.connecteur_leboncoin")


LBC_API = "https://api.leboncoin.fr/finder/search"

LBC_HEADERS = {
    "User-Agent": user_agent(),
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Origin": "https://www.leboncoin.fr",
    "Referer": "https://www.leboncoin.fr/",
}


def lbc_rechercher(nom_carte: str, langue: str, limite: int = 30) -> list[dict]:
    _stats_fiabilite["leboncoin_appels"] += 1
    requete = f"carte pokemon {nom_carte}"
    requete += SUFFIXES_LANGUE.get(langue, "")
    payload = {
        "filters": {
            "category": {"id": "41"},  # Jeux & Jouets
            "keywords": {"text": requete},
        },
        "limit": limite,
        "sort_by": "time",
        "sort_order": "desc",
    }
    try:
        r = requete_avec_retry(requests.post, LBC_API, json=payload, headers=LBC_HEADERS, timeout=25)
        if r.status_code in (403, 429):
            log.info("Leboncoin a bloqué la requête (%s) — plateforme ignorée ce tour-ci", r.status_code)
            return []
        r.raise_for_status()
        ads = r.json().get("ads", []) or []
    except Exception as e:  # noqa: BLE001
        log.info("Leboncoin indisponible (%s) — on continue sans", e)
        _stats_fiabilite["leboncoin_echecs"] += 1
        return []

    annonces = []
    for ad in ads:
        prix_liste = ad.get("price") or []
        if not prix_liste:
            continue
        try:
            prix = float(prix_liste[0])
        except (ValueError, TypeError):
            continue
        annonces.append(
            {
                "plateforme": "Leboncoin",
                "id": f"lbc-{ad.get('list_id', '')}",
                "titre": ad.get("subject", ""),
                "prix": prix,
                "port": 4.0,  # estimation lettre suivie / Mondial Relay
                "url": ad.get("url", ""),
                "etat_texte": (ad.get("subject") or "") + " " + (ad.get("body") or ""),
            }
        )
    return annonces


RE_LBC_LIEN = re.compile(r'https://www\.leboncoin\.fr/(?:[a-z_]+/)?(?:ad/)?[a-z_]*/?(\d{6,12})[^"\s<>]*')
RE_LBC_PRIX = re.compile(r'(\d{1,3}(?:[\s.\u202f\u00a0]?\d{3})*(?:[,.]\d{2})?)\s*€')


def _html_vers_texte(html: str, separateur: str = " ") -> str:
    """Dégrossit du HTML d'email en texte ; chaque balise devient `separateur`."""
    html = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<[^>]+>', separateur, html)
    html = html.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&#8239;', ' ')
    return re.sub(r'[ \t\r\n]+', ' ', html)


def _prix_depuis_texte(texte: str) -> float | None:
    m = RE_LBC_PRIX.search(texte)
    if not m:
        return None
    brut = m.group(1).replace(' ', '').replace('\u202f', '').replace('\u00a0', '')
    brut = brut.replace('.', '').replace(',', '.') if ',' in brut else brut.replace(' ', '')
    try:
        return float(brut)
    except ValueError:
        return None


def lbc_extraire_annonces_email(html: str) -> list[dict]:
    """Extrait (id, url, titre?, prix?) des emails d'alerte Leboncoin.

    Analyse tolérante : on repère chaque lien d'annonce, puis on cherche un
    titre et un prix dans le texte qui l'entoure. Les emails LBC changent de
    mise en page régulièrement, donc on reste volontairement générique.
    """
    annonces = []
    vus = set()
    for m in RE_LBC_LIEN.finditer(html):
        ad_id = m.group(1)
        if ad_id in vus:
            continue
        vus.add(ad_id)
        # Fenêtre de texte autour du lien pour trouver titre et prix
        debut, fin = max(0, m.start() - 600), min(len(html), m.end() + 600)
        fenetre = html[debut:fin]
        # Le prix d'une annonce LBC suit son lien : on cherche d'abord APRÈS,
        # sinon la fenêtre attraperait le prix de l'annonce précédente.
        prix = _prix_depuis_texte(_html_vers_texte(html[m.end():fin]))
        if prix is None:
            prix = _prix_depuis_texte(_html_vers_texte(fenetre))

        # Titre : d'abord le texte du lien <a ...>...</a> de cette annonce
        titre = ""
        m_a = re.search(r'<a[^>]*' + re.escape(ad_id) + r'[^>]*>(.*?)</a>',
                        fenetre, flags=re.DOTALL | re.IGNORECASE)
        if m_a:
            titre = _html_vers_texte(m_a.group(1)).strip()
        if not (10 <= len(titre) <= 120):
            # Secours : plus long segment de texte plausible autour du lien
            titre = ""
            for morceau in _html_vers_texte(fenetre, separateur="|").split('|'):
                morceau = morceau.strip()
                if 10 <= len(morceau) <= 120 and '€' not in morceau and 'http' not in morceau:
                    if len(morceau) > len(titre):
                        titre = morceau
        annonces.append({
            "id": f"lbc-{ad_id}",
            "url": f"https://www.leboncoin.fr/ad/collection/{ad_id}",
            "titre": titre,
            "prix": prix if prix is not None else 0.0,
            "port": 0.0,
            "plateforme": "Leboncoin (alerte)",
            "etat_texte": "",
            "vendeur_nom": "voir annonce",
            "vendeur_pct": 100,
        })
    return [a for a in annonces if a["prix"] > 0 and a["titre"]]


def lbc_relever_alertes_email(cfg: dict, secrets: dict) -> list[dict]:
    """Lit les emails d'alerte Leboncoin non lus dans Gmail et en extrait les annonces."""
    conf = cfg.get("leboncoin_alertes_email", {})
    if not conf.get("actif"):
        return []
    mdp = secrets.get("GMAIL_APP_PASSWORD", "")
    adresse = cfg.get("email", {}).get("destinataire", "")
    if not mdp or not adresse:
        log.info("Alertes email LBC : GMAIL_APP_PASSWORD ou adresse manquant — ignoré")
        return []

    annonces = []
    try:
        imap = imaplib.IMAP4_SSL(conf.get("imap_hote", "imap.gmail.com"))
        imap.login(adresse, mdp)
        imap.select(conf.get("boite", "INBOX"))
        # Emails NON LUS venant de Leboncoin
        statut, donnees = imap.search(None, '(UNSEEN FROM "leboncoin")')
        ids = donnees[0].split() if statut == "OK" and donnees and donnees[0] else []
        for num in ids[-20:]:  # au plus 20 emails par passage
            statut, msg_data = imap.fetch(num, "(RFC822)")  # fetch marque l'email comme lu
            if statut != "OK":
                continue
            message = email_lib.message_from_bytes(msg_data[0][1])
            html = ""
            for part in message.walk():
                if part.get_content_type() == "text/html":
                    charset = part.get_content_charset() or "utf-8"
                    html += part.get_payload(decode=True).decode(charset, errors="replace")
            if html:
                annonces.extend(lbc_extraire_annonces_email(html))
        imap.logout()
        # V46 : avant, rien n'était loggé si 0 email trouvé ou 0 annonce
        # extraite -> impossible de savoir depuis les logs GitHub Actions si
        # le canal Leboncoin est bloqué (aucune alerte Leboncoin reçue côté
        # Gmail) ou cassé côté code (mise en page LBC changée, regex à jour
        # mais extraction vide). Les trois cas sont maintenant distingués.
        if annonces:
            log.info("Alertes email LBC : %d annonce(s) extraite(s) de %d email(s)", len(annonces), len(ids))
        elif ids:
            log.warning("Alertes email LBC : %d email(s) non lu(s) de Leboncoin trouvé(s) mais AUCUNE annonce "
                        "extraite (mise en page Leboncoin changée ?)", len(ids))
        else:
            log.info("Alertes email LBC : aucun email non lu de Leboncoin trouvé dans %s", adresse)
    except Exception as e:  # noqa: BLE001
        log.warning("Alertes email LBC en erreur (non bloquant) : %s", e)
    return annonces
