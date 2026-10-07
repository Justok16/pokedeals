"""Vérifie que chaque image d'une page est assez grande pour sa surface d'affichage × densité d'écran.
Usage : python3 nettete.py page.html  → liste des images insuffisantes (ratio < 0,95) par taille d'écran."""

import os
import sys
from playwright.sync_api import sync_playwright

JS = """()=>{const out=[];for(const i of document.images){const r=i.getBoundingClientRect();if(!r.width||!i.naturalWidth)continue;
const need=Math.max(r.width,r.height*(i.naturalWidth/i.naturalHeight))*devicePixelRatio;out.push([i.currentSrc.split('/').pop().slice(0,40)||i.alt.slice(0,30),i.naturalWidth,Math.round(need),+(i.naturalWidth/need).toFixed(2)])}
for(const e of document.querySelectorAll('*')){const bg=getComputedStyle(e).backgroundImage;if(bg&&bg.startsWith('url(')&&e.getBoundingClientRect().width){out.push(['fond CSS : '+bg.slice(4,60),0,Math.round(e.getBoundingClientRect().width*devicePixelRatio),-1])}}
return out}"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    for w, h, d in [
        (360, 780, 3),
        (390, 844, 3),
        (768, 1024, 2),
        (1440, 900, 2),
        (1920, 1080, 1),
    ]:
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=d)
        pg.goto("file://" + os.path.abspath(sys.argv[1]))
        pg.wait_for_timeout(1200)
        pg.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')")
        pg.wait_for_timeout(1500)
        r = pg.evaluate(JS)
        bad = [x for x in r if 0 <= x[3] < 0.95]
        fonds = [x for x in r if x[3] == -1]
        print(
            w,
            "x",
            d,
            "insuffisantes :",
            bad,
            ("| fonds CSS à vérifier : %s" % fonds) if fonds else "",
        )
        pg.close()
    b.close()
