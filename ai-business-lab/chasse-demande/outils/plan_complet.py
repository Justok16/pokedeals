"""Régénère supports/Dig-Plan-complet.pdf à partir des fichiers à jour du dossier
(règle « PDF toujours à jour » : relancer après toute modification de 39, 40, 41, 42 ou 36).

Usage : python3 outils/plan_complet.py
Produit supports/plan-complet.html puis supports/Dig-Plan-complet.pdf (A4) avec Playwright.
"""
import datetime, os, re
import markdown
from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, '..'))
PARTIES = [('39-business-plan-sites.md', 'Business plan'),
           ('40-cadre-legal-sites.md', 'Cadre légal'),
           ('41-prospection-questionnaire-et-textes.md', "Questionnaire et textes d'appel"),
           ('42-flyer-et-prompt.md', 'Flyer et prompts'),
           ('36-aides-creation.md', 'Aides à la création')]
STYLE = """
@page{size:A4;margin:16mm 14mm}
body{font-family:Inter,Arial,sans-serif;font-size:9.5pt;line-height:1.45;color:#1f1b16}
h1{font-size:17pt;color:#1f3b2d;border-bottom:2px solid #c98a4b;padding-bottom:4px}
h2{font-size:13pt;color:#1f3b2d;margin-top:16px} h3{font-size:11pt}
table{border-collapse:collapse;width:100%;margin:6px 0;font-size:8.3pt}
th{background:#1f3b2d;color:#fff;text-align:left;padding:3px 5px}
td{border-bottom:1px solid #e7e0d5;padding:3px 5px;vertical-align:top}
tr,img{page-break-inside:avoid}
blockquote{border-left:3px solid #c98a4b;margin:6px 0;padding:2px 10px;background:#faf7f2}
code{background:#f1e7da;padding:0 3px;border-radius:3px;word-break:break-all}
a{color:#1f3b2d;word-break:break-all} del{color:#8a8176}
section{page-break-before:always} .cover{text-align:center;padding-top:60mm}
.cover h1{border:0;font-size:30pt}
"""


def main():
    jour = datetime.date.today().strftime('%d/%m/%Y')
    corps = [f'<div class=cover><h1>DIG16 — Plan complet</h1>'
             '<p>Sites internet pour artisans, commerçants et indépendants</p>'
             f'<p>Version du {jour} (régénérée depuis les fichiers du dossier)</p>'
             '<ol style="text-align:left;display:inline-block">'
             + ''.join(f'<li>{t}</li>' for _, t in PARTIES) + '</ol>'
             '<p style="margin-top:30mm;color:#6b645a">Les listes de prospects et toute donnée '
             'personnelle sont dans des documents privés séparés.</p></div>']
    for fichier, _ in PARTIES:
        texte = open(os.path.join(RACINE, fichier), encoding='utf-8').read()
        texte = re.sub(r'~~(.+?)~~', r'<del>\1</del>', texte)
        html = markdown.markdown(texte, extensions=['tables', 'sane_lists'])
        corps.append(f'<section>{html}</section>')
    page = ('<!doctype html><html lang=fr><head><meta charset=utf-8><style>' + STYLE +
            '</style></head><body>' + ''.join(corps) + '</body></html>')
    sortie_html = os.path.join(RACINE, 'supports', 'plan-complet.html')
    open(sortie_html, 'w', encoding='utf-8').write(page)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg = b.new_page()
        pg.goto('file://' + sortie_html)
        pg.pdf(path=os.path.join(RACINE, 'supports', 'Dig-Plan-complet.pdf'), format='A4',
               print_background=True, prefer_css_page_size=True)
        b.close()
    print('Plan complet régénéré :', sortie_html)


if __name__ == '__main__':
    main()
