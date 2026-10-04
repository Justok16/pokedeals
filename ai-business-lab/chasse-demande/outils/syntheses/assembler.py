# Assemble un document par chaîne (Markdown + HTML + PDF) à partir des synthèses par thème nettoyées.
import os, re, glob, markdown
from playwright.sync_api import sync_playwright
S = os.path.dirname(os.path.abspath(__file__))
NOMS = {
 'bourse_etf': 'Bourse et ETF', 'epargne_budget': 'Épargne et budget', 'assurance_vie_per_retraite': 'Assurance-vie, PER et retraite',
 'immobilier': 'Immobilier', 'fiscalite_succession_societe': 'Fiscalité, transmission et société', 'crypto': 'Cryptomonnaies',
 'alternatifs': 'Placements alternatifs (or, private equity, produits structurés, passion)', 'marches_macro': 'Marchés et économie',
 'strategie_psychologie': 'Stratégie et psychologie de l’investisseur', 'patrimoine_portraits': 'Portraits et analyses de patrimoines',
 'divers': 'Autres sujets', 'autres': 'Autres sujets (stratégie, immobilier, épargne, fiscalité)',
 'ia_chatbots': 'Intelligence artificielle', 'images_video_audio': 'Images, vidéo et son', 'internet_securite': 'Sites, internet et sécurité',
 'productivite_bureautique': 'Productivité et logiciels', 'apprendre_etudes': 'Apprendre et étudier', 'argent_business': 'Argent et petits business',
}
ORDRE = {
 'finary': ['epargne_budget', 'bourse_etf', 'assurance_vie_per_retraite', 'immobilier', 'fiscalite_succession_societe', 'crypto', 'alternatifs',
            'marches_macro', 'strategie_psychologie', 'patrimoine_portraits', 'divers'],
 'fintales': ['crypto', 'marches_macro', 'bourse_etf', 'autres'],
 'gabzer': ['argent_business', 'ia_chatbots', 'internet_securite', 'productivite_bureautique', 'images_video_audio', 'apprendre_etudes'],
}
TITRES = {'finary': 'Synthèse Finary', 'fintales': 'Synthèse Fintales', 'gabzer': 'Synthèse Gabzer'}
CSS = """
@page { size: A4; margin: 18mm 16mm 20mm; }
body { font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif; font-size: 10.5pt; line-height: 1.5; color: #1b1f24; background: #fff; }
h1 { font-size: 22pt; color: #0f2a44; margin: 0 0 6pt; }
h2 { font-size: 14pt; color: #0f2a44; border-bottom: 1.5pt solid #d8e1ea; padding-bottom: 3pt; margin-top: 18pt; break-after: avoid; }
h3 { font-size: 11.5pt; color: #1f4e79; margin-top: 12pt; break-after: avoid; }
h4 { font-size: 10.5pt; break-after: avoid; }
.theme { break-before: page; }
.theme > h1 { font-size: 17pt; background: #0f2a44; color: #fff; padding: 8pt 10pt; border-radius: 4pt; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; font-size: 9.5pt; break-inside: auto; }
th, td { border: 0.75pt solid #c9d3dd; padding: 4pt 6pt; vertical-align: top; text-align: left; }
th { background: #eef3f8; }
tr { break-inside: avoid; }
li { margin: 2pt 0; }
em { color: #44505c; }
hr { border: none; border-top: 0.75pt solid #d8e1ea; margin: 10pt 0; }
code { font-family: inherit; }
.sommaire li { margin: 1pt 0; }
"""
def md2html(t):
    return markdown.markdown(t, extensions=['tables', 'sane_lists'])
def demote(t):  # les synthèses Gemini utilisent ## et ### : on les garde sous le titre du thème
    if t.startswith('<!-- modèle'):  # première ligne technique ajoutée par lancer.py
        t = t.split('\n', 1)[1] if '\n' in t else ''
    t = re.sub(r'^(Voici|Pour conclure|Cette synthèse)[^\n]*\n', '', t.strip(), count=1)
    return t
for ch, themes in ORDRE.items():
    parties = []
    intro = os.path.join(S, f'intro_{ch}.md')
    if not os.path.exists(intro): print('intro manquante', ch); continue
    md = [open(intro).read()]
    if ch != 'gabzer':
        md += [open(os.path.join(S, 'regles_verifiees.md')).read(), open(os.path.join(S, 'regles_perimees.md')).read()]
    som = ['## Sommaire des thèmes', '']
    corps = []
    for i, th in enumerate(themes, 1):
        f = os.path.join(S, f'{ch}__{th}.propre.md')
        if not os.path.exists(f): print('thème manquant', ch, th); continue
        n = re.search(r'; (\d+) vidéos', open(os.path.join(S, f'{ch}__{th}.md')).read())
        n = n.group(1) if n else '?'
        som.append(f'{i}. {NOMS[th]} ({n} vidéos)')
        corps.append((f'Thème {i} : {NOMS[th]} ({n} vidéos)', demote(open(f).read())))
    md.append('\n'.join(som))
    full_md = '\n\n'.join(md) + '\n\n' + '\n\n'.join(f'# {t}\n\n{c}' for t, c in corps)
    open(os.path.join(S, f'Synthese-{ch}.md'), 'w').write(full_md)
    html = '<section>' + md2html('\n\n'.join(md)) + '</section>' + ''.join(
        f'<section class="theme"><h1>{t}</h1>{md2html(c)}</section>' for t, c in corps)
    page = f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{TITRES[ch]}</title><style>{CSS}</style></head><body>{html}</body></html>'
    hp = os.path.join(S, f'Synthese-{ch}.html'); open(hp, 'w').write(page)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        pg = b.new_page(); pg.goto('file://' + hp); pg.wait_for_timeout(300)
        pg.pdf(path=os.path.join(S, f'Dig-Synthese-{ch.capitalize()}.pdf'), format='A4', print_background=True,
               display_header_footer=True, header_template='<span></span>',
               footer_template=f'<div style="font-size:8px;width:100%;text-align:center;color:#888">{TITRES[ch]} · page <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
               margin={'top': '18mm', 'bottom': '20mm', 'left': '16mm', 'right': '16mm'})
        b.close()
    print('ok', ch, len(full_md))
