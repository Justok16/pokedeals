import json,re,unicodedata,socket,urllib.request,concurrent.futures as cf,html,sys
# Usage : python3 devine_sites.py <département> — devine le domaine (.fr/.com) de chaque entreprise et vérifie la commune.
DEP=sys.argv[1]
UA='Mozilla/5.0 (DigEtudeMarche)'
STOP={'sarl','sas','sasu','eurl','earl','gaec','sa','sci','et','de','du','des','la','le','les','l','d','monsieur','madame','ets','etablissements','entreprise','societe','scea','snc','selarl','selas','m','mme','mr'}
def norm(s): return unicodedata.normalize('NFD',(s or '').lower()).encode('ascii','ignore').decode()
d=[r for r in json.load(open(f'reg{DEP}.json')) if r['categorie'] not in ('ETI','GE') and (r['nature'] or '')[:1] in ('1','5')]
print('cibles',len(d),flush=True)
def cands(r):
    noms=[r['nom']]+(r['enseignes'] or [])+([r['nom_commercial']] if r.get('nom_commercial') else [])+re.findall(r'\(([^)]+)\)',r['nom'])
    out=[]; com=re.sub(r'[^a-z0-9]+','-',norm(r['commune'])).strip('-')
    for n in noms:
        n=re.sub(r'\(.*?\)','',norm(n)); w=[x for x in re.findall(r'[a-z0-9]+',n) if x not in STOP]
        if not w: continue
        for base in dict.fromkeys([''.join(w),'-'.join(w)]):
            if len(base)<5: continue
            out+= [base+'.fr',base+'.com']
        if com and len(w)<=3: out.append('-'.join(w)+'-'+com+'.fr')
    return list(dict.fromkeys(out))[:10]
PARK=('domain is for sale','ce domaine est à vendre','parking','sedo','domaine en vente','this domain','godaddy.com/domainsearch','site en construction','coming soon')
def outil(t):
    t2=t.lower()
    for k,v in [('solocal','SoLocal'),('wix.com','Wix'),('wp-content','WordPress'),('jimdo','Jimdo'),('squarespace','Squarespace'),('webflow','Webflow'),('cdn-website.com','Duda'),('shopify','Shopify'),('site123','Site123'),('e-monsite','e-monsite'),('simplebo','Simplébo'),('pagesjaunes','PJ?'),('orange','Orange?')]:
        if k in t2: return v
    return 'autre'
def test(dom,r):
    try: socket.gethostbyname(dom)
    except Exception: return None
    for u in (f'https://{dom}/',f'https://www.{dom}/',f'http://{dom}/'):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=15) as x:
                t=x.read(500000).decode('utf-8','ignore'); fin=x.geturl()
        except Exception: continue
        tt=norm(html.unescape(t))
        lieu=(r['cp'] in tt) or (norm(r['commune']) in tt) or False
        an=re.findall(r'(?:©|&copy;|copyright)\s*(?:[^0-9<]{0,20})?(20\d\d)',t,re.I)
        return {'dom':dom,'final':fin,'lieu_ok':lieu,'parking':any(p in tt for p in PARK) and len(tt)<30000,'outil':outil(t),'copyright':max(an) if an else '',
                'titre':html.unescape((re.search(r'<title[^>]*>(.*?)</title>',t,re.S|re.I) or [None,''])[1]).strip()[:90]}
    return {'dom':dom,'final':'','lieu_ok':False,'parking':False,'outil':'','copyright':'','titre':'(DNS ok, page injoignable)'}
def un(r):
    res=[x for x in (test(dm,r) for dm in cands(r)) if x]
    r=dict(r); r['sites']=res; return r
out=[]
with cf.ThreadPoolExecutor(40) as ex:
    for i,x in enumerate(ex.map(un,d)):
        out.append(x)
        if i%1000==0: print(i,flush=True)
json.dump(out,open(f'devine{DEP}.json','w'),ensure_ascii=False)
print('confirmés',sum(1 for r in out if any(s['lieu_ok'] for s in r['sites'])),'domaine répond',sum(1 for r in out if r['sites']))
