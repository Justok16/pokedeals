#!/usr/bin/env python3
"""Carte du dossier de travail DIG16 : une ligne par fiche, par fichier de connaissances et par outil (26/10).

Idée tirée de l'article « Claude Second Brain & Folder Workflow » (envoyé le 26/10) : un seul fichier index
dit à l'agent où se trouve chaque information. La carte est fabriquée à partir du titre de chaque fiche
et de la première ligne de description de chaque outil : elle ne s'écrit jamais à la main.

Usage :
  python3 outils/carte.py             écrit CARTE.md à la racine du dossier de travail
  python3 outils/carte.py --verifier  code de sortie 1 si CARTE.md n'est plus à jour (contrôle global)
"""

import ast
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
CARTE = RACINE / "CARTE.md"

# Statut connu des fiches, quand le titre ne le dit pas (décisions de l'utilisateur, CLAUDE.md)
STATUT = {
    "62-campagne-test-du-pouce.md": "campagne abandonnée le 19/10 (la page outil reste)",
}


def titre(fichier: Path) -> str:
    for ligne in fichier.read_text(encoding="utf-8", errors="replace").splitlines():
        if ligne.startswith("# "):
            return re.sub(r"^#\s+(\d+\s+—\s+)?", "", ligne).strip()
    return "(sans titre)"


def description_outil(fichier: Path) -> str:
    texte = fichier.read_text(encoding="utf-8", errors="replace")
    try:
        doc = ast.get_docstring(ast.parse(texte)) or ""
    except SyntaxError:
        doc = ""
    if not doc:
        for ligne in texte.splitlines()[:6]:
            if ligne.startswith("#") and not ligne.startswith("#!") and len(ligne) > 3:
                doc = ligne.lstrip("# ")
                break
    return doc.strip().splitlines()[0] if doc.strip() else "(pas de description)"


def ligne(nom: str, texte: str) -> str:
    texte = texte.replace("|", "/")
    return f"| `{nom}` | {texte} |"


def fabriquer() -> str:
    fiches = sorted(p for p in RACINE.glob("*.md") if re.match(r"\d\d-", p.name))
    actives = [p for p in fiches if p.name.startswith("00") or int(p.name[:2]) >= 31]
    archives = [p for p in fiches if p not in actives]
    out = [
        "# Carte du dossier de travail DIG16",
        "",
        "Fabriquée par `outils/carte.py` (ne pas modifier à la main : relancer l'outil). Une ligne par fichier,",
        "pour savoir où chercher avant de lire. Règles permanentes : `.claude/CLAUDE.md` et",
        "`connaissances/consignes-detaillees.md` ; erreurs à ne pas refaire : `connaissances/lecons.md` ;",
        "liste unique des tâches : `64-mise-en-ordre-administrative.md` § 0.",
        "",
        "## Fiches DIG16 (actives)",
        "",
        "| Fichier | Sujet |",
        "|---|---|",
    ]
    for p in actives:
        t = titre(p)
        if p.name in STATUT:
            t += f" — **{STATUT[p.name]}**"
        out.append(ligne(p.name, t))
    out += ["", "## Connaissances", "", "| Fichier | Sujet |", "|---|---|"]
    for p in sorted((RACINE / "connaissances").glob("*.md")):
        out.append(ligne("connaissances/" + p.name, titre(p)))
    dossiers = sorted(d.name for d in (RACINE / "connaissances").iterdir() if d.is_dir())
    out += ["", f"Sous-dossiers de résumés par source ({len(dossiers)}) : " + ", ".join(dossiers) + "."]
    out += ["", "## Outils", "", "| Outil | Rôle |", "|---|---|"]
    for p in sorted((RACINE / "outils").glob("*.py")):
        out.append(ligne("outils/" + p.name, description_outil(p)))
    out += [
        "",
        "## Archives : chasse à la demande (23 au 25/09/2026, avant le choix de DIG16)",
        "",
        "| Fichier | Sujet |",
        "|---|---|",
    ]
    for p in archives:
        out.append(ligne(p.name, titre(p)))
    for p in sorted(RACINE.glob("radar-*.md")):
        out.append(ligne(p.name, titre(p)))
    return "\n".join(out) + "\n"


def main() -> int:
    contenu = fabriquer()
    if "--verifier" in sys.argv:
        actuel = CARTE.read_text(encoding="utf-8") if CARTE.exists() else ""
        if actuel != contenu:
            print("CARTE.md n'est plus à jour : lancer python3 outils/carte.py")
            return 1
        print("CARTE.md à jour")
        return 0
    CARTE.write_text(contenu, encoding="utf-8")
    print(f"CARTE.md écrite ({contenu.count(chr(10))} lignes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
