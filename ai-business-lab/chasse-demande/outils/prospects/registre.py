import json,subprocess,time,sys
# Usage : python3 registre.py <département>  (ex. 79). Passe par le relais Vercel (cookie cj.txt).
DEP=sys.argv[1]
B="https://relais-dig-justok1.vercel.app/api/cc"
NAF="""41.20A 41.20B 43.11Z 43.12A 43.12B 43.21A 43.22A 43.22B 43.29A 43.29B 43.31Z 43.32A 43.32B 43.32C 43.33Z 43.34Z 43.39Z 43.91A 43.91B 43.99A 43.99B 43.99C 43.99D 43.99E
45.11Z 45.20A 45.20B 45.32Z 45.40Z 55.10Z 55.20Z 55.30Z 56.10A 56.10B 56.10C 56.21Z 56.30Z 96.02A 96.02B 96.04Z 96.09Z 96.01B
10.13B 10.71C 10.71D 47.22Z 47.76Z 47.24Z 81.30Z 81.29A 74.20Z 49.32Z 95.11Z 95.12Z 95.21Z 95.22Z 95.23Z 95.24Z 95.25Z 95.29Z 33.12Z
16.23Z 25.11Z 25.12Z 31.09B 77.39Z 93.13Z 85.53Z 96.03Z 47.78C 47.71Z 47.52A 47.30Z 01.30Z 71.12B 49.41B 38.11Z 43.13Z 32.12Z 18.12Z 80.20Z""".split()
out=[];vu=set()
def get(url):
    for t in range(5):
        r=subprocess.run(['curl','-s','-m','60','-b','cj.txt',url],capture_output=True,text=True).stdout
        try: return json.loads(r)
        except Exception: time.sleep(3*(t+1))
    return None
for naf in NAF:
    p=1
    while True:
        d=get(f"{B}?chemin=entreprises&departement={DEP}&activite_principale={naf}&etat_administratif=A&per_page=25&page={p}")
        if d is None: print('échec',naf,p,file=sys.stderr); break
        for e in d['results']:
            for et in e.get('matching_etablissements',[]):
                if (et.get('code_postal') or '')[:2]!=DEP or et.get('etat_administratif')!='A' or et['siret'] in vu: continue
                vu.add(et['siret'])
                out.append({'siren':e['siren'],'siret':et['siret'],'nom':e['nom_complet'],'enseignes':et.get('liste_enseignes'),'nom_commercial':et.get('nom_commercial'),
                 'naf':et.get('activite_principale') or naf,'nature':e.get('nature_juridique'),'categorie':e.get('categorie_entreprise'),
                 'adresse':et.get('adresse'),'cp':et.get('code_postal'),'commune':et.get('libelle_commune'),'creation':et.get('date_creation'),
                 'effectif':et.get('tranche_effectif_salarie'),'employeur':et.get('caractere_employeur'),'siege':et.get('est_siege'),
                 'diffusion':e.get('statut_diffusion'),'rge':bool(et.get('liste_rge')),'ei':e.get('complements',{}).get('est_entrepreneur_individuel'),
                 'finances':e.get('finances'),'dirigeants':[(x.get('prenoms','') or '')+' '+(x.get('nom') or '')+' — '+(x.get('qualite') or '') for x in e.get('dirigeants',[]) if x.get('type_dirigeant')=='personne physique'][:2],
                 'lat':et.get('latitude'),'lon':et.get('longitude')})
        if p>=d.get('total_pages',1) or p>=400: break
        p+=1; time.sleep(0.25)
    print(naf,len(out),flush=True)
json.dump(out,open(f'reg{DEP}.json','w'),ensure_ascii=False)
print('TOTAL',len(out))
