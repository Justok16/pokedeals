#!/bin/sh
# Avant chaque « git commit » lancé par Claude : cherche une clé, un jeton ou un mot de passe
# dans les fichiers préparés (règle du dépôt public : aucune clé ni jeton). Bloque le commit
# (code 2, message renvoyé à Claude) si un secret nouveau apparaît. Outil : detect-secrets (Yelp).
cmd=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null)
case "$cmd" in *"git "*commit*) ;; *) exit 0 ;; esac
command -v detect-secrets-hook >/dev/null 2>&1 || { echo "detect-secrets absent : pip install detect-secrets" >&2; exit 0; }
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" || exit 0
fichiers=$(git diff --cached --name-only --diff-filter=ACM | grep -v -E '\.(png|jpe?g|webp|pdf|woff2?|ico)$')
[ -z "$fichiers" ] && exit 0
if ! sortie=$(echo "$fichiers" | tr '\n' '\0' | xargs -0 detect-secrets-hook --baseline .secrets.baseline 2>&1); then
  echo "Commit bloqué : secret possible dans les fichiers préparés (dépôt public)." >&2
  echo "$sortie" | head -30 >&2
  exit 2
fi
exit 0
