#!/usr/bin/env python3
"""Garde-fou des quotas de publication (19/10/2026).

Leçon du 19/10 : une série de publications a été programmée sur Metricool sans vérifier la limite de l'offre
gratuite (20 publications publiées par mois, aide Metricool lue le 19/10). Noter la leçon ne suffit pas : ce crochet
BLOQUE toute nouvelle publication programmée au-delà du quota du mois.

Fonctionnement (crochet PreToolUse sur createScheduledPost de Metricool) :
- le registre .claude/hooks/quotas.json donne, par outil, la limite et le nombre déjà publié ou programmé par mois ;
- un mois absent du registre = compte inconnu → refus : lire d'abord getScheduledPosts pour ce mois et l'inscrire ;
- un brouillon (draft true) ne compte pas ; une publication acceptée incrémente le mois.
Pour changer la limite (offre payante choisie par l'utilisateur), modifier « limite » dans quotas.json.
"""

import json
import os
import sys

REGISTRE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quotas.json")


def refuser(raison):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": raison}}, ensure_ascii=False))
    sys.exit(0)


def main():
    donnees = json.load(sys.stdin)
    entree = donnees.get("tool_input", {})
    info = entree.get("info", {})
    if isinstance(info, str):
        try:
            info = json.loads(info)
        except ValueError:
            info = {}
    if info.get("draft") is True:
        return
    date = entree.get("date") or (info.get("publicationDate") or {}).get("dateTime") or ""
    mois = date[:7]
    if len(mois) != 7:
        refuser("Quota : date de publication illisible, impossible de vérifier la limite du mois.")
    with open(REGISTRE, encoding="utf-8") as f:
        reg = json.load(f)
    outil = reg["metricool"]
    compte = outil["mois"].get(mois)
    if compte is None:
        refuser(f"Quota Metricool : le nombre de publications de {mois} n'est pas connu. Lire getScheduledPosts "
                f"pour ce mois (publiées + programmées hors brouillons), l'inscrire dans .claude/hooks/quotas.json, "
                f"puis recommencer.")
    if compte >= outil["limite"]:
        refuser(f"Quota Metricool atteint pour {mois} : {compte}/{outil['limite']} (offre gratuite, au-delà rien "
                f"n'est publié). Mettre en brouillon, reporter au mois suivant ou passer par un autre outil.")
    outil["mois"][mois] = compte + 1
    with open(REGISTRE, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
