#!/usr/bin/env python3
"""Visuels des profils DIG16 sur les réseaux (08/10/2026), à la charte premium (60-charte-dig16.md).

Usage : python3 outils/marque/visuels_reseaux.py
Écrit dans supports/reseaux/ :
  avatar-1080.png         photo de profil (Facebook, Instagram, LinkedIn, Google, YouTube, TikTok), rognée en rond :
                          l'emblème reste dans le cercle central ;
  couverture-facebook.png 1640 × 624 (zone utile centrale, le texte évite les bords) ;
  banniere-linkedin.png   1584 × 396 ;
  couverture-google.png   1080 × 608 ;
  banniere-youtube.png    2560 × 1440 (texte dans la zone sûre centrale 1546 × 423).
Contrôles : polices chargées, aucun texte hors de sa zone sûre.
"""

import os

from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, "..", ".."))
SORTIE = os.path.join(RACINE, "supports", "reseaux")
MARQUE = "file://" + os.path.join(RACINE, "site-dig", "img", "marque") + "/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
POLICES = ('<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1'
           '&family=Geist:wght@400;500&family=Geist+Mono&display=block" rel="stylesheet">')

FOND = ("background:#0f0e0c;background-image:radial-gradient(60% 90% at 85% 10%,rgba(200,164,110,.20),"
        "rgba(200,164,110,0) 70%),radial-gradient(50% 70% at 0% 100%,rgba(200,164,110,.10),rgba(200,164,110,0) 70%);")

# nom, largeur, hauteur, zone sûre (largeur, hauteur) centrée, contenu
FORMATS = [
    ("couverture-facebook.png", 1640, 624, (1300, 480), "bandeau"),
    ("banniere-linkedin.png", 1584, 396, (1150, 300), "bandeau"),
    ("couverture-google.png", 1080, 608, (960, 500), "bandeau"),
    ("banniere-youtube.png", 2560, 1440, (1546, 423), "bandeau"),
    ("avatar-1080.png", 1080, 1080, (860, 860), "avatar"),
]


def page(larg, h, zone, genre):
    zl, zh = zone
    if genre == "avatar":
        corps = f'<img id="z" src="{MARQUE}embleme-or@6x.png" style="width:{zl * 0.82}px;height:auto">'
    else:
        t = min(zh / 300, zl / 1150)  # échelle du texte selon la zone sûre
        corps = (f'<div id="z" style="display:flex;align-items:center;gap:{48 * t}px;max-width:{zl}px">'
                 f'<img src="{MARQUE}embleme-or@6x.png" style="width:{150 * t}px;height:auto;flex:none">'
                 f'<div><div style="font:400 {17 * t}px \'Geist Mono\';letter-spacing:.22em;color:#c8a46e;'
                 f'text-transform:uppercase">Sites internet · Charente</div>'
                 f'<div style="font:400 {62 * t}px/1.02 \'Instrument Serif\';color:#efe9df;margin:{12 * t}px 0">'
                 f'Vos clients vous cherchent<br>sur leur téléphone. <em style="color:#d9bb8a">Ils vous trouvent ?</em></div>'
                 f'<div style="font:400 {21 * t}px Geist;color:#a8a093">dig16.fr · dès 49 € par mois · 0 € de création</div>'
                 f'</div></div>')
    return (f'<!doctype html><html><head><meta charset="utf-8">{POLICES}<style>html,body{{margin:0}}'
            f'body{{width:{larg}px;height:{h}px;{FOND}display:grid;place-items:center;overflow:hidden}}</style></head>'
            f'<body>{corps}</body></html>')


def main():
    os.makedirs(SORTIE, exist_ok=True)
    fautes = []
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME)
        for nom, larg, h, zone, genre in FORMATS:
            pg = nav.new_page(viewport={"width": larg, "height": h})
            tmp = os.path.join(SORTIE, "_tmp.html")  # file:// pour que les images de la marque se chargent
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(page(larg, h, zone, genre))
            pg.goto("file://" + tmp)
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(600)
            r = pg.evaluate("(()=>{const b=document.getElementById('z').getBoundingClientRect();"
                            "return [b.width,b.height,[...document.fonts].filter(f=>f.status==='loaded').length,"
                            "[...document.images].every(i=>i.complete&&i.naturalWidth>0)]})()")
            os.remove(tmp)
            if not r[3]:
                fautes.append(f"{nom} : image de la marque non chargée")
            if r[0] > zone[0] + 1 or r[1] > zone[1] + 1:
                fautes.append(f"{nom} : contenu {round(r[0])}×{round(r[1])} > zone sûre {zone[0]}×{zone[1]}")
            if genre != "avatar" and r[2] < 2:
                fautes.append(f"{nom} : polices non chargées")
            pg.screenshot(path=os.path.join(SORTIE, nom))
            pg.close()
            print(nom, larg, "×", h)
        nav.close()
    for f in fautes:
        print("ALERTE", f)
    return 1 if fautes else 0


if __name__ == "__main__":
    raise SystemExit(main())
