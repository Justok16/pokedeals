"""
Verification periodique de disponibilite/prix des "bonnes affaires" deja
enregistrees dans watchlist_alerts (dashboard SaaS pokedeals-saas) -- ajoute
le 03/09/2026, demande explicite de Justok : la liste affichee au dashboard
restait figee sur le prix/statut au moment de la detection, sans jamais
reverifier ensuite si la carte etait encore disponible.

Systeme INDEPENDANT du reste du scraper (nouveau fichier, aucune modification
des connecteurs/orchestrateurs existants) -- reutilise uniquement les
fonctions d'extraction JSON-LD/microdata deja eprouvees de
connecteur_prestashop_sitemap.py/connecteur_woocommerce.py (memes garde-fous
DOM deja en place pour ces deux plateformes, cf. leurs docstrings), sans
jamais les modifier.

Couverture par plateforme (v1) :
- Shopify : fiable -- endpoint public /products/<handle>.json (le prix/stock
  EXACT que le site affiche, aucune ambiguite de parsing, meme technique que
  connecteur_shopify.py).
- PrestaShop / WooCommerce : reutilise les memes extracteurs JSON-LD/microdata
  + garde-fous DOM que les connecteurs de scan (meme fiabilite qu'un scan
  normal), appliques a l'URL individuelle de l'alerte plutot qu'a un sitemap
  complet.
- eBay/Vinted/Leboncoin (main.py) : PAS de verification fiable possible sans
  API dediee (eBay Browse API necessiterait l'item ID, jamais stocke
  aujourd'hui dans watchlist_alerts ; Vinted/Leboncoin bloques par anti-bot,
  deja documente dans CLAUDE.md) -- volontairement HORS PERIMETRE en v1,
  `disponible` reste NULL pour ces alertes (jamais "False" par exces de
  confiance sur une plateforme qu'on ne sait pas verifier). A etendre plus
  tard si besoin reel.

Optionnel et non bloquant (meme philosophie que verification_photo.py) :
toute erreur individuelle (page introuvable de facon ambigue, page cassee,
timeout, JSON-LD absent) laisse l'alerte INCHANGEE pour ce cycle (retentee
au prochain), jamais un "disponible=False" par exces de confiance sur une
incertitude technique -- seule une confirmation POSITIVE de rupture/
suppression (404, stock explicitement a 0/rupture) met `disponible=False`.

**Notification sur transition** (ajoute le 03/09/2026, meme jour que le
reste de ce module) : jusqu'ici, ce radar ecrivait silencieusement
disponible/prix_verifie/derniere_verification a chaque cycle, sans jamais
prevenir l'utilisateur -- il fallait rouvrir le dashboard pour voir qu'une
carte avait ete vendue ou que son prix avait encore baisse.
detecter_transition() compare le resultat FRAIS de verifier_une_alerte() a
l'etat PRECEDENT de la ligne watchlist_alerts (lu par lister_alertes_recentes()
AVANT l'appel a enregistrer_verification(), qui l'ecrase) pour ne signaler
QUE deux transitions, jamais un etat deja connu re-signale a chaque cycle
de 30 min :
- "vendu" : `disponible` passe de True/None (jamais verifie) a False pour
  la PREMIERE fois -- un True->False deja vu au cycle precedent ne re-notifie
  pas.
- "baisse_prix" : `prix_verifie` devient significativement (>SEUIL_BAISSE_
  PRIX_SUPPLEMENTAIRE) inferieur au prix D'ORIGINE de l'alerte (`prix`,
  jamais modifie apres l'insertion initiale) -- comparaison a l'origine,
  pas cycle-a-cycle, pour capter une baisse progressive sur plusieurs
  cycles ; mais seulement la PREMIERE fois que ce seuil est franchi (le
  precedent `prix_verifie` n'etait pas deja sous ce seuil), pas a chaque
  cycle tant que le prix reste bas.
L'envoi lui-meme (push/email) est delegue a
notifications_saas.notifier_transition_verification() -- meme
infrastructure que les autres notifications SaaS, mais sans le mecanisme
de retry "push_envoye/email_envoye" des alertes de detection (pas de
colonne dediee pour cet evenement) : un envoi qui echoue ce cycle n'est
PAS retente, best-effort, jamais bloquant -- meme philosophie que le reste
de ce fichier (une erreur reseau/secret n'interrompt jamais le radar).
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests

from connecteur_prestashop_sitemap import (
    _analyser_offre as _analyser_offre_prestashop,
    _extraire_jsonld_produit as _extraire_jsonld_prestashop,
    _extraire_microdata_produit,
    _stock_indisponible_selon_dom as _stock_indisponible_prestashop,
)
from connecteur_shopify import HEADERS, HEADERS_HTML, TIMEOUT
from connecteur_woocommerce import (
    _analyser_offre_jsonld as _analyser_offre_woocommerce,
    _attente_sans_panier_selon_dom,
    _extraire_html_woocommerce,
    _extraire_jsonld_produit as _extraire_jsonld_woocommerce,
    _stock_indisponible_selon_dom as _stock_indisponible_woocommerce,
)

log = logging.getLogger("pokedeals.verification_alertes")

TAILLE_PAGE = 100  # garde-fou de volume, meme esprit que TAILLE_PAGE_WATCHLIST (connecteur_supabase.py)
DELAI_ENTRE_VERIFICATIONS = 1.0  # politesse reseau, meme ordre de grandeur que DELAI_ENTRE_BOUTIQUES ailleurs


def _domaine_depuis_url(url: str) -> str:
    return urlparse(url).netloc.removeprefix("www.")


def _plateforme_boutique(domaine: str) -> str | None:
    """"shopify"/"prestashop"/"woocommerce" si le domaine est une boutique
    ACTIVEMENT scannee par le radar boutiques TCG (memes listes que
    scan_boutique*.py -- LOT_A/LOT_B pour PrestaShop/WooCommerce, cf. leur
    docstring "repartition pour la production"), None sinon (ex. eBay,
    Vinted, ou une boutique retiree depuis -- jamais une erreur, juste "non
    verifiable" pour ce domaine)."""
    from boutiques_decouvertes import (
        BOUTIQUES_SHOPIFY_AUTO,
        BOUTIQUES_SHOPIFY_AUTO_PRECOMMANDE_SEULEMENT,
        BOUTIQUES_WOOCOMMERCE_AUTO,
        BOUTIQUES_WOOCOMMERCE_AUTO_PRECOMMANDE_SEULEMENT,
    )
    from boutiques_prestashop import LOT_A as PRESTASHOP_LOT_A
    from boutiques_prestashop import LOT_B as PRESTASHOP_LOT_B
    from boutiques_shopify import BOUTIQUES_SHOPIFY, BOUTIQUES_SHOPIFY_PRECOMMANDE_SEULEMENT
    from boutiques_woocommerce import BOUTIQUES_WOOCOMMERCE_PRECOMMANDE_SEULEMENT
    from boutiques_woocommerce import LOT_A as WOOCOMMERCE_LOT_A
    from boutiques_woocommerce import LOT_B as WOOCOMMERCE_LOT_B

    if domaine in {
        *BOUTIQUES_SHOPIFY, *BOUTIQUES_SHOPIFY_PRECOMMANDE_SEULEMENT,
        *BOUTIQUES_SHOPIFY_AUTO, *BOUTIQUES_SHOPIFY_AUTO_PRECOMMANDE_SEULEMENT,
    }:
        return "shopify"
    if domaine in {
        *WOOCOMMERCE_LOT_A, *WOOCOMMERCE_LOT_B,
        *BOUTIQUES_WOOCOMMERCE_PRECOMMANDE_SEULEMENT,
        *BOUTIQUES_WOOCOMMERCE_AUTO, *BOUTIQUES_WOOCOMMERCE_AUTO_PRECOMMANDE_SEULEMENT,
    }:
        return "woocommerce"
    if domaine in {*PRESTASHOP_LOT_A, *PRESTASHOP_LOT_B}:
        return "prestashop"
    return None


def _verifier_shopify(url: str) -> dict | None:
    try:
        r = requests.get(f"{url.rstrip('/')}.json", headers=HEADERS, timeout=TIMEOUT)
    except requests.RequestException as e:
        log.warning("Vérification Shopify échouée pour %s (%s) -- ignorée ce cycle", url, e)
        return None
    if r.status_code == 404:
        return {"disponible": False, "prix": None}
    if not r.ok:
        return None
    try:
        produit = r.json().get("product", {})
    except ValueError:
        return None
    variants = produit.get("variants") or []
    if not variants:
        return None
    en_stock = any(v.get("available") for v in variants)
    try:
        prix = float(variants[0].get("price"))
    except (TypeError, ValueError):
        prix = None
    return {"disponible": en_stock, "prix": prix}


def _verifier_prestashop(url: str) -> dict | None:
    try:
        r = requests.get(url, headers=HEADERS_HTML, timeout=TIMEOUT)
    except requests.RequestException as e:
        log.warning("Vérification PrestaShop échouée pour %s (%s) -- ignorée ce cycle", url, e)
        return None
    if r.status_code == 404:
        return {"disponible": False, "prix": None}
    if not r.ok:
        return None
    html = r.text
    produit = _extraire_jsonld_prestashop(html)
    offre = _analyser_offre_prestashop(produit) if produit else _extraire_microdata_produit(html)
    if not offre or offre.get("prix") is None:
        return None
    en_stock = bool(offre.get("en_stock"))
    if _stock_indisponible_prestashop(html):
        en_stock = False
    return {"disponible": en_stock, "prix": offre["prix"]}


def _verifier_woocommerce(url: str) -> dict | None:
    try:
        r = requests.get(url, headers=HEADERS_HTML, timeout=TIMEOUT)
    except requests.RequestException as e:
        log.warning("Vérification WooCommerce échouée pour %s (%s) -- ignorée ce cycle", url, e)
        return None
    if r.status_code == 404:
        return {"disponible": False, "prix": None}
    if not r.ok:
        return None
    html = r.text
    produit = _extraire_jsonld_woocommerce(html)
    offre = _analyser_offre_woocommerce(produit) if produit else _extraire_html_woocommerce(html)
    if not offre or offre.get("prix") is None:
        return None
    en_stock = bool(offre.get("en_stock"))
    if _stock_indisponible_woocommerce(html) or _attente_sans_panier_selon_dom(html):
        en_stock = False
    return {"disponible": en_stock, "prix": offre["prix"]}


def verifier_une_alerte(url: str) -> dict | None:
    """Retourne {"disponible": bool, "prix": float|None} si la plateforme de
    `url` est verifiable et que la verification a reussi, None sinon
    (plateforme non couverte -- eBay/Vinted/Leboncoin, ou toute autre
    boutique retiree des listes actives -- ou echec technique de la
    verification). None ne doit JAMAIS etre interprete comme "indisponible",
    seulement comme "on ne sait pas cette fois-ci"."""
    domaine = _domaine_depuis_url(url)
    type_boutique = _plateforme_boutique(domaine)
    if type_boutique == "shopify":
        return _verifier_shopify(url)
    if type_boutique == "prestashop":
        return _verifier_prestashop(url)
    if type_boutique == "woocommerce":
        return _verifier_woocommerce(url)
    return None


# --- Notification sur transition (03/09/2026) ---

# >5% : un simple bruit de re-verification (arrondi, frais de port
# recalcules...) ne doit pas notifier -- seule une VRAIE baisse
# supplementaire le doit. Meme ordre de grandeur que les seuils de decote
# deja utilises ailleurs dans le projet (ex. bonne_affaire_shopify.py,
# decote >=30%), mais volontairement plus bas ici : ce n'est pas une
# alerte de "bonne affaire" (deja envoyee a la detection), juste un signal
# "encore moins cher qu'avant" sur une carte deja repérée par l'utilisateur.
SEUIL_BAISSE_PRIX_SUPPLEMENTAIRE = 0.05


def _prix_deja_signale_bas(prix_origine: float | None, prix_verifie_precedent: float | None) -> bool:
    """True si `prix_verifie_precedent` était déjà sous le seuil de baisse
    par rapport à `prix_origine` -- sert à ne notifier "baisse_prix" que la
    PREMIÈRE fois que ce seuil est franchi, jamais à chaque cycle tant que
    le prix reste bas."""
    if prix_verifie_precedent is None or not prix_origine:
        return False
    return prix_verifie_precedent <= prix_origine * (1 - SEUIL_BAISSE_PRIX_SUPPLEMENTAIRE)


def detecter_transition(alerte: dict, resultat: dict) -> str | None:
    """Compare le résultat FRAIS d'une vérification (`resultat`, cf.
    verifier_une_alerte()) à l'état PRÉCÉDENT de la ligne watchlist_alerts
    (`alerte`, tel que renvoyé par lister_alertes_recentes() -- doit donc
    être lu AVANT tout appel à enregistrer_verification(), qui écrase cet
    état). Retourne :
    - "vendu" : `disponible` passe de True/None (jamais vérifié) à False
      pour la PREMIÈRE fois -- un True/None->False déjà connu au cycle
      précédent (donc déjà `disponible: False` en base) ne re-notifie pas.
    - "baisse_prix" : `prix_verifie` devient significativement
      (SEUIL_BAISSE_PRIX_SUPPLEMENTAIRE) inférieur au prix D'ORIGINE de
      l'alerte (`alerte["prix"]`, jamais modifié après l'insertion
      initiale -- pas le `prix_verifie` du cycle précédent), la PREMIÈRE
      fois que ce seuil est franchi.
    - None : aucune transition notable (y compris si `resultat` est None,
      c-a-d verifier_une_alerte() n'a rien pu conclure ce cycle)."""
    if not resultat:
        return None

    if resultat.get("disponible") is False and alerte.get("disponible") is not False:
        return "vendu"

    prix_verifie = resultat.get("prix")
    prix_origine = alerte.get("prix")
    if (prix_verifie is not None and prix_origine
            and prix_verifie <= prix_origine * (1 - SEUIL_BAISSE_PRIX_SUPPLEMENTAIRE)
            and not _prix_deja_signale_bas(prix_origine, alerte.get("prix_verifie"))):
        return "baisse_prix"

    return None


def message_transition(alerte: dict, resultat: dict, transition: str) -> tuple[str, str]:
    """Compose (titre, corps) de la notification pour une transition
    détectée par detecter_transition() -- fonction pure, séparée pour
    rester testable sans réseau ni Supabase."""
    titre_carte = (alerte.get("titre") or "une carte")[:80]
    if transition == "vendu":
        titre = f"Vendue/retirée : {titre_carte}"
        corps = "Cette annonce que tu suivais semble avoir été vendue ou retirée"
        if alerte.get("plateforme"):
            corps += f" ({alerte['plateforme']})"
        corps += " -- plus la peine de la chasser."
        return titre, corps

    # "baisse_prix"
    titre = f"Encore moins cher : {titre_carte}"
    prix_origine = alerte.get("prix")
    corps = f"{resultat['prix']:.2f}€ maintenant"
    if prix_origine:
        corps += f" (contre {float(prix_origine):.2f}€ à l'alerte d'origine)"
    if alerte.get("plateforme"):
        corps += f", sur {alerte['plateforme']}"
    corps += "."
    return titre, corps


# --- Pont Supabase (dashboard pokedeals-saas) ---

def _headers(service_role_key: str) -> dict:
    return {"apikey": service_role_key, "Authorization": f"Bearer {service_role_key}"}


def lister_alertes_recentes(supabase_url: str, service_role_key: str) -> list[dict]:
    """Retourne jusqu'a TAILLE_PAGE alertes les plus recentes (memes que
    celles affichees au dashboard, qui n'en montre que 20 -- une marge est
    prise pour rester robuste si la limite d'affichage change un jour).
    [] si secrets absents ou erreur reseau (module optionnel et non
    bloquant, meme philosophie que connecteur_supabase.py)."""
    if not supabase_url or not service_role_key:
        return []
    try:
        r = requests.get(
            f"{supabase_url.rstrip('/')}/rest/v1/watchlist_alerts",
            params={
                # id/url : necessaires a la verification elle-meme.
                # user_id/titre/prix/plateforme : necessaires a la
                # notification de transition (cf. detecter_transition() et
                # notifications_saas.notifier_transition_verification()).
                # disponible/prix_verifie : etat PRECEDENT, lu AVANT
                # d'etre ecrase par enregistrer_verification() -- c'est ce
                # qui permet de detecter une transition plutot que de
                # re-signaler un etat deja connu a chaque cycle.
                "select": "id,url,user_id,titre,prix,plateforme,disponible,prix_verifie",
                "order": "created_at.desc",
                "limit": str(TAILLE_PAGE),
            },
            headers=_headers(service_role_key),
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        log.warning("Lecture des alertes récentes échouée (%s) -- ignorée ce cycle", e)
        return []


def enregistrer_verification(
    supabase_url: str, service_role_key: str, alerte_id: str, resultat: dict,
) -> None:
    """Enregistre le resultat d'une verification reussie (disponible/prix),
    horodate a maintenant. Erreur reseau : loguee et ignoree, retentee au
    prochain cycle (comportement sur, meme pattern que
    connecteur_supabase.marquer_notification_envoyee)."""
    if not supabase_url or not service_role_key:
        return
    try:
        r = requests.patch(
            f"{supabase_url.rstrip('/')}/rest/v1/watchlist_alerts",
            params={"id": f"eq.{alerte_id}"},
            json={
                "disponible": resultat["disponible"],
                "prix_verifie": resultat["prix"],
                "derniere_verification": datetime.now(timezone.utc).isoformat(),
            },
            headers={**_headers(service_role_key), "Content-Type": "application/json"},
            timeout=TIMEOUT,
        )
        r.raise_for_status()
    except requests.RequestException as e:
        log.warning("Écriture de la vérification échouée pour l'alerte %s (%s) -- retentée au prochain cycle",
                    alerte_id, e)
