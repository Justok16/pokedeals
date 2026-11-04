@echo off
setlocal
if "%~1"=="" (
  echo Glissez votre fichier CSV sur ce fichier BAT, ou lancez-le depuis PowerShell avec le chemin du CSV.
  echo Exemple: py -3 migration_audit.py correspondances.csv -o rapport_migration.csv
  pause
  exit /b 2
)
py -3 "%~dp0migration_audit.py" "%~1" -o "%~dp0rapport_migration.csv"
set "RC=%ERRORLEVEL%"
echo.
echo Code de sortie: %RC%
pause
exit /b %RC%
