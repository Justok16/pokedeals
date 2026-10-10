"""Résume un reel Instagram public sans compte : page « embed » d'Instagram -> fichier vidéo ->
vidéo réduite (< 3 Mo) -> Gemini via le relais (/api/avis, lecture seule).
Usage : python3 resumer_reel_instagram.py <lien reel> <dossier_sortie> [cookies.txt]
Écrit <dossier>/<code>.md (légende + résumé). Aucun secret dans ce fichier."""

import sys
import re
import os
import json
import html
import base64
import subprocess
import imageio_ffmpeg

RELAIS = "https://relais-dig-justok1.vercel.app/api/avis"
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)"
CONSIGNE = (
    "Regarde et écoute cette courte vidéo (reel Instagram). Donne en français : 1) l'idée principale ; "
    "2) les outils, sites, skills ou méthodes présentés, avec leur nom exact tel qu'affiché ou prononcé et "
    "leur rôle ; 3) ce que l'auteur dit de leur prix ; 4) chiffres cités (affirmés par l'auteur) ; 5) ce "
    "qu'un entrepreneur solo qui vend des sites web à des artisans pourrait appliquer. N'invente rien."
)


def main(lien, dossier, cookies="/tmp/cj.txt"):
    m = re.search(r"instagram\.com/(?:reel|p)/([A-Za-z0-9_-]{5,20})", lien)
    if not m:
        sys.exit("lien de reel invalide")
    code = m[1]
    os.makedirs(dossier, exist_ok=True)
    page = subprocess.run(
        [
            "curl",
            "-s",
            "-m",
            "30",
            "-A",
            UA,
            f"https://www.instagram.com/reel/{code}/embed/captioned/",
        ],
        capture_output=True,
        text=True,
    ).stdout
    leg = re.search(r'class="Caption"[^>]*>(.*?)</div>', page, re.S)
    legende = (
        re.sub(r"\s+", " ", html.unescape(re.sub("<[^>]+>", " ", leg[1]))).strip()
        if leg
        else ""
    )
    i = page.find("video_url")
    u = (
        re.search(r'(https:[^"]*?\.mp4\?[^"]*?)\\+"', page[i : i + 3000])
        if i >= 0
        else None
    )
    if not u:
        sys.exit(f"{code} : vidéo introuvable (reel privé ou supprimé ?)")
    url = re.sub(r"\\+u0025", "%", re.sub(r"\\+/", "/", u[1])).replace("\\", "")
    brut = (
        f"/tmp/reel-{code}.mp4"  # vidéos hors du dépôt public (droits d'auteur, taille)
    )
    subprocess.run(["curl", "-s", "-f", "-m", "120", "-o", brut, url], check=True)
    resumer_fichier(brut, code, legende, dossier, cookies, "reel Instagram")


def resumer_fichier(
    brut, code, legende, dossier, cookies="/tmp/cj.txt", origine="reel"
):
    """Réduit une vidéo locale (~2,6 Mo, limite du relais Vercel ~4,5 Mo), la fait lire par Gemini et écrit
    <dossier>/<code>.md. Partagé avec resumer_reel_facebook.py."""
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    info = subprocess.run([ff, "-i", brut], capture_output=True, text=True).stderr
    h, mi, se = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info).groups()
    dur = 3600 * int(h) + 60 * int(mi) + float(se)
    petit = f"/tmp/reel-{code}-petit.mp4"
    debit = max(
        120, min(600, int(2.6e6 * 8 / 1000 / max(dur, 1)) - 40)
    )  # vise ~2,6 Mo au total
    subprocess.run(
        [
            ff,
            "-loglevel",
            "error",
            "-y",
            "-i",
            brut,
            "-vf",
            "scale=-2:640",
            "-c:v",
            "libx264",
            "-b:v",
            f"{debit}k",
            "-c:a",
            "aac",
            "-b:a",
            "32k",
            "-ac",
            "1",
            petit,
        ],
        check=True,
    )
    corps = f"/tmp/reel-{code}-corps.json"
    json.dump(
        {
            "texte": f"Légende ({origine}) : " + (legende or "(aucune)"),
            "consigne": CONSIGNE.replace("reel Instagram", origine),
            "media_base64": base64.b64encode(open(petit, "rb").read()).decode(),
            "media_type": "video/mp4",
            "modeles": os.environ.get("MODELES", ""),
        },
        open(corps, "w"),
    )
    r = subprocess.run(
        [
            "curl",
            "-s",
            "-m",
            "280",
            "-b",
            cookies,
            "-H",
            "content-type: application/json",
            "--data-binary",
            "@" + corps,
            RELAIS,
        ],
        capture_output=True,
        text=True,
    ).stdout
    for f in (corps, petit, brut):
        os.remove(f)
    avis = json.loads(r).get("avis", "") if r.startswith("{") else ""
    if avis:
        open(os.path.join(dossier, code + ".md"), "w").write(
            f"Légende : {legende}\nDurée : {dur:.0f} s\n\n{avis}"
        )
    print(code, round(dur), "s", "ok" if avis else "ÉCHEC " + r[:120])
    return bool(avis)


if __name__ == "__main__":
    main(*sys.argv[1:4])
