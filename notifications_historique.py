"""
Notifications (Telegram + email) du systeme historique de PokeDeals (main.py).

Extrait de main.py le 16/08/2026 (deuxieme module du decoupage progressif
de main.py, cf. SESSION_NOTES.md) : formatage et envoi des messages
Telegram/email pour les deals eBay/Vinted/Leboncoin, les alertes de
revente et les messages libres (recap, anomalies...). Bloc entierement
autonome -- aucune dependance vers l'avant dans main.py, seulement des
dicts de donnees (deal/vente) passes en parametre.

verifier_photo_annonce (verification_photo.py) est appelee ici, juste
avant l'envoi de chaque deal Telegram -- cf. ce module pour le detail et
la justification du perimetre (verification optionnelle et non bloquante).
"""
from __future__ import annotations

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

from verification_photo import verifier_photo_annonce

log = logging.getLogger("pokedeals.notifications_historique")


def envoyer_telegram_texte(textes: list[str], cfg_tg: dict, token: str) -> bool:
    """Envoie des messages Telegram libres (récap quotidien, anomalies...)."""

    if not textes:
        return True
    if not token or not str(cfg_tg.get("chat_id", "")).strip():
        log.error("Telegram non configuré : message non envoyé")
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    ok = True
    for txt in textes:
        try:
            r = requests.post(
                url,
                json={"chat_id": str(cfg_tg["chat_id"]), "text": txt, "parse_mode": "HTML"},
                timeout=20,
            )
            if r.status_code != 200:
                log.error("Telegram a refusé le message (%s)", r.status_code)
                ok = False
        except Exception as e:  # noqa: BLE001
            log.error("Échec message Telegram : %s", e)
            ok = False
    return ok


def _echapper_html(texte) -> str:
    """Échappe les caractères spéciaux HTML (< > &) avant insertion dans un
    message Telegram en parse_mode HTML. Sans ça, un titre d'annonce
    contenant '<', '>' ou '&' casse le formatage et Telegram REFUSE le
    message (alerte perdue). On échappe uniquement les 3 caractères
    réservés, dans le bon ordre (& en premier)."""
    s = str(texte)
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _texte_vente(v: dict) -> str:
    return (
        f"💰 <b>C'EST LE MOMENT DE VENDRE !</b>\n"
        f"🎴 <b>{_echapper_html(v['nom'])}</b>\n"
        f"🛒 Acheté : {v['prix_achat']:.2f}€\n"
        f"📈 Cote actuelle : <b>{v['cote']:.2f}€</b> (x{v['multiple']})\n"
        f"✅ Gain net estimé après frais : <b>+{v['gain_net_estime']:.2f}€</b>"
    )


def envoyer_telegram_ventes(ventes: list[dict], cfg_tg: dict, token: str) -> bool:
    """Alertes de revente (stock ayant atteint l'objectif) sur Telegram."""

    if not ventes:
        return True
    if not token or not str(cfg_tg.get("chat_id", "")).strip():
        log.error("Telegram non configuré : alerte de vente non envoyée")
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    ok = True
    for v in ventes:
        try:
            r = requests.post(
                url,
                json={"chat_id": str(cfg_tg["chat_id"]), "text": _texte_vente(v), "parse_mode": "HTML"},
                timeout=20,
            )
            if r.status_code != 200:
                log.error("Telegram a refusé l'alerte vente (%s)", r.status_code)
                ok = False
        except Exception as e:  # noqa: BLE001
            log.error("Échec alerte vente Telegram : %s", e)
            ok = False
    return ok


def _echapper_url_html(url: str) -> str:
    """Échappe uniquement le '&' dans une URL pour usage en attribut HTML
    (href="..."). Les '<', '>' et '"' sont volontairement laissés intacts
    dans le chemin/la requête d'une URL normale, mais '&' doit être encodé
    en &amp; dans du HTML, sinon Telegram peut refuser le message si l'URL
    contient plusieurs paramètres (ex. '?item=1&category=2')."""
    return str(url).replace("&", "&amp;")


def _ligne_verification_photo(verif_photo: tuple[str | None, str] | None) -> str:
    """Formatte le resultat de verification_photo.verifier_photo_annonce()
    en une ligne Telegram. verif_photo est None quand la verification n'a
    pas ete tentee (secret absent, pas d'image) -- distinct de (None, raison)
    quand elle a ete tentee mais n'a pas ete concluante ; les deux cas
    n'affichent simplement rien de plus (cf. avertissement generique V37,
    inchange par ailleurs)."""
    if verif_photo is None:
        return ""
    verdict, raison = verif_photo
    if verdict == "coherent":
        return "\n📸 Vérification IA : photo cohérente avec la carte/langue attendue."
    if verdict == "incoherent":
        # V51 : reformule pour ne plus afficher "INCOHÉRENTE" comme un fait
        # confirmé -- cas réel (17/08/2026) où l'IA de vision a confondu
        # Méga-Dracaufeu X et Y (variantes visuellement proches) sur une
        # vraie bonne affaire (+305€ de profit estimé), photo pourtant
        # correcte. Le verdict reste affiché (signal utile la plupart du
        # temps), mais explicitement présenté comme une IA généraliste
        # pouvant se tromper, pas une certitude -- pour ne plus faire fuir
        # un vrai deal sur un faux positif.
        return (f"\n🚨 <b>Vérification IA</b> : photo semble incohérente "
                f"({_echapper_html(raison)}) — cette vérification automatique "
                f"peut se tromper (ex. variantes visuellement proches), "
                f"regarde toi-même la photo avant de décider !")
    return ""  # non concluant (None, raison) : pas de ligne, ni confirmation ni rejet


def _texte_telegram(d: dict, verif_photo: tuple[str | None, str] | None = None) -> str:
    # V46 : ligne Cardmarket, purement informative -- n'existe QUE quand
    # main() a pu la calculer en toute confiance (cf. commentaire V46 dans
    # main(), juste après les GARDE-FOU 4/5). N'influence jamais "cote" ni
    # aucune décision : simple info affichée en plus pour vérification
    # visuelle rapide avant achat.
    ligne_cardmarket = ""
    if d.get("cardmarket_prix") is not None:
        ligne_cardmarket = f"\n🇪🇺 Cardmarket (tendance) : {d['cardmarket_prix']:.2f}€"

    ligne_photo = _ligne_verification_photo(verif_photo)

    # V45 : message dédié pour un deal sur seuil de prix fixe (confiance
    # 100). Pas de cote/décote/profit à afficher, ça n'a pas de sens ici.
    if d.get("confiance") == 100:
        return (
            f"🎯 <b>{_echapper_html(d['titre'])}</b>\n"
            f"🛒 {_echapper_html(d['plateforme'])} — <b>{d['prix']:.2f}€</b> "
            f"(seuil fixé : {d['cote']:.2f}€, port non compté)"
            f"{ligne_cardmarket}{ligne_photo}\n"
            f"👉 <a href=\"{_echapper_url_html(d['url'])}\">Voir l'annonce</a>"
        )
    # V37 : AVERTISSEMENT sur les écarts extrêmes. Une décote de plus de 30%
    # sous la cote est un vrai signal d'alerte, PAS une bonne nouvelle plus
    # grande : le programme lit uniquement le TEXTE de l'annonce, jamais la
    # photo (sauf verification_photo.py, quand ANTHROPIC_API_KEY est
    # configuré -- cf. ligne_photo ci-dessus, qui vient compléter cet
    # avertissement générique sans jamais s'y substituer). Cas vécu : une
    # annonce titrée entièrement en français (drapeau 🇫🇷, "EV3.5", "Écarlate
    # et Violet") pointait en réalité vers une carte CORÉENNE sur la photo —
    # le vendeur avait mis la mauvaise image. Aucun filtre textuel ne peut
    # détecter ça. Un écart de prix trop généreux est souvent le seul indice
    # indirect qu'il faut vérifier la photo avant d'acheter.
    avertissement = ""
    if d.get("decote_pct", 0) and float(d["decote_pct"]) >= 30:
        avertissement = (
            "\n⚠️ <b>Écart important avec la cote — vérifie la photo avant "
            "d'acheter</b> (le titre peut être juste, mais l'image parfois "
            "ne correspond pas à la carte annoncée).")
    return (
        f"🔥 <b>{_echapper_html(d['titre'])}</b>\n"
        f"🛒 {_echapper_html(d['plateforme'])} — <b>{d['prix']:.2f}€</b> + {d['port']:.2f}€ port = <b>{d['total']:.2f}€</b>\n"
        f"📊 Cote : {d['cote']:.2f}€ (<b>-{d['decote_pct']}%</b>)"
        f"{ligne_cardmarket}\n"
        f"💶 Revente conseillée : {d['prix_revente_conseille']:.2f}€\n"
        f"✅ Profit net estimé : <b>+{d['profit_net_estime']:.2f}€</b>"
        f"{avertissement}{ligne_photo}\n"
        f"👉 <a href=\"{_echapper_url_html(d['url'])}\">Voir l'annonce</a>"
    )


def envoyer_telegram(deals: list[dict], cfg_tg: dict, token: str, anthropic_api_key: str = "") -> bool:
    """Envoie une notification Telegram par deal (instantané).

    `anthropic_api_key` (optionnel) : si fourni, chaque deal AVEC une photo
    disponible (cf. image_url dans ebay_rechercher/vinted_rechercher) passe
    par verification_photo.verifier_photo_annonce() juste avant l'envoi --
    uniquement sur ces quelques deals déjà filtrés, jamais sur le flux brut
    d'annonces. Absent -> comportement strictement inchangé (cf.
    verification_photo.py pour le détail et la justification du périmètre).
    """
    if not deals:
        return True
    if not token:
        log.error("TELEGRAM_BOT_TOKEN manquant : notification Telegram impossible")
        return False
    chat_id = str(cfg_tg.get("chat_id", "")).strip()
    if not chat_id:
        log.error("telegram.chat_id manquant dans config.yaml")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    ok = True
    for d in deals:
        verif_photo = None
        if anthropic_api_key and d.get("image_url"):
            verif_photo = verifier_photo_annonce(
                d["image_url"], d.get("carte", d.get("titre", "")), d.get("langue", "fr"), anthropic_api_key)
            verdict, raison = verif_photo
            log.info("Vérification photo (%s) : %s%s", d.get("titre", "")[:60],
                     verdict or "non concluante", f" ({raison})" if raison else "")
        try:
            r = requests.post(
                url,
                json={
                    "chat_id": chat_id,
                    "text": _texte_telegram(d, verif_photo),
                    "parse_mode": "HTML",
                    "disable_web_page_preview": False,
                },
                timeout=20,
            )
            if r.status_code != 200:
                log.error("Telegram a refusé le message (%s) : %s", r.status_code, r.text[:200])
                ok = False
        except Exception as e:  # noqa: BLE001
            log.error("Échec envoi Telegram : %s", e)
            ok = False
    if ok:
        log.info("Telegram : %d notification(s) envoyée(s)", len(deals))
    return ok


def _html_deal(d: dict) -> str:
    return f"""
    <div style="border:1px solid #ddd;border-radius:8px;padding:14px;margin:10px 0;font-family:Arial">
      <h3 style="margin:0 0 6px">🔥 {d['titre']}</h3>
      <p style="margin:4px 0">
        <b>Plateforme :</b> {d['plateforme']}<br>
        <b>Prix :</b> {d['prix']:.2f}€ + {d['port']:.2f}€ de port = <b>{d['total']:.2f}€</b><br>
        <b>Cote estimée :</b> {d['cote']:.2f}€ &nbsp;(<b style="color:green">-{d['decote_pct']}%</b>)<br>
        <b>Prix de revente conseillé :</b> {d['prix_revente_conseille']:.2f}€<br>
        <b>Profit net estimé :</b> <b style="color:green">+{d['profit_net_estime']:.2f}€</b>
      </p>
      <a href="{d['url']}" style="display:inline-block;background:#1a73e8;color:#fff;
         padding:8px 16px;border-radius:6px;text-decoration:none">Voir l'annonce ➜</a>
    </div>"""


def envoyer_alertes(deals: list[dict], cfg_email: dict, mot_de_passe: str) -> bool:
    if not deals:
        return True
    if not mot_de_passe:
        log.error("GMAIL_APP_PASSWORD manquant : impossible d'envoyer le mail")
        return False

    corps = "".join(_html_deal(d) for d in deals)
    html = f"""<html><body style="font-family:Arial">
      <h2>💰 PokéDeals — {len(deals)} affaire(s) détectée(s)</h2>
      {corps}
      <p style="color:#888;font-size:12px">Vérifie toujours les photos et la description
      avant d'acheter : le bot ne voit que le texte de l'annonce.</p>
    </body></html>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🔥 PokéDeals : {len(deals)} bonne(s) affaire(s) !"
    msg["From"] = cfg_email["expediteur"]
    msg["To"] = cfg_email["destinataire"]
    msg.attach(MIMEText(html, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as srv:
            srv.login(cfg_email["expediteur"], mot_de_passe)
            srv.send_message(msg)
        log.info("Email envoyé (%d deals)", len(deals))
        return True
    except Exception as e:  # noqa: BLE001
        log.error("Échec de l'envoi du mail : %s", e)
        return False
