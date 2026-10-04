"""Synthèse du dimanche : index des fiches vidéo d'une chaîne (connaissances/<chaine>/SYNTHESE.md).

Pour chaque fiche <id>.md : le titre (première ligne « # ») et la thèse principale résumée par Gemini.
Usage : python3 outils/synthese_chaine.py <chaine> [<chaine> ...]   (ex. finary fintales melvynx)
"""
import datetime
import json
import os
import re
import sys

RACINE = os.path.join(os.path.dirname(__file__), '..', 'connaissances')
NOMS = {'finary': 'Finary', 'fintales': 'Fintales', 'melvynx': 'Melvynx', 'mreflow': 'Matt Wolfe',
        'gabzer': 'Gabzer', 'iaboss': 'IA Boss', 'unefille': 'Une fille'}
JOURS = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']


def these(texte):
    m = re.search(r'Th[èe]se principale\s*:?\**\s*:?\s*(.+)', texte, re.I)
    if not m:
        m = re.search(r'^(?!#|Vidéo|\(|Voici|---|\s*$)(.{60,})$', texte, re.M)
    if not m:
        return ''
    t = re.sub(r'[*_`]', '', m.group(1)).strip()
    return t if len(t) <= 280 else t[:278].rsplit(' ', 1)[0] + '…'


def synthese(chaine):
    dos = os.path.join(RACINE, chaine)
    fiches = sorted(f for f in os.listdir(dos) if f.endswith('.md') and f not in ('SYNTHESE.md', 'README.md'))
    total = '?'
    liste = os.path.join(dos, 'liste-videos.json')
    if os.path.exists(liste):
        total = len(json.load(open(liste, encoding='utf-8')).get('videos', []))
    lignes = []
    for f in fiches:
        t = open(os.path.join(dos, f), encoding='utf-8', errors='ignore').read()
        titre = (re.search(r'^# (.+)$', t, re.M) or [None, f[:-3]])[1].strip()
        th = these(t)
        lignes.append(f'- **[{titre}]({f})**' + (f' — {th}' if th else ''))
    lignes.sort(key=lambda s: s.lower())
    auj = datetime.date.today()
    tete = (f'# {NOMS.get(chaine, chaine)} — index des fiches (synthèse du {JOURS[auj.weekday()]} {auj:%d/%m/%Y})\n\n'
            f'{len(fiches)} vidéos résumées sur {total}. Pour chaque vidéo : la thèse principale, en une phrase, '
            'telle que résumée par Gemini.\n'
            'Connaissances générales **non vérifiées** : tout chiffre, plafond ou règle fiscale est revérifié à la '
            'source officielle avant d’être affirmé (voir `../README.md`).\n\n')
    open(os.path.join(dos, 'SYNTHESE.md'), 'w', encoding='utf-8').write(tete + '\n'.join(lignes) + '\n')
    print(chaine, len(fiches), '/', total)


if __name__ == '__main__':
    for c in sys.argv[1:]:
        synthese(c)
