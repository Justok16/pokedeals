#!/bin/sh
# Copie dans le dépôt les nouvelles fiches vidéo produites dans le dossier de travail, en une fois
# (au lieu d'un enregistrement et d'une mise en ligne par fiche). Usage :
#   sh synchro_fiches.sh <dossier_de_travail> <dossier_du_depot>
# Affiche le nombre de fiches copiées ; ne remplace jamais une fiche déjà présente dans le dépôt.
src="$1"; dst="$2"; n=0
for f in "$src"/*.md; do
  [ -e "$f" ] || continue
  b=$(basename "$f")
  if [ ! -e "$dst/$b" ]; then cp "$f" "$dst/$b"; n=$((n+1)); fi
done
echo "fiches copiées : $n"
