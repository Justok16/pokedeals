"""Résume une vidéo publiée sur X (Twitter) : récupère seulement la piste son (HLS), la découpe
en morceaux légers et la fait écouter par Gemini via le relais (/api/avis, lecture seule).
Usage : python3 resumer_video_x.py <lien x.com/.../status/ID> <dossier_sortie> [cookies.txt]
Écrit <dossier>/resume_partN.md. Aucun secret dans ce fichier (le cookie du relais reste local)."""
import sys, re, json, os, subprocess, base64, concurrent.futures as cf
import imageio_ffmpeg

RELAIS = 'https://relais-dig-justok1.vercel.app/api/avis'
B = 'https://video.twimg.com'
CONSIGNE = ("Écoute cet enregistrement. Rédige en français un résumé fidèle et détaillé : 1) sujet et "
            "intervenant ; 2) idées principales dans l'ordre ; 3) méthodes, outils et commandes cités (noms "
            "exacts) ; 4) chiffres cités (affirmés par l'orateur) ; 5) ce qu'un entrepreneur solo qui vend des "
            "sites web à des artisans pourrait appliquer. N'invente rien ; signale les passages inaudibles.")

def get(url, binaire=False):
    r = subprocess.run(['curl', '-s', '-f', '-m', '30', url], capture_output=True)
    if r.returncode: raise RuntimeError('échec du téléchargement : ' + url[:80])
    return r.stdout if binaire else r.stdout.decode()

def main(lien, dossier, cookies='/tmp/cj.txt'):
    m = re.search(r'x\.com/([A-Za-z0-9_]{1,15})/status/(\d{10,20})', lien)
    if not m: sys.exit('lien X invalide (ID complet requis)')
    t = json.loads(get(f'https://api.fxtwitter.com/{m[1]}/status/{m[2]}'))['tweet']
    vid = [x for x in (t.get('media') or {}).get('all', []) if x.get('type') == 'video']
    if not vid: sys.exit('pas de vidéo dans ce message')
    hls = [f['url'] for f in vid[0]['formats'] if f.get('container') == 'm3u8'][0]
    audio = re.search(r'TYPE=AUDIO[^\n]*URI="([^"]+)"', get(hls))[1]      # la plus légère (32 kb/s)
    pl = get(B + audio + '?tag=29')
    urls = [B + re.search(r'#EXT-X-MAP:URI="([^"]+)"', pl)[1]] + [B + l for l in pl.splitlines() if l and not l.startswith('#')]
    os.makedirs(dossier, exist_ok=True)
    with cf.ThreadPoolExecutor(8) as ex: morceaux = list(ex.map(lambda u: get(u, True), urls))
    src = os.path.join(dossier, 'audio.mp4'); open(src, 'wb').write(b''.join(morceaux))
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ff, '-loglevel', 'error', '-y', '-i', src, '-ac', '1', '-c:a', 'libopus', '-b:a', '12k',
                    '-application', 'voip', '-f', 'segment', '-segment_time', '1560',
                    os.path.join(dossier, 'part%d.ogg')], check=True)
    parts = sorted(f for f in os.listdir(dossier) if re.fullmatch(r'part\d+\.ogg', f))
    for i, p in enumerate(parts):
        corps = json.dumps({'texte': '(audio joint)', 'consigne': CONSIGNE + f' (Partie {i+1} sur {len(parts)}.)',
                            'media_base64': base64.b64encode(open(os.path.join(dossier, p), 'rb').read()).decode(),
                            'media_type': 'audio/ogg'})
        f = os.path.join(dossier, 'corps.json'); open(f, 'w').write(corps)
        r = subprocess.run(['curl', '-s', '-m', '280', '-b', cookies, '-H', 'content-type: application/json',
                            '--data-binary', '@' + f, RELAIS], capture_output=True, text=True).stdout
        avis = json.loads(r).get('avis', '') if r.startswith('{') else ''
        open(os.path.join(dossier, f'resume_part{i+1}.md'), 'w').write(avis)
        print(p, 'ok' if avis else 'ÉCHEC', len(avis))
    os.remove(f)

if __name__ == '__main__':
    main(*sys.argv[1:4])
