#!/bin/sh
# Audit qualité de TOUTES les pages d'un site (vitesse, accessibilité, bonnes pratiques, référencement), sur téléphone.
# Outil : Unlighthouse 0.19.1 (MIT, npm, version du 03/10/2026, vérifiée le 03/11/2026). Installé à la demande dans le
# scratchpad (le conteneur peut redémarrer), version figée. Demande de l'utilisateur du 03/11 : « installe Unlighthouse ».
# Usage : sh outils/unlighthouse/audit.sh https://site-a-tester.fr [dossier_de_sortie]
# Sortie : <dossier>/ci-result.json (score par page, de 0 à 1). Budget : 0,80 minimum par catégorie, sinon échec.
set -e
SITE="$1"; [ -n "$SITE" ] || { echo "usage : audit.sh https://site [sortie]"; exit 2; }
ICI=$(cd "$(dirname "$0")" && pwd)
TRAVAIL=$(ls -d /tmp/claude-*/*/*/scratchpad 2>/dev/null | head -n 1)/unlighthouse
SORTIE="${2:-$TRAVAIL/rapport-$(echo "$SITE" | sed 's#https\?://##; s#[/:]#_#g')}"
mkdir -p "$TRAVAIL"
if [ ! -x "$TRAVAIL/node_modules/.bin/unlighthouse-ci" ]; then
  (cd "$TRAVAIL" && PUPPETEER_SKIP_DOWNLOAD=1 npm i --no-audit --no-fund @unlighthouse/cli@0.19.1 puppeteer-core >/dev/null 2>&1)
fi
cp "$ICI/unlighthouse.config.ts" "$TRAVAIL/"
cd "$TRAVAIL" && npx unlighthouse-ci --site "$SITE" --reporter jsonSimple --output-path "$SORTIE"
python3 -c "
import json,sys
for p in json.load(open(sys.argv[1])):
    print(f\"{p['path']:<32} global {p['score']:.2f} · vitesse {p['performance']:.2f} · accessibilité {p['accessibility']:.2f} · bonnes pratiques {p['best-practices']:.2f} · référencement {p['seo']:.2f}\")
" "$SORTIE/ci-result.json"
