# Teste les noms de domaine probables d'une entreprise (DNS puis page HTTP) : repère un site que la recherche web aurait raté.
import re, sys, json, socket, unicodedata, subprocess, concurrent.futures as cf
VIDE = r'(domaine|domain).{0,40}(vente|sale|parked|parking)|site en construction|en maintenance|coming soon|index of /|default web site page|welcome to nginx|page par d[ée]faut|hébergé par|is for sale'
def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', t).split()
STOP = {'sarl','sas','sasu','eurl','sa','ets','etablissements','entreprise','societe','d','de','du','des','la','le','les','l','et','exploitation','fils','freres','generale','g'}
def candidats(nom):
    m = [w for w in slug(re.sub(r'\(.*?\)', '', nom)) if w not in STOP]
    tous = slug(nom)
    bases = {''.join(m), '-'.join(m), ''.join(tous), '-'.join(tous)}
    if len(m) > 1: bases |= {m[0] + m[-1], m[-1] + m[0], m[0]}
    # Sigles (leçon du 01/10 : « Sud Ouest Rénovations Constructions » = sorc16.fr) et nom sans le sigle
    # répété (« ADI Froid ADI Génie Climatique ADI » = adigenieclimatique.com)
    if len(m) >= 3: bases.add(''.join(w[0] for w in m))
    vus, sans_rep = set(), []
    for w in m:
        if w not in vus: vus.add(w); sans_rep.append(w)
    if len(sans_rep) >= 2: bases |= {''.join(sans_rep), '-'.join(sans_rep), ''.join(sans_rep[:3]), '-'.join(sans_rep[:3])}
    out = set()
    for b in bases:
        if len(b) < 4: continue
        for suf in ('', '16', '-16'):
            for tld in ('.fr', '.com'):
                out.add(b + suf + tld)
    return sorted(out)
def tester(d):
    try: socket.getaddrinfo(d, 443)
    except Exception: return None
    r = subprocess.run(['curl', '-s', '-L', '-m', '12', '-A', 'Mozilla/5.0', '-o', '-', '-w', '\n%{http_code} %{url_effective}', 'https://' + d], capture_output=True, text=True, errors='ignore').stdout
    corps, _, fin = r.rpartition('\n'); code = fin.split(' ')[0]
    titre = re.search(r'<title[^>]*>(.*?)</title>', corps, re.S | re.I)
    titre = re.sub(r'\s+', ' ', titre[1]).strip()[:80] if titre else ''
    vide = bool(re.search(VIDE, (titre + corps[:3000]).lower())) or len(corps) < 800
    return {'domaine': d, 'code': code, 'url': fin.split(' ', 1)[-1], 'titre': titre, 'vide_ou_parking': vide}
if __name__ == '__main__':
    noms = json.load(open(sys.argv[1]))
    res = {}
    with cf.ThreadPoolExecutor(16) as ex:
        for n, nom in noms.items():
            trouves = [x for x in ex.map(tester, candidats(nom)) if x]
            res[n] = trouves
            print(n, nom, '→', [(t['domaine'], t['code'], t['titre'][:40], 'VIDE' if t['vide_ou_parking'] else 'PAGE') for t in trouves] or 'aucun domaine', flush=True)
    json.dump(res, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
