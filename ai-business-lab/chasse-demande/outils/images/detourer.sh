#!/bin/sh
# Détourage automatique (retire le fond) d'un logo ou d'une photo d'artisan → PNG transparent.
# Outil : rembg 2.0.86 (MIT, PyPI, vérifié le 03/11/2026), installé à la demande dans un environnement Python du
# scratchpad, version figée. Modèle « isnet-general-use » téléchargé au premier usage (licence à relire alors).
# Demande de l'utilisateur du 03/11 (« TOUT »). Usage : sh outils/images/detourer.sh entree.jpg sortie.png
# Toujours regarder le résultat (bords, détails fins) avant de l'utiliser ; garder l'original.
set -e
[ -f "$1" ] && [ -n "$2" ] || { echo "usage : detourer.sh entree.jpg sortie.png"; exit 2; }
T=$(ls -d /tmp/claude-*/*/*/scratchpad 2>/dev/null | head -n 1)/rembg
if [ ! -x "$T/venv/bin/rembg" ]; then
  python3 -m venv "$T/venv" && "$T/venv/bin/pip" install -q "rembg[cpu,cli]==2.0.86"
fi
"$T/venv/bin/rembg" i -m isnet-general-use "$1" "$2"
echo "détouré : $2"
