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

PAGES = ['/', '/prestige.html', '/mentions-legales.html', '/test-du-pouce/', '/le-projet/', '/site-internet-artisan/', '/demos/prestige/',
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

def regles_interface():
    """Règles d'interface de Vercel (10/10) sur les pages publiques : lien d'accès direct au contenu, toucher sans
    délai, champs de formulaire avec saisie automatique, focus visible au clavier."""
    import re
    site = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site-dig')
    souci = 0
    for page in ('index.html', 'prestige.html', 'mentions-legales.html', 'test-du-pouce/index.html'):
        t = open(os.path.join(site, page), encoding='utf-8').read()
        manque = [nom for nom, ok in (
            ('lien « Aller au contenu »', 'class="saut"' in t and 'id="contenu"' in t),
            ('touch-action', 'touch-action' in t),
            ('focus visible', 'focus-visible' in t),
            ('saisie automatique', all('autocomplete' in i or 'type="hidden"' in i
                                      for i in re.findall(r'<input\b[^>]*>', t))),
        ) if not ok]
        souci += bool(manque)
        print(('ALERTE' if manque else 'OK    '), 'interface', page, manque or '')
    return souci

def plan_du_site():
    """Leçon du 18/10 : un <url> resté ouvert avait glissé la page guide DANS l'entrée de « Le projet » (XML bien formé,
    mais Google ne voyait plus la page guide dans le plan). Chaque <url> doit être au premier niveau et chaque page publique
    du test doit y figurer."""
    import xml.etree.ElementTree as ET
    site = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site-dig')
    ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    racine = ET.parse(os.path.join(site, 'sitemap.xml')).getroot()
    imbriquees = [u.findtext(ns + 'loc') for u in racine.iter(ns + 'url') if u not in list(racine)]
    adresses = {u.findtext(ns + 'loc') for u in racine.findall(ns + 'url')}
    publiques = [p for p in PAGES if not p.startswith('/demos/')]
    absentes = [p for p in publiques if not ({'https://dig16.fr' + p, 'https://dig16.fr' + p.removesuffix('.html')} & adresses)]
    ok = not (imbriquees or absentes)
    print(('OK    ' if ok else 'ALERTE'), 'plan du site', '' if ok else f'imbriquées={imbriquees} absentes={absentes}')
    return not ok

def accessibilite():
    """Audit d'accessibilité (outils/audit_acces.py) sur les pages publiques : cibles tactiles de 44 px,
    étiquettes, titres, contrastes. Intégré le 22/10 après la correction des liens du pied de page."""
    site = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site-dig')
    pages = [os.path.join(site, p) for p in ('index.html', 'prestige.html', 'le-projet/index.html',
                                             'site-internet-artisan/index.html', 'mentions-legales.html')]
    r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audit_acces.py'), *pages],
                       capture_output=True, text=True, timeout=600)
    ok = 'problèmes : 0' in r.stdout
    detail = [l for l in r.stdout.splitlines() if 'px' in l or 'sans' in l][:4] or r.stderr.strip().splitlines()[-3:]
    print(('OK    ' if ok else 'ALERTE'), 'accessibilité', '' if ok else detail)
    return 0 if ok else 1

def markdown_a_jour():
    """24/10 : la version Markdown des pages (servie aux agents IA) doit suivre chaque modification d'une page."""
    outil = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pages_markdown.py')
    r = subprocess.run([sys.executable, outil, '--verifier'], capture_output=True, text=True)
    print((r.stdout or r.stderr).strip())
    return 0 if r.returncode == 0 else 1

def main():
    base = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else None
    serveur = None
    if not base:
        site = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site-dig')
        serveur = subprocess.Popen([sys.executable, '-m', 'http.server', '4699'], cwd=site,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1.5); base = 'http://localhost:4699'
    souci = son_videos() + regles_interface() + plan_du_site() + accessibilite() + markdown_a_jour()
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
                    # 'load' d'abord, puis réseau calme si possible : chez GitHub (15/10), la démo Prestige (vidéos
                    # d'ambiance en boucle) ne devenait jamais « networkidle » en 30 s et faisait échouer le test.
                    pg.goto(base + u, wait_until='load')
                    try:
                        pg.wait_for_load_state('networkidle', timeout=15000)
                    except Exception:
                        pass
                    for y in range(0, pg.evaluate('document.body.scrollHeight'), 700):
                        pg.evaluate(f'scrollTo(0,{y})'); pg.wait_for_timeout(60)
                    pg.wait_for_timeout(400)
                    ov = pg.evaluate('document.documentElement.scrollWidth-innerWidth')
                    # Leçon du 15/10 : une barre du bas passée en <nav> a hérité de « nav{position:fixed;top:0} »
                    # et a couvert tout l'écran du téléphone. Toute barre fixe de plus de 30 % de la hauteur = alerte.
                    geante = pg.evaluate("""[...document.querySelectorAll('nav,#barre,.basbar,.mobile-cta,[role=navigation]')]
                        .filter(e=>getComputedStyle(e).position==='fixed').map(e=>[e.className||e.id,Math.round(e.getBoundingClientRect().height)])
                        .filter(x=>x[1]>innerHeight*0.3)""")
                    if geante:
                        errs.append(f'barre fixe géante {geante}')
                    nb = pg.evaluate('[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src)')
                    ok = not (errs or bad or nb or ov > 0)
                    souci += not ok
                    print(('OK    ' if ok else 'ALERTE'), w, u, '' if ok else f'débord={ov} erreurs={errs[:2]} 404={bad[:2]} images={nb[:2]}')
                    pg.close()
            # Bug du 22/10 : sur téléphone, un toucher laisse « :hover » collé sur l'éventail et une règle tactile
            # retirait le centrage de la vidéo, qui sautait en bas à droite. Contrôle : après survol, la vidéo
            # reste centrée dans l'éventail (écart de 24 px au plus).
            c = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
            pg = c.new_page(); pg.goto(base + '/', wait_until='load'); pg.wait_for_timeout(800)
            pg.hover('.eventail'); pg.wait_for_timeout(700)
            ecart = pg.evaluate("""(()=>{const f=document.getElementById('fig-film').getBoundingClientRect(),
                e=document.querySelector('.eventail').getBoundingClientRect();
                return [Math.round(Math.abs((f.left+f.width/2)-(e.left+e.width/2))),Math.round(Math.abs((f.top+f.height/2)-(e.top+e.height/2)))]})()""")
            ok = max(ecart) <= 24
            souci += not ok
            print(('OK    ' if ok else 'ALERTE'), 'tactile', '/ vidéo centrée après un toucher', '' if ok else f'écart={ecart}px')
            c.close()
            b.close()
    finally:
        if serveur: serveur.terminate()
    print(f'{souci} page(s) à corriger' if souci else 'Toutes les pages sont propres.')
    sys.exit(1 if souci else 0)

if __name__ == '__main__':
    main()
