#!/usr/bin/env python3
"""Bloque un heredoc non protégé (<<EOF sans guillemets) dont le texte contient un accent grave ou $( (27/10/2026).

Leçon du 27/10 : avec <<EOF, le shell exécute ce qui est entre accents graves, et le texte du résumé d'une vidéo a
perdu ses noms de fichiers. Un mot comme `rm` aurait pu s'exécuter. Il faut écrire <<'EOF'.
Crochet PreToolUse (Bash) : lit la commande sur l'entrée standard (JSON), répond « deny » avec la raison.
"""

import json
import re
import sys

try:
    commande = json.load(sys.stdin).get("tool_input", {}).get("command", "")
except (ValueError, AttributeError):
    sys.exit(0)

# D'abord, retirer le texte des heredocs protégés (<<'X' ou <<"X") : il peut citer « <<EOF » sans danger.
def sans_proteges(texte):
    while True:
        m = re.search(r"<<-?\s*(['\"])([A-Za-z_][A-Za-z0-9_]*)\1", texte)
        if not m:
            return texte
        fin = re.search(rf"^\s*{m.group(2)}\s*$", texte[m.end():], re.M)
        texte = texte[: m.start()] + (texte[m.end() + fin.end():] if fin else "")


commande = sans_proteges(commande)

# <<EOF, <<-EOF, << EOF : délimiteur nu (sans ' ni ") ; le corps va jusqu'à la ligne qui ne contient que ce mot.
for m in re.finditer(r"<<-?\s*([A-Za-z_][A-Za-z0-9_]*)\b", commande):
    mot = m.group(1)
    fin = re.search(rf"^\s*{mot}\s*$", commande[m.end():], re.M)
    corps = commande[m.end(): m.end() + fin.start()] if fin else commande[m.end():]
    if "`" in corps or "$(" in corps:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"Heredoc non protégé (<<{mot}) avec un accent grave ou $( dans le texte : le shell l'exécuterait "
                f"(leçon du 27/10). Écrire <<'{mot}' et passer les variables par l'environnement ou un fichier."
            ),
        }}, ensure_ascii=False))
        sys.exit(0)
sys.exit(0)
