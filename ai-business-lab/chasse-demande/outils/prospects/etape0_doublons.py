# Étape 0 (02/10) : doublons d'un lot de candidats contre la feuille de suivi.
# Usage : python3 etape0_doublons.py <debut> <fin> <sortie.json> <dossier_de_travail>
# Le dossier de travail contient appels/suivi_appels.csv et verif8/cands.json (données privées, hors dépôt).
import json, csv, re, sys, unicodedata
S=sys.argv[4] if len(sys.argv)>4 else '.'
def norm(s):
    s=unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode().lower()
    s=re.sub(r'\b(sarl|sas|eurl|sasu|sa|snc|ei|le|la|les|l|du|de|des|d|et)\b',' ',s)
    return re.sub(r'[^a-z0-9]+','',s)
def tel9(t): d=re.sub(r'\D','',t or ''); return d[-9:] if len(d)>=9 else ''
rows=list(csv.DictReader(open(S+'/appels/suivi_appels.csv',encoding='utf-8')))
tels={}; noms={}
for r in rows:
    for k,v in r.items():
        if v and ('tel' in k.lower() or 'phone' in k.lower()):
            for t in re.findall(r'(?:\+33|0)[\d\s.]{8,}',v):
                t9=tel9(t)
                if t9: tels.setdefault(t9,r)
    for k in r:
        if any(x in k.lower() for x in ('nom','enseigne','prospect')):
            n=norm(r[k]); 
            if len(n)>=5: noms.setdefault(n,r)
a,b=int(sys.argv[1]),int(sys.argv[2])
cands=json.load(open(S+'/verif8/cands.json'))
out={}; dup=[]; flags={}
for i in range(a,b+1):
    c=cands[i]; t9=tel9(c.get('telephone',''))
    names=[c['nom']]+re.findall(r'\(([^)]+)\)',c['nom'])+([c['enseigne']] if c.get('enseigne') else [])
    hit=None
    nhit=None
    for n in names:
        nn=norm(n)
        if len(nn)>=5 and nn in noms: nhit=noms[nn]; break
    if nhit: hit=('nom',nhit)
    elif t9 and t9 in tels:
        r=tels[t9]; rn=norm(r.get('Entreprise',''))
        same=any(norm(n) and (norm(n) in rn or rn in norm(n)) for n in names)
        if same: hit=('tel',r)
        else: flags[str(i)]='téléphone du registre partagé avec n° %s (%s) : non fiable, à confirmer par un annuaire public'%(next((r[k] for k in r if k.lower().startswith('n')),'?'),r.get('Entreprise',''))
    if hit:
        r=hit[1]; num=next((r[k] for k in r if k.lower().startswith('n')),'?')
        dup.append((i,c['nom'],c['commune'],hit[0],num)); continue
    out[str(i)]=c['nom']
print('doublons',len(dup)); [print(' ',d) for d in dup]
print('à sonder',len(out)); print('drapeaux',flags)
json.dump(flags,open(sys.argv[3].replace('.json','_drapeaux.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=0)
json.dump(out,open(sys.argv[3],'w',encoding='utf-8'),ensure_ascii=False,indent=0)
