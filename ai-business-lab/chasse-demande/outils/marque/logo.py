"""Logo DIG16 (08/10/2026) : emblème « D16 » et signature « DIG16 », charte premium (60-charte-dig16.md).

Fabrique les fichiers PNG (transparents) et SVG dans site-dig/img/marque/ à partir des polices
Instrument Serif et Geist Mono (Google Fonts), rendues par Chromium (Playwright).
Usage : python3 outils/marque/logo.py
"""
import os
from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, '..', '..', 'site-dig', 'img', 'marque')
OR, OR_FONCE, IVOIRE, ENCRE = '#c8a46e', '#8a6a3a', '#efe9df', '#1a1814'

def embleme(fond=None, cadre=OR, d=OR, seize=IVOIRE):
    plein = f'<rect x="24" y="24" width="152" height="152" rx="30" fill="{fond}"/>' if fond else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">{plein}'
            f'<rect x="24" y="24" width="152" height="152" rx="30" fill="none" stroke="{cadre}" stroke-width="1.3"/>'
            f'<rect x="30" y="30" width="140" height="140" rx="25" fill="none" stroke="{cadre}" stroke-width=".45" opacity=".55"/>'
            f'<text x="90" y="136" text-anchor="middle" font-family="Instrument Serif" font-size="116" fill="{d}">D</text>'
            f'<text x="134" y="136" text-anchor="middle" font-family="Instrument Serif" font-style="italic" font-size="42" fill="{seize}">16</text></svg>')

def signature(texte=IVOIRE, accent=OR):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 92">'
            f'<text x="4" y="58" font-family="Instrument Serif" font-size="60" fill="{texte}" letter-spacing="3">DIG'
            f'<tspan fill="{accent}" font-style="italic" dx="3" letter-spacing="0">16</tspan></text>'
            f'<line x1="6" y1="71" x2="233" y2="71" stroke="{accent}" stroke-width=".8"/>'
            f'<text x="6" y="86" font-family="Geist Mono" font-size="7.75" letter-spacing="4.55" fill="{texte}" opacity=".75">SITES INTERNET · CHARENTE</text></svg>')

FICHIERS = {
    'embleme-sombre': (embleme(fond='#0f0e0c'), 200, 200),   # icône d'appli, réseaux, favicon
    'embleme-or': (embleme(), 200, 200),                      # sur fond sombre, transparent
    'embleme-clair': (embleme(cadre=OR_FONCE, d=OR_FONCE, seize=ENCRE), 200, 200),
    'signature-ivoire': (signature(), 240, 92),               # sur fond sombre
    'signature-encre': (signature(texte=ENCRE, accent=OR_FONCE), 240, 92),  # sur fond clair
}

def main():
    os.makedirs(SORTIE, exist_ok=True)
    polices = '<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist+Mono:wght@400&display=block" rel="stylesheet">'
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        for nom, (svg, w, h) in FICHIERS.items():
            open(os.path.join(SORTIE, nom + '.svg'), 'w').write(svg)
            for echelle in (2, 6):
                pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=echelle)
                pg.set_content(f'<!doctype html><html><head><meta charset="utf-8">{polices}<style>html,body{{margin:0;background:transparent}}svg{{display:block;width:{w}px;height:{h}px}}</style></head><body>{svg}</body></html>', wait_until='networkidle')
                pg.wait_for_timeout(600)
                pg.screenshot(path=os.path.join(SORTIE, f'{nom}@{echelle}x.png'), omit_background=True)
                pg.close()
        # favicons et icône d'écran d'accueil (iPhone)
        for taille, nom in ((32, 'favicon-32.png'), (180, 'apple-touch-icon.png'), (512, 'icone-512.png')):
            pg = b.new_page(viewport={'width': taille, 'height': taille})
            sv = embleme(fond='#0f0e0c').replace('viewBox="0 0 200 200"', 'viewBox="20 20 160 160"')
            pg.set_content(f'<!doctype html><html><head><meta charset="utf-8">{polices}<style>html,body{{margin:0;background:#0f0e0c}}svg{{display:block;width:{taille}px;height:{taille}px}}</style></head><body>{sv}</body></html>', wait_until='networkidle')
            pg.wait_for_timeout(600)
            pg.screenshot(path=os.path.join(SORTIE, nom))
            pg.close()
        b.close()
    print('logo fabriqué dans', os.path.normpath(SORTIE))

if __name__ == '__main__':
    main()
