import re
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

PAGES = ['/', '/prestige.html', '/mentions-legales.html', '/test-du-pouce/', '/le-projet/', '/creation-site-internet-charente/', '/site-internet-artisan/', '/demos/prestige/',
         '/demos/paysagiste/', '/demos/menuisier/', '/demos/menuisier-visite/', '/demos/garage/']
CHROME = '/opt/pw-browsers/chromium'

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
    pages = [os.path.join(site, p) for p in ('index.html', 'prestige.html', 'le-projet/index.html', 'creation-site-internet-charente/index.html',
                                             'site-internet-artisan/index.html', 'mentions-legales.html')]
    r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audit_acces.py'), *pages],
                       capture_output=True, text=True, timeout=600)
    ok = 'problèmes : 0' in r.stdout
    detail = [l for l in r.stdout.splitlines() if 'px' in l or 'sans' in l][:4] or r.stderr.strip().splitlines()[-3:]
    print(('OK    ' if ok else 'ALERTE'), 'accessibilité', '' if ok else detail)
    return 0 if ok else 1

def palette():
    """27/10 : règle des couleurs 60/30/10 (reel De7K4bwIeR3) : accent laiton discret, pas de deuxième couleur vive."""
    r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'palette_60_30_10.py')],
                       capture_output=True, text=True, timeout=900)
    alertes = [l for l in r.stdout.splitlines() if l.startswith('ALERTE')]
    detail = alertes[:3] or (r.stderr.strip().splitlines()[-2:] if r.returncode else '')
    print(('ALERTE' if r.returncode else 'OK    '), 'palette 60/30/10', detail)
    return 1 if r.returncode else 0

def markdown_a_jour():
    """24/10 : la version Markdown des pages (servie aux agents IA) doit suivre chaque modification d'une page."""
    outil = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pages_markdown.py')
    r = subprocess.run([sys.executable, outil, '--verifier'], capture_output=True, text=True)
    print((r.stdout or r.stderr).strip())
    return 0 if r.returncode == 0 else 1

def polices_locales():
    """28/10 : aucune police chargée depuis Google (RGPD, consigne du 15/10). Le skill ui-ux-pro-max propose des liens
    fonts.googleapis.com dans ses paires de polices (relevé par Grok le 28/10) : ce contrôle empêche qu'ils passent."""
    site = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site-dig')
    trouves = []
    for racine, _, fichiers in os.walk(site):
        for f in fichiers:
            if f.endswith(('.html', '.css', '.js')):
                chemin = os.path.join(racine, f)
                with open(chemin, encoding='utf-8', errors='ignore') as fh:
                    if 'fonts.googleapis.com' in (t := fh.read()) or 'fonts.gstatic.com' in t:
                        trouves.append(os.path.relpath(chemin, site))
    print(('ALERTE' if trouves else 'OK    '), 'polices hébergées sur le site', trouves[:5] or '')
    return 1 if trouves else 0

def reseaux_visibles():
    """28/10 : TikTok et Threads figuraient dans les données structurées (sameAs) mais pas dans le pied de page de
    l'accueil (remarque de l'utilisateur). Chaque compte de sameAs doit avoir un lien visible sur l'accueil."""
    site = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site-dig')
    t = open(os.path.join(site, 'index.html'), encoding='utf-8').read()
    m = re.search(r'"sameAs":\[([^\]]*)\]', t)
    comptes = re.findall(r'"([^"]+)"', m.group(1)) if m else []
    reseaux = ('facebook.com', 'instagram.com', 'threads.com', 'tiktok.com', 'youtube.com', 'x.com')
    manquants = [u for u in comptes if any(r in u for r in reseaux) and f'href="{u}"' not in t]
    print(('ALERTE' if manquants or not comptes else 'OK    '), 'réseaux visibles sur l\'accueil', manquants or '')
    return 1 if manquants or not comptes else 0

def titres_uniques():
    """Leçon du 05/11 : la page Charente a gardé le <title> de « Le projet » (remplacement de modèle raté sans erreur).
    Chaque page publique doit avoir son propre titre et sa propre description."""
    import re
    site = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site-dig')
    vus, doublons = {}, []
    for p in [p for p in PAGES if not p.startswith('/demos/')]:
        f = os.path.join(site, p.lstrip('/'), 'index.html') if p.endswith('/') else os.path.join(site, p.lstrip('/'))
        with open(f, encoding='utf-8') as fh:
            h = fh.read()
        for balise in (r'<title>([^<]*)</title>', r'<meta name="description" content="([^"]*)"'):
            m = re.search(balise, h)
            cle = (balise[:6], m.group(1).strip() if m else '')
            if cle in vus:
                doublons.append(f'{p} = {vus[cle]} ({cle[1][:50]})')
            vus.setdefault(cle, p)
    print(('OK    ' if not doublons else 'ALERTE'), 'titres et descriptions uniques', '' if not doublons else doublons)
    return 1 if doublons else 0

def main():
    base = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else None
    serveur = None
    if not base:
        site = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site-dig')
        serveur = subprocess.Popen([sys.executable, '-m', 'http.server', '4699'], cwd=site,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1.5); base = 'http://localhost:4699'
    souci = son_videos() + regles_interface() + plan_du_site() + titres_uniques() + accessibilite() + palette() + markdown_a_jour() + polices_locales() + reseaux_visibles()
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=CHROME) if os.path.exists(CHROME) else p.chromium.launch()
            # 360 px ajouté le 24/10 : un visiteur sur un petit téléphone voyait le bouton de l'en-tête coupé.
            for w, h in ((1440, 900), (390, 844), (360, 780)):
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
                    # 26/10 : la galerie horizontale des démos de l'accueil (.vitrine-piste) glisse volontairement hors écran.
                    # 24/10 : bouton ou lien coupé par le bord de l'écran (le débordement est masqué, donc invisible
                    # pour scrollWidth). Pages du site seulement : les démos ont des carrousels hors écran volontaires.
                    if not u.startswith('/demos/'):
                        coupes = pg.evaluate("""[...document.querySelectorAll('a,button')].filter(e=>{const r=e.getBoundingClientRect();
                            return r.width>0&&r.height>0&&getComputedStyle(e).visibility!=='hidden'&&(r.right>innerWidth+1||r.left<-1)
                            &&!e.closest('.eventail,figure,[aria-hidden=true],.avant,.saut,.vitrine-piste')}).map(e=>e.textContent.trim().slice(0,30))""")
                        if coupes:
                            errs.append(f'bouton coupé {coupes[:3]}')
                    # 26/10 (skill mobile-native) : un survol qui bouge (transform, pause d'animation) reste « collé »
                    # après un toucher sur téléphone (carte de démo restée soulevée). Il doit être réservé à la souris :
                    # @media (hover:hover) and (pointer:fine), ou annulé dans un bloc (hover:none)/(pointer:coarse).
                    if w == 390:
                        colles = pg.evaluate(r"""(()=>{const bouge=[],annule=new Set();
                            const parcours=(regles,conds)=>{for(const r of regles){
                              if(r.cssRules&&r.conditionText!==undefined){const ct=r.conditionText;
                                // bloc qui ne s'applique pas à un téléphone de 390 px (ex. grand écran) : ignoré
                                if(!/hover|pointer/.test(ct)&&!matchMedia(ct).matches)continue;
                                parcours(r.cssRules,conds.concat(ct.replace(/\s+/g,'')));continue}
                              if(!r.selectorText||!r.style)continue;
                              const t=r.style.transform||r.style.translate||r.style.scale||r.style.animationPlayState;
                              if(!t)continue;
                              const c=conds.join(' ');const sels=r.selectorText.split(',').map(s=>s.trim());
                              // réglage prévu pour le toucher : annule ou remplace l'effet de survol
                              if(/hover:none|pointer:coarse/.test(c)){sels.forEach(s=>annule.add(s));continue}
                              if(/hover:hover/.test(c))continue;
                              sels.filter(s=>s.includes(':hover')).forEach(s=>bouge.push(s))}};
                            for(const f of document.styleSheets){try{parcours(f.cssRules,[])}catch(e){}}
                            return [...new Set(bouge.filter(s=>!annule.has(s)))]})()""")
                        if colles:
                            errs.append(f'survol collé au toucher {colles[:3]}')
                    ok = not (errs or bad or nb or ov > 0)
                    souci += not ok
                    print(('OK    ' if ok else 'ALERTE'), w, u, '' if ok else f'débord={ov} erreurs={errs[:2]} 404={bad[:2]} images={nb[:2]}')
                    pg.close()
            # Bug du 11/11 (vu par l'utilisateur sur son téléphone, jamais par les audits) : l'écran final de la
            # présentation (#film-fin, caché tant que la vidéo n'est pas finie) débordait du téléphone dessiné.
            # Règle : tout écran caché à l'ouverture est affiché de force et mesuré, à 10 largeurs et 3 tailles de texte.
            for w in (320, 360, 390, 412, 600, 768, 820, 1024, 1440, 1920):
                pg = b.new_page(viewport={'width': w, 'height': 850})
                pg.goto(base + '/', wait_until='load'); pg.wait_for_timeout(500)
                pires = []
                for fs in (100, 130, 160):
                    r = pg.evaluate("""fs=>{document.documentElement.style.fontSize=fs+'%';
                        const f=document.getElementById('film-fin');if(!f)return ['écran final absent'];
                        f.hidden=false;for(const i of ['film-muet','film-pause']){const e=document.getElementById(i);if(e)e.hidden=true}
                        const c=f.getBoundingClientRect(),out=[];
                        const els=[...f.querySelectorAll('p,a,button')].filter(e=>getComputedStyle(e).display!=='none');
                        for(const e of els){const r=e.getBoundingClientRect();
                          if(r.left<c.left-1||r.right>c.right+1||r.top<c.top-1||r.bottom>c.bottom+1)out.push('sort du cadre: '+e.textContent.trim().slice(0,25));
                          if(e.scrollWidth>e.clientWidth+1)out.push('texte coupé: '+e.textContent.trim().slice(0,25))}
                        const blocs=[...f.children].filter(e=>getComputedStyle(e).display!=='none').map(e=>e.getBoundingClientRect());
                        for(let i=1;i<blocs.length;i++)if(blocs[i].top<blocs[i-1].bottom-1)out.push('blocs superposés '+i);
                        if(els.length<3)out.push('écran final vide');
                        return out}""", fs)
                    if r:
                        pires.append(f'texte {fs} % : {r[:3]}')
                souci += bool(pires)
                print(('ALERTE' if pires else 'OK    '), w, '/ écran final de la présentation (texte 100, 130, 160 %)', pires[:2] or '')
                pg.close()
            # Même jour : proportions sur tous les supports. Les pages du site (hors démos) aux largeurs que la boucle
            # du haut ne voit pas (petit téléphone, tablette, grand écran) et sur téléphone avec le texte agrandi.
            for w, fs in ((320, 100), (768, 100), (1024, 100), (1920, 100), (360, 130)):
                for u in [x for x in PAGES if not x.startswith('/demos/')]:
                    pg = b.new_page(viewport={'width': w, 'height': 850})
                    pg.goto(base + u, wait_until='load'); pg.wait_for_timeout(400)
                    pg.evaluate("fs=>{document.documentElement.style.fontSize=fs+'%'}", fs)
                    for y in range(0, pg.evaluate('document.body.scrollHeight'), 700):
                        pg.evaluate(f'scrollTo(0,{y})'); pg.wait_for_timeout(40)
                    ov = pg.evaluate('document.documentElement.scrollWidth-innerWidth')
                    coupes = pg.evaluate("""[...document.querySelectorAll('a,button')].filter(e=>{const r=e.getBoundingClientRect();
                        return r.width>0&&r.height>0&&getComputedStyle(e).visibility!=='hidden'&&(r.right>innerWidth+1||r.left<-1)
                        &&!e.closest('.eventail,figure,[aria-hidden=true],.avant,.saut,.vitrine-piste')}).map(e=>e.textContent.trim().slice(0,30))""")
                    # points de séparation restés seuls en début ou en fin de ligne dans le bas de page
                    orphelins = pg.evaluate("""[...document.querySelectorAll('footer *')].some(e=>[...e.childNodes].some(n=>n.nodeType===3&&/^\\s*·\\s*$/.test(n.textContent)))""")
                    ok = not (ov > 0 or coupes or orphelins)
                    souci += not ok
                    print(('OK    ' if ok else 'ALERTE'), w, f'texte {fs} %', u, '' if ok else f'débord={ov} coupés={coupes[:3]} points seuls={orphelins}')
                    pg.close()
            # 12/11 : retouches validées le 11/11. (1) Premier écran de l'accueil sur téléphone : le prix « Dès 49 € par mois »
            # et la barre « Appeler / Démo gratuite » sont visibles sans défiler, la barre ne recouvre ni le prix ni le titre.
            for w, h in ((320, 568), (360, 640), (360, 780), (390, 844), (412, 915)):
                c = b.new_context(viewport={'width': w, 'height': h}, is_mobile=True, has_touch=True)
                pg = c.new_page(); pg.goto(base + '/', wait_until='load'); pg.wait_for_timeout(1500)
                r = pg.evaluate("""()=>{const out=[],q=s=>document.querySelector(s),p=q('.prix-heros'),ba=q('#barre');
                    if(!p||!/49\\s€ par mois, 0\\s€ de création/.test(p.textContent))return ['prix du premier écran absent'];
                    const rp=p.getBoundingClientRect(),rb=ba.getBoundingClientRect(),st=getComputedStyle(ba);
                    if(st.display==='none'||st.opacity!=='1'||rb.height<44)out.push('barre du bas invisible à l’arrivée');
                    if(rb.bottom>innerHeight+1||rb.top<0)out.push('barre du bas hors écran');
                    if(rp.bottom>rb.top-4||rp.top<0)out.push('prix caché ou sous la barre');
                    if(!/Appeler/.test(ba.textContent)||!/Démo gratuite/.test(ba.textContent))out.push('texte de la barre');
                    return out}""")
                souci += bool(r)
                print(('ALERTE' if r else 'OK    '), f'{w}x{h}', '/ premier écran : prix et barre visibles sans défiler', r or '')
                c.close()
            # (2) Bandeau « Vu dans Charente Libre » : présent en haut de chaque page du site (pas des démos), entièrement
            # visible à l'arrivée (rien ne le recouvre), sur une ligne ou deux, lien vers le journal, cible d'au moins 38 px.
            for w, fs in ((320, 100), (360, 130), (390, 100), (768, 100), (1440, 100), (1920, 100)):
                for u in [x for x in PAGES if not x.startswith('/demos/')]:
                    pg = b.new_page(viewport={'width': w, 'height': 850})
                    pg.goto(base + u, wait_until='load'); pg.wait_for_timeout(500)
                    r = pg.evaluate("""fs=>{document.documentElement.style.fontSize=fs+'%';const e=document.querySelector('a.vu-presse');
                        if(!e)return ['bandeau absent'];const out=[],r=e.getBoundingClientRect(),s=e.querySelector('span').getBoundingClientRect();
                        if(!/charentelibre\\.fr/.test(e.href))out.push('lien');
                        if(!/Vu dans Charente Libre, 10\\s novembre\\s 2026|Vu dans Charente Libre, 10.novembre.2026/.test(e.textContent))out.push('texte : '+e.textContent);
                        if(r.top<-1||r.left<-1||r.right>innerWidth+1)out.push('hors écran');
                        if(r.height<38)out.push('cible trop petite');
                        if(s.left<0||s.right>innerWidth||s.height>r.height)out.push('texte coupé');
                        const top=document.elementFromPoint(innerWidth/2,r.top+r.height/2);
                        if(!top||!e.contains(top))out.push('recouvert par '+(top&&(top.id||top.className||top.tagName)));
                        const n=document.getElementById('nav');
                        if(n){const rn=n.getBoundingClientRect();if(rn.top<r.bottom-1)out.push('menu sur le bandeau');
                          scrollTo(0,600);const r2=n.getBoundingClientRect();if(Math.abs(r2.top)>1)out.push('menu décollé après défilement : '+Math.round(r2.top))}
                        return out}""", fs)
                    souci += bool(r)
                    print(('ALERTE' if r else 'OK    '), w, f'texte {fs} %', u, 'bandeau presse', r or '')
                    pg.close()
            # (3) Article de Charente Libre en grand (fenêtre cachée à l'ouverture) : affichée de force et mesurée,
            # à 10 largeurs et 3 tailles de texte (leçon du 11/11), puis ouverte par un vrai clic et fermée par Échap.
            for u in ('/', '/le-projet/'):
                for w in (320, 360, 390, 412, 600, 768, 820, 1024, 1440, 1920):
                    pg = b.new_page(viewport={'width': w, 'height': 700 if w < 600 else 850})
                    pg.goto(base + u, wait_until='load'); pg.wait_for_timeout(400)
                    pires = []
                    for fs in (100, 130, 160):
                        r = pg.evaluate("""async fs=>{document.documentElement.style.fontSize=fs+'%';
                            const d=document.getElementById('article-grand'),v=document.getElementById('article-ouvrir');
                            if(!d||!v)return ['article absent'];const out=[];
                            const rv=v.getBoundingClientRect(),iv=v.querySelector('img');
                            if(rv.width<120||rv.right>innerWidth+1||rv.left<-1)out.push('vignette '+Math.round(rv.width));
                            if(!iv.alt||iv.alt.length<80)out.push('texte alternatif trop court');
                            const leg=v.closest('figure').querySelector('figcaption');
                            if(!/Charente Libre, édition du 10\\s novembre\\s 2026|Charente Libre, édition du 10.novembre.2026/.test(leg.textContent))out.push('légende');
                            if(!/charentelibre\\.fr/.test(leg.querySelector('a').href))out.push('lien du journal');
                            if(d.open)d.close();const larg0=document.documentElement.scrollWidth;d.showModal();const im=document.getElementById('article-image');
                            for(let i=0;i<40&&!(im.complete&&im.naturalWidth);i++)await new Promise(r=>setTimeout(r,100));
                            if(!im.naturalWidth)out.push('image agrandie non chargée');
                            const c=d.getBoundingClientRect();
                            if(c.left<-1||c.top<-1||c.right>innerWidth+1||c.bottom>innerHeight+1)out.push('fenêtre hors écran '+[c.left,c.top,c.right,c.bottom].map(Math.round));
                            const f=document.getElementById('article-fermer').getBoundingClientRect();
                            if(f.height<44||f.width<44||f.right>c.right+1||f.top<c.top-1||f.bottom>innerHeight)out.push('bouton Fermer');
                            const z=document.getElementById('article-zone').getBoundingClientRect();
                            if(z.height<Math.min(220,innerHeight*.3))out.push('image trop petite : '+Math.round(z.height)+' px');
                            const ri=im.getBoundingClientRect();if(ri.width>z.width+1)out.push('image plus large que son cadre');
                            for(const e of d.querySelectorAll('span,a,button')){const r=e.getBoundingClientRect();
                              if(r.width&&(r.left<c.left-1||r.right>c.right+1||r.bottom>c.bottom+1))out.push('sort du cadre : '+e.textContent.trim().slice(0,22))}
                            const blocs=[...d.children].map(e=>e.getBoundingClientRect());
                            for(let i=1;i<blocs.length;i++)if(blocs[i].top<blocs[i-1].bottom-1)out.push('blocs superposés '+i);
                            if(document.documentElement.scrollWidth>larg0)out.push('la fenêtre élargit la page');
                            d.close();return out}""", fs)
                        if r:
                            pires.append(f'texte {fs} % : {r[:3]}')
                    if w in (390, 1440):
                        pg.evaluate("document.documentElement.style.fontSize=''")
                        pg.locator('#article-ouvrir').scroll_into_view_if_needed(); pg.wait_for_timeout(900)
                        pg.locator('#article-ouvrir').click(); pg.wait_for_timeout(400)
                        if not pg.evaluate("document.getElementById('article-grand').open"): pires.append('le clic n’ouvre pas l’image')
                        pg.locator('#article-zone').click(position={'x': 60, 'y': 60}); pg.wait_for_timeout(200)
                        if not pg.evaluate("document.getElementById('article-zone').classList.contains('zoom')"): pires.append('second agrandissement inactif')
                        pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
                        if pg.evaluate("document.getElementById('article-grand').open"): pires.append('Échap ne ferme pas')
                    souci += bool(pires)
                    print(('ALERTE' if pires else 'OK    '), w, u, 'article de presse en grand (texte 100, 130, 160 %)', pires[:2] or '')
                    pg.close()
            # (4) Démos : mêmes proportions que le reste du site (320, 768, 1024, 1920 px et texte à 130 %), mention
            # « Démonstration fictive » visible en haut dès l'arrivée, aucune note ni avis d'exemple.
            for w, fs in ((320, 100), (768, 100), (1024, 100), (1920, 100), (360, 130)):
                for u in [x for x in PAGES if x.startswith('/demos/')]:
                    pg = b.new_page(viewport={'width': w, 'height': 850})
                    errs = []
                    pg.on('pageerror', lambda e: errs.append(str(e)))
                    pg.goto(base + u, wait_until='load'); pg.wait_for_timeout(700)
                    pg.evaluate("fs=>{document.documentElement.style.fontSize=fs+'%'}", fs); pg.wait_for_timeout(150)
                    r = pg.evaluate("""()=>{const out=[],e=document.querySelector('.demo-fictive');
                        if(!e)return ['mention « Démonstration fictive » absente'];const r=e.getBoundingClientRect();
                        if(!/Démonstration fictive/.test(e.textContent))out.push('texte de la mention');
                        if(r.top<-1||r.bottom>innerHeight*.3||r.left<-1||r.right>innerWidth+1||r.height<20)out.push('mention pas en haut : '+[r.top,r.bottom].map(Math.round));
                        const t=[...e.querySelectorAll('*')].find(x=>/Démonstration fictive/.test(x.textContent)&&!x.children.length)||e,rt=t.getBoundingClientRect();
                        const top=document.elementFromPoint(Math.min(innerWidth-2,Math.max(2,rt.left+rt.width/2)),rt.top+rt.height/2);
                        if(!top||!(e.contains(top)))out.push('mention recouverte par '+(top&&(top.id||top.className||top.tagName)));
                        if(/4,9|38 avis|★|Avis d.exemple|Avis fictif/.test(document.body.innerText))out.push('note ou avis d’exemple encore affiché');
                        if(/aggregateRating|"review"/.test(document.documentElement.innerHTML))out.push('note dans les données structurées');
                        return out}""")
                    for y in range(0, pg.evaluate('document.body.scrollHeight'), 700):
                        pg.evaluate(f'scrollTo(0,{y})'); pg.wait_for_timeout(40)
                    ov = pg.evaluate('document.documentElement.scrollWidth-innerWidth')
                    ok = not (r or ov > 0 or errs)
                    souci += not ok
                    print(('OK    ' if ok else 'ALERTE'), w, f'texte {fs} %', u, '' if ok else f'débord={ov} {r[:3]} erreurs={errs[:1]}')
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
