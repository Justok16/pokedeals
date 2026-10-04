import json,glob,subprocess,os,sys,time
S=os.path.dirname(os.path.abspath(__file__))
NOMS={'finary':'Finary (finances personnelles, investissement)','fintales':'Fintales (crypto, marchés, finance)','gabzer':'Gabzer (outils et astuces gratuits du web)'}
C_FIN="""Tu es un analyste financier pédagogue et rigoureux. Voici des fiches qui résument des vidéos de la chaîne YouTube {nom}, thème « {theme} » ({n} vidéos). Rédige en français une synthèse TRÈS détaillée et structurée (2 500 à 4 000 mots), pour un débutant qui veut apprendre et savoir vers où aller dans ses décisions d'investissement. Plan obligatoire, titres Markdown ## :
1. Les idées fortes et convictions récurrentes de la chaîne sur ce thème (les plus répétées d'abord ; citer entre parenthèses 1 à 3 identifiants de vidéos sources).
2. Les notions à connaître, expliquées simplement.
3. La méthode et les conseils concrets, étape par étape (ordre conseillé, à qui ça s'adresse, montants ou durées si cités).
4. Les chiffres, plafonds, taux et règles fiscales cités, sous forme de liste, chacun marqué « selon la chaîne » ; signaler les contradictions entre vidéos et les règles qui ont pu changer avec le temps.
5. Les risques, mises en garde et erreurs fréquentes à éviter.
6. Les nuances, débats et désaccords entre vidéos.
7. Ce que la chaîne promeut ou vend (son application, partenaires, produits) pour garder un regard critique.
8. En résumé : 5 à 10 points à retenir.
Règles : n'invente rien, uniquement ce qui est dans les fiches ; pas de conseil personnalisé ; style clair, phrases courtes."""
C_OUT="""Tu es un rédacteur pédagogue. Voici des fiches qui résument des vidéos courtes de la chaîne YouTube {nom}, thème « {theme} » ({n} vidéos). Rédige en français une synthèse TRÈS détaillée et structurée (2 000 à 3 500 mots). Plan obligatoire, titres Markdown ## :
1. Ce que la chaîne montre sur ce thème (idées principales).
2. Les outils et sites cités, regroupés par usage, avec pour chacun : à quoi il sert, gratuit ou non (selon la chaîne), identifiant de la vidéo.
3. Les astuces concrètes réutilisables, étape par étape.
4. Les promesses d'argent ou de gains annoncées (selon la chaîne) et leur crédibilité apparente.
5. Les risques : sécurité, données personnelles, légalité (téléchargement, contournement), arnaques possibles.
6. En résumé : 5 à 10 points à retenir.
Règles : n'invente rien, uniquement ce qui est dans les fiches ; style clair, phrases courtes."""
for f in sorted(glob.glob(S+'/*__*.txt')):
    out=f[:-4]+'.md'
    if os.path.exists(out) and os.path.getsize(out)>2000: continue
    ch,theme=os.path.basename(f)[:-4].split('__')
    texte=open(f).read(); n=texte.count('\n### ')+1
    c=(C_OUT if ch=='gabzer' else C_FIN).format(nom=NOMS[ch],theme=theme.replace('_',' '),n=n)
    corps={'consigne':c,'texte':texte,'modeles':os.environ.get('MODELES','gemini-3.5-flash,gemini-flash-latest,gemini-3-flash-preview')}
    json.dump(corps,open(S+'/corps.json','w'),ensure_ascii=False)
    for essai in range(3):
        r=subprocess.run(['curl','-s','-m','290','-b','/tmp/cj.txt','-H','Content-Type: application/json','--data-binary','@'+S+'/corps.json','https://relais-dig-justok1.vercel.app/api/avis'],capture_output=True,text=True).stdout
        try:
            j=json.loads(r); a=j.get('avis','')
        except Exception: a=''; j={'brut':r[:300]}
        if len(a)>2000:
            open(out,'w').write(f'<!-- modèle : {j.get("modele")} ; {n} vidéos -->\n'+a); print('ok',ch,theme,len(a),j.get('modele'),flush=True); break
        print('échec',ch,theme,str(j)[:300],flush=True); time.sleep(20)
