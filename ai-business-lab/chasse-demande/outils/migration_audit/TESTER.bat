@echo off
setlocal
pushd "%~dp0"
set "TEMP_RELEASE=%TEMP%\dig16-migration-audit-verification.zip"

echo [1/4] Verification de Python 3.11+
py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)"
if errorlevel 1 goto failed

echo.
echo [2/4] Compilation des scripts
py -3 -m py_compile "%~dp0migration_audit.py" "%~dp0build_release.py"
if errorlevel 1 goto failed

echo.
echo [3/4] Tests unitaires
py -3 -m unittest discover -s "%~dp0tests" -v
if errorlevel 1 goto failed

echo.
echo [4/4] Construction et verification d'une archive de controle
py -3 "%~dp0build_release.py" --output "%TEMP_RELEASE%"
if errorlevel 1 goto failed

echo.
echo Tous les controles locaux ont reussi.
echo Archive de controle : %TEMP_RELEASE%
echo Somme SHA-256 : %TEMP_RELEASE%.sha256
pause
popd
exit /b 0

:failed
echo.
echo Echec d'un controle. Le code de sortie est %ERRORLEVEL%.
pause
popd
exit /b 1
