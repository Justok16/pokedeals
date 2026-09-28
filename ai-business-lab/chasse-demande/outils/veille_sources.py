"""Veille quotidienne sur toutes les sources ajoutées par l'utilisateur (demande du 28/09/2026 :
« tous les sites, les outils, les chaînes que j'ai rajoutés […] vérifier dès qu'il y a du nouveau
et l'apprendre pour t'améliorer au fur et à mesure »).

Usage : python3 veille_sources.py cookies.txt
- Chaînes YouTube : chaque dossier connaissances/<chaine>/ qui a un liste-videos.json est relu
  par le relais (/api/chaine) ; les nouvelles vidéos passent en tête de liste. Pour les chaînes
  « triées » (clé "filtre" dans liste-videos.json), seules les nouvelles vidéos dont le titre
  correspond au filtre (et de 3 min ou plus) sont ajoutées à prio.json, la file de résumés.
- Annuaires d'outils (voir SOURCES) : la liste actuelle est comparée à la précédente
  (veille/etat/<source>.json) ; les nouveautés sont écrites dans le rapport du jour.
Rapport : veille/AAAA-MM-JJ.md (à lire au point automatique, puis trier selon
46-apprentissage-continu.md : appliquer ce qui est gratuit, légal et utile).
"""
import datetime, json, os, re, subprocess, sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, '..'))
CONNAISSANCES = os.path.join(RACINE, 'connaissances')
VEILLE = os.path.join(RACINE, 'veille')
ETAT = os.path.join(VEILLE, 'etat')
RELAIS = 'https://relais-dig-justok1.vercel.app/api/chaine?chaine='


def telecharger(url, cookies=None, delai=60):
    cmd = ['curl', '-s', '-L', '-m', str(delai), '-A', 'Mozilla/5.0']
    if cookies:
        cmd += ['-b', cookies]
    for _ in range(3):  # certains plans de site arrivent vides une fois sur deux : on réessaie
        sortie = subprocess.run(cmd + [url], capture_output=True, text=True, errors='ignore').stdout
        if sortie.strip():
            return sortie
    return ''


def secondes(d):
    t = 0
    for x in str(d).split(':'):
        t = t * 60 + int(x or 0)
    return t


# --- Annuaires d'outils : chacun renvoie {identifiant: libellé} -------------------------------
def nosignups():
    d = json.loads(telecharger('https://raw.githubusercontent.com/BraveOPotato/FckSignups/refs/heads/main/tools.json'))
    return {t['id']: f"{t['name']} — {t.get('description', '')[:100]} ({t['url']})" for t in d['tools']}


def futuretools():
    index = telecharger('https://futuretools.io/sitemap.xml')
    outils = {}
    for plan in re.findall(r'<loc>(https://futuretools\.io/sitemaps/tools-\d+\.xml)</loc>', index):
        for url in re.findall(r'<loc>([^<]+)</loc>', telecharger(plan)):
            outils[url] = url
    return outils


def free_for_dev():
    texte = telecharger('https://raw.githubusercontent.com/ripienaar/free-for-dev/master/README.md')
    lignes = [l.strip() for l in texte.splitlines() if l.strip().startswith('* [')]
    return {l[:160]: l[:300] for l in lignes}


def mrfreetools():
    index = telecharger('https://mrfreetools.com/sitemap.xml')
    outils = {}
    for plan in re.findall(r'<loc>(https://mrfreetools\.com/tool-sitemap\d*\.xml)</loc>', index):
        for url in re.findall(r'<loc>([^<]+)</loc>', telecharger(plan)):
            outils[url] = url
    return outils


SOURCES = {'nosignups': nosignups, 'futuretools': futuretools, 'free-for-dev': free_for_dev,
           'mrfreetools': mrfreetools}


def veille_outils(rapport):
    os.makedirs(ETAT, exist_ok=True)
    for nom, lire in SOURCES.items():
        try:
            actuel = lire()
        except Exception as e:
            rapport.append(f'- **{nom}** : lecture impossible ({str(e)[:80]})')
            continue
        if not actuel:
            rapport.append(f'- **{nom}** : liste vide (site modifié ou bloqué ?)')
            continue
        chemin = os.path.join(ETAT, nom + '.json')
        ancien = json.load(open(chemin)) if os.path.exists(chemin) else None
        # Mémoire cumulée : un élément déjà vu n'est jamais oublié (une lecture partielle d'un
        # plan de site ne doit pas faire réapparaître des outils anciens comme « nouveaux »).
        json.dump({**actuel, **(ancien or {})}, open(chemin, 'w'), ensure_ascii=False, separators=(',', ':'))
        if ancien is None:
            rapport.append(f'- **{nom}** : premier relevé ({len(actuel)} éléments), rien à comparer')
            continue
        nouveaux = [actuel[k] for k in actuel if k not in ancien]
        rapport.append(f'- **{nom}** : {len(nouveaux)} nouveauté(s) sur {len(actuel)}')
        rapport += [f'  - {n}' for n in nouveaux[:60]]
        if len(nouveaux) > 60:
            rapport.append(f'  - … et {len(nouveaux) - 60} autres (voir veille/etat/{nom}.json)')


def veille_chaines(cookies, rapport):
    for nom in sorted(os.listdir(CONNAISSANCES)):
        chemin = os.path.join(CONNAISSANCES, nom, 'liste-videos.json')
        if not os.path.exists(chemin):
            continue
        liste = json.load(open(chemin))
        try:
            neuve = json.loads(telecharger(RELAIS + liste['chaine'], cookies, 150))['videos']
        except Exception:
            rapport.append(f'- **{nom}** : lecture impossible (cookie du relais expiré ?)')
            continue
        connues = {v['id'] for v in liste['videos']}
        nouvelles = [v for v in neuve if v['id'] not in connues]
        if nouvelles:
            liste['videos'] = nouvelles + liste['videos']
            liste['nombre'] = len(liste['videos'])
            json.dump(liste, open(chemin, 'w'), ensure_ascii=False, separators=(',', ':'))
        ligne = f'- **{nom}** : {len(nouvelles)} nouvelle(s) vidéo(s)'
        if liste.get('filtre') and nouvelles:
            retenues = [v for v in nouvelles if secondes(v['duree']) >= liste.get('duree_min', 180)
                        and re.search(liste['filtre'], v['titre'], re.I)]
            p = os.path.join(CONNAISSANCES, nom, 'prio.json')
            prio = json.load(open(p)) if os.path.exists(p) else {'videos': []}
            deja = {v['id'] for v in prio['videos']}
            prio['videos'] = [v for v in retenues if v['id'] not in deja] + prio['videos']
            json.dump(prio, open(p, 'w'), ensure_ascii=False, indent=0)
            ligne += f', dont {len(retenues)} ajoutée(s) à la file de résumés'
        rapport.append(ligne)
        rapport += [f"  - {v['id']} ({v['duree']}) {v['titre']}" for v in nouvelles[:15]]


def main():
    cookies = sys.argv[1]
    jour = datetime.date.today().isoformat()
    rapport = [f'# Veille du {jour}', '', '## Chaînes YouTube', '']
    veille_chaines(cookies, rapport)
    rapport += ['', "## Annuaires d'outils", '']
    veille_outils(rapport)
    rapport += ['', 'Pages Facebook : connexion obligatoire pour lister les vidéos ; on surveille à la '
                'place la chaîne YouTube du même créateur quand elle existe (ex. reels « gabzermp4 » = '
                'YouTube @gabzer.mp4) ; un lien Facebook isolé se lit via m.facebook.com + /api/avis.']
    os.makedirs(VEILLE, exist_ok=True)
    open(os.path.join(VEILLE, jour + '.md'), 'w').write('\n'.join(rapport) + '\n')
    print('\n'.join(rapport))


if __name__ == '__main__':
    main()
