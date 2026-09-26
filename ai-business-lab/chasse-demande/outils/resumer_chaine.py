"""Résume, par lots, les vidéos d'une chaîne YouTube via le relais Vercel (clé Gemini
gratuite de l'utilisateur, stockée dans Vercel). Reprend là où il s'est arrêté.

Usage : python3 resumer_chaine.py <liste.json> <dossier_sortie> <cookies.txt> [minutes_max] [mode]
- liste.json : sortie de /api/chaine (id, titre, durée)
- minutes_max : durée cumulée de vidéo à traiter pendant ce lot (défaut 60)
Limites de l'offre gratuite : 8 h de vidéo YouTube par jour, débit limité (pause de 80 s).
"""
import json, os, sys, time, subprocess, datetime

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
for v in videos:
    f = os.path.join(sortie, v['id'] + '.md')
    if os.path.exists(f):
        continue
    d = secondes(v['duree'])
    if fait and fait + d > maxi * 60:
        break
    url = f"https://relais-dig-justok1.vercel.app/api/video?id={v['id']}&mode={mode}"
    r = subprocess.run(['curl', '-s', '-m', '295', '-b', cookies, url], capture_output=True, text=True).stdout
    try:
        j = json.loads(r)
    except Exception:
        print('réponse illisible', v['id'], r[:120]); break
    if 'resume' not in j:
        err = str(j.get('erreur', ''))[:300]
        print('échec', v['id'], err)
        if '429' in err or 'quota' in err.lower():
            break  # limite gratuite atteinte : on reprendra au prochain lot
        time.sleep(80); continue
    date = datetime.date.today().isoformat()
    open(f, 'w').write(f"# {v['titre']}\n\nVidéo : https://youtu.be/{v['id']} · durée {v['duree']} · résumé Gemini du {date}\n"
                       f"(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)\n\n{j['resume'].strip()}\n")
    fait += d
    print('ok', v['id'], v['duree'], v['titre'][:60], flush=True)
    time.sleep(80)
print('minutes traitées', round(fait / 60), '; restantes', sum(1 for v in videos if not os.path.exists(os.path.join(sortie, v['id'] + '.md'))))
