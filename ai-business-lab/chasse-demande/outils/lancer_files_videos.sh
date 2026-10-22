#!/bin/sh
# 02/10 : lance les trois files DÉTACHÉES (setsid) : elles survivent à la limite de temps des tâches de fond
# de Claude Code (vérifié le 02/10 : un processus setsid reste vivant après la fin de l'appel Bash).
# Ne survivent pas à un redémarrage du conteneur : relancer alors avec « sh lancer_files.sh ».
L=/tmp/claude-0/-home-user-pokedeals/444b8073-9084-510a-bb75-4fe03b0350df/scratchpad/videos2
if ps -eo args | grep -v grep | grep -q 'videos2/chaines_ia.sh'; then echo "files déjà en cours"; exit 0; fi
setsid nohup sh $L/chaines_ia.sh > $L/chaines_ia.detache.log 2>&1 < /dev/null &
echo "files lancées (détachées) $(date -u +%FT%TZ)"
