# Construit un nouveau vivier de candidats (02/10/2026) à partir du registre d'un département (reg<dép>.json de registre.py)
# et de la détection de sites (devine<dép>.json de devine_sites.py), en écartant les SIRET déjà présents dans des viviers
# antérieurs et les noms déjà dans la feuille de suivi. Le téléphone n'est pas requis : il est cherché dans les annuaires
# publics au moment de la vérification une par une.
# Usage : python3 construire_vivier.py <reg.json> <devine.json> <sortie.json> [--exclure ancien1.json,ancien2.json] [--suivi suivi_appels.csv] [--max 300]
import json, sys, re, unicodedata, csv, datetime, argparse
p=argparse.ArgumentParser(); p.add_argument('reg'); p.add_argument('devine'); p.add_argument('sortie')
p.add_argument('--exclure',default=''); p.add_argument('--suivi',default=''); p.add_argument('--max',type=int,default=300)
a=p.parse_args()
def norm(s):
    s=(s or '').replace('’',"'").replace("'",' ')
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    s=re.sub(r'\b(sarl|sas|eurl|sasu|sa|snc|ei|le|la|les|l|du|de|des|d|et)\b',' ',s)
    return re.sub(r'[^a-z0-9]+','',s)
reg=json.load(open(a.reg)); dev={d.get('siret'):d for d in json.load(open(a.devine))}
used=set()
for f in filter(None,a.exclure.split(',')):
    for x in json.load(open(f)): used.add(x.get('siret'))
noms=set()
if a.suivi:
    for r in csv.DictReader(open(a.suivi,encoding='utf-8')):
        n=norm(r.get('Entreprise','')); 
        if len(n)>=5: noms.add(n)
# secteurs visés (préfixe NAF) et leur libellé ; les holdings, l'immobilier, l'agriculture et les particuliers sont exclus
SECT={'43':'Bâtiment','41':'Construction','33':'Réparation industrielle','45':'Garage / auto','47':'Commerce','56':'Restauration',
      '96':'Coiffure / beauté / services','10':'Alimentation artisanale','81':'Paysagiste','95':'Réparation','71':'Bureau d\'études',
      '74':'Services spécialisés','49':'Transport','55':'Hébergement','31':'Ameublement','25':'Métallerie','32':'Fabrication','85':'Formation','86':'Santé','90':'Création'}
EFF={'00':0,'NN':0,'01':1,'02':3,'03':6,'11':10,'12':20,'21':50,'22':100}
auj=datetime.date.today()
out=[]
for x in reg:
    if x['siret'] in used: continue
    naf=x.get('naf') or ''; sect=SECT.get(naf[:2])
    if not sect: continue
    if naf in ('70.10Z','68.20B','68.20A','68.31Z','55.20Z') : continue   # holdings, immobilier, meublés de particuliers
    d=dev.get(x['siret'],{})
    if d.get('site'): continue
    nom=x.get('nom') or ''; ens=x.get('enseignes') or x.get('nom_commercial') or ''
    cles=[nom]+re.findall(r'\(([^)]+)\)',nom)+([ens] if isinstance(ens,str) else list(ens or []))
    if any(len(norm(n))>=5 and norm(n) in noms for n in cles): continue
    eff=EFF.get(str(x.get('effectif') or 'NN'),0)
    try: age=(auj-datetime.date.fromisoformat(x['creation'][:10])).days/365
    except Exception: age=0
    sc=0; r=[]
    if 1<=eff<=19: sc+=25; r.append('a des salariés (budget)')
    elif eff==0: sc+=5
    else: sc-=10; r.append('grande entreprise (souvent une agence)')
    if age>=2: sc+=10; r.append('installée depuis plus de 2 ans')
    if age<1: sc+=8; r.append('entreprise récente (bon moment pour un site)')
    if x.get('rge'): sc+=10; r.append('RGE')
    if naf[:2] in ('43','45','56','96','10','81','47','41'): sc+=10
    if isinstance(ens,str) and ens: sc+=5; r.append('a une enseigne')
    if x.get('employeur')=='O': sc+=5
    out.append({'score':sc,'nom':nom+(f' ({ens})' if isinstance(ens,str) and ens and ens.lower() not in nom.lower() else ''),'enseigne':ens if isinstance(ens,str) else '',
        'activite':f'{sect} ({naf})','commune':x.get('commune',''),'cp':x.get('cp',''),'adresse':x.get('adresse',''),'telephone':'',
        'dirigeant':', '.join(str(z.get('nom',z)) if isinstance(z,dict) else str(z) for z in (x.get('dirigeants') or [])[:2]),
        'creation':x.get('creation',''),'salaries':str(x.get('effectif') or ''),'rge':x.get('rge') or '','presence_web':d.get('presence_web','non testé'),'site':'',
        'raisons':', '.join(r),'lien_maps':'https://www.google.com/maps/search/?api=1&query='+re.sub(r'\s+','+',(ens if isinstance(ens,str) and ens else nom)+' '+x.get('commune','')),'siret':x['siret']})
out.sort(key=lambda z:(-z['score'],z['nom']))
json.dump(out[:a.max],open(a.sortie,'w'),ensure_ascii=False,indent=0)
import collections
print('candidats retenus',min(len(out),a.max),'sur',len(out),'; scores',out[0]['score'] if out else None,'→',out[min(len(out),a.max)-1]['score'] if out else None)
print(collections.Counter(z['activite'].split(' (')[0] for z in out[:a.max]).most_common())
