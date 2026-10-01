"""Résume, par lots, les vidéos d'une chaîne YouTube via le relais Vercel (clé Gemini
gratuite de l'utilisateur, stockée dans Vercel). Reprend là où il s'est arrêté.

Usage : python3 resumer_chaine.py <liste.json> <dossier_sortie> <cookies.txt> [minutes_max] [mode]
- liste.json : sortie de /api/chaine (id, titre, durée)
- minutes_max : durée cumulée de vidéo à traiter pendant ce lot (défaut 60)
Limites de l'offre gratuite (constatées le 27/09) : environ 20 vidéos par jour et PAR MODÈLE ;
on alterne donc entre les 9 modèles Gemini capables de lire une vidéo (les plus puissants d'abord),
et on passe au suivant dès qu'un modèle a épuisé son quota. Pause de 30 s entre deux requêtes (80 s avant le 01/10 ; les relances réseau et le changement de modèle suffisent).
Depuis le 01/10 : les vidéos de 7 min au plus partent par lots de 8 (15 min cumulées au plus) dans UNE requête (relais ids=…),
ce qui multiplie le nombre de vidéos résumées par jour avec le même quota.
"""
MODELES = ['gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-3.6-flash', 'gemini-3.5-flash',
           'gemini-3-flash-preview', 'gemini-3.5-flash-lite', 'gemini-3.1-flash-lite',
           'gemini-3.1-flash-lite-preview', 'gemini-flash-lite-latest']  # 2 ajoutés le 28/09 (testés : lisent les vidéos)
import json, os, sys, time, subprocess, datetime, re
# 01/10 (soir) : plusieurs files en parallèle, chacune avec SES modèles (variable MODELES=a,b,c) : les quotas
# par minute sont par modèle, donc des files aux modèles disjoints ne se gênent pas et multiplient le débit.
if os.environ.get('MODELES'):
    MODELES = [m for m in os.environ['MODELES'].split(',') if m]


def sans_email(t):  # aucune adresse e-mail dans le dépôt public
    return re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', '[adresse e-mail retirée]', t)


def secondes(d):
    t = 0
    for x in str(d).split(':'):
        t = t * 60 + int(x or 0)
    return t

liste, sortie, cookies = sys.argv[1], sys.argv[2], sys.argv[3]
maxi = int(sys.argv[4]) if len(sys.argv) > 4 else 60
mode = sys.argv[5] if len(sys.argv) > 5 else 'finance'
os.makedirs(sortie, exist_ok=True)
videos = json.load(open(liste))['videos']
# Longues d'abord (>= 3 min), de la plus récente à la plus ancienne ; les courtes ensuite.
videos = [v for v in videos if secondes(v['duree']) >= 180] + [v for v in videos if secondes(v['duree']) < 180]
fait = 0
illisibles = 0  # réponses vides d'affilée (relais expiré ou vidéo trop longue pour le délai)
LOT_MAX, LOT_DUREE, COURTE = 8, 20 * 60, 600  # 01/10 : jusqu'à 8 vidéos de 10 min au plus (20 min cumulées) par requête (15 min = 68 s au relais, marge jusqu'à 295 s)

def appeler(ids):
    """Une requête au relais, en changeant de modèle si quota épuisé (429) ou surcharge (503)."""
    essais = 0
    while MODELES:
        cle = 'ids' if len(ids) > 1 else 'id'
        url = f"https://relais-dig-justok1.vercel.app/api/video?{cle}={','.join(ids)}&mode={mode}&modeles={MODELES[0]}"
        for essai in range(3):  # coupure réseau passagère (tunnel fermé, constaté le 01/10) : on relance 2 fois
            t0 = time.time()
            r = subprocess.run(['curl', '-s', '-m', '295', '-b', cookies, url], capture_output=True, text=True).stdout
            if r.startswith('{') or time.time() - t0 > 240:
                break  # réponse reçue, ou délai du relais dépassé (vidéo trop lourde) : relancer ne servirait à rien
            time.sleep(20)
        try:
            j = json.loads(r)
        except Exception:
            print('réponse illisible', ids[0], r[:120]); return {'erreur': 'illisible'}
        err = str(j.get('erreur', ''))
        if 'resume' not in j and ('429' in err or 'quota' in err.lower()):
            print('quota épuisé :', MODELES.pop(0), flush=True); continue
        if 'resume' not in j and ' 503 ' in err and essais < len(MODELES) - 1:
            essais += 1; MODELES.append(MODELES.pop(0)); continue  # modèle surchargé : le suivant, sans le perdre
        return j
    return {}

def ecrire(v, texte, modele):
    date = datetime.date.today().isoformat()
    open(os.path.join(sortie, v['id'] + '.md'), 'w').write(
        f"# {v['titre']}\n\nVidéo : https://youtu.be/{v['id']} · durée {v['duree']} · résumé Gemini ({modele}) du {date}\n"
        f"(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)\n\n{sans_email(texte.strip())}\n")
    print('ok', v['id'], v['duree'], v['titre'][:60], flush=True)

# Vidéos déjà en échec 2 fois (délai du relais dépassé, vidéo illisible…) : en fin de file, pour ne pas
# bloquer chaque lancement sur elles (constaté le 01/10 : 5 min perdues à chaque passage sur une même vidéo).
f_echecs = os.path.join(sortie, '.echecs.json')
echecs = json.load(open(f_echecs)) if os.path.exists(f_echecs) else {}
a_faire = [v for v in videos if not os.path.exists(os.path.join(sortie, v['id'] + '.md'))]
a_faire = [v for v in a_faire if echecs.get(v['id'], 0) < 2] + [v for v in a_faire if echecs.get(v['id'], 0) >= 2]
while a_faire and MODELES:
    v = a_faire.pop(0)
    lot = [v]
    if secondes(v['duree']) <= COURTE:  # complète le lot avec d'autres vidéos courtes de la liste, dans l'ordre
        for x in list(a_faire):
            if len(lot) >= LOT_MAX:
                break
            if secondes(x['duree']) <= COURTE and sum(secondes(y['duree']) for y in lot) + secondes(x['duree']) <= LOT_DUREE:
                lot.append(x); a_faire.remove(x)
    d = sum(secondes(x['duree']) for x in lot)
    if fait and fait + d > maxi * 60:
        break
    j = appeler([x['id'] for x in lot])
    if not MODELES:
        print('tous les modèles ont épuisé leur quota du jour'); break
    if 'resume' not in j:
        print('échec', ','.join(x['id'] for x in lot), str(j.get('erreur', ''))[:300], flush=True)
        if len(lot) == 1:
            echecs[v['id']] = echecs.get(v['id'], 0) + 1
            json.dump(echecs, open(f_echecs, 'w'))
        if j.get('erreur') == 'illisible':
            illisibles += 1
            if illisibles >= 3:
                print('3 réponses vides d’affilée : relais à revérifier (lien de partage expiré ?)'); break
        time.sleep(30); continue
    illisibles = 0
    if len(lot) == 1:
        ecrire(v, j['resume'], j.get('modele', '?'))
    else:  # découpe la réponse sur les lignes « === VIDEO <id> === » ; une vidéo absente sera refaite plus tard
        morceaux = re.split(r'^[#*\s]*=+\s*VID[EÉ]O\s+([A-Za-z0-9_-]{11})\s*=+[*\s]*$', j['resume'], flags=re.M | re.I)
        recus = {morceaux[i]: morceaux[i + 1] for i in range(1, len(morceaux) - 1, 2) if morceaux[i + 1].strip()}
        for x in lot:
            if x['id'] in recus:
                ecrire(x, recus[x['id']], j.get('modele', '?') + f', lot de {len(lot)}')
            else:
                print('absente du lot', x['id'], flush=True)
    fait += d
    time.sleep(30)
print('minutes traitées', round(fait / 60), '; restantes', sum(1 for v in videos if not os.path.exists(os.path.join(sortie, v['id'] + '.md'))))
