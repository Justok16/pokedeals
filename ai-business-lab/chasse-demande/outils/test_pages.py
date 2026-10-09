#!/usr/bin/env python3
"""Test de non-régression du site DIG16 (07/10).

Ouvre chaque page en local (ordinateur 1440 px et téléphone 390 px), la fait défiler
jusqu'en bas et signale : erreurs JavaScript ou console, fichiers introuvables (404),
images cassées, débordement horizontal. Vérifie aussi le son des vidéos du site (09/10) : fréquence
d'échantillonnage de 48 kHz au plus, sinon le lecteur de Windows et certains téléphones les lisent muettes.

Usage : python3 outils/test_pages.py [adresse]   (par défaut un serveur local lancé ici)
Code de sortie 1 si un problème est trouvé.
"""
import subprocess, sys, time, os
from playwright.sync_api import sync_playwright

PAGES = ['/', '/prestige.html', '/mentions-legales.html', '/test-du-pouce/', '/demos/prestige/',
         '/demos/paysagiste/', '/demos/menuisier/', '/demos/menuisier-visite/']
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

def son_videos():
    """Vidéos MP4 et WebM du site qui ont un son : lisible partout (48 kHz au plus).
    Les vidéos d'ambiance des démos sont muettes exprès (aucune piste son) : rien à signaler."""
    site = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site-dig')
    souci = 0
    for racine, _, fichiers in os.walk(site):
        for f in fichiers:
            if not f.endswith(('.mp4', '.webm')):
                continue
            chemin = os.path.join(racine, f)
            r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=sample_rate',
                                '-of', 'csv=p=0', chemin], capture_output=True, text=True).stdout.split()
            if not r:
                continue
            ok = all(int(x) <= 48000 for x in r)
            souci += not ok
            print(('OK    ' if ok else 'ALERTE'), 'son', os.path.relpath(chemin, site), r)
    return souci

def main():
    base = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else None
    serveur = None
    if not base:
        site = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site-dig')
        serveur = subprocess.Popen([sys.executable, '-m', 'http.server', '4699'], cwd=site,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1.5); base = 'http://localhost:4699'
    souci = son_videos()
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=CHROME) if os.path.exists(CHROME) else p.chromium.launch()
            for w, h in ((1440, 900), (390, 844)):
                for u in PAGES:
                    pg = b.new_page(viewport={'width': w, 'height': h})
                    errs, bad = [], []
                    pg.on('pageerror', lambda e: errs.append(str(e)))
                    pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
                    pg.on('response', lambda r: r.status >= 400 and bad.append(f'{r.status} {r.url}'))
                    pg.goto(base + u, wait_until='networkidle')
                    for y in range(0, pg.evaluate('document.body.scrollHeight'), 700):
                        pg.evaluate(f'scrollTo(0,{y})'); pg.wait_for_timeout(60)
                    pg.wait_for_timeout(400)
                    ov = pg.evaluate('document.documentElement.scrollWidth-innerWidth')
                    nb = pg.evaluate('[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src)')
                    ok = not (errs or bad or nb or ov > 0)
                    souci += not ok
                    print(('OK    ' if ok else 'ALERTE'), w, u, '' if ok else f'débord={ov} erreurs={errs[:2]} 404={bad[:2]} images={nb[:2]}')
                    pg.close()
            b.close()
    finally:
        if serveur: serveur.terminate()
    print(f'{souci} page(s) à corriger' if souci else 'Toutes les pages sont propres.')
    sys.exit(1 if souci else 0)

if __name__ == '__main__':
    main()
