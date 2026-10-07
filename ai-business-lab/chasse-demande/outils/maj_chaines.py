"""Ajoute les nouvelles vidéos des chaînes suivies à leur liste (demande de l'utilisateur du 28/09 :
« à chaque nouvelle vidéo des chaînes Finary et Fintales, prends-les en compte »).

Usage : python3 maj_chaines.py cookies.txt
Pour chaque dossier de connaissances/ qui contient un liste-videos.json, relit la chaîne via le
relais Vercel (/api/chaine) et place en tête de liste les vidéos absentes ; resumer_chaine.py
les traitera ensuite comme les autres (les plus récentes d'abord).
"""

import json
import os
import subprocess
import sys

RELAIS = "https://relais-dig-justok1.vercel.app/api/chaine?chaine="
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "connaissances")


def main():
    cookies = sys.argv[1]
    for nom in sorted(os.listdir(BASE)):
        chemin = os.path.join(BASE, nom, "liste-videos.json")
        if not os.path.exists(chemin):
            continue
        liste = json.load(open(chemin))
        sortie = subprocess.run(
            ["curl", "-s", "-m", "120", "-b", cookies, RELAIS + liste["chaine"]],
            capture_output=True,
            text=True,
        ).stdout
        try:
            neuve = json.loads(sortie)["videos"]
        except Exception:
            print(nom, "lecture impossible (relais ?)", sortie[:80])
            continue
        connues = {v["id"] for v in liste["videos"]}
        nouvelles = [v for v in neuve if v["id"] not in connues]
        if nouvelles:
            liste["videos"] = nouvelles + liste["videos"]
            liste["nombre"] = len(liste["videos"])
            json.dump(
                liste, open(chemin, "w"), ensure_ascii=False, separators=(",", ":")
            )
        print(nom, len(nouvelles), "nouvelle(s) vidéo(s) ; total", len(liste["videos"]))


if __name__ == "__main__":
    main()
