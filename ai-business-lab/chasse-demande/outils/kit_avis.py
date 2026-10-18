#!/usr/bin/env python3
"""Kit « avis Google » (18/10/2026) : carte A6 avec QR code vers la page « Laisser un avis » d'une fiche Google,
plus les messages prêts à envoyer (SMS, email) et le texte des réponses aux avis. Même kit pour DIG16 et pour
chaque client (offre Visibilité : « demandes d'avis clients »).

Usage : python3 outils/kit_avis.py "<Nom affiché>" <place_id Google> <dossier_sortie> [--metier "menuisier"]
Le place_id se lit dans la fiche publique (outil OpenSEO get_business_profile, champ place_id) ; le lien
https://search.google.com/local/writereview?placeid=<place_id> ouvre directement la fenêtre d'avis.

Contrôles intégrés (44-controle-qualite.md) : QR décodé sur l'image finale (OpenCV), lien testé en ligne,
carte rendue à 300 ppp (1240 × 1748 px, A6) avec les polices du site.
Règles : jamais d'avis rédigé, acheté ou récompensé ; jamais de tri des clients « contents » seulement
(règles Google sur les contenus, lues le 18/10/2026).
"""

import argparse
import base64
import io
import pathlib
import sys
import urllib.request

import segno

RACINE = pathlib.Path(__file__).resolve().parents[1]
POLICES = RACINE / "site-dig" / "moteur" / "polices"

CARTE = """<!doctype html><html lang="fr"><head><meta charset="utf-8">
<style>{css}</style>
<style>
html,body{{margin:0;background:#0f0e0c}}
body{{width:1240px;height:1748px;font-family:Geist,'Geist Fallback',system-ui,sans-serif;color:#efe9df;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:120px 100px 110px;box-sizing:border-box;text-align:center}}
h1{{font-family:'Instrument Serif','Instrument Serif Fallback',Georgia,serif;font-weight:400;font-size:112px;line-height:1.02;margin:0;letter-spacing:-.012em}}
h1 em{{font-style:italic;color:#c8a46e}}
.nom{{font-family:'Geist Mono','Geist Mono Fallback',ui-monospace,monospace;font-size:34px;letter-spacing:.24em;text-transform:uppercase;color:#a8a093;margin-top:34px}}
.qr{{background:#fff;padding:44px;border-radius:40px;box-shadow:0 0 0 3px rgba(200,164,110,.6)}}
.qr img{{display:block;width:620px;height:620px}}
.mode{{font-size:40px;line-height:1.35;color:#efe9df;max-width:980px}}
.mode b{{color:#c8a46e;font-weight:600}}
.merci{{font-family:'Instrument Serif','Instrument Serif Fallback',Georgia,serif;font-size:58px;color:#c8a46e;margin:0}}
.pied{{font-size:28px;color:#a8a093;letter-spacing:.04em}}
</style></head><body>
<div><h1>Votre avis<br><em>compte vraiment.</em></h1><div class="nom">{nom}</div></div>
<div class="qr"><img src="{qr}" alt=""></div>
<div><p class="mode">Scannez avec l’appareil photo du téléphone, <b>30 secondes</b> suffisent. Un avis sincère, même court, aide {qui} à être trouvé par d’autres.</p></div>
<div><p class="merci">Merci.</p><p class="pied">{pied}</p></div>
</body></html>"""

SMS = """Bonjour {prenom}, merci pour votre confiance. Si vous avez 30 secondes, un avis sur notre fiche Google nous aide beaucoup à être trouvés par d'autres clients : {lien_court}
Bonne journée, {signature}"""

EMAIL = """Objet : Un petit mot sur votre expérience avec {nom} ?

Bonjour {prenom},

Merci encore pour votre confiance. Si vous êtes satisfait du travail, votre avis sur notre fiche Google nous aide vraiment à être trouvés par d'autres personnes de la région. Ça prend 30 secondes :

{lien}

Et si quelque chose ne vous a pas plu, dites-le-nous directement en répondant à ce message : nous préférons le savoir et le corriger.

{signature}"""

REPONSES = """## Répondre à chaque avis (dans les 48 h)

Avis positif :
« Merci <prénom> pour ce retour, ça fait vraiment plaisir. Au plaisir de travailler à nouveau avec vous. »

Avis mitigé ou négatif (toujours calme, jamais d'excuse publique sur un détail privé) :
« Merci d'avoir pris le temps d'écrire. Je suis désolé que cela n'ait pas été à la hauteur. Je vous appelle (ou : écrivez-moi à <email>) pour comprendre et trouver une solution. »

Jamais : répondre à chaud, contester publiquement, demander de retirer l'avis, proposer un geste en échange.
"""


def lien_ok(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


def qr_data_uri(url):
    buf = io.BytesIO()
    segno.make(url, error="h").save(buf, kind="png", scale=16, border=0, dark="#14110d")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def css_polices():
    """Feuille des polices du site avec les fichiers incorporés (le CSS cite /moteur/polices/… : hors du site,
    ces chemins ne mènent nulle part et la carte tomberait sur la police de secours)."""
    import re

    css = (POLICES / "instrumentserif-geist-geistmono.css").read_text(encoding="utf-8")

    def inc(m):
        data = base64.b64encode((POLICES / m.group(1)).read_bytes()).decode()
        return f"url(data:font/woff2;base64,{data})"

    return re.sub(r"url\(/moteur/polices/([^)]+)\)", inc, css)


def rendre(html, sortie):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = b.new_page(viewport={"width": 1240, "height": 1748}, device_scale_factor=1)
        pg.set_content(html, wait_until="load")
        pg.wait_for_timeout(800)  # polices
        pg.screenshot(path=str(sortie), full_page=False)
        b.close()


def decoder_qr(image):
    import cv2

    img = cv2.imread(str(image))
    texte, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
    return texte


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nom")
    ap.add_argument("place_id")
    ap.add_argument("sortie")
    ap.add_argument("--metier", default="")
    ap.add_argument("--signature", default="")
    a = ap.parse_args()
    out = pathlib.Path(a.sortie)
    out.mkdir(parents=True, exist_ok=True)
    lien = f"https://search.google.com/local/writereview?placeid={a.place_id}"
    code = lien_ok(lien)
    if code not in (200, 302, 303):
        sys.exit(f"Lien d'avis injoignable ({code}) : {lien}")
    qui = f"{a.nom}" if not a.metier else f"votre {a.metier}"
    html = CARTE.format(css=css_polices(), nom=a.nom, qr=qr_data_uri(lien), qui=qui, pied="Fiche Google · avis sincères uniquement")
    png = out / "carte-avis-A6-300ppp.png"
    rendre(html, png)
    lu = decoder_qr(png)
    if lu != lien:
        sys.exit(f"QR illisible ou faux : {lu!r}")
    sig = a.signature or a.nom
    (out / "messages-avis.md").write_text(
        f"# Kit avis Google — {a.nom}\n\nLien direct : {lien}\n(code HTTP {code} le jour de la génération ; Google demande une connexion au compte Google du client, c'est normal)\n\n"
        f"## SMS (après un chantier ou une commande livrée)\n\n{SMS.format(prenom='<prénom>', lien_court=lien, signature=sig)}\n\n"
        f"## Email\n\n{EMAIL.format(prenom='<prénom>', nom=a.nom, lien=lien, signature=sig)}\n\n{REPONSES}",
        encoding="utf-8",
    )
    print(f"ok : {png} (QR décodé = lien), {out/'messages-avis.md'}")


if __name__ == "__main__":
    main()
