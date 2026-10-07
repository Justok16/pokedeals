"""Résume par lots de 15 les vidéos courtes (TikTok, reels) déjà collectées en texte
(légende + sous-titres, collecte privée hors dépôt) via le relais /api/avis (Gemini gratuit).

Usage : python3 resumer_lots_tiktok.py <dossier_textes> <dossier_fiches> <cookies.txt> [taille_lot]
- dossier_textes : un fichier JSON par vidéo {id, url, date, legende, sous_titres}
- dossier_fiches : fiches lot-001.md, lot-002.md… (nos synthèses, publiables ; pas de texte brut des créateurs)
Reprend là où il s'est arrêté. Pause de 20 s entre deux lots.
"""

import json
import os
import sys
import glob
import subprocess
import time
import datetime
import re

textes, fiches, cookies = sys.argv[1], sys.argv[2], sys.argv[3]
taille = int(sys.argv[4]) if len(sys.argv) > 4 else 15
os.makedirs(fiches, exist_ok=True)
V = sorted(
    (json.load(open(f)) for f in glob.glob(os.path.join(textes, "*.json"))),
    key=lambda v: v.get("date") or "",
    reverse=True,
)
C = (
    "Voici les légendes et sous-titres de courtes vidéos d'un créateur sur l'IA. Pour CHAQUE vidéo, fais une fiche : "
    "titre court ; idée principale en une phrase ; chaque outil, site, skill, connecteur ou dépôt GitHub cité (nom exact, "
    "à quoi il sert, gratuit ou payant SELON LA VIDÉO) ; astuce concrète réutilisable. Garde le numéro [n] et le lien de chaque vidéo. "
    "Termine par un tableau récapitulatif des outils (outil | usage | gratuit/payant selon la vidéo | vidéos). "
    "N'invente rien ; si un nom est incertain, écris « à vérifier ». Ne recopie pas les textes : résume. Réponds en français."
)


def propre(t):  # aucune adresse e-mail dans le dépôt public
    return re.sub(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[adresse e-mail retirée]", t
    )


MOD = "gemini-3.5-flash-lite,gemini-3.1-flash-lite,gemini-flash-lite-latest,gemini-3-flash-preview"
for k in range(0, len(V), taille):
    lot = V[k : k + taille]
    n = k // taille + 1
    f = os.path.join(fiches, f"lot-{n:03d}.md")
    if os.path.exists(f):
        continue
    corps = "\n\n".join(
        f"[{k + i + 1}] {v['url']} ({v.get('date') or '?'})\nLégende : {v['legende'][:2500]}\nSous-titres : {v['sous_titres'][:3000]}"
        for i, v in enumerate(lot)
    )
    json.dump(
        {"consigne": C, "texte": corps, "modeles": MOD},
        open("/tmp/lot_corps.json", "w"),
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
            "Content-Type: application/json",
            "--data-binary",
            "@/tmp/lot_corps.json",
            "https://relais-dig-justok1.vercel.app/api/avis",
        ],
        capture_output=True,
        text=True,
    ).stdout
    try:
        j = json.loads(r)
    except Exception:
        print("réponse illisible (relais expiré ?)", r[:150])
        break
    if "avis" not in j:
        print("échec lot", n, str(j)[:300])
        break
    d = [v.get("date") or "?" for v in lot]
    open(f, "w").write(
        f"# Lot {n} : vidéos {k + 1} à {k + len(lot)} (du {d[-1]} au {d[0]})\n\n"
        f"Résumé Gemini ({j.get('modele')}) du {datetime.date.today().isoformat()}, à partir des légendes et "
        f"sous-titres. Affirmations des créateurs non vérifiées : offre gratuite et légalité à contrôler à la source avant tout usage.\n\n{propre(j['avis'].strip())}\n"
    )
    print("ok lot", n, flush=True)
    time.sleep(20)
