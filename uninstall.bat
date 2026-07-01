@echo off
chcp 65001 >nul
setlocal

:: =============================================================================
:: RADI - Script de désinstallation
:: Supprime RADI du démarrage automatique et les raccourcis.
:: =============================================================================

:: Vérifier si on est en mode administrateur
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ⚠️  Ce script doit être exécuté en tant qu'ADMINISTRATEUR !
    echo    Clique droit sur ce fichier et choisis "Exécuter en tant qu'administrateur".
    echo.
    pause
    exit /b 1
)

:: Nom de l'application
set "APP_NAME=RADI"

:: =============================================================================
:: SUPPRESSION DES RACCOURCIS
:: =============================================================================

echo 🗑️  Suppression des raccourcis...

:: Raccourci dans le menu Démarrage
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
if exist "%STARTUP_FOLDER%\%APP_NAME%.lnk" (
    del "%STARTUP_FOLDER%\%APP_NAME%.lnk"
    echo    ✅ Raccourci supprimé du menu Démarrage
) else (
    echo    ❌ Raccourci introuvable dans le menu Démarrage
)

:: Raccourci sur le bureau (Public)
if exist "%PUBLIC%\Desktop\%APP_NAME%.lnk" (
    del "%PUBLIC%\Desktop\%APP_NAME%.lnk"
    echo    ✅ Raccourci supprimé du bureau (Public)
) else (
    echo    ❌ Raccourci introuvable sur le bureau (Public)
)

:: Raccourci sur le bureau (Utilisateur)
if exist "%USERPROFILE%\Desktop\%APP_NAME%.lnk" (
    del "%USERPROFILE%\Desktop\%APP_NAME%.lnk"
    echo    ✅ Raccourci supprimé du bureau (Utilisateur)
) else (
    echo    ❌ Raccourci introuvable sur le bureau (Utilisateur)
)

:: =============================================================================
:: SUPPRESSION DE L'ENTRÉE DANS LE REGISTRE
:: =============================================================================

echo.
echo 🔑 Suppression de l'entrée dans le registre...

reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%APP_NAME%" /f >nul 2>&1
if %errorLevel% equ 0 (
    echo    ✅ Entrée supprimée du registre
) else (
    echo    ⚠️  Entrée introuvable dans le registre (déjà supprimée ?)
)

:: =============================================================================
:: VÉRIFICATION
:: =============================================================================

echo.
echo 🔍 Vérification...

:: Vérifier que le raccourci dans le menu Démarrage a bien été supprimé
if not exist "%STARTUP_FOLDER%\%APP_NAME%.lnk" (
    echo    ✅ Plus de raccourci dans le menu Démarrage
) else (
    echo    ❌ Le raccourci est toujours présent dans le menu Démarrage
)

:: Vérifier que l'entrée dans le registre a bien été supprimée
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%APP_NAME%" >nul 2>&1
if %errorLevel% neq 0 (
    echo    ✅ Plus d'entrée dans le registre
) else (
    echo    ❌ L'entrée est toujours présente dans le registre
)

:: =============================================================================
:: RÉSUMÉ
:: =============================================================================

echo.
echo =========================================================================
echo ✅ DÉSINSTALLATION TERMINÉE !
echo =========================================================================
echo.
echo RADI ne se lancera plus automatiquement au démarrage de Windows.
echo.
echo Pour réinstaller RADI :
    echo   Exécute le fichier install.bat dans le dossier RADI
echo.
echo =========================================================================

pause
endlocal
