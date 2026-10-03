#!/usr/bin/env python3
"""Complément automatique de lot_rge.py pour les entreprises NON RGE d'un lot (02/10/2026, après-midi).

Pour chaque « candidat » ou « à vérifier » sans téléphone ADEME : liste des commerçants de sa commune sur
Mappy (données PagesJaunes), repérage de sa fiche par son enseigne, son nom ou le nom du dirigeant, lecture
des téléphones de la fiche et des sites qui y sont liés (un site lié est parfois celui d'un voisin : il n'est
retenu que si son titre ou son texte cite l'entreprise ou la commune ; une page edan.io / lany.io / eatbu /
wixsite / site-solocal « en construction » est une page générée ou gratuite, qui ne compte pas ; Planity,
dylentab, La Maison Officielle, TikTok, Facebook, Instagram = réservation ou réseau, ne comptent pas mais
peuvent donner le téléphone). Met à jour le pré-verdict et écrit appels/lot<N>_mappy.md.

Usage : python3 outils/prospects/mappy_lot.py <scratchpad> <numero_lot>
(appelé automatiquement en fin de lot_rge.py). Rien de ce qui est produit n'entre dans le dépôt public.
"""
import sys, os, re, json, time, html, subprocess, unicodedata

UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
RESEAU = r'planity\.com|dylentab\.fr|lamaisonofficielle\.fr|tiktok\.com|facebook\.com|instagram\.com|linkedin\.com|treatwell|lafourchette|thefork|ubereats|deliveroo'
# Page DÉDIÉE d'un réseau, d'une enseigne ou d'un constructeur (vérifié à la main lots 54 à 66) : le commerce
# a déjà une page à son nom dans un réseau → écarté. Une page de recherche générale (ad.fr/...recherche-garage?...)
# n'en est pas une.
DEDIE = (r'eurorepar\.fr/garage-|ad\.fr/garage-auto/(?!recherche|ville)|autoprimo\.com/(magasin|storelocator)|motrio\.fr/garage|'
         r'top-truck\.fr/distributeur|reseau\.garage-premier\.fr/\d|distinxion\.fr/distributeur|autofit|proximeca\.fr|'
         r'g-truck\.fr/.+/details|groupauto\.fr/.+/details|concessions\.(peugeot|citroen|renault)\.fr/|agents\.(peugeot|renault)\.fr/|'
         r'alombredesmarques\.fr/c/|komilfo\.fr/magasins/|artisansfleuristesdefrance\.com/(module|livraison)|casino\.fr/fr/stores/|'
         r'salon\.dessange\.com|jeanlouisdavid|franckprovost|saint-algue|feuvert\.fr|midas\.fr|speedy\.fr|norauto\.fr|vulco\.fr')
ENSEIGNE = r'\b(eurorepar|motrio|autoprimo|ad (garage|carrosserie|expert)|peugeot|renault|citro[eë]n|dessange|jean[- ]louis david|franck provost|top carrosserie|autofit|distinxion)\b'
GENERE = r'edan\.io|lany\.io|eatbu\.com|wixsite\.com|site-solocal\.com|business\.site|frmaps\.xyz|metro\.rest'
VIDES = ('sarl', 'sas', 'sasu', 'eurl', 'snc', 'sci', 'entreprise', 'ets', 'etablissements', 'societe', 'les', 'des', 'du', 'de', 'la', 'le', 'et', 'en', 'sur', 'saint', 'sainte', 'charente', 'coiffure', 'coiff', 'beaute', 'institut', 'garage', 'auto', 'boulangerie', 'restaurant', 'bar', 'salon')

def norm(s):
    s = unicodedata.normalize('NFKD', html.unescape(s or '')).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()

def slug(cp, commune):
    return f"{cp}-{norm(commune).replace(' ', '-')}"

def curl(url, t=25):
    return subprocess.run(['curl', '-sL', '-m', str(t), '-A', UA, url], capture_output=True, text=True, errors='ignore').stdout

def liste(s, cache):
    f = os.path.join(cache, s + '.json')
    if os.path.exists(f) and time.time() - os.path.getmtime(f) < 30 * 86400:
        return json.load(open(f))
    vus = {}
    for p in range(1, 150):
        h = curl(f'https://fr.mappy.com/poi/liste/{s}/page{p}')
        L = re.findall(r'href="/poi/([0-9a-f]{24})"[^>]*>([^<]{1,120})', h)
        new = [(i, html.unescape(n)) for i, n in L if i not in vus]
        if not new: break
        vus.update(new); time.sleep(0.15)
    json.dump(vus, open(f, 'w'), ensure_ascii=False)
    return vus

def cles(e):
    """Jeux de mots qui identifient l'entreprise : enseigne, nom sans parenthèses, nom du dirigeant."""
    nom = e['nom']; jeux = []
    for ens in re.findall(r'\(([^)]+)\)', nom): jeux.append(norm(ens))
    jeux.append(norm(re.sub(r'\s*\([^)]*\)', '', nom)))
    dir_ = (e.get('pappers') or {}).get('dirigeants') or ''
    for d in dir_.split(','):
        w = [x for x in norm(d).split() if len(x) >= 3]
        if w: jeux.append(' '.join(w))
    return [j for j in jeux if j]

def score(jeu, cand):
    """Correspondance entre un jeu de mots et un nom de fiche Mappy."""
    c = norm(cand); cw = set(c.split())
    if jeu and jeu in c: return 3
    court = ' '.join(w for w in jeu.split() if w not in VIDES)
    if court and len(court) >= 3 and (' ' + court + ' ') in (' ' + c + ' '): return 2
    mots = [w for w in jeu.split() if len(w) >= 4 and w not in VIDES]
    if not mots: return 0
    k = sum(w in cw for w in mots)
    if k >= 2 or (k == 1 and len(mots) == 1 and len(mots[0]) >= 5): return 2
    if k == 1 and any(w in cw and len(w) >= 5 for w in mots): return 1
    return 0

def fiche(id_):
    h = curl(f'https://fr.mappy.com/poi/{id_}')
    i = h.find(f'"id":"{id_}"'); seg = h[i:i + 6000] if i >= 0 else ''
    # La page liste aussi les fiches voisines : on coupe au début de la fiche suivante,
    # sinon leurs numéros et sites seraient attribués à tort à cette fiche.
    suiv = re.search(r'"id":"[0-9a-f]{24}"', seg[10:])
    if suiv: seg = seg[:10 + suiv.start()]
    tels = re.findall(r'"phone":\{"number":"([^"]+)","againstDirectMarketing":(true|false)', seg)
    webs = [w for w in re.findall(r'"(?:website|webSite|siteWeb|url)":"(https?://[^"]+)"', seg)
            if not re.search(r'pagesjaunes\.fr/media|mappy|partoo|qualit-enr|qualibat|pano\.mappy', w)]
    adr = re.search(r'"way":"([^"]*)"', h); cp = re.search(r'"postcode":"(\d+)"', h); ville = re.search(r'"town":"([^"]+)"', h)
    act = re.search(r'"url":"/activite/([^"/]+)', seg)
    return {'id': id_, 'tels': [t for t, _ in tels][:3], 'refus': any(r == 'true' for _, r in tels),
            'webs': list(dict.fromkeys(webs))[:4], 'adresse': f"{adr[1] if adr else ''} {cp[1] if cp else ''} {ville[1] if ville else ''}".strip(),
            'activite': act[1] if act else ''}

def classer_site(url, e):
    """Un site lié à une fiche : réseau/réservation, page générée, site vivant plausible, site d'un voisin, mort."""
    if re.search(DEDIE, url, re.I): return {'url': url, 'etat': "page dédiée d'un réseau (écarté)"}
    if re.search(RESEAU, url):
        tel = ''
        if re.search(r'planity|dylentab|lamaisonofficielle|treatwell', url):
            h = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', curl(url, 20), flags=re.S)
            cands = re.findall(r'(?<!\d)(0[1-9](?:[ .]?\d\d){4})(?!\d)', re.sub(r'<[^>]+>', ' ', h)) + re.findall(r'(0[1-9]\d{8})(?!\d)', url)
            cands = [re.sub(r'\D', '', c) for c in cands]
            cands = [c for c in cands if not re.search(r'(\d)\1{3,}', c) and c[:2] not in ('08', '00') and len(set(c[2:])) > 2]
            tel = re.sub(r'(\d\d)(?=\d)', r'\1 ', cands[0]) if cands else ''
        return {'url': url, 'etat': 'réservation ou réseau (ne compte pas)' + (' — téléphone affiché' if tel else ''), 'tel': tel}
    if re.search(GENERE, url): return {'url': url, 'etat': 'page générée ou gratuite (ne compte pas)'}
    if re.search(r'booking\.com|bstatic\.com|airbnb|tripadvisor|pagesjaunes\.fr|118712|118000|annuaire|mappy|google\.', url): return {'url': url, 'etat': 'annuaire ou plateforme (ne compte pas)'}
    r = subprocess.run(['curl', '-sL', '-m', '20', '-A', UA, '-o', '-', '-w', '\n%{http_code}', url], capture_output=True, text=True, errors='ignore').stdout
    corps, _, code = r.rpartition('\n')
    if code in ('', '000'): return {'url': url, 'etat': 'muet (ne répond pas au relais : à confirmer par Firecrawl, peut être un site vivant)'}
    if code[0] in '45': return {'url': url, 'etat': f'erreur HTTP {code}'}
    t = re.search(r'<title[^>]*>(.*?)</title>', corps, re.S | re.I); titre = re.sub(r'\s+', ' ', html.unescape(t[1])).strip()[:90] if t else ''
    texte = norm(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', corps, flags=re.S))[:40000])
    if re.search(r'site en cours de creation|en construction|coming soon|site en construction', texte): return {'url': url, 'etat': 'site en construction (ne compte pas)', 'titre': titre}
    mots = {w for j in cles(e) for w in j.split() if len(w) >= 4 and w not in VIDES}
    com = {w for w in norm(e['commune']).split() if len(w) >= 4 and w not in VIDES}
    mt = set(texte.split()); dom = norm(re.sub(r'^https?://(www\.)?', '', url).split('/')[0]); tit = set(norm(titre).split())
    # mots entiers seulement (« allo » ne doit pas valider « allons ») ; le nom doit être dans le titre ou le domaine
    ok_titre = any(w in tit or w in dom.replace(' ', '') or w in dom for w in mots)
    ok_texte = any(w in mt for w in mots); ok_com = any(w in mt or w in tit for w in com)
    if ok_titre and ok_com: etat = 'site vivant à son nom'
    elif ok_titre: etat = 'site vivant à vérifier (nom dans le titre, commune absente)'
    elif ok_texte and ok_com: etat = 'site vivant à vérifier (nom dans le texte seulement)'
    elif ok_com: etat = "site d'un voisin probable (commune citée, nom absent)"
    else: etat = "site d'un voisin ou sans rapport"
    return {'url': url, 'etat': etat, 'titre': titre}

def main():
    S, lot = sys.argv[1], sys.argv[2]
    app = os.path.join(S, 'appels'); cache = os.path.join(app, 'mappy_cache'); os.makedirs(cache, exist_ok=True)
    out = json.load(open(os.path.join(app, f'lot{lot}.json')))
    lignes = []
    for n, e in out.items():
        v = e.get('pre_verdict', '')
        if not (v.startswith('candidat') or v.startswith('à vérifier')) or e.get('ademe', {}).get('tels'): continue
        cp = re.search(r'\b(\d{5})\b', e.get('adresse') or ''); cp = cp[1] if cp else '16000'
        s = slug(cp, e['commune']); L = liste(s, cache)
        jeux = cles(e)
        meilleurs = sorted(((max(score(j, nom) for j in jeux), i, nom) for i, nom in L.items()), reverse=True)
        meilleurs = [m for m in meilleurs if m[0] > 0][:3]
        m = {'slug': s, 'fiches_commune': len(L), 'candidats': [(sc, nom) for sc, _, nom in meilleurs], 'fiche': None, 'sites': []}
        if meilleurs:
            sc, id_, nom = meilleurs[0]
            f = fiche(id_); f['nom_fiche'] = nom; f['score'] = sc; m['fiche'] = f; time.sleep(0.3)
            m['sites'] = [classer_site(u, e) for u in f['webs']]
        e['mappy'] = m
        vivants = [x for x in m['sites'] if x['etat'] == 'site vivant à son nom']
        douteux = [x for x in m['sites'] if x['etat'].startswith('site vivant à vérifier')]
        reseaux = [x for x in m['sites'] if x['etat'].startswith('page dédiée')]
        ens = re.search(ENSEIGNE, norm(m['fiche']['nom_fiche'])) if m['fiche'] else None
        if vivants: nv = 'écarté : site lié sur Mappy ' + ', '.join(x['url'] for x in vivants)
        elif reseaux: nv = 'écarté : page dédiée d\'un réseau ' + ', '.join(x['url'] for x in reseaux)
        elif ens and sc >= 2: nv = 'écarté : enseigne de réseau sur la fiche Mappy (« ' + m['fiche']['nom_fiche'] + ' »)'
        elif not meilleurs: nv = 'à vérifier : introuvable sur Mappy (' + str(len(L)) + ' fiches dans la commune) — recherche web'
        elif douteux: nv = 'à vérifier : site lié ' + ', '.join(x['url'] for x in douteux)
        elif m['fiche']['refus']: nv = 'écarté : refus du démarchage (PagesJaunes)'
        elif sc <= 1 and m['fiche']['tels']: nv = 'à vérifier : fiche Mappy probable « ' + m['fiche']['nom_fiche'] + ' » (un seul mot en commun)'
        elif m['fiche']['tels']: nv = 'candidat (Mappy : téléphone trouvé' + (', fiche ' + m['fiche']['nom_fiche'] if sc < 3 else '') + ')'
        elif any(x.get('tel') for x in m['sites']): nv = 'candidat (téléphone lu sur la page de réservation, à confirmer au premier appel)'
        else: nv = 'à vérifier : fiche Mappy sans numéro'
        e['pre_verdict_mappy'] = nv
        if not v.startswith('à vérifier : domaine') or nv.startswith('écarté'): e['pre_verdict'] = nv
        lignes.append((n, e))
        print(f"{n} {e['nom'][:34]:34} | {nv[:80]:80} | {len(m['fiche']['tels']) if m['fiche'] else 0} tél.")
    json.dump(out, open(os.path.join(app, f'lot{lot}.json'), 'w'), ensure_ascii=False, indent=1)
    with open(os.path.join(app, f'lot{lot}_mappy.md'), 'w') as f:
        f.write(f"# Lot {lot} : complément Mappy pour les non-RGE ({time.strftime('%d/%m/%Y %H:%M')})\n\n| idx | Entreprise | Fiche Mappy (score) | Téléphones | Adresse Mappy | Sites liés | Pré-verdict |\n|---|---|---|---|---|---|---|\n")
        for n, e in lignes:
            m = e['mappy']; fi = m['fiche'] or {}
            tels = list(fi.get('tels', [])) + [x['tel'] + ' (réservation)' for x in m['sites'] if x.get('tel')]
            f.write(f"| {n} | {e['nom']} | {fi.get('nom_fiche', '—')} ({fi.get('score', 0)}) ; autres : {', '.join(nm for sc, nm in m['candidats'][1:])} | {' / '.join(tels)} | {fi.get('adresse', '')} | {'<br>'.join(x['url'] + ' → ' + x['etat'] for x in m['sites'])} | {e['pre_verdict_mappy']} |\n")
    k = lambda p: sum(1 for _, e in lignes if e['pre_verdict_mappy'].startswith(p))
    print('Mappy : candidats avec téléphone :', k('candidat'), '| à vérifier :', k('à vérifier'), '| écartés :', k('écarté'))

if __name__ == '__main__':
    main()
