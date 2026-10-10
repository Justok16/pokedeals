#!/usr/bin/env python3
"""Signature des emails DIG16 (08/10/2026), à la charte (60-charte-dig16.md) et aux règles du démarchage B2B :
expéditeur identifiable (nom, EI, SIREN, téléphone, adresse du site), désinscription simple (35-demarchage-cadre-legal.md).

Usage : python3 outils/marque/signature_email.py
  écrit supports/signature-email.html (champs entre crochets, version publique) et son aperçu PNG.
La version remplie n'est jamais écrite dans le dépôt : Claude la remplit à l'immatriculation et la remet à
l'utilisateur (document privé du Drive « Dig »). Signature riche : Gmail sur ordinateur (Paramètres > Signature,
coller le rendu de la page) ; signature texte : application Gmail du téléphone (TEXTE ci-dessous).
Compatibilité des messageries : tableau et styles en ligne, polices de secours (Georgia, Arial), logo hébergé
sur dig16.fr (vérifié en ligne le 08/10), aucune image indispensable à la lecture.
"""

import os

from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, "..", ".."))
SUP = os.path.join(RACINE, "supports")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
LOGO = "https://dig16.fr/img/marque/signature-encre@2x.png"

SIGNATURE = f"""<table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;font-family:Arial,Helvetica,sans-serif;color:#1a1814">
<tr><td style="padding:0 18px 0 0;border-right:2px solid #c8a46e;vertical-align:top">
<a href="https://dig16.fr/" style="text-decoration:none"><img src="{LOGO}" width="96" alt="DIG16" style="display:block;border:0;width:96px;height:auto"></a></td>
<td style="padding:0 0 0 18px;vertical-align:top">
<div style="font-family:Georgia,'Times New Roman',serif;font-size:19px;line-height:1.2;color:#1a1814">[Prénom Nom]</div>
<div style="font-size:13px;line-height:1.5;color:#7a5a2c;margin-top:2px">DIG16, sites internet pour artisans et commerçants de Charente</div>
<div style="font-size:13px;line-height:1.6;margin-top:8px"><a href="tel:[TELEPHONE]" style="color:#1a1814;text-decoration:none">[Téléphone]</a>
&nbsp;|&nbsp; <a href="https://dig16.fr/" style="color:#1a1814;text-decoration:none;font-weight:bold">dig16.fr</a></div>
<div style="font-size:12px;line-height:1.5;color:#655e54;margin-top:8px">Le test du pouce : tapez votre métier et votre ville sur votre téléphone. Vous êtes où&nbsp;?</div>
<div style="font-size:11px;line-height:1.5;color:#8a8278;margin-top:8px">[Prénom Nom] EI, SIREN [numéro à l’immatriculation], [adresse]<br>
Vous ne souhaitez plus recevoir de message de ma part&nbsp;? Répondez simplement « STOP ».</div></td></tr></table>"""

TEXTE = """--
[Prénom Nom]
DIG16, sites internet pour artisans et commerçants de Charente
[Téléphone] | dig16.fr
[Prénom Nom] EI, SIREN [numéro à l’immatriculation], [adresse]
Répondez « STOP » pour ne plus recevoir de message."""

PAGE = """<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Signature email DIG16</title></head>
<body style="margin:0;padding:32px;background:#fff;font-family:Arial,sans-serif">
<p style="font:13px Arial;color:#655e54;margin:0 0 20px">Gmail sur ordinateur : sélectionner la signature ci-dessous, copier,
puis Paramètres &gt; Voir tous les paramètres &gt; Signature &gt; coller. Application du téléphone : texte en bas.</p>
<div id="sig">""" + SIGNATURE + """</div>
<pre style="margin-top:32px;font:13px/1.5 Arial;color:#1a1814;background:#f3eee5;padding:16px;border-radius:8px">""" + TEXTE + """</pre>
</body></html>"""


def main():
    html = os.path.join(SUP, "signature-email.html")
    with open(html, "w", encoding="utf-8") as f:
        f.write(PAGE)
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME)
        pg = nav.new_page(viewport={"width": 760, "height": 400}, device_scale_factor=2)
        pg.goto("file://" + html, wait_until="networkidle")
        ok = pg.evaluate("[...document.images].every(i=>i.complete&&i.naturalWidth>0)")
        pg.locator("#sig").screenshot(path=os.path.join(SUP, "signature-email.png"))
        nav.close()
    print("signature-email.html et .png", "" if ok else "| ALERTE logo non chargé depuis dig16.fr")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
