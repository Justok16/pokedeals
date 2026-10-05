"""Régénère supports/Dig-Campagne-lancement.pdf depuis 50-campagne-lancement.md
(règle « PDF toujours à jour » : relancer après toute modification de 50).

Usage : python3 outils/campagne_pdf.py
"""
import datetime, os, re
import markdown
from playwright.sync_api import sync_playwright
from plan_complet import STYLE, RACINE

EXTRA = """
input[type=checkbox]{margin-right:4px}
li{margin:2px 0} blockquote p{margin:4px 0} blockquote,.bloc{page-break-inside:avoid}
h2{page-break-after:avoid} h3{page-break-after:avoid}
table{page-break-inside:avoid}
"""


def main():
    jour = datetime.date.today().strftime('%d/%m/%Y')
    texte = open(os.path.join(RACINE, '50-campagne-lancement.md'), encoding='utf-8').read()
    texte = re.sub(r'^# .*\n', '', texte, count=1)
    texte = texte.replace('- [ ] ', '- ☐ ')
    corps = markdown.markdown(texte, extensions=['tables', 'sane_lists', 'md_in_html'])
    couverture = ('<div class=cover><h1>DIG16 — Campagne de lancement</h1>'
                  '<p>Budget 0 € · démarchage direct, visites, visibilité, recommandation</p>'
                  f'<p>Version du {jour}</p>'
                  '<p style="margin-top:30mm;color:#6b645a">Les listes de prospects et le suivi '
                  'nominatif sont dans des documents privés séparés.</p></div>')
    page = ('<!doctype html><html lang=fr><head><meta charset=utf-8><style>' + STYLE + EXTRA +
            '</style></head><body>' + couverture + '<section>' + corps + '</section></body></html>')
    sortie_html = os.path.join(RACINE, 'supports', 'campagne-lancement.html')
    open(sortie_html, 'w', encoding='utf-8').write(page)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg = b.new_page()
        pg.goto('file://' + sortie_html)
        pg.pdf(path=os.path.join(RACINE, 'supports', 'Dig-Campagne-lancement.pdf'), format='A4',
               print_background=True, prefer_css_page_size=True)
        b.close()
    print('Campagne régénérée :', sortie_html)


if __name__ == '__main__':
    main()
