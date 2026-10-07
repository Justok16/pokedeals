"""Traite TOUTES les vidéos des chaînes suivies (demande de l'utilisateur du 07/10/2026 : « les 40 467 vidéos »).

Usage : python3 toutes_videos.py <groupe 0|1|2> <dossier_fiches> <cookies.txt>
  (variables MODELES, FPS, LOT_DUREE, COURTE, LOT_MAX, PAUSE transmises à resumer_chaine.py)

- Chaînes : connaissances/<chaine>/liste-videos.json (sauf les comptes TikTok), réparties en 3 groupes
  (chaque groupe a ses propres modèles Gemini, donc ses propres quotas gratuits).
- Pour chaque chaîne, la file « reste » = vidéos prioritaires (prio.json) puis toute la liste, sans celles
  déjà résumées (dans le dépôt ou dans le dossier de travail).
- Les vidéos de plus de 2 h vont dans une file à part (longues.json) : une seule dépasserait la limite
  gratuite de jetons par minute ; elles seront résumées par morceaux (resumer_video_longue.py).
- Tour par tour : au plus TOUR minutes de vidéo par chaîne et par tour, pour que les grosses chaînes
  ne bloquent pas les autres. S'arrête dès que les modèles du groupe ont épuisé leur quota du jour.
"""

import json
import os
import subprocess
import sys

RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CONNAISSANCES = os.path.join(RACINE, "connaissances")
EXCLUES = {"unefille", "iaboss"}  # comptes TikTok, traités autrement
SANS_MODE_FINANCE = {"gabzer", "melvynx", "mreflow"}
TOUR = int(os.environ.get("TOUR", 240))  # minutes de vidéo par chaîne et par tour
LONGUE = 2 * 3600


def secondes(d):
    p = [int(x) for x in str(d).split(":") if x.isdigit()] or [0]
    while len(p) < 3:
        p.insert(0, 0)
    return p[0] * 3600 + p[1] * 60 + p[2]


def chaines():
    return sorted(
        c
        for c in os.listdir(CONNAISSANCES)
        if c not in EXCLUES
        and os.path.exists(os.path.join(CONNAISSANCES, c, "liste-videos.json"))
    )


def reste(c, fiches):
    liste = json.load(open(os.path.join(CONNAISSANCES, c, "liste-videos.json")))[
        "videos"
    ]
    f_prio = os.path.join(CONNAISSANCES, c, "prio.json")
    prio = json.load(open(f_prio))["videos"] if os.path.exists(f_prio) else []
    vus, ordre = set(), []
    for v in prio + liste:
        if v["id"] not in vus:
            vus.add(v["id"])
            ordre.append(v)

    def fait(i):
        return os.path.exists(
            os.path.join(CONNAISSANCES, c, i + ".md")
        ) or os.path.exists(os.path.join(fiches, c, i + ".md"))

    a_faire = [v for v in ordre if not fait(v["id"])]
    os.makedirs(os.path.join(fiches, c), exist_ok=True)
    courtes = [v for v in a_faire if secondes(v["duree"]) <= LONGUE]
    longues = [v for v in a_faire if secondes(v["duree"]) > LONGUE]
    json.dump(
        {"videos": courtes},
        open(os.path.join(fiches, c, ".reste.json"), "w"),
        ensure_ascii=False,
    )
    json.dump(
        {"videos": longues},
        open(os.path.join(fiches, c, ".longues.json"), "w"),
        ensure_ascii=False,
    )
    return len(courtes)


def main():
    groupe, fiches, cookies = int(sys.argv[1]), sys.argv[2], sys.argv[3]
    # répartition équilibrée et stable : chaînes triées par taille de liste, chacune au groupe le moins chargé
    charge, groupes = [0, 0, 0], [[], [], []]
    tailles = {
        c: len(
            json.load(open(os.path.join(CONNAISSANCES, c, "liste-videos.json")))[
                "videos"
            ]
        )
        for c in chaines()
    }
    for c in sorted(tailles, key=lambda x: (-tailles[x], x)):
        g = charge.index(min(charge))
        groupes[g].append(c)
        charge[g] += tailles[c]
    mes_chaines = groupes[groupe]
    print("groupe", groupe, "chaînes :", " ".join(mes_chaines), flush=True)
    while True:
        restantes = 0
        for c in mes_chaines:
            n = reste(c, fiches)
            restantes += n
            if not n:
                continue
            mode = "" if c in SANS_MODE_FINANCE else "finance"
            r = subprocess.run(
                [
                    "python3",
                    os.path.join(RACINE, "outils", "resumer_chaine.py"),
                    os.path.join(fiches, c, ".reste.json"),
                    os.path.join(fiches, c),
                    cookies,
                    str(TOUR),
                    mode,
                ],
                capture_output=True,
                text=True,
                cwd=RACINE,
            )
            sortie = r.stdout + r.stderr
            print(f"--- {c} ({n} à faire)\n{sortie.strip()[-1500:]}", flush=True)
            if (
                "épuisé leur quota" in sortie
                or "cookie du relais" in sortie
                or r.returncode == 3
            ):
                print(
                    "arrêt du groupe : quota du jour épuisé ou relais à renouveler",
                    flush=True,
                )
                return
        if not restantes:
            print("toutes les vidéos de ce groupe sont résumées", flush=True)
            return


if __name__ == "__main__":
    main()
