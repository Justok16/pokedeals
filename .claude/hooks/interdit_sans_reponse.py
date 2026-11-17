#!/usr/bin/env python3
"""Crochet Stop : bloque une fin de tour qui répond « No response requested ».

Leçon du 20/10/2026 (4 occurrences) : un rappel programmé ou un « Continue » doit toujours être exécuté.
Idée tirée de la vidéo RPS5U6oa03o (21/10) : remplacer une règle écrite par un blocage automatique.
"""
import json
import sys

INTERDIT = "no response requested"
# 17/11/2026 : panne d'outil signalée à l'utilisateur au lieu d'être réparée (consigne : « je te laisse toujours
# gérer seul ce genre de problème »). Ces tournures bloquent la fin du tour : réparer d'abord, puis le dire.
NON_REPARE = (
    "pas encore réparé", "pas encore regardé", "pas encore cherché à", "je n'ai pas réparé",
    "je n'ai pas encore réparé", "je n'ai pas encore corrigé", "reste à réparer", "réparer plus tard",
    "toujours en panne", "reste en panne", "je n'ai pas encore cherché",
)


def dernier_texte(chemin):
    texte = ""
    try:
        with open(chemin, encoding="utf-8") as f:
            for ligne in f:
                try:
                    d = json.loads(ligne)
                except ValueError:
                    continue
                if d.get("type") != "assistant":
                    continue
                contenu = (d.get("message") or {}).get("content") or []
                morceaux = [c.get("text", "") for c in contenu if isinstance(c, dict) and c.get("type") == "text"]
                if morceaux:
                    texte = "\n".join(morceaux)
    except OSError:
        return ""
    return texte


def main():
    try:
        entree = json.load(sys.stdin)
    except ValueError:
        return
    if entree.get("stop_hook_active"):
        return
    texte = entree.get("last_assistant_message") or dernier_texte(entree.get("transcript_path", ""))
    t = (texte or "").strip().lower()
    # Bloque la réponse vide elle-même, pas un message qui la cite pour l'expliquer (faux positif du 21/10).
    if INTERDIT in t and len(t) < 80:
        print(json.dumps({
            "decision": "block",
            "reason": "Réponse interdite (« No response requested ») : reprends la tâche ouverte "
                      "(dernier rappel programmé ou « Continue ») avec les outils, puis réponds en français.",
        }))
        return
    import re
    # les tournures citées entre guillemets (pour expliquer le crochet) ne comptent pas : faux positif du 17/11
    t2 = re.sub(r"«[^»]*»|\"[^\"]*\"|`[^`]*`", " ", t.replace("’", "'"))
    trouve = [x for x in NON_REPARE if x in t2]
    if trouve:
        print(json.dumps({
            "decision": "block",
            "reason": f"Panne signalée sans réparation ({trouve[0]!r}) : consigne du 17/11, répare d'abord l'outil "
                      "ou le service toi-même (autre méthode, autre outil gratuit, dépendance à installer), vérifie, "
                      "puis dis-le en une ligne. Seules une protection automatique ou une décision qui engage "
                      "l'utilisateur justifient de lui demander.",
        }))


if __name__ == "__main__":
    main()
