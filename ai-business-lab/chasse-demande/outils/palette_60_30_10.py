#!/usr/bin/env python3
"""Mesure la répartition des couleurs d'un site selon la règle des designers 60/30/10 (27/10/2026).

Idée envoyée par l'utilisateur (reel Instagram De7K4bwIeR3, résumé dans connaissances/reels/) : 60 % de couleur
dominante, 30 % de secondaire, 10 % d'accent ; l'accent, le plus discret, est réservé aux boutons, titres et appels
à l'action ; une seule palette, gardée partout ; contraste vérifié sur téléphone ; palette testée en petit format.

Ce que fait l'outil, page par page, à 390 px (téléphone) et 1440 px (ordinateur), animations coupées :
- masque les photos et vidéos (img, video, canvas, iframe, fonds en url(...)) et les zones exclues (--exclure) : on
  mesure le dessin du site, pas les photos ;
- classe chaque pixel en OKLab : neutre (fond, texte : dominante et secondaire, séparées par la clarté), accent (teinte
  à moins de 25° de l'accent déclaré), « autre couleur vive » (ni neutre ni accent) ;
- ALERTE si l'accent dépasse 15 % (il crie au lieu de guider), si aucun accent n'est visible (aucun bouton repérable),
  ou si une autre couleur vive dépasse 1,5 % (deuxième accent, interdit par la charte) ;
- avec --planche LOGO : fabrique une planche du logo ou de l'icône à 16, 32, 48 et 180 px sur fond clair et sombre,
  à regarder à l'œil (le reel : « ton logo en petit format doit rester lisible »).

Le 60/30/10 est un repère de designer, pas une loi : seules les dérives nettes sont signalées. Le contraste des textes
reste contrôlé par outils/audit_acces.py (test_pages.py).

Usage :
  python3 outils/palette_60_30_10.py                       # dig16.fr en local (site-dig), accent laiton
  python3 outils/palette_60_30_10.py --dossier chemin/site --accent "#1f6f8b" [--pages / /contact/] [--exclure .x]
  python3 outils/palette_60_30_10.py --planche chemin/logo.png [--sortie planche.png]
Code de sortie : 0 sans ALERTE, 1 sinon.
"""

import argparse
import functools
import http.server
import io
import os
import sys
import threading

import numpy as np
from PIL import Image

RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
# Pages publiques de dig16.fr ; .vieux = l'illustration « ancien site » (couleurs volontairement criardes).
PAGES_DIG = ['/', '/prestige.html', '/le-projet/', '/site-internet-artisan/', '/test-du-pouce/', '/mentions-legales.html']
EXCLURE_DIG = ['.vieux']
ACCENT_DIG = '#c8a46e'  # laiton, 60-charte-dig16.md

SEUIL_NEUTRE = 0.035      # chroma OKLab sous laquelle un pixel est un gris, un ivoire, un noir
ECART_TEINTE = 25         # degrés autour de la teinte d'accent
ACCENT_MAX = 15.0         # % de pixels dessinés
AUTRE_MAX = 1.5


def oklab(rgb):
    """rgb : tableau (..., 3) en 0-255 -> OKLab (formules de Björn Ottosson)."""
    c = rgb.astype(np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    l = 0.4122214708 * c[..., 0] + 0.5363325363 * c[..., 1] + 0.0514459929 * c[..., 2]
    m = 0.2119034982 * c[..., 0] + 0.6806995451 * c[..., 1] + 0.1073969566 * c[..., 2]
    s = 0.0883024619 * c[..., 0] + 0.2817188376 * c[..., 1] + 0.6299787005 * c[..., 2]
    l, m, s = np.cbrt(l), np.cbrt(m), np.cbrt(s)
    return np.stack([0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
                     1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
                     0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s], axis=-1)


def teinte(hexa):
    rgb = np.array([[int(hexa.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]])
    lab = oklab(rgb)[0]
    return float(np.degrees(np.arctan2(lab[2], lab[1])) % 360), float(np.hypot(lab[1], lab[2]))


def repartition(image, masque, accent_hexa):
    """image PIL RGB, masque bool (True = pixel à ignorer) -> dict de parts en %."""
    px = np.asarray(image.convert('RGB'))
    garder = ~masque
    lab = oklab(px[garder])
    if lab.size == 0:
        return None
    chroma = np.hypot(lab[:, 1], lab[:, 2])
    h = np.degrees(np.arctan2(lab[:, 2], lab[:, 1])) % 360
    h_acc, _ = teinte(accent_hexa)
    ecart = np.abs((h - h_acc + 180) % 360 - 180)
    neutre = chroma < SEUIL_NEUTRE
    accent = ~neutre & (ecart <= ECART_TEINTE)
    autre = ~neutre & ~accent
    clair = neutre & (lab[:, 0] >= 0.6)
    sombre = neutre & ~clair
    n = len(lab)
    parts = {k: 100.0 * v.sum() / n for k, v in (('sombre', sombre), ('clair', clair), ('accent', accent), ('autre', autre))}
    dom, sec = sorted(('sombre', 'clair'), key=lambda k: -parts[k])
    parts['dominante'], parts['secondaire'] = parts[dom], parts[sec]
    parts['dominante_nom'] = dom
    # Teintes des « autres couleurs vives », pour dire lesquelles (par tranches de 30°).
    if autre.any():
        hist = np.bincount((h[autre] // 30).astype(int), minlength=12)
        parts['autres_teintes'] = [f'{30 * i}-{30 * i + 30}°:{100.0 * c / n:.1f}%' for i, c in enumerate(hist) if 100.0 * c / n >= 0.3]
    return parts


MASQUER_JS = """(exclure) => {
  const zones = [];
  const sel = ['img', 'video', 'canvas', 'iframe', 'picture', ...exclure].join(',');
  document.querySelectorAll(sel).forEach(e => zones.push(e));
  document.querySelectorAll('*').forEach(e => { if (getComputedStyle(e).backgroundImage.includes('url(')) zones.push(e); });
  return zones.map(e => { const r = e.getBoundingClientRect();
    return [r.left + scrollX, r.top + scrollY, r.width, r.height]; }).filter(z => z[2] > 0 && z[3] > 0);
}"""


def mesurer(base, pages, accent, exclure):
    from playwright.sync_api import sync_playwright
    alertes, lignes = 0, []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME) if os.path.exists(CHROME) else p.chromium.launch()
        for largeur, hauteur in ((390, 844), (1440, 900)):
            ctx = b.new_context(viewport={'width': largeur, 'height': hauteur}, reduced_motion='reduce')
            for chemin in pages:
                pg = ctx.new_page()
                pg.goto(base + chemin, wait_until='networkidle')
                pg.wait_for_timeout(1200)
                # Défilement complet : déclenche les apparitions au défilement avant la capture.
                pg.evaluate("async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); }")
                pg.wait_for_timeout(600)
                zones = pg.evaluate(MASQUER_JS, exclure)
                img = Image.open(io.BytesIO(pg.screenshot(full_page=True)))
                masque = np.zeros((img.height, img.width), dtype=bool)
                for x, y, w, h in zones:
                    x0, y0 = max(0, int(x)), max(0, int(y))
                    masque[y0:min(img.height, int(y + h) + 1), x0:min(img.width, int(x + w) + 1)] = True
                r = repartition(img, masque, accent)
                pg.close()
                if r is None:
                    lignes.append(f'OK     {largeur:>4} px {chemin} : page entièrement photographique')
                    continue
                pb = []
                if r['accent'] > ACCENT_MAX:
                    pb.append(f"accent {r['accent']:.1f} % > {ACCENT_MAX:.0f} %")
                if r['accent'] < 0.05:
                    pb.append('aucun accent visible (boutons ?)')
                if r['autre'] > AUTRE_MAX:
                    pb.append(f"autre couleur vive {r['autre']:.1f} % ({', '.join(r.get('autres_teintes', []))})")
                alertes += bool(pb)
                lignes.append(f"{'ALERTE' if pb else 'OK    '} {largeur:>4} px {chemin} : dominante ({r['dominante_nom']}) "
                              f"{r['dominante']:.0f} % · secondaire {r['secondaire']:.0f} % · accent {r['accent']:.1f} % · "
                              f"autre {r['autre']:.1f} %" + (f"  <- {' ; '.join(pb)}" if pb else ''))
            ctx.close()
        b.close()
    print('\n'.join(lignes))
    print(f'palette 60/30/10 : {alertes} ALERTE' + ('' if alertes == 1 else 's') if alertes else 'palette 60/30/10 : OK')
    return 1 if alertes else 0


def planche(logo, sortie):
    """Logo à 16, 32, 48 et 180 px, sur ivoire, blanc, noir chaud et gris moyen, à regarder à l'œil."""
    src = Image.open(logo).convert('RGBA')
    tailles, fonds = (16, 32, 48, 180), ('#ffffff', '#efe9df', '#7f7f7f', '#0b0a08')
    marge = 24
    largeur = marge + sum(t + marge for t in tailles)
    hauteur = marge + len(fonds) * (180 + marge)
    out = Image.new('RGB', (largeur, hauteur), '#ffffff')
    for j, fond in enumerate(fonds):
        y = marge + j * (180 + marge)
        Image.Image.paste(out, Image.new('RGB', (largeur, 180 + marge), fond), (0, y - marge // 2))
        x = marge
        for t in tailles:
            ratio = t / max(src.size)
            petit = src.resize((max(1, round(src.width * ratio)), max(1, round(src.height * ratio))), Image.LANCZOS)
            out.paste(petit, (x, y + (180 - petit.height) // 2), petit)
            x += t + marge
    out.save(sortie)
    print(f'planche : {sortie} ({", ".join(map(str, tailles))} px sur {len(fonds)} fonds) : à regarder à l\'œil')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dossier', help='site à servir en local (défaut : site-dig)')
    ap.add_argument('--url', help='site déjà en ligne, au lieu d\'un dossier')
    ap.add_argument('--accent', help='couleur d\'accent déclarée (#rrggbb)')
    ap.add_argument('--pages', nargs='*')
    ap.add_argument('--exclure', nargs='*', default=None, help='sélecteurs CSS à ignorer (illustrations volontaires)')
    ap.add_argument('--planche', help='logo ou icône (png) : fabrique la planche des petits formats')
    ap.add_argument('--sortie', default='planche-petits-formats.png')
    a = ap.parse_args()
    if a.planche:
        planche(a.planche, a.sortie)
        return 0
    dig = not (a.dossier or a.url)
    accent = a.accent or ACCENT_DIG
    pages = a.pages or (PAGES_DIG if dig else ['/'])
    exclure = a.exclure if a.exclure is not None else (EXCLURE_DIG if dig else [])
    if a.url:
        return mesurer(a.url.rstrip('/'), pages, accent, exclure)
    dossier = os.path.abspath(a.dossier or os.path.join(RACINE, 'site-dig'))
    class Silencieux(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *x):
            pass
    gestion = functools.partial(Silencieux, directory=dossier)
    serveur = http.server.ThreadingHTTPServer(('127.0.0.1', 0), gestion)
    threading.Thread(target=serveur.serve_forever, daemon=True).start()
    try:
        return mesurer(f'http://127.0.0.1:{serveur.server_port}', pages, accent, exclure)
    finally:
        serveur.shutdown()


if __name__ == '__main__':
    sys.exit(main())
