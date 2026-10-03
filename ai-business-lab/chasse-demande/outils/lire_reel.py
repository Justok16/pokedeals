"""Lit un reel Instagram (ou toute vidéo courte publique lisible par yt-dlp) et le fait résumer par Gemini
via le relais /api/avis (limite 4,5 Mo : la vidéo est réduite en 360p avec ffmpeg).

Pré-requis (hors dépôt) : python3 -m venv /tmp/ytdlp/v && /tmp/ytdlp/v/bin/pip install yt-dlp imageio-ffmpeg
Usage : python3 lire_reel.py <cookies.txt> <dossier_sortie> <url> [<url> ...]
Solution trouvée le 29/09/2026 : Firecrawl refuse Instagram et la page intégrée exige une connexion.
"""
import sys, os, json, base64, subprocess, glob, datetime, re


def sans_email(t):  # aucune adresse e-mail dans le dépôt public
    return re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', '[adresse e-mail retirée]', t)

Y = '/tmp/ytdlp/v/bin/yt-dlp'
FF = subprocess.run(['/tmp/ytdlp/v/bin/python', '-c', 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())'],
                    capture_output=True, text=True).stdout.strip()
cookies, sortie = sys.argv[1], sys.argv[2]
os.makedirs(sortie, exist_ok=True)
C = ("Regarde et écoute entièrement cette courte vidéo. Résume-la en français : 1) idée principale ; 2) chaque outil, site, "
     "skill ou dépôt GitHub cité : nom exact, usage, gratuit ou payant selon la vidéo ; 3) astuces concrètes ; 4) chiffres annoncés ; "
     "5) texte affiché à l'écran s'il liste des outils. N'invente rien ; si un nom est incertain, écris « à vérifier ».")
for url in sys.argv[3:]:
    rid = url.rstrip('/').split('/')[-1].split('?')[0]
    f = os.path.join(sortie, f'reel-{rid}.md')
    if os.path.exists(f):
        continue
    b = f'/tmp/reel_{rid}'
    subprocess.run([Y, '-q', '--no-warnings', '-f', 'b[ext=mp4]/b', '-o', b + '.%(ext)s', '--write-info-json', url])
    try:
        info = json.load(open(b + '.info.json'))
    except Exception:
        print('illisible', url); continue
    src = glob.glob(b + '.mp4')[0]
    subprocess.run([FF, '-y', '-loglevel', 'error', '-i', src, '-vf', 'scale=-2:360,fps=10', '-c:v', 'libx264', '-crf', '32',
                    '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '48k', '-ac', '1', b + '_p.mp4'])
    json.dump({'consigne': C, 'media_base64': base64.b64encode(open(b + '_p.mp4', 'rb').read()).decode(), 'media_type': 'video/mp4',
               'modeles': 'gemini-3-flash-preview,gemini-3.5-flash-lite,gemini-3.1-flash-lite,gemini-flash-lite-latest'},
              open(b + '.corps.json', 'w'))
    r = subprocess.run(['curl', '-s', '-m', '280', '-b', cookies, '-H', 'Content-Type: application/json', '--data-binary',
                        '@' + b + '.corps.json', 'https://relais-dig-justok1.vercel.app/api/avis'], capture_output=True, text=True).stdout
    try:
        j = json.loads(r)
    except Exception:
        j = {}
    if 'avis' not in j:
        print('échec', url, r[:200]); continue
    open(f, 'w').write(f"# Reel de {info.get('uploader') or '?'} (@{info.get('channel') or '?'})\n\n{url} · résumé Gemini "
                       f"({j.get('modele')}) du {datetime.date.today().isoformat()} (affirmations non vérifiées)\n\n{sans_email(j['avis'].strip())}\n")
    for x in glob.glob(b + '*'):
        os.remove(x)
    print('ok', url)
