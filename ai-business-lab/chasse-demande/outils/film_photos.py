"""Fabrique un plan-séquence « caméra » à partir de photos fixes (poussées, travellings), sans IA payante.
Usage : python3 film_photos.py <dossier_photos> <sortie.mp4> <largeur> <hauteur> [plans.json]"""

import subprocess
import sys

from PIL import Image

src, out, W, H = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
FPS, SHOT, FONDU = 30, 3.6, 0.7
# (photo, centre départ (x,y), zoom départ, centre arrivée, zoom arrivée) ; zoom 1 = photo qui couvre juste le cadre
PLANS = [
    ("atelier", (0.50, 0.55), 1.00, (0.56, 0.64), 1.22),
    ("reserve-bois", (0.66, 0.50), 1.18, (0.42, 0.52), 1.18),
    ("assemblage", (0.44, 0.58), 1.04, (0.40, 0.62), 1.28),
    ("artisan", (0.52, 0.48), 1.02, (0.56, 0.44), 1.24),
    ("finitions", (0.64, 0.56), 1.32, (0.58, 0.52), 1.06),
]
# 08/10 : liste de plans réglable (fichier JSON en 5e argument) pour réutiliser l'outil sur d'autres démos.
if len(sys.argv) > 5:
    import json

    PLANS = [
        tuple(x if not isinstance(x, list) else tuple(x) for x in p)
        for p in json.load(open(sys.argv[5]))
    ]
ims = {p[0]: Image.open(f"{src}/{p[0]}.jpg").convert("RGB") for p in PLANS}


def doux(t):  # accélère puis ralentit
    return t * t * (3 - 2 * t)


def image(nom, c, z):
    im = ims[nom]
    iw, ih = im.size
    couv = max(W / iw, H / ih) * z  # échelle source -> cadre
    cw, ch = W / couv, H / couv  # taille de la fenêtre dans la photo
    cx = min(max(c[0] * iw, cw / 2), iw - cw / 2)
    cy = min(max(c[1] * ih, ch / 2), ih - ch / 2)
    x0, y0 = cx - cw / 2, cy - ch / 2
    # transformation affine sous-pixel (pas de tremblement, contrairement à zoompan)
    return im.transform(
        (W, H), Image.AFFINE, (cw / W, 0, x0, 0, ch / H, y0), resample=Image.BICUBIC
    )


def plan(i, t):  # t en secondes dans le plan (peut dépasser pour le fondu)
    nom, c0, z0, c1, z1 = PLANS[i]
    u = doux(min(max(t / (SHOT + FONDU), 0), 1))
    return image(
        nom,
        (c0[0] + (c1[0] - c0[0]) * u, c0[1] + (c1[1] - c0[1]) * u),
        z0 + (z1 - z0) * u,
    )


total = len(PLANS) * SHOT + FONDU
ff = subprocess.Popen(
    [
        "ffmpeg",
        "-y",
        "-loglevel",
        "error",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{W}x{H}",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-crf",
        "16",
        "-pix_fmt",
        "yuv420p",
        out,
    ],
    stdin=subprocess.PIPE,
)
n = int(total * FPS)
for k in range(n):
    t = k / FPS
    i = min(int(t // SHOT), len(PLANS) - 1)
    fr = plan(i, t - i * SHOT)
    debut_suivant = (i + 1) * SHOT - FONDU / 2
    if i + 1 < len(PLANS) and t >= debut_suivant:
        a = (t - debut_suivant) / FONDU
        if a < 1:
            fr = Image.blend(fr, plan(i + 1, t - (i + 1) * SHOT + FONDU / 2), doux(a))
    if i + 1 < len(PLANS) and t >= (i + 1) * SHOT + FONDU / 2:
        fr = plan(i + 1, t - (i + 1) * SHOT + FONDU / 2)
    ff.stdin.write(fr.tobytes())
ff.stdin.close()
ff.wait()
print(out, n, "images")
