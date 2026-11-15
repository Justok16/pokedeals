#!/usr/bin/env python3
"""Fiche des effets d'un site : oblige à passer TOUT le catalogue en revue avant de montrer un site ou une démo.

Créé le 15/11/2026 (question de l'utilisateur : « comment être sûr que tu essaieras de l'appliquer aux sites en
construction ? »). Le catalogue `connaissances/effets-prestige.md` garde chaque idée d'effet ; cette fiche prouve que
chacune a été regardée pour CE site.

  python3 outils/fiche_effets.py creer <dossier du site> "<nom du site>"
      écrit <dossier>/EFFETS.md : une ligne par effet du catalogue, colonne « Décision » à remplir par
      « retenu : où » ou « écarté : pourquoi » (pour un client, mettre le dossier hors du dépôt public).
  python3 outils/fiche_effets.py verifier <dossier du site>
      ALERTE (code 1) s'il manque la fiche, si une décision est vide, si un effet du catalogue n'y figure pas
      (catalogue enrichi depuis), ou si aucun effet n'est retenu. À lancer avant de montrer le site à l'utilisateur.
  python3 outils/fiche_effets.py resume <dossier du site>
      affiche les effets retenus et écartés, à recopier dans le message qui montre le site.
"""
import datetime
import os
import re
import sys

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOGUE = os.path.join(ICI, "connaissances", "effets-prestige.md")


def effets():
    """Liste (nom, ce que ça donne) lue dans le tableau du catalogue."""
    lignes = open(CATALOGUE, encoding="utf-8").read().split("\n")
    debut = next(i for i, l in enumerate(lignes) if l.startswith("| Effet |"))
    sortie = []
    for l in lignes[debut + 2:]:
        if not l.startswith("|"):
            break
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) >= 2 and c[0]:
            sortie.append((c[0], c[1]))
    return sortie


def lire(fiche):
    d = {}
    for l in open(fiche, encoding="utf-8").read().split("\n"):
        if l.startswith("|") and not l.startswith("| Effet |") and not l.startswith("|---"):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if len(c) >= 3:
                d[c[0]] = c[2]
    return d


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("creer", "verifier", "resume"):
        sys.exit(__doc__)
    dossier = sys.argv[2]
    fiche = os.path.join(dossier, "EFFETS.md")
    cat = effets()
    if sys.argv[1] == "creer":
        nom = sys.argv[3] if len(sys.argv) > 3 else os.path.basename(os.path.abspath(dossier))
        deja = lire(fiche) if os.path.exists(fiche) else {}
        jour = datetime.date.today().strftime("%d/%m/%Y")
        t = [f"# Effets du site « {nom} » (fiche du {jour})", "",
             "Chaque effet du catalogue `connaissances/effets-prestige.md` est regardé pour ce site. Décision :",
             "« retenu : où » ou « écarté : pourquoi ». Une seule signature forte par page ; rapidité sur téléphone d'abord.", "",
             "| Effet | Ce que ça donne | Décision |", "|---|---|---|"]
        t += [f"| {n} | {q} | {deja.get(n, '')} |" for n, q in cat]
        os.makedirs(dossier, exist_ok=True)
        open(fiche, "w", encoding="utf-8").write("\n".join(t) + "\n")
        print(f"écrit : {fiche} ({len(cat)} effets, {sum(1 for n, _ in cat if deja.get(n))} déjà décidés)")
        print("À faire aussi maintenant : python3 outils/reserve_a_proposer.py --evenement site (puis --evenement photos) : "
              "outils mis en réserve pour un site, à examiner un par un.")
        return
    if not os.path.exists(fiche):
        sys.exit(f"ALERTE : pas de fiche des effets ({fiche}) : lancer « creer » puis la remplir")
    d = lire(fiche)
    if sys.argv[1] == "resume":
        for titre, mot in (("Effets retenus", "retenu"), ("Effets écartés", "écarté")):
            print(titre + " :")
            for n, _ in cat:
                if d.get(n, "").lower().startswith(mot):
                    print(f"  - {n} ({d[n]})")
        return
    alertes = []
    for n, _ in cat:
        v = d.get(n)
        if v is None:
            alertes.append(f"effet du catalogue absent de la fiche : {n} (relancer « creer »)")
        elif not re.match(r"^(retenu|écarté)\s*:\s*\S", v, re.I):
            alertes.append(f"décision manquante ou mal écrite : {n}")
    if not any(v.lower().startswith("retenu") for v in d.values()):
        alertes.append("aucun effet retenu : en choisir au moins un, ou écrire pourquoi dans chaque ligne")
    if alertes:
        print("\n".join("ALERTE : " + a for a in alertes))
        sys.exit(1)
    print(f"Fiche des effets complète : {sum(1 for v in d.values() if v.lower().startswith('retenu'))} retenu(s), "
          f"{sum(1 for v in d.values() if v.lower().startswith('écarté'))} écarté(s).")


if __name__ == "__main__":
    main()
