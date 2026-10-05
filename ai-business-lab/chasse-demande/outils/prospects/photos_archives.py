# Récupère les photos des anciens sites (archivés par la Wayback Machine) des prospects (05/10/2026).
# web.archive.org est bloqué depuis le conteneur : index via le relais Vercel (/api/cc?chemin=wayback), images via
# wsrv.nl (proxy d'images public et gratuit). Usage : python3 photos_archives.py <domaines.json> <dossier> [clé ...]
# domaines.json = {"<n°>-<nom>": ["ancien-domaine.fr", ...]} ; photos rangées dans <dossier>/<n°>/ + sources.txt.
# Toujours trier à l'œil ensuite : logos, images du modèle de site, visages, domaine repris par un tiers -> écarter.
import json,subprocess,os,sys,hashlib,io,re,urllib.parse
from PIL import Image
ICI=os.path.abspath(sys.argv[2])
dom=json.load(open(sys.argv[1]))
EXCLU=re.compile(r'logo|icon|favicon|sprite|bouton|button|banniere-?pub|qualibat|rge|label|picto|facebook|twitter|google|map|arrow|fleche|bg[-_]|background|loader|pixel|spacer|partenaire|cacc|cedeo|rexel|legrand|atlantic|bosch|viessmann|yesss|woodstock|moretti|captcha|avatar|thumb',re.I)
def run(args,timeout=90):
    try: return subprocess.run(args,capture_output=True,timeout=timeout).stdout
    except subprocess.TimeoutExpired: return b''
cibles=sys.argv[3:] or list(dom)
for k in cibles:
    n=k.split('-')[0]; dest=os.path.join(ICI,n); os.makedirs(dest,exist_ok=True)
    vus=set(); src=open(os.path.join(dest,'sources.txt'),'a'); ok=0
    for d in dom[k]:
        for motif in (d+'/*','www.'+d+'/*'):
            q=urllib.parse.urlencode({'chemin':'wayback','url':motif,'fl':'timestamp,original,mimetype','filter':'mimetype:image/(jpeg|png|webp)','collapse':'urlkey','limit':'400'})
            txt=run(['curl','-s','-m','80','-b','/tmp/cj.txt','https://relais-dig-justok1.vercel.app/api/cc?'+q],100).decode(errors='ignore')
            for ligne in txt.splitlines():
                p=ligne.split(' ')
                if len(p)<3: continue
                ts,orig=p[0],p[1]
                cle=orig.split('://',1)[-1].replace('www.','').lower()
                if cle in vus or EXCLU.search(orig.rsplit('/',1)[-1]): continue
                vus.add(cle)
                u='https://wsrv.nl/?url='+urllib.parse.quote(f'web.archive.org/web/{ts}im_/{orig}',safe='')
                b=run(['curl','-s','-m','40',u],50)
                try: im=Image.open(io.BytesIO(b)); w,h=im.size
                except Exception: continue
                if min(w,h)<350 or max(w,h)<600: continue
                f=hashlib.md5(b).hexdigest()[:10]+'.jpg'
                if os.path.exists(os.path.join(dest,f)): continue
                im.convert('RGB').save(os.path.join(dest,f),quality=90)
                src.write(f'{f} {w}x{h} https://web.archive.org/web/{ts}/{orig}\n'); ok+=1
    print(k,dom[k],ok,'photos',flush=True)
