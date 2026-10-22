"""Instants d'apparition des phrases d'une vidéo « Le conseil » 2D (creux de luminosité de la zone du texte)."""
import subprocess
import sys

import numpy as np


def instants(chemin, nb_scenes):
    """Renvoie les débuts des scènes 1..nb_scenes-1 (la scène 0 commence à 0,6 s) : creux entre deux textes + 0,12 s."""
    l, h, fps = 108, 192, 30
    brut = subprocess.run(["ffmpeg", "-v", "error", "-i", chemin, "-vf", f"fps={fps},scale={l}:{h},format=gray",
                           "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    img = np.frombuffer(brut, np.uint8).reshape(-1, h, l)
    zone = img[:, 66:150, 8:100].astype(float)  # du haut des phrases au bas de l'écran final, hors barre et signature
    lum = zone.mean(axis=(1, 2))
    lum = np.convolve(lum, np.ones(3) / 3, mode="same")
    creux = [i for i in range(25, len(lum) - 5) if lum[i] == lum[i - 6:i + 7].min() and lum[i] < lum[i - 6:i + 7].max() - 1.0]
    creux = sorted(creux, key=lambda i: lum[i])[:nb_scenes - 1]
    return [0.6] + [round(i / fps + .12, 2) for i in sorted(creux)]


if __name__ == "__main__":
    print(instants(sys.argv[1], int(sys.argv[2])))
