# v7 (24/10/2026, demande de l'utilisateur : plus aucun délai de création annoncé, montrer qu'il est toujours joignable).
# La voix Algieba de la v6 (validée le 08/10) est gardée telle quelle : on retire seulement la phrase « En ligne en
# sept jours. » de la bande-son de la v6 (fondu de 60 ms) et l'écran « 7 jours pour être en ligne » devient
# « 7 j/7, toujours joignable » (video.html). L'animation suit la voix comme en v6 : repères des 7 phrases relevés
# par transcription (faster-whisper) sur la v6, décalés de la durée coupée.
# Usage : python3 v7.py  (depuis ce dossier) → dig16-presentation.mp4 (1080 × 1920), puis versions web dans site-dig/video/.
import os, subprocess, sys
from playwright.sync_api import sync_playwright
ICI = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.join(ICI, '..', '..', 'site-dig', 'video', 'presentation-v6.mp4')
C0, C1 = float(sys.argv[1]) if len(sys.argv) > 1 else 18.80, float(sys.argv[2]) if len(sys.argv) > 2 else 20.62
L = C1 - C0
FPS = 30
ORIG = [0.7, 3.55, 5.6, 11.2, 19.6, 26.2, 31.5]           # temps de l'animation (video.html) de chaque phrase
V6_DEB = [0.76, 3.40, 4.84, 9.30, 17.56, 22.48, 26.23]    # début de chaque phrase dans la v6 (transcription)
DEB = [x if x < C0 else x - L for x in V6_DEB]
DUR = round(33.233 - L, 3)
pts = [(0, 0)] + list(zip(DEB, ORIG)) + [(DUR, 38.5)]
def warp(t):
    for (a, x), (b, y) in zip(pts, pts[1:]):
        if t <= b:
            return x + (y - x) * (t - a) / (b - a)
    return 38.5
# images de l'animation : copiées depuis le site le temps du rendu (non suivies dans le dépôt)
import shutil
IMG = os.path.join(ICI, '..', '..', 'site-dig', 'img')
COPIES = {'embleme-or@6x.png': 'marque', 'signature-ivoire@6x.png': 'marque', 'vitrine-essentiel-tel.webp': '',
          'vitrine-paysagiste-tel.webp': '', 'vitrine-prestige-tel.webp': ''}
for nom, dossier in COPIES.items():
    shutil.copy(os.path.join(IMG, dossier, nom), os.path.join(ICI, nom))
son = os.path.join(ICI, 'son-v7.m4a')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', V6, '-filter_complex',
                f'[0:a]atrim=0:{C0},asetpts=N/SR/TB[a];[0:a]atrim={C1},asetpts=N/SR/TB[b];[a][b]acrossfade=d=0.06[o]',
                '-map', '[o]', '-c:a', 'aac', '-b:a', '192k', son], check=True)
sortie = os.path.join(ICI, 'dig16-presentation.mp4')  # remplace le master de la v6
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                       '-i', son, '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                       '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', '-shortest', sortie], stdin=subprocess.PIPE)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + os.path.join(ICI, 'video.html'), wait_until='networkidle'); pg.wait_for_timeout(1500)
    for i in range(int(FPS * DUR)):
        pg.evaluate(f'seek({warp(i / FPS):.4f})'); ff.stdin.write(pg.screenshot(type='jpeg', quality=93))
    b.close()
ff.stdin.close(); ff.wait()
for nom in COPIES:
    os.remove(os.path.join(ICI, nom))
print('v7 durée', DUR, 'coupé', round(L, 2), 's')
