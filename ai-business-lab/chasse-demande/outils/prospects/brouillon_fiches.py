"""Brouillon des fiches d'un ajout à partir d'un lot pré-vérifié (lot_rge.py + mappy_lot.py).

Usage : python3 brouillon_fiches.py <dossier appels> <numéro de lot> <idx> [<idx> ...]
Imprime, pour chaque index retenu, un tuple prêt à coller dans build<N>.py :
(nom, "métier (effectif) · Dirigeant", commune, téléphone, situation, accroche).
Le métier et la situation restent à relire et à reformuler à la main ; l'outil fait la mise en forme
(enseigne en casse normale, commune avec accents, effectif « 1 à 2 salariés », année de création,
adresse abrégée, premier numéro de la fiche Mappy ou de l'ADEME). Rien n'est écrit sur disque.
"""

import json
import os
import re
import sys

MIN = {
    "de",
    "du",
    "des",
    "la",
    "le",
    "les",
    "et",
    "en",
    "à",
    "au",
    "aux",
    "sur",
    "sous",
    "d'",
    "l'",
}
SIGLES = {
    "eurl",
    "sarl",
    "sas",
    "sasu",
    "ei",
    "snc",
    "rge",
    "tp",
    "bge",
    "hvf",
    "dme",
    "id",
    "bms",
    "tplc",
    "sos",
}


def casse(t):
    """« AU SALON D'ELONA » → « Au Salon d'Elona » ; sigles connus en capitales."""
    t = t.replace("’", "'")
    mots = []
    for i, m in enumerate(re.split(r"(\s+)", t.strip())):
        if not m.strip():
            mots.append(m)
            continue
        parts = m.split("'")
        out = []
        for j, p in enumerate(parts):
            pl = p.lower()
            if pl in SIGLES or (
                p.isupper() and len(p) <= 3 and p.isalpha() and i > 0 and pl not in MIN
            ):
                out.append(p.upper())
            elif i > 0 and pl in MIN and j == 0:
                out.append(pl)
            elif j > 0 and pl in ("d", "l"):
                out.append(pl)
            else:
                out.append(p[:1].upper() + p[1:].lower())
        mots.append("'".join(out))
    return "".join(mots).replace("'", "’")


def enseigne(nom):
    """Dernière parenthèse = enseigne ; sinon le nom entier (sans la parenthèse du nom de naissance)."""
    p = re.findall(r"\(([^)]*)\)", nom)
    if p:
        return casse(p[-1])
    return casse(nom)


def dirigeant(d):
    """« NARFIT Emilie » → « Emilie Narfit » ; plusieurs dirigeants séparés par « et »."""
    if not d:
        return ""
    noms = []
    for x in re.split(r"\s*,\s*", d):
        x = x.strip()
        if not x:
            continue
        m = re.match(r"^([A-ZÀ-Ý][A-ZÀ-Ý\- ]+?)\s+([A-ZÀ-Ý][a-zà-ÿ].*)$", x)
        if m:
            noms.append(
                f"{m[2].strip()} {m[1].strip().title().replace(' De ', ' de ')}"
            )
        else:
            noms.append(x)
    return " et ".join(noms)


def effectif(e):
    e = (e or "").lower()
    m = re.search(r"entre (\d+) et (\d+)", e)
    if m:
        return f"{m[1]} à {m[2]} salariés"
    if "au moins 1" in e:
        return "au moins 1 salarié"
    if "0 salari" in e:
        return "0 salarié"
    return "effectif non publié"


def commune(c):
    c = (
        c.title()
        .replace(" Sur ", "-sur-")
        .replace(" De ", "-de-")
        .replace(" La ", "-la-")
        .replace(" Le ", "-le-")
        .replace(" Les ", "-les-")
        .replace(" Des ", "-des-")
        .replace(" En ", "-en-")
        .replace(" Et ", "-et-")
    )
    c = re.sub(r"-(Sur|De|La|Le|Les|Des|En|Et)-", lambda m: "-" + m[1].lower() + "-", c)
    c = c.replace("L'", "L’").replace("D'", "D’")
    return c


def adresse(a, com):
    a = re.sub(r"\s*\d{5}\s+" + re.escape(com) + r"\s*$", "", a or "", flags=re.I)
    a = a.title()
    a = (
        re.sub(r"\b(Rte)\b", "route", a)
        .replace(" Rue ", " rue ")
        .replace(" Av ", " avenue ")
        .replace(" Avenue ", " avenue ")
        .replace(" Pl ", " place ")
        .replace(" Place ", " place ")
        .replace(" Imp ", " impasse ")
        .replace(" Impasse ", " impasse ")
        .replace(" Che ", " chemin ")
        .replace(" Chemin ", " chemin ")
        .replace(" Route ", " route ")
        .replace(" Bd ", " boulevard ")
        .replace(" Ld ", "")
        .replace(" All ", " allée ")
    )
    a = re.sub(
        r"^(Rue|Route|Avenue|Place|Impasse|Chemin|Boulevard|Allée) ",
        lambda m: m[1].lower() + " ",
        a,
    )
    a = re.sub(r"\b(De|Du|Des|La|Le|Les|Et|D)\b", lambda m: m[1].lower(), a)
    return a.strip()


def main():
    app, lot, idxs = sys.argv[1], sys.argv[2], sys.argv[3:]
    d = json.load(open(os.path.join(app, f"lot{lot}.json")))
    for k in idxs:
        e = d[k]
        p = e.get("pappers", {})
        tel = ""
        if e.get("ademe", {}).get("tels"):
            tel = e["ademe"]["tels"][0]
        elif ((e.get("mappy") or {}).get("fiche") or {}).get("tels"):
            tel = e["mappy"]["fiche"]["tels"][0]
        annee = (p.get("creation") or "")[-4:]
        act = (
            (p.get("activite") or "")
            .split("Code NAF")[0]
            .split("Autres activités")[0]
            .strip()
            .rstrip(".")
        )
        nom = enseigne(e["nom"])
        com = commune(e["commune"])
        adr = adresse(e.get("adresse"), e["commune"])
        metier = f"{act[:60]} ({effectif(p.get('effectif'))}) · {dirigeant(p.get('dirigeants'))}"
        situation = f"Annuaire seulement (Mappy) ; aucun site. Entreprise créée en {annee}, {adr}."
        print(
            f'("{nom}","{metier}","{com}","{tel}","{situation}","Annuaire seulement"),'
        )
        print(f"#   idx {k} : {e.get('pre_verdict', '')[:90]}")


if __name__ == "__main__":
    main()
