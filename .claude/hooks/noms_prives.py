#!/usr/bin/env python3
"""Avant chaque « git commit » : bloque si une ligne ajoutée contient un nom de prospect ou de client (04/11/2026).

Pourquoi : le 04/11/2026, le nom d'un prospect s'est glissé dans un rapport d'audit du dépôt PUBLIC (relevé par le
relecteur). Règle de CLAUDE.md : aucune donnée de prospect dans le dépôt.
Comment : lit les noms dans les fichiers JSON privés (scratchpad/prive/**.json : champs nom, nom_complet, enseigne(s),
dirigeant(s), contact), puis cherche ces noms dans les lignes AJOUTÉES du commit préparé. Aucun nom n'est affiché en
entier dans le message (seulement ses 2 premières lettres), pour ne pas les recopier ailleurs.
Contournement exceptionnel (nom public, ex. une enseigne nationale) : préfixer la commande par NOMS_OK=1.
"""

import glob
import json
import re
import subprocess
import sys

CHAMPS = {"nom", "nom_complet", "enseigne", "enseignes", "dirigeant", "dirigeants", "contact", "gerant"}
COURANTS = {"france", "ruffec", "charente", "garage", "boulangerie", "coiffure", "restaurant", "services", "societe",
            "entreprise", "atelier", "maison", "boucherie", "fleuriste", "epicerie", "auto", "sarl", "eurl", "sas",
            "claude", "service", "petit", "audit", "ligne", "action", "michel", "pierre", "marie", "jean"}


def noms(obj, acc):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() in CHAMPS:
                textes(v, acc, personne=k.lower().startswith(("dirigeant", "contact", "gerant")))
            else:
                noms(v, acc)
    elif isinstance(obj, list):
        for x in obj:
            noms(x, acc)


def textes(v, acc, personne=False):
    if isinstance(v, str):
        propre = re.sub(r"\(.*?\)", " ", v).strip()
        if len(propre) >= 6 and propre.lower() not in COURANTS:
            acc.add(propre)
        for mot in re.findall(r"[A-Za-zÀ-ÿ'-]{5,}", propre):
            if personne and mot.isupper() and mot.lower() not in COURANTS:  # nom de famille (registre)
                acc.add(mot)
    elif isinstance(v, (list, tuple, dict)):
        for x in (v.values() if isinstance(v, dict) else v):
            if x:
                textes(x, acc, personne)


def main():
    try:
        cmd = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    except ValueError:
        return 0
    if not re.search(r"\bgit\b.*\bcommit\b", cmd) or "NOMS_OK=1" in cmd:
        return 0
    acc = set()
    for f in glob.glob("/tmp/claude-0/*/*/scratchpad/prive/**/*.json", recursive=True):
        try:
            with open(f, encoding="utf-8") as h:
                noms(json.load(h), acc)
        except (OSError, ValueError):
            continue
    if not acc:
        return 0
    racine = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=False).stdout.strip()
    diff = subprocess.run(["git", "-C", racine or ".", "diff", "--cached", "-U0", "--no-color"], capture_output=True, check=False,
                          text=True).stdout
    ajouts = "\n".join(l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")).lower()
    trouves = sorted({n for n in acc if re.search(r"(?<![a-zà-ÿ])" + re.escape(n.lower()) + r"(?![a-zà-ÿ])", ajouts)})
    if trouves:
        print("Commit bloqué : nom de prospect ou de client possible dans les lignes ajoutées (dépôt public) : "
              + ", ".join(n[:2] + "…" for n in trouves[:10])
              + ". Retirer le nom (ou NOMS_OK=1 si c'est un nom public sans lien avec un prospect).", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
