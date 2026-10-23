#!/bin/sh
# Relance la file des résumés finance si elle ne tourne pas (conteneur redémarré = processus détachés perdus).
# Autorisé par l'utilisateur le 07/10/2026. 22/10 : le réglage local avait disparu avec le conteneur et la file est
# restée arrêtée ; le crochet est donc dans settings.json (SessionStart + UserPromptSubmit) et trouve seul la file
# dans le scratchpad (aucun chemin privé dans le dépôt).
F="$1"
[ -n "$F" ] || F=$(ls -t /tmp/claude-*/*/*/scratchpad/videos3/finance.sh 2>/dev/null | head -n 1)
[ -f "$F" ] || exit 0
[ "$(ps -eo args | grep -cE '[r]esumer_chaine|[t]outes_videos|[v]ideos3/finance\.sh')" = 0 ] || exit 0
# 23/10 : lancé à la main, CLAUDE_PROJECT_DIR est vide → racine déduite de l'emplacement du script
RACINE="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
cd "$RACINE/ai-business-lab/chasse-demande" || exit 0
setsid nohup sh "$F" > "$(dirname "$F")/finance.detache.log" 2>&1 < /dev/null &
echo '{"systemMessage":"File des résumés finance relancée (machine redémarrée)"}'
