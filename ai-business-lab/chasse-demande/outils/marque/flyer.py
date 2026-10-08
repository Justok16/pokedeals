#!/usr/bin/env python3
"""Flyer A5 de DIG16, charte premium du 08/10/2026, version claire et accessible (textes de 10 pt minimum,
contrastes AA contrôlés).

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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import identite  # noqa: E402

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
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600;700&display=block" rel="stylesheet">
<style>
/* Version « accessible à tous » (08/10/2026) : textes de 10 pt minimum (mentions légales 6,5 pt),
   contrastes AA vérifiés par le script, pas de petites capitales espacées, phrases courtes. */
@page{size:148mm 210mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
:root{--encre:#1a1712;--texte:#2e2a24;--bronze:#6e5025;--or:#c8a46e;--ivoire:#efe9df;--doux:#cfc6b8;--papier:#f3eee5;--ligne:rgba(26,24,20,.16)}
body{font-family:Geist,Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact;background:var(--papier)}
.page{width:148mm;height:210mm;position:relative;overflow:hidden;color:var(--encre);
 background:radial-gradient(100mm 80mm at 120mm 18mm,rgba(200,164,110,.28),rgba(200,164,110,0) 70%),
  radial-gradient(90mm 80mm at 6mm 135mm,rgba(200,164,110,.14),rgba(200,164,110,0) 70%),
  linear-gradient(180deg,#f8f4ec 0%,#f3eee5 55%,#ede6d9 100%)}
.filet{position:absolute;inset:5mm;border:.3mm solid rgba(110,80,37,.4);border-radius:3mm}
.corps{position:absolute;inset:10mm 10mm 7.5mm;display:flex;flex-direction:column;justify-content:space-between}
.haut{display:flex;justify-content:space-between;align-items:center}
.haut img{height:14mm;display:block}
.pastille{font-size:10pt;font-weight:600;color:var(--encre);background:#fffdf9;border:.3mm solid rgba(110,80,37,.45);border-radius:10mm;padding:1.8mm 3.6mm;display:flex;align-items:center;gap:2mm}
.pastille i{width:2.2mm;height:2.2mm;border-radius:50%;background:var(--bronze);display:block}
h1{font-family:'Instrument Serif',Georgia,serif;font-weight:400;font-size:29pt;line-height:1;letter-spacing:-.005em}
.titre{margin-top:2.5mm}
h1 em{color:var(--bronze)}
.sous{margin-top:2.6mm;font-size:12.5pt;line-height:1.3;color:var(--texte);font-weight:600}
.milieu{position:relative;display:grid;grid-template-columns:40mm 1fr;gap:5mm}
.tel{position:absolute;left:1mm;top:3mm;width:35mm;height:74mm;border-radius:5.6mm;background:#060605;padding:1.3mm;transform:rotate(-4deg);z-index:1;
 box-shadow:0 0 0 .35mm #3a342b,0 0 0 .7mm #0a0908,0 8mm 16mm rgba(70,48,18,.38)}
.tel img{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:4.4mm;display:block}
.notif{position:absolute;left:-1mm;top:30mm;z-index:2;background:var(--encre);color:#fff;border-radius:2.8mm;padding:2.2mm 3mm;box-shadow:0 3mm 8mm rgba(40,28,10,.4),0 0 0 .3mm var(--or);font-size:10pt;font-weight:600;line-height:1.2;width:39mm}
.notif span{display:block;color:var(--or);font-size:10pt;font-weight:600}
.avantages{grid-column:2}
.av{display:grid;grid-template-columns:8mm 1fr;align-items:baseline;padding:1.7mm 0 1.8mm;border-top:.3mm solid var(--ligne)}
.av:last-child{border-bottom:.3mm solid var(--ligne)}
.av .n{font-size:11pt;font-weight:700;color:var(--bronze)}
.av b{display:block;font-size:13pt;font-weight:700;line-height:1.15;color:var(--encre)}
.av span{display:block;font-size:10.5pt;line-height:1.3;color:var(--texte);margin-top:.6mm}
.offre{position:relative;z-index:3;margin:0 -1.5mm;background:#fffdf9;color:var(--encre);border:.4mm solid rgba(200,164,110,.8);border-radius:3.5mm;padding:4mm 4.5mm 4mm 5mm;display:grid;grid-template-columns:1fr 34mm;gap:4mm;box-shadow:0 -1mm 8mm rgba(80,55,20,.10),0 5mm 14mm rgba(80,55,20,.18)}
.offre .k{font-size:10pt;font-weight:700;color:var(--bronze)}
.offre h2{font-family:'Instrument Serif',Georgia,serif;font-weight:400;font-size:18.5pt;line-height:1.02;margin-top:1mm}
.offre h2 em{color:var(--bronze)}
.prix{display:flex;align-items:baseline;gap:1.6mm;margin-top:1.6mm}
.prix small{font-size:12pt;color:var(--texte);font-weight:500}
.prix b{font-family:'Instrument Serif',Georgia,serif;font-weight:400;font-size:27pt;line-height:1}
.puces{margin-top:1.4mm;font-size:10.5pt;font-weight:600;line-height:1.35;color:var(--encre)}
.puces span{display:block}
.puces span::before{content:"✓ ";color:var(--bronze)}
.contact{margin-top:2mm;font-size:10.5pt;line-height:1.35;color:var(--texte)}
.contact b{display:block;font-size:12pt;font-weight:700;color:var(--encre)}
.qr{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1.8mm}
.qr .cadre{width:34mm;height:34mm;background:#fff;border:.3mm solid #cfc4b2;border-radius:2.5mm;padding:2.6mm}
.qr svg{width:100%;height:100%;display:block}
.qr p{font-size:10.5pt;font-weight:700;color:var(--encre);text-align:center;line-height:1.25}
.qr p span{display:block;font-weight:600;color:var(--bronze)}
.legal{font-size:6.5pt;line-height:1.38;color:#4a443b;text-align:center;margin-top:2.6mm}
</style></head><body>
<section class="page"><div class="filet"></div>
<div class="corps">
<div class="haut"><img src="../site-dig/img/marque/signature-encre@6x.png" alt="DIG16, sites internet, Charente"><div class="pastille"><i></i>Fait près de chez vous</div></div>
<div class="titre">
 <h1>Vos clients vous cherchent<br>sur leur téléphone.<br><em>Ils vous trouvent&#8239;?</em></h1>
 <p class="sous">Un site moderne, rapide, qui vous appartient.</p>
</div>
<div class="milieu">
<div class="tel"><img src="../site-dig/img/vitrine-essentiel-tel.webp" alt="Exemple de site d’artisan sur téléphone"></div>
<div class="notif">Nouvelle demande de devis<span>depuis votre site</span></div>
<div class="avantages">
 <div class="av"><div class="n">1</div><div><b>Facile à appeler</b><span>Pensé pour le téléphone.</span></div></div>
 <div class="av"><div class="n">2</div><div><b>Votre site est à vous</b><span>Site et nom de domaine à votre nom.</span></div></div>
 <div class="av"><div class="n">3</div><div><b>En ligne en 7 jours</b><span>20 minutes ensemble, je fais le reste.</span></div></div>
 <div class="av"><div class="n">4</div><div><b>Suivi chaque mois</b><span>Changements faits en 3 jours ouvrés.</span></div></div>
</div>
</div>
<div class="offre">
 <div>
  <div class="k">Offre découverte</div>
  <h2>Votre page d’accueil refaite <em>gratuitement</em>, avant de décider.</h2>
  <div class="prix"><small>dès</small><b>49&nbsp;€</b><small>par mois</small></div>
  <div class="puces"><span>0 € de création</span><span>6 mois, puis sans engagement</span></div>
  <p class="contact"><b>[Téléphone] · contact@dig16.fr</b>Recommandé par un client ? Premier mois offert.</p>
 </div>
 <div class="qr"><div class="cadre">{QR}</div><p>Scannez-moi<span>dig16.fr</span></p></div>
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
  // Accessibilité : taille minimale et contraste (WCAG AA : 4,5:1, ou 3:1 au-delà de 18 pt / 14 pt gras)
  const lum = c => { const v = c.match(/[\\d.]+/g).slice(0, 3).map(x => { x = x / 255; return x <= .03928 ? x / 12.92 : Math.pow((x + .055) / 1.055, 2.4); }); return .2126 * v[0] + .7152 * v[1] + .0722 * v[2]; };
  const fond = el => { for (let e = el; e; e = e.parentElement) { const b = getComputedStyle(e).backgroundColor; const a = b.match(/[\\d.]+/g); if (a && (a.length < 4 || +a[3] > .9)) return b; if (e.classList.contains('page')) return 'rgb(243,238,229)'; } return 'rgb(243,238,229)'; };
  let mini = 99, pire = 99;
  for (const el of document.querySelectorAll('.corps *')) {
    const t = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).length;
    if (!t) continue;
    const cs = getComputedStyle(el), pt = parseFloat(cs.fontSize) * .75, gras = +cs.fontWeight >= 700;
    const legal = !!el.closest('.legal');
    if (!legal) mini = Math.min(mini, pt);
    if (pt < (legal ? 6.45 : 9.95)) fautes.push('texte trop petit (' + pt.toFixed(1) + ' pt) : ' + el.textContent.trim().slice(0, 30));
    const L1 = lum(cs.color), L2 = lum(fond(el)), ratio = (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05);
    pire = Math.min(pire, ratio);
    const seuil = (pt >= 18 || (pt >= 14 && gras)) ? 3 : 4.5;
    if (ratio < seuil) fautes.push('contraste ' + ratio.toFixed(2) + ' : ' + el.textContent.trim().slice(0, 30));
  }
  const fonts = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family);
  return {fautes, fonts: [...new Set(fonts)], bas_tel: Math.round(r('.tel').bottom - r('.offre').top), mini: mini.toFixed(1), pire: pire.toFixed(2)};
}"""


def main():
    ident = identite.charger()  # version remplie : fichiers dans DIG16_SORTIE, jamais dans supports/
    html_path = os.path.join(SUP, "flyer-dig-a5-prive.html" if ident else "flyer-dig-a5.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(identite.remplir(HTML.replace("{QR}", qr_svg()), ident))
    png = os.path.join(identite.sortie(SUP), "Dig-Flyer-A5.png")
    pdf = os.path.join(identite.sortie(SUP), "Dig-Flyer-A5.pdf")
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
    if ident:
        os.remove(html_path)
    print("Téléphone glissé sous l'offre de", res["bas_tel"], "px (voulu : > 0) ; plus petit texte hors mentions :", res["mini"], "pt ; pire contraste :", res["pire"])
    for f in res["fautes"]:
        print("ALERTE", f)
    manque = {"Instrument Serif", "Geist"} - set(res["fonts"])
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
