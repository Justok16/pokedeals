"""Contrôle de la marque dans toutes les vidéos parlées du site (22/10/2026).

Leçon du 22/10 : plusieurs vidéos disaient « Di seize » / « dixseize » au lieu de « dig16 » et sont parties sur les
réseaux. Ce contrôle transcrit (faster-whisper, local, gratuit) chaque vidéo de site-dig/ qui a une voix et vérifie que
la marque y est bien dite. Résultat mis en cache par empreinte du fichier (videos/controle-voix.json) : seules les
vidéos nouvelles ou modifiées sont retranscrites.

Usage : python3 outils/controle_voix_videos.py   → code de sortie = nombre de vidéos où la marque est mal dite.
"""

import glob
import hashlib
import json
import os
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
CD = os.path.normpath(os.path.join(ICI, ".."))
SITE = os.path.join(CD, "site-dig")
CACHE = os.path.join(CD, "videos", "controle-voix.json")
sys.path.insert(0, os.path.join(CD, "videos", "conseils"))
from fabriquer import marque_mal_dite


def empreinte(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()[:16]


def main():
    cache = {}
    if os.path.exists(CACHE):
        with open(CACHE, encoding="utf-8") as f:
            cache = json.load(f)
    modele = None
    mal = []
    for f in sorted(glob.glob(os.path.join(SITE, "**", "*.mp4"), recursive=True)):
        rel = os.path.relpath(f, SITE)
        e = empreinte(f)
        if cache.get(rel, {}).get("empreinte") != e:
            with tempfile.TemporaryDirectory() as tmp:
                wav = os.path.join(tmp, "a.wav")
                r = subprocess.run(["ffmpeg", "-y", "-loglevel", "quiet", "-i", f, "-vn", "-ac", "1", "-ar", "16000",
                                    wav], check=False)
                texte = ""
                if r.returncode == 0 and os.path.exists(wav) and os.path.getsize(wav) > 2000:
                    if modele is None:
                        from faster_whisper import WhisperModel

                        modele = WhisperModel("small", compute_type="int8")
                    texte = " ".join(x.text for x in modele.transcribe(wav, language="fr", beam_size=5)[0]).strip()
            # une vidéo muette (démos) ou sans parole n'est pas concernée
            etat = "sans voix" if len(texte.split()) < 4 else ("mal dite" if marque_mal_dite(texte) else "ok")
            cache[rel] = {"empreinte": e, "etat": etat, "fin": texte[-90:]}
        etat = cache[rel]["etat"]
        print(f"{etat:9} {rel}" + (f" | …{cache[rel]['fin']}" if etat == "mal dite" else ""))
        if etat == "mal dite":
            mal.append(rel)
    for rel in [k for k in cache if not os.path.exists(os.path.join(SITE, k))]:
        del cache[rel]
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    return len(mal)


if __name__ == "__main__":
    sys.exit(main())
