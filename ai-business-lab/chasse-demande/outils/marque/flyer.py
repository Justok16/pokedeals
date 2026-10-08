#!/usr/bin/env python3
"""Flyer A5 de DIG16, charte premium du 08/10/2026 (noir chaud, laiton, Instrument Serif, Geist).

Usage : python3 outils/marque/flyer.py
Écrit supports/flyer-dig-a5.html, puis supports/Dig-Flyer-A5.png (300 ppp, 1748 × 2480 px)
et supports/Dig-Flyer-A5.pdf (A5 exact, fait à partir de l'image : rendu identique dans toutes
les visionneuses, leçon du 28/09). Contrôles : QR décodé depuis le PNG, rien ne déborde du cadre.
Les champs entre crochets se remplissent à l'immatriculation (aucune donnée personnelle ici).
"""

import os
import sys

import cv2
import numpy as np
import segno
from PIL import Image
from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, "..", ".."))
SUP = os.path.join(RACINE, "supports")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
LIEN = "https://dig16.fr/"


def qr_svg():
    q = segno.make(LIEN, error="q")
    chemin = q.svg_inline(scale=1, border=0, dark="#14110d", omitsize=True)
    return chemin


HTML = """<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Flyer DIG16 A5</title>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=block" rel="stylesheet">
<style>
@page{size:148mm 210mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
:root{--nuit:#0f0e0c;--nuit2:#181613;--ivoire:#efe9df;--doux:#a8a093;--or:#c8a46e;--or-clair:#d9bb8a;--encre:#14110d;--papier:#f3eee5;--bronze:#7a5a2c;--ligne:rgba(26,24,20,.13);--gris:#655e54}
body{font-family:Geist,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact;background:var(--papier)}
.page{width:148mm;height:210mm;position:relative;overflow:hidden;color:var(--encre);
 background:radial-gradient(100mm 80mm at 120mm 18mm,rgba(200,164,110,.30),rgba(200,164,110,0) 70%),
  radial-gradient(90mm 80mm at 6mm 135mm,rgba(200,164,110,.16),rgba(200,164,110,0) 70%),
  linear-gradient(180deg,#f8f4ec 0%,#f3eee5 55%,#ede6d9 100%)}
.grain{position:absolute;inset:0;opacity:.05;mix-blend-mode:multiply;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
.filet{position:absolute;inset:5mm;border:.3mm solid rgba(122,90,44,.38);border-radius:3mm;pointer-events:none}
.corps{position:absolute;inset:11mm 11mm 7.5mm;display:flex;flex-direction:column;justify-content:space-between}
.haut{margin-bottom:3mm;display:flex;justify-content:space-between;align-items:center}
.haut img{height:13.5mm;display:block}
.pastille{font-family:'Geist Mono',monospace;font-size:6.2pt;letter-spacing:.16em;text-transform:uppercase;color:var(--encre);background:rgba(255,253,249,.7);border:.25mm solid rgba(122,90,44,.35);border-radius:10mm;padding:1.6mm 3mm;display:flex;align-items:center;gap:1.8mm}
.pastille i{width:1.6mm;height:1.6mm;border-radius:50%;background:var(--bronze);display:block}
.k{font-family:'Geist Mono',monospace;font-size:6.4pt;letter-spacing:.2em;text-transform:uppercase;color:var(--bronze);display:flex;align-items:center;gap:2.5mm}
.k::before{content:"";width:8mm;height:.3mm;background:var(--bronze)}
h1{font-family:'Instrument Serif',serif;font-weight:400;font-size:29pt;line-height:.98;letter-spacing:-.01em;margin-top:3.2mm}
h1 em{color:var(--bronze)}
.sous{margin-top:3.2mm;font-size:9.2pt;line-height:1.48;color:var(--gris);font-weight:400;text-wrap:balance}
.sous b{color:var(--encre);font-weight:600}
.milieu{position:relative;display:grid;grid-template-columns:47mm 1fr;gap:6mm}
.tel{position:absolute;left:2mm;top:1mm;width:38mm;height:80mm;border-radius:6mm;background:#060605;padding:1.4mm;transform:rotate(-4deg);z-index:1;
 box-shadow:0 0 0 .35mm #3a342b,0 0 0 .7mm #0a0908,0 8mm 16mm rgba(70,48,18,.38)}
.tel img{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:4.8mm;display:block}
.notif{position:absolute;left:0;top:33mm;z-index:2;background:var(--encre);color:var(--ivoire);border-radius:2.8mm;padding:2mm 2.8mm 2mm 2.2mm;display:flex;gap:2mm;align-items:center;box-shadow:0 3mm 8mm rgba(40,28,10,.4),0 0 0 .25mm rgba(200,164,110,.5);white-space:nowrap}
.notif .ic{width:6mm;height:6mm;border-radius:1.7mm;background:rgba(200,164,110,.16);display:grid;place-items:center}
.notif b{display:block;font-size:6.8pt;font-weight:600;line-height:1.15}
.notif span{display:block;font-size:5.8pt;color:var(--doux);line-height:1.2}
.avantages{grid-column:2}
.av{display:grid;grid-template-columns:7mm 1fr;padding:2.3mm 0 2.4mm;border-top:.25mm solid var(--ligne)}
.av:last-child{border-bottom:.25mm solid var(--ligne)}
.av .n{font-family:'Geist Mono',monospace;font-size:6.4pt;color:var(--bronze);padding-top:1mm}
.av b{display:block;font-family:'Instrument Serif',serif;font-weight:400;font-size:12.6pt;line-height:1.08}
.av span{display:block;font-size:7pt;line-height:1.36;color:var(--gris);margin-top:.5mm;font-weight:400}
.offre{position:relative;z-index:3;margin:0 -2mm;background:#fffdf9;color:var(--encre);border:.3mm solid rgba(200,164,110,.6);border-radius:3.5mm;padding:4.6mm 5mm 4.4mm 6mm;display:grid;grid-template-columns:1fr 30mm;gap:5mm;box-shadow:0 -1mm 8mm rgba(80,55,20,.10),0 5mm 14mm rgba(80,55,20,.18)}
.offre .k{color:var(--bronze)}.offre .k::before{background:var(--bronze)}
.offre h2{font-family:'Instrument Serif',serif;font-weight:400;font-size:16pt;line-height:1.02;margin-top:2mm;letter-spacing:-.005em}
.offre h2 em{color:var(--bronze)}
.prix{display:flex;align-items:baseline;gap:1.6mm;margin-top:2mm}
.prix small{font-size:7.8pt;color:#655e54}
.prix b{font-family:'Instrument Serif',serif;font-weight:400;font-size:22pt;line-height:1}
.puces{display:flex;gap:1.5mm;margin-top:1.8mm;flex-wrap:wrap}
.puces span{font-size:6.4pt;font-weight:500;border:.25mm solid #d8cfbf;border-radius:10mm;padding:.9mm 2.3mm;white-space:nowrap}
.contact{margin-top:2.4mm;font-size:7.1pt;line-height:1.45;color:#3d3830}
.contact b{font-weight:600;color:var(--encre)}
.qr{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2mm}
.qr .cadre{width:30mm;height:30mm;background:#fbf8f2;border:.25mm solid #d8cfbf;border-radius:2.5mm;padding:2.5mm}
.qr svg{width:100%;height:100%;display:block}
.qr p{font-family:'Geist Mono',monospace;font-size:6pt;letter-spacing:.18em;text-transform:uppercase;color:var(--bronze);text-align:center;line-height:1.5}
.legal{font-size:5.2pt;line-height:1.42;color:#8c8478;text-align:center;margin-top:3mm}
</style></head><body>
<section class="page"><div class="grain"></div><div class="filet"></div>
<div class="corps">
<div class="haut"><img src="../site-dig/img/marque/signature-encre@6x.png" alt="DIG16, sites internet"><div class="pastille"><i></i>Fait près de chez vous</div></div>
<div class="titre">
 <div class="k">Artisans · commerçants · indépendants</div>
 <h1>Vos clients vous cherchent<br>sur leur téléphone.<br><em>Ils vous trouvent&#8239;?</em></h1>
 <p class="sous"><b>Un site moderne, rapide, qui vous appartient.</b> Fait près de chez vous, sans contrat qui vous enferme.</p>
</div>
<div class="milieu">
<div class="tel"><img src="../site-dig/img/vitrine-essentiel-tel.webp" alt="Exemple de site d’artisan sur téléphone"></div>
<div class="notif"><div class="ic"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#c8a46e" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg></div><div><b>Nouvelle demande de devis</b><span>depuis votre site · à l’instant</span></div></div>
<div class="avantages">
 <div class="av"><div class="n">01</div><div><b>Facile à appeler</b><span>Pensé d’abord pour le téléphone.</span></div></div>
 <div class="av"><div class="n">02</div><div><b>Votre site vous appartient</b><span>Site et nom de domaine à votre nom.</span></div></div>
 <div class="av"><div class="n">03</div><div><b>En ligne en 7 jours</b><span>20 minutes ensemble, je m’occupe du reste.</span></div></div>
 <div class="av"><div class="n">04</div><div><b>Suivi chaque mois</b><span>Modifications sous 3 jours ouvrés, bilan mensuel.</span></div></div>
</div>
</div>
<div class="offre">
 <div>
  <div class="k">Offre découverte</div>
  <h2>Votre page d’accueil refaite <em>gratuitement</em>, avant de décider.</h2>
  <div class="prix"><small>dès</small><b>49&nbsp;€</b><small>/ mois</small></div>
  <div class="puces"><span>0 € de création</span><span>6 mois, puis sans engagement</span></div>
  <p class="contact"><b>[Téléphone] · contact@dig16.fr</b><br>Appelez ou scannez : la démo est gratuite.<br>Recommandé par un client ? Premier mois offert.</p>
 </div>
 <div class="qr"><div class="cadre">{QR}</div><p>Scannez-moi<br>dig16.fr</p></div>
</div>
<p class="legal">DIG16 — [Prénom Nom], entrepreneur individuel (EI) — SIREN [à compléter] — [adresse]. TVA non applicable, art. 293 B du CGI. Offre « Essentiel » : site 5 pages, hébergement, 1 modification par mois ; engagement minimal 6 mois ; premier mois réglé avant la mise en ligne ; nom de domaine à la charge du client. Démo sans obligation d’achat. Visuel d’illustration. Ne pas jeter sur la voie publique.</p>
</div>
</section></body></html>"""

CONTROLE = """() => {
  const P = document.querySelector('.page').getBoundingClientRect();
  const C = document.querySelector('.corps');
  const marge = 5 * 96 / 25.4;  // 5 mm : zone de sécurité de l'imprimeur
  const fautes = [];
  if (C.scrollHeight > C.clientHeight + 1) fautes.push('contenu trop haut de ' + (C.scrollHeight - C.clientHeight) + ' px');
  const r = s => document.querySelector(s).getBoundingClientRect();
  for (const s of ['.haut', 'h1', '.sous', '.tel', '.notif', '.avantages', '.offre', '.legal']) {
    const b = r(s);
    if (b.left < P.left + marge || b.right > P.right - marge || b.top < P.top + marge || b.bottom > P.bottom - marge) fautes.push('hors zone de sécurité : ' + s);
  }
  const touche = (A, B) => A.left < B.right && B.left < A.right && A.top < B.bottom && B.top < A.bottom;
  const paires = [['.sous', '.tel'], ['.sous', '.avantages'], ['.tel', '.avantages'], ['.notif', '.avantages'], ['.avantages', '.offre'], ['.offre', '.legal'], ['.notif', '.offre']];
  for (const [a, b] of paires) if (touche(r(a), r(b))) fautes.push('chevauchement ' + a + ' / ' + b);
  for (const el of document.querySelectorAll('.offre *, .av *, .notif *'))
    if (el.scrollWidth > el.clientWidth + 1 && getComputedStyle(el).overflow !== 'visible') fautes.push('texte coupé : ' + el.textContent.slice(0, 30));
  const fonts = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family);
  return {fautes, fonts: [...new Set(fonts)], bas_tel: Math.round(r('.tel').bottom - r('.offre').top)};
}"""


def main():
    html_path = os.path.join(SUP, "flyer-dig-a5.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML.replace("{QR}", qr_svg()))
    png = os.path.join(SUP, "Dig-Flyer-A5.png")
    pdf = os.path.join(SUP, "Dig-Flyer-A5.pdf")
    largeur = 148 * 96 / 25.4
    hauteur = 210 * 96 / 25.4
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME)
        pg = nav.new_page(viewport={"width": round(largeur), "height": round(hauteur)}, device_scale_factor=1748 / largeur)
        pg.goto("file://" + html_path)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(800)
        res = pg.evaluate(CONTROLE)
        pg.locator(".page").screenshot(path=png)
        nav.close()
    print("Téléphone glissé sous l'offre de", res["bas_tel"], "px (voulu : > 0)")
    for f in res["fautes"]:
        print("ALERTE", f)
    manque = {"Instrument Serif", "Geist", "Geist Mono"} - set(res["fonts"])
    if manque:
        print("ALERTE polices non chargées :", manque)
    im = Image.open(png).convert("RGB")
    if im.size != (1748, 2480):
        im = im.resize((1748, 2480), Image.LANCZOS)
    im.save(png, dpi=(300, 300))
    im.save(pdf, "PDF", resolution=300.0)
    lu = cv2.QRCodeDetector().detectAndDecode(cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR))[0]
    petit = im.resize((583, 827), Image.LANCZOS)  # 100 ppp
    lu2 = cv2.QRCodeDetector().detectAndDecode(cv2.cvtColor(np.array(petit), cv2.COLOR_RGB2BGR))[0]
    print("QR (300 ppp) ->", lu, "| QR (100 ppp) ->", lu2)
    ok = lu == LIEN and not res["fautes"] and not manque
    print("Flyer prêt :" if ok else "ALERTE flyer :", png, pdf)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
