"""
Verification par IA de vision de la coherence photo/annonce pour PokeDeals.

Systeme OPTIONNEL et NON BLOQUANT, ajoute le 16/08/2026 apres etude de
faisabilite (cf. SESSION_NOTES.md) : ne s'active QUE si le secret
ANTHROPIC_API_KEY est fourni, et n'est appele QUE par main.envoyer_telegram
sur les annonces qui ont DEJA passe tous les filtres texte et sont sur le
point de declencher une alerte -- jamais sur le flux brut d'annonces
scannees a chaque cycle. Volume attendu : quelques appels par jour au
maximum (cf. data/deals.csv), cout negligeable.

Perimetre volontairement restreint : verifier que la PHOTO montre bien le
bon Pokemon dans la bonne langue -- PAS l'authenticite (proxy/fake) ni la
condition/le centrage, qu'une IA de vision generaliste ne peut pas juger
de facon fiable sur une photo de petite annonce (angle, lumiere, resolution
variables). Cas reel qui motive ce module (cf. commentaire V37 dans
main.py, _texte_telegram) : une annonce Vinted titree entierement en
francais pointait en realite vers une carte COREENNE sur la photo -- aucun
filtre texte ne peut detecter ca.

Ne bloque JAMAIS une alerte : en cas d'echec (secret absent, image
inaccessible, reponse ambigue, erreur reseau...), verifier_photo_annonce
renvoie (None, raison) et l'appelant garde le comportement actuel
(avertissement generique existant sur les fortes decotes), jamais un rejet
silencieux d'un deal reel.
"""
from __future__ import annotations

import base64
import logging

import requests

log = logging.getLogger("pokedeals.verification_photo")

MODELE = "claude-haiku-4-5-20251001"
API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"

LIBELLES_LANGUE = {
    "fr": "française", "jp": "japonaise", "en": "anglaise",
    "kr": "coréenne", "cn": "chinoise",
}


def _telecharger_image(image_url: str) -> tuple[bytes, str] | None:
    """Telecharge l'image et devine son type MIME. None si echec."""
    try:
        r = requests.get(image_url, timeout=15)
        r.raise_for_status()
    except Exception as e:  # noqa: BLE001
        log.warning("Téléchargement image échoué (%s) : %s", image_url, e)
        return None
    contenu_type = r.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()
    if not contenu_type.startswith("image/"):
        contenu_type = "image/jpeg"  # repli raisonnable, la plupart des photos d'annonce sont en JPEG
    return r.content, contenu_type


def _interpreter_reponse(texte: str) -> tuple[str | None, str]:
    """Parse la reponse du modele. Toute reponse hors format attendu (ou
    "INCERTAIN") est traitee comme NON CONCLUANTE (None) -- jamais
    interpretee par defaut comme une confirmation ou un rejet."""
    t = (texte or "").strip()
    if t.upper().startswith("COHERENT"):
        return "coherent", ""
    if t.upper().startswith("INCOHERENT"):
        raison = t.split(":", 1)[1].strip() if ":" in t else "carte/langue différente sur la photo"
        return "incoherent", raison
    if t.upper().startswith("INCERTAIN"):
        raison = t.split(":", 1)[1].strip() if ":" in t else "vérification incertaine"
        return None, raison
    return None, f"réponse inattendue du modèle ({t[:80]!r})"


def verifier_photo_annonce(image_url: str, nom_carte: str, langue: str, api_key: str) -> tuple[str | None, str]:
    """Verifie par IA de vision que la photo de l'annonce montre bien
    `nom_carte` dans la langue `langue`.

    Retourne (verdict, raison) :
      - ("coherent", "")       : la photo confirme la carte/langue attendue
      - ("incoherent", raison) : la photo montre visiblement autre chose
      - (None, raison)         : verification indisponible/non concluante --
                                   ne JAMAIS traiter comme une confirmation
                                   ni comme un rejet, c'est juste "on ne sait pas"
    """
    if not api_key:
        return None, "ANTHROPIC_API_KEY non configuré"
    if not image_url:
        return None, "aucune image disponible pour cette annonce"

    telechargement = _telecharger_image(image_url)
    if telechargement is None:
        return None, "image inaccessible"
    contenu, mime = telechargement

    langue_libelle = LIBELLES_LANGUE.get(langue, langue or "française")
    prompt = (
        f"Cette photo est celle d'une annonce de vente d'une carte Pokémon. "
        f"La carte recherchée est : \"{nom_carte}\", en langue {langue_libelle}. "
        f"Réponds UNIQUEMENT selon ce format strict, sans autre texte :\n"
        f"- \"COHERENT\" si la photo montre bien ce Pokémon dans cette langue\n"
        f"- \"INCOHERENT: <raison courte>\" si la photo montre un AUTRE Pokémon "
        f"ou une AUTRE langue de façon claire\n"
        f"- \"INCERTAIN: <raison courte>\" si tu ne peux pas juger avec confiance "
        f"(photo floue, carte non visible, angle...)"
    )

    try:
        r = requests.post(
            API_URL,
            headers={
                "x-api-key": api_key,
                "anthropic-version": API_VERSION,
                "content-type": "application/json",
            },
            json={
                "model": MODELE,
                "max_tokens": 100,
                "messages": [{
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": mime,
                                "data": base64.b64encode(contenu).decode("ascii"),
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }],
            },
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        texte = "".join(
            bloc.get("text", "") for bloc in data.get("content", []) if bloc.get("type") == "text"
        ).strip()
    except Exception as e:  # noqa: BLE001
        log.warning("Appel de vérification photo échoué : %s", e)
        return None, "erreur API de vérification"

    return _interpreter_reponse(texte)
