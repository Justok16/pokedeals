#!/bin/sh
# Copie les nouvelles fiches du dossier de travail dans le dépôt (jamais de remplacement), refait les synthèses
# des chaînes touchées, puis commit + push. À lancer une fois par point.
D=/home/user/pokedeals/ai-business-lab/chasse-demande
S="${SCRATCHPAD:-/tmp/claude-0/-home-user-pokedeals/444b8073-9084-510a-bb75-4fe03b0350df/scratchpad}"
cd "$D" || exit 1
touchees=""; total=0
for c in "$S"/fiches3/*/; do
  [ -d "$c" ] || continue
  n=$(basename "$c"); mkdir -p "connaissances/$n"
  r=$(sh outils/synchro_fiches.sh "$c" "connaissances/$n" | sed 's/[^0-9]//g'); r=${r:-0}
  if [ "$r" -gt 0 ]; then touchees="$touchees $n"; total=$((total+r)); fi
done
echo "fiches copiées : $total ($touchees)"
if [ "$total" -gt 0 ]; then
  python3 outils/synthese_chaine.py $touchees >/dev/null 2>&1
  git add connaissances && git -c user.name=Claude -c user.email=noreply@anthropic.com commit -qm "Base de connaissances vidéo : $total fiche(s) ($(echo $touchees | tr ' ' ','))

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HXUPij67xudweYwrEb9uHq" && git push -q -u origin claude/ai-business-portfolio-strategy-96yf4g && echo "poussé"
fi
