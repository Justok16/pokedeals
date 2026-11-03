#!/bin/sh
# Copie tarteaucitron.js 1.37.0 (MIT, version figée vérifiée le 03/11/2026) dans <site>/tarteaucitron/.
set -e
SITE="$1"; [ -d "$SITE" ] || { echo "usage : recuperer.sh <dossier_du_site>"; exit 2; }
T=$(mktemp -d)
(cd "$T" && npm pack tarteaucitronjs@1.37.0 >/dev/null 2>&1 && tar xzf tarteaucitronjs-1.37.0.tgz)
P="$T/package"; D="$SITE/tarteaucitron"
mkdir -p "$D/lang" "$D/css"
cp "$P/LICENSE" "$P/tarteaucitron.min.js" "$P/tarteaucitron.services.min.js" "$D/"
cp "$P/lang/tarteaucitron.fr.min.js" "$D/lang/"
cp -r "$P/css/." "$D/css/"
rm -rf "$T"
echo "tarteaucitron 1.37.0 copié dans $D"
