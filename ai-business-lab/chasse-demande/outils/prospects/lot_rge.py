#!/usr/bin/env python3
"""Pré-vérification automatique d'un lot d'artisans RGE tirés d'un vivier (02/10/2026).

Enchaîne en une commande ce qui se faisait en six étapes : étape 0 (doublons), annuaire RGE de l'ADEME
par SIRET (téléphone fiable, fin de validité, site déclaré), test des sites déclarés et des domaines
probables (curl), registre + BODACC (verif_entreprises.py), fiche Pappers (opposition, radiation,
effectif, dirigeant, création, activité). Produit un JSON et un tableau Markdown de pré-verdicts.
Il reste à faire à la main : la recherche web « nom + commune » pour les candidats restants et la fiche.

Usage :
  python3 outils/prospects/lot_rge.py <scratchpad> <vivier.json> <debut> <fin> <numero_lot> [/tmp/cj.txt]
Résultats : <scratchpad>/appels/lot<numero>.json et lot<numero>.md ; pages Pappers dans appels/pappers<numero>/.
Rien de ce que produit cet outil n'entre dans le dépôt public (données de prospects = Drive « Dig »).
"""
import sys, os, json, re, html, time, subprocess, urllib.request, urllib.parse

VIDE = r'(domaine|domain).{0,40}(vente|sale|parked|parking)|site en construction|en maintenance|coming soon|index of /|default web site page|welcome to nginx|page par d[ée]faut|is for sale|dovendi'
UA = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15']

def texte(h):
    h = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', h, flags=re.S)
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h)))

def ademe(siret):
    url = ('https://data.ademe.fr/data-fair/api/v1/datasets/liste-des-entreprises-rge-2/lines?size=30&'
           + urllib.parse.urlencode({'qs': f'siret:"{siret}"'}))
    try:
        res = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA[0]}), timeout=30)).get('results', [])
    except Exception as e:
        return {'erreur': str(e)[:80]}
    fins = sorted({x.get('lien_date_fin') for x in res if x.get('lien_date_fin')})
    return {'tels': sorted({x.get('telephone') for x in res if x.get('telephone')}),
            'fin': fins[-1] if fins else None,
            'sites': sorted({x.get('site_internet') for x in res if x.get('site_internet') and 'qualit-enr' not in x.get('site_internet')}),
            'domaines': sorted({str(x.get('domaine'))[:30] for x in res}),
            'organismes': sorted({x.get('organisme') for x in res if x.get('organisme')})}

def site(url):
    """Teste un site déclaré : vivant / vide ou parking / mort."""
    u = url if url.startswith('http') else 'http://' + url
    if not re.search(r'\.[a-z]{2,}(/|$)', u.split('//', 1)[-1]):
        return {'url': url, 'etat': 'adresse invalide'}
    r = subprocess.run(['curl', '-sL', '-m', '20', '-A', UA[0], '-o', '-', '-w', '\n%{http_code} %{url_effective}', u],
                       capture_output=True, text=True, errors='ignore').stdout
    corps, _, fin = r.rpartition('\n')
    code = fin.split(' ')[0] if fin else '000'
    titre = re.search(r'<title[^>]*>(.*?)</title>', corps, re.S | re.I)
    titre = re.sub(r'\s+', ' ', titre[1]).strip()[:80] if titre else ''
    if code in ('000', '') : etat = 'mort (ne répond pas)'
    elif code.startswith('4') or code.startswith('5'): etat = f'erreur HTTP {code}'
    elif re.search(VIDE, (titre + corps[:3000]).lower()) or len(corps) < 800: etat = 'vide ou parking'
    else: etat = 'vivant'
    return {'url': url, 'code': code, 'titre': titre, 'etat': etat, 'final': fin.split(' ', 1)[-1] if ' ' in fin else ''}

def pappers(siren, dest):
    for k in range(3):
        code = subprocess.run(['curl', '-sL', '-m', '40', '-A', UA[k % 2], '-w', '%{http_code}', '-o', dest,
                               f'https://www.pappers.fr/entreprise/{siren}'], capture_output=True, text=True).stdout
        if code == '200': break
        time.sleep(20)
    tt = texte(open(dest, errors='ignore').read())
    g = lambda rx: (re.search(rx, tt) or [None, None])[1]
    return {'http': code, 'opposition': "opposée à l" in tt, 'radie': bool(re.search(r'RADI[ÉE]', tt)),
            'effectif': (g(r'Effectif\s*:\s*([^(]{0,30})') or '').strip() or None,
            'dirigeants': (g(r'Dirigeants?\s*:\s*(.{0,90}?) (?:Voir|Informations)') or '').strip() or None,
            'creation': g(r'Date de création\s*:\s*(\d\d/\d\d/\d{4})'),
            'activite': (g(r'Activité principale déclarée\s*:\s*(.{0,120})') or '').strip() or None}

def main():
    S, vivier, a, b, lot = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    cookies = sys.argv[6] if len(sys.argv) > 6 else '/tmp/cj.txt'
    ici = os.path.dirname(os.path.abspath(__file__))
    app = os.path.join(S, 'appels'); os.makedirs(os.path.join(app, f'pappers{lot}'), exist_ok=True)
    c = json.load(open(vivier))
    # étape 0 : doublons
    r0 = subprocess.run(['python3', os.path.join(app, 'etape0.py'), str(a), str(b), f'sonder{lot}_in.json', S, vivier],
                        cwd=app, capture_output=True, text=True).stdout
    print(r0.strip())
    a_sonder = json.load(open(os.path.join(app, f'sonder{lot}_in.json')))
    drapeaux = json.load(open(os.path.join(app, f'sonder{lot}_in_drapeaux.json')))
    # domaines probables
    subprocess.run(['python3', os.path.join(ici, 'sonder_domaines.py'), f'sonder{lot}_in.json', f'sonder{lot}.json'], cwd=app, capture_output=True)
    sondes = dict(json.load(open(os.path.join(app, f'sonder{lot}.json'))))
    # registre + BODACC
    json.dump([{'n': n, 'nom': c[int(n)]['nom'], 'commune': c[int(n)]['commune'], 'siren': c[int(n)]['siret'][:9]} for n in a_sonder],
              open(os.path.join(app, f'entree{lot}.json'), 'w'), ensure_ascii=False)
    subprocess.run(['python3', os.path.join(ici, '..', 'verif_entreprises.py'), f'entree{lot}.json', f'sortie{lot}.json', cookies, '16'], cwd=app, capture_output=True)
    reg = {x['n']: x for x in json.load(open(os.path.join(app, f'sortie{lot}.json')))}
    out = {}
    for n in a_sonder:
        i = int(n); e = c[i]
        d = {'nom': e['nom'], 'commune': e['commune'], 'adresse': e.get('adresse'), 'siret': e['siret'], 'naf': e.get('activite'),
             'drapeau': drapeaux.get(n), 'registre': reg.get(n, {}).get('etat'), 'bodacc': reg.get(n, {}).get('bodacc', [])}
        d['ademe'] = ademe(e['siret']); time.sleep(1)
        d['sites_declares'] = [site(u) for u in d['ademe'].get('sites', [])]
        d['domaines_vivants'] = [x for x in sondes.get(n, []) if x.get('code') == '200' and not x.get('vide_ou_parking')]
        d['pappers'] = pappers(e['siret'][:9], os.path.join(app, f'pappers{lot}', f'{i}.html')); time.sleep(4)
        # pré-verdict
        p = d['pappers']
        if d['registre'] not in (None, 'A') or d['bodacc']: v = 'écarté : registre/BODACC'
        elif p['opposition']: v = 'écarté : opposition'
        elif p['radie']: v = 'écarté : radié (vérifier)'
        elif any(s['etat'] == 'vivant' for s in d['sites_declares']): v = 'écarté : site vivant ' + ', '.join(s['url'] for s in d['sites_declares'] if s['etat'] == 'vivant')
        elif d['domaines_vivants']: v = 'à vérifier : domaine probable vivant ' + ', '.join(x['domaine'] for x in d['domaines_vivants'])
        elif d['drapeau']: v = 'à vérifier : ' + d['drapeau']
        elif d['sites_declares']: v = 'candidat « Sans site » (site déclaré ' + '; '.join(s['etat'] for s in d['sites_declares']) + ')'
        else: v = 'candidat (recherche web à faire)'
        d['pre_verdict'] = v
        out[n] = d
        print(f"{n} {e['nom'][:34]:34} | {v[:60]:60} | tel {','.join(d['ademe'].get('tels', []))} | RGE {d['ademe'].get('fin')} | {p['effectif']} | {p['dirigeants']} | {p['creation']}")
    json.dump(out, open(os.path.join(app, f'lot{lot}.json'), 'w'), ensure_ascii=False, indent=1)
    with open(os.path.join(app, f'lot{lot}.md'), 'w') as f:
        f.write(f"# Lot {lot} : index {a} à {b} (pré-verdicts automatiques, {time.strftime('%d/%m/%Y %H:%M')})\n\n| idx | Entreprise | Commune | Pré-verdict | Tél. ADEME | RGE jusqu'au | Effectif | Dirigeants | Création | Adresse |\n|---|---|---|---|---|---|---|---|---|---|\n")
        for n, d in out.items():
            f.write(f"| {n} | {d['nom']} | {d['commune']} | {d['pre_verdict']} | {', '.join(d['ademe'].get('tels', []))} | {d['ademe'].get('fin')} | {d['pappers']['effectif']} | {d['pappers']['dirigeants']} | {d['pappers']['creation']} | {d['adresse']} |\n")
    print('candidats :', sum(1 for d in out.values() if d['pre_verdict'].startswith('candidat')), '| à vérifier :', sum(1 for d in out.values() if d['pre_verdict'].startswith('à vérifier')))

if __name__ == '__main__':
    main()
