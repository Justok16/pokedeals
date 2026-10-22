#!/bin/sh
# Après chaque écriture d'un fichier .py : erreurs graves seulement (syntaxe, nom inconnu)
# avec ruff ; renvoie le détail à Claude (code 2) pour correction immédiate.
f=$(python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("tool_input",{}).get("file_path",""))' 2>/dev/null)
case "$f" in *.py) ;; *) exit 0 ;; esac
[ -f "$f" ] || exit 0
command -v ruff >/dev/null 2>&1 || exit 0
if ! sortie=$(ruff check --no-cache --select E9,F63,F7,F82 --output-format concise "$f" 2>&1); then
  echo "Erreur Python détectée par ruff dans $f :" >&2
  echo "$sortie" | head -20 >&2
  exit 2
fi
exit 0
