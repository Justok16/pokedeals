#!/bin/sh
# Installe LanguageTool (correcteur libre, LGPL) pour le français, hors ligne, dans /tmp/lt.
# Téléchargement depuis Maven Central uniquement, empreintes vérifiées (checksum.policy=fail).
# L'API publique en ligne de LanguageTool interdit les requêtes automatiques : on n'y fait pas appel.
set -e
d=$(dirname "$0")
mkdir -p /tmp/lt
cp "$d/pom.xml" /tmp/lt/pom.xml
cd /tmp/lt && mvn -q -B -Dmaven.repo.local=/tmp/lt/m2 dependency:copy-dependencies -DoutputDirectory=/tmp/lt/lib -Dchecksum.policy=fail
echo "LanguageTool installé : $(ls /tmp/lt/lib | wc -l) bibliothèques"
