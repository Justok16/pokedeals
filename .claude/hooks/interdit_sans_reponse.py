#!/usr/bin/env python3
"""Crochet Stop : bloque une fin de tour qui répond « No response requested ».

Leçon du 20/10/2026 (4 occurrences) : un rappel programmé ou un « Continue » doit toujours être exécuté.
Idée tirée de la vidéo RPS5U6oa03o (21/10) : remplacer une règle écrite par un blocage automatique.
"""
import json
import sys

INTERDIT = "no response requested"


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


if __name__ == "__main__":
    main()
