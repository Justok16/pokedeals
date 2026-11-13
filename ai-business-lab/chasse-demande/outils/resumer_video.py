#!/usr/bin/env python3
"""Résumé d'UNE vidéo YouTube envoyée par l'utilisateur, par le relais (Gemini gratuit).

Usage : python3 outils/resumer_video.py <id ou lien YouTube> [fichier de cookies, défaut /tmp/cj.txt]
Écrit videos-resumes/<id>.md (en-tête, titre et auteur lus sur YouTube, section « Tri pour DIG16 » À REMPLIR, puis le
résumé) et affiche le résumé. Reste à faire à la main : remplir le tri, ajouter la ligne à 46-registre-videos.md.
Créé le 13/11/2026 (auto-analyse) : deux vidéos traitées à la main le même jour ; un appel au relais SANS « modeles= »
est resté sans réponse (près de 5 minutes perdues), d'où la liste de modèles toujours passée ici.
"""
import datetime
import json
import os
import re
import subprocess
import sys
import urllib.parse

MODELES = "gemini-3.5-flash,gemini-3.6-flash,gemini-3.8-flash"


def curl(*args):
    return subprocess.run(["curl", "-s", *args], capture_output=True, text=True).stdout


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    m = re.search(r"(?:v=|youtu\.be/|shorts/|^)([A-Za-z0-9_-]{11})(?:[?&/]|$)", sys.argv[1])
    if not m:
        sys.exit("identifiant YouTube introuvable")
    vid = m.group(1)
    cookies = sys.argv[2] if len(sys.argv) > 2 else "/tmp/cj.txt"
    ici = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dest = os.path.join(ici, "videos-resumes", vid + ".md")
    if os.path.exists(dest):
        sys.exit(f"déjà résumée : {dest}")
    titre, auteur = "(titre non lu)", "(auteur non lu)"
    try:
        o = json.loads(curl("-m", "20", "https://www.youtube.com/oembed?format=json&url="
                            + urllib.parse.quote(f"https://www.youtube.com/watch?v={vid}", safe="")))
        titre, auteur = o["title"], o["author_name"]
    except Exception:
        pass
    r = curl("-m", "295", "-b", cookies,
             f"https://relais-dig-justok1.vercel.app/api/video?id={vid}&modeles={MODELES}")
    if "Protected by Vercel Authentication" in r or not r.strip():
        sys.exit("relais sans réponse : cookie expiré ? (get_access_to_vercel_url, puis curl -s -L -c /tmp/cj.txt -b /tmp/cj.txt)")
    try:
        d = json.loads(r)
    except Exception:
        sys.exit("réponse illisible du relais : " + r[:200])
    if "resume" not in d:
        sys.exit("pas de résumé : " + str(d.get("erreur", d))[:400])
    resume = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[adresse e-mail retirée]", d["resume"])
    jour = datetime.date.today().strftime("%d/%m/%Y")
    texte = (f"# {vid} — « {titre} »\n\n- Auteur : {auteur} ; lien : https://youtu.be/{vid}\n"
             f"- Envoyée par l'utilisateur ; résumée le {jour} par Gemini (via le relais, modèle {d.get('modele')})\n"
             "- Les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.\n\n"
             f"## Tri pour DIG16 ({jour[:5]})\n\nÀ REMPLIR\n\n## Résumé (Gemini)\n\n{resume}\n")
    with open(dest, "w", encoding="utf-8") as f:
        f.write(texte)
    print(f"{titre} | {auteur}\nécrit : {dest}\n\n{resume}")


if __name__ == "__main__":
    main()
