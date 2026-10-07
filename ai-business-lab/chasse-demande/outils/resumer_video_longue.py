"""Résume une vidéo YouTube trop longue pour Gemini (plus de ~3 h : « input token count exceeds
1048576 ») en la découpant en morceaux de 20 minutes (paramètres debut/fin du relais, ajoutés le 30/09),
puis fait une synthèse d'ensemble avec /api/avis.

Usage : python3 resumer_video_longue.py <id_video> <durée h:mm:ss> <cookies.txt> <fichier_sortie.md> [titre]
La durée se lit avec /api/chaine?chaine=@nom (champ « duree »).
"""

import json
import os
import re
import subprocess
import sys
import time
import datetime

RELAIS = "https://relais-dig-justok1.vercel.app"
MODELES = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3-flash-preview",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.1-flash-lite-preview",
    "gemini-flash-lite-latest",
]  # les 9 modèles qui lisent une vidéo (2 ajoutés le 01/10, comme resumer_chaine.py)
if os.environ.get(
    "MODELES"
):  # 01/10 : liste de modèles imposée (files parallèles aux modèles disjoints)
    MODELES = [m for m in os.environ["MODELES"].split(",") if m]
MORCEAU = 1200  # secondes (20 min, environ 120 000 jetons : 50 min dépassait la limite gratuite par minute, 30/09)

vid, duree, cookies, sortie = sys.argv[1:5]
titre = sys.argv[5] if len(sys.argv) > 5 else vid
if not re.fullmatch(r"[A-Za-z0-9_-]{11}", vid):
    sys.exit("identifiant vidéo invalide")
total = 0
for x in duree.split(":"):
    total = total * 60 + int(x)


def hms(s):
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def sans_email(t):  # aucune adresse e-mail dans le dépôt public
    return re.sub(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[adresse e-mail retirée]", t
    )


CACHE = f"/tmp/video-longue-{vid}"  # morceaux déjà réussis : une relance ne refait que les manquants
os.makedirs(CACHE, exist_ok=True)


def morceau(bornes):
    debut, fin = bornes
    f = f"{CACHE}/{debut}-{fin}.json"
    if os.path.exists(f):
        return tuple(json.load(open(f)))
    for m in (
        MODELES
    ):  # un autre modèle si le premier est saturé (503) ou à court de quota (429)
        url = f"{RELAIS}/api/video?id={vid}&mode=ia&modeles={m}&debut={debut}&fin={fin}"
        r = subprocess.run(
            ["curl", "-s", "-m", "295", "-b", cookies, url],
            capture_output=True,
            text=True,
        ).stdout
        try:
            j = json.loads(r)
        except Exception:
            print(f"{debut}-{fin} {m} : réponse illisible {r[:80]!r}", flush=True)
            continue
        if j.get("resume"):
            res = (debut, fin, m, j["resume"].strip())
            json.dump(res, open(f, "w"))
            return res
        print(f"{debut}-{fin} {m} : {str(j.get('erreur'))[:160]}", flush=True)
    return debut, fin, None, None


bornes = [(d, min(d + MORCEAU, total)) for d in range(0, total, MORCEAU)]


# Un morceau à la fois, 65 s d'écart : l'offre gratuite limite aussi les jetons PAR MINUTE
# (30/09 : 5 morceaux envoyés en parallèle → 429 sur tous les modèles).
# Morceau refusé par tous les modèles (429 « quota » même sur 20 min, constaté le 01/10 alors que
# 1 min passait) : on le recoupe en deux moitiés, jusqu'à 5 min minimum.
def avec_decoupe(b):
    deja = os.path.exists(f"{CACHE}/{b[0]}-{b[1]}.json")
    r = morceau(b)
    if r[3] or b[1] - b[0] <= 300:
        return [r], deja
    milieu = (b[0] + b[1]) // 2
    sous = []
    for moitie in ((b[0], milieu), (milieu, b[1])):
        time.sleep(65)
        sous += avec_decoupe(moitie)[0]
    return sous, False


parts = []
for i, b in enumerate(bornes):
    res, deja = avec_decoupe(b)
    parts += res
    if not deja and i < len(bornes) - 1:
        time.sleep(65)
manquants = [f"{hms(d)}–{hms(f)}" for d, f, m, t in parts if not t]
if manquants:
    sys.exit("morceaux non résumés : " + ", ".join(manquants))

texte = "\n\n".join(f"## Partie {hms(d)} à {hms(f)}\n\n{t}" for d, f, m, t in parts)
consigne = (
    "Voici les résumés successifs des parties d'une même longue vidéo. Fais-en UNE synthèse en français : "
    "1) idée principale ; 2) outils, sites et prix cités (gratuit/payant) ; 3) méthode pas à pas et astuces "
    "réutilisables ; 4) chiffres annoncés, marqués « affirmé par l'auteur ». Sans répétitions."
)
r = subprocess.run(
    [
        "curl",
        "-s",
        "-m",
        "295",
        "-b",
        cookies,
        "-H",
        "Content-Type: application/json",
        "--data-binary",
        "@-",
        f"{RELAIS}/api/avis",
    ],
    input=json.dumps({"texte": texte, "consigne": consigne}),
    capture_output=True,
    text=True,
).stdout
try:
    j = json.loads(r)
    synthese = (j.get("avis") or j.get("resume") or j.get("texte") or "").strip()
except Exception:
    synthese = ""
modeles = ", ".join(sorted({m for d, f, m, t in parts}))
date = datetime.date.today().strftime("%d/%m/%Y")
open(sortie, "w").write(
    f"# {titre} (vidéo YouTube {vid})\n\nSource : https://youtu.be/{vid} · durée {duree} · résumé Gemini ({modeles}) du {date}, "
    f"en {len(parts)} parties de 20 min ou moins, puis synthèse. Affirmations de l'auteur, non vérifiées.\n\n"
    + (f"# Synthèse\n\n{sans_email(synthese)}\n\n" if synthese else "")
    + f"# Détail par partie\n\n{sans_email(texte)}\n"
)
print("ok", sortie, len(parts), "parties", "synthèse" if synthese else "SANS synthèse")
