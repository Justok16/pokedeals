# Publie des maquettes privées sur le site public de Dig, chiffrées (04/10/2026).
# Chaque page HTML produite par gen2.py (mode hébergé : DIG_IMG_BASE=/img/d/ DIG_CSS_EXT=1) est chiffrée en
# AES-GCM avec une clé aléatoire de 128 bits et déposée dans site-dig/m/x/<id>.bin. La clé n'existe que dans le
# lien privé (https://digsite.pages.dev/m/#<id>.<clé>) : le dépôt public ne contient ni nom ni contenu lisible.
# Le registre des liens (privé, avec les noms) reste HORS du dépôt ; un lien déjà attribué est conservé.
# Usage : python3 publier_maquettes.py <dossier_pages> <registre_prive.json> [--retirer <nom_de_page> ...]
import os, sys, json, secrets, base64, shutil
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
ICI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(ICI, '..', '..', 'site-dig'))
X = os.path.join(SITE, 'm', 'x')
BASE = 'https://digsite.pages.dev/m/#'
src, reg_f = sys.argv[1], sys.argv[2]
retirer = sys.argv[sys.argv.index('--retirer') + 1:] if '--retirer' in sys.argv else []
reg = json.load(open(reg_f)) if os.path.exists(reg_f) else {}
os.makedirs(X, exist_ok=True)
b64 = lambda b: base64.urlsafe_b64encode(b).decode().rstrip('=')
for nom in retirer:  # prospect qui refuse : la maquette est supprimée (et le lien ne mène plus à rien)
    r = reg.pop(nom, None)
    if r and os.path.exists(os.path.join(X, r['id'] + '.bin')): os.remove(os.path.join(X, r['id'] + '.bin'))
    print('retirée', nom)
if os.path.exists(os.path.join(src, 'd.css')): shutil.copy(os.path.join(src, 'd.css'), os.path.join(SITE, 'm', 'd.css'))
for f in sorted(os.listdir(src)):
    if not f.endswith('.html'): continue
    nom = f[:-5]
    if nom in retirer: continue
    html = open(os.path.join(src, f), encoding='utf-8').read().replace('href="/d.css"', 'href="/m/d.css"')
    r = reg.get(nom)
    if not r:
        ids = {v['id'] for v in reg.values()}
        while True:
            i = ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(8))
            if i not in ids: break
        r = reg[nom] = {'id': i, 'cle': b64(secrets.token_bytes(16))}
    cle = base64.urlsafe_b64decode(r['cle'] + '==')
    iv = secrets.token_bytes(12)
    open(os.path.join(X, r['id'] + '.bin'), 'wb').write(iv + AESGCM(cle).encrypt(iv, html.encode(), None))
    r['lien'] = BASE + r['id'] + '.' + r['cle']
json.dump(reg, open(reg_f, 'w'), ensure_ascii=False, indent=1)
print(len(reg), 'maquettes au registre ;', len(os.listdir(X)), 'fichiers chiffrés')
