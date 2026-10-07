#!/bin/sh
# Au démarrage d'une session (conteneur redémarré = processus détachés perdus) : relance la file des résumés finance
# si elle ne tourne pas. Autorisé par l'utilisateur le 07/10/2026 ; enregistré seulement dans settings.local.json.
F="$1"
[ -f "$F" ] || exit 0
[ "$(ps -eo args | grep -c '[r]esumer_chaine')" = 0 ] || exit 0
cd "$CLAUDE_PROJECT_DIR/ai-business-lab/chasse-demande" || exit 0
setsid nohup sh "$F" > "$(dirname "$F")/finance.detache.log" 2>&1 < /dev/null &
echo '{"systemMessage":"File des résumés finance relancée"}'
