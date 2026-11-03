#!/bin/sh
# Liens cassés d'un site entier (pages, images, scripts, liens externes). Outil : Linkinator 8.1.0 (MIT, npm, version du
# 29/08/2026, vérifiée le 03/11/2026), installé à la demande dans le scratchpad, version figée. Demande du 03/11 (« TOUT »).
# Usage : sh outils/liens/verifier.sh https://site.fr   → liste les liens en erreur ; code de sortie 1 s'il y en a.
set -e
SITE="$1"; [ -n "$SITE" ] || { echo "usage : verifier.sh https://site"; exit 2; }
T=$(ls -d /tmp/claude-*/*/*/scratchpad 2>/dev/null | head -n 1)/linkinator
mkdir -p "$T"
[ -x "$T/node_modules/.bin/linkinator" ] || (cd "$T" && npm i --no-audit --no-fund linkinator@8.1.0 >/dev/null 2>&1)
"$T/node_modules/.bin/linkinator" "$SITE" --recurse --timeout 15000 --retry --skip "^mailto:|^tel:" --format json > "$T/resultat.json" || true
python3 - "$T/resultat.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
mauvais=[l for l in d.get("links",[]) if l.get("state")=="BROKEN"]
print(f"{len(d.get('links',[]))} liens vérifiés, {len(mauvais)} cassé(s)")
for l in mauvais: print(f"  {l.get('status')}  {l.get('url')}  (sur {l.get('parent')})")
sys.exit(1 if mauvais else 0)
PY
