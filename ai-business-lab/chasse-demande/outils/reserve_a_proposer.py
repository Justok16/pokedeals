#!/usr/bin/env python3
"""Outils de la réserve à proposer au bon moment (27/10/2026).

Demande de l'utilisateur du 27/10 : « parmi tous les outils que tu as mis de côté, propose-moi d'utiliser certains
d'entre eux quand l'occasion se présentera ; toujours chercher à améliorer ».

Lit `connaissances/reserve-prete.md` (colonnes « Sert à » et « Le ressortir quand… ») et cherche les lignes dont les
mots importants se retrouvent dans un texte : le message de l'utilisateur (crochet UserPromptSubmit) ou une tâche
(`--texte`). Ne propose rien si moins de 2 mots communs, au plus 3 outils : pas de bruit sur un simple « fait ».

    python3 outils/reserve_a_proposer.py --texte "premier client, il veut corriger sa maquette"
    echo '{"prompt": "..."}' | python3 outils/reserve_a_proposer.py --crochet
"""
import argparse
import json
import os
import re
import sys
import unicodedata

ICI = os.path.dirname(os.path.abspath(__file__))
RESERVE = os.path.join(ICI, "..", "connaissances", "reserve-prete.md")

VIDES = {"avec", "dans", "pour", "sans", "sous", "chez", "entre", "vers", "depuis", "pendant", "avant", "apres", "plus", "moins", "tres", "tout", "tous", "toute", "toutes", "cette", "ceci", "cela", "celui", "celle", "ceux", "elle", "elles", "nous", "vous", "leur", "leurs", "mais", "donc", "ainsi", "alors", "aussi", "comme", "quand", "quoi", "quel", "quelle", "quels", "quelles", "dont", "etre", "avoir", "fait", "faire", "sont", "sera", "seront", "peut", "peuvent", "doit", "faut", "deja", "encore", "jamais", "rien", "chaque", "meme", "autre", "autres", "outil", "outils", "gratuit", "gratuite", "offre", "compte", "site", "sites", "besoin", "lire", "seulement", "utiliser", "utile", "utilise", "selon", "voir", "ligne", "lignes", "texte", "textes", "premier", "premiere", "client", "clients", "veut", "veulent", "voulez", "vouloir", "peux", "pouvez", "comment", "pourquoi", "aider", "aide"}


def mots(texte):
    t = unicodedata.normalize("NFD", texte.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    # racine grossière (4 premières lettres) : « corriger » rejoint « corrections », « artisans » rejoint « artisan »
    return {m[:4] for m in re.findall(r"[a-z0-9]+", t) if len(m) >= 4 and m not in VIDES}


def lignes_reserve(chemin=RESERVE):
    sortie, section = [], ""
    try:
        with open(chemin, encoding="utf-8") as fh:
            contenu = fh.read().splitlines()
    except OSError:
        return sortie
    for ligne in contenu:
        if ligne.startswith("## "):
            section = ligne[3:].strip()
            continue
        if not ligne.startswith("|") or set(ligne) <= set("|-: "):
            continue
        cases = [c.strip() for c in ligne.strip("|").split("|")]
        if len(cases) < 3 or cases[1].lower().startswith("sert à"):  # ligne d'en-tête
            continue
        outil = re.sub(r"\s*\(.*?\)\s*", " ", cases[0]).replace("**", "").replace("`", "").strip()
        sortie.append({"section": section, "outil": outil, "sert": cases[1], "quand": cases[2],
                       "cles": mots(cases[0] + " " + cases[1] + " " + cases[2])})
    return sortie


def proposer(texte, maxi=3, seuil=2):
    cible = mots(texte)
    if len(cible) < 2:
        return []
    notes = []
    for r in lignes_reserve():
        communs = r["cles"] & cible
        if len(communs) >= seuil:
            notes.append((len(communs), r, sorted(communs)))
    notes.sort(key=lambda x: -x[0])
    return notes[:maxi]


def rendu(propositions):
    return " ; ".join(
        f"{r['outil']} : {r['sert']} (le ressortir quand : {r['quand']} ; mots communs : {', '.join(c[:4])})"
        for _, r, c in propositions)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Outils de la réserve à proposer au bon moment")
    ap.add_argument("--texte", help="texte de la tâche ou du message")
    ap.add_argument("--crochet", action="store_true", help="lit le JSON du crochet UserPromptSubmit sur l'entrée")
    a = ap.parse_args(argv)
    if a.crochet:
        try:
            texte = json.load(sys.stdin).get("prompt", "")
        except (ValueError, AttributeError):
            return 0
        props = proposer(texte)
        if props:
            msg = ("RÉSERVE À PROPOSER (demande de l'utilisateur du 27/10 : proposer les outils mis de côté quand "
                   "l'occasion se présente ; vérifier la pertinence, relire la gratuité à la source le jour même, "
                   "ne proposer que si cela sert vraiment la demande) : " + rendu(props))
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                                     "additionalContext": msg}}, ensure_ascii=False))
        return 0
    props = proposer(a.texte or "")
    if not props:
        print("Rien dans la réserve pour ce besoin.")
    for n, r, c in props:
        print(f"[{n}] {r['outil']} ({r['section']})\n    sert à : {r['sert']}\n    quand : {r['quand']}\n"
              f"    mots communs : {', '.join(c)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
