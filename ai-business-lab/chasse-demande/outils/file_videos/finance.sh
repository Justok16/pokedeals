#!/bin/sh
# File des résumés vidéo (recréée le 22/10/2026 après la perte du dossier de travail au redémarrage du 21/10).
# 4 groupes de chaînes, chacun avec ses propres modèles Gemini (quotas gratuits séparés), via le relais Vercel
# (cookie /tmp/cj.txt, renouvelé par le rappel dédié). Chaque groupe attend seul la remise à zéro des quotas.
D=/home/user/pokedeals/ai-business-lab/chasse-demande
S="${SCRATCHPAD:-/tmp/claude-0/-home-user-pokedeals/444b8073-9084-510a-bb75-4fe03b0350df/scratchpad}"
cd "$D" || exit 1
lancer() { # groupe modèles
  setsid nohup env NB_GROUPES=4 MODELES="$2" python3 outils/toutes_videos.py "$1" "$S/fiches3" /tmp/cj.txt \
    >> "$S/videos3/file_g$1.log" 2>&1 < /dev/null &
}
lancer 0 "gemini-3.8-flash,gemini-3.7-flash"
lancer 1 "gemini-3.6-flash,gemini-3.5-flash"
lancer 2 "gemini-3-flash-preview,gemini-3.5-flash-lite"
lancer 3 "gemini-3.1-flash-lite,gemini-3.1-flash-lite-preview,gemini-flash-lite-latest"
echo "4 groupes lancés $(date -u +%d/%m\ %H:%M) UTC"
