@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: =============================================================================
:: RADI - Script d'installation automatique pour Windows
:: Ce script ajoute RADI au démarrage et crée un raccourci dans le menu Démarrer.
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

:: =============================================================================
:: CONFIGURATION
:: =============================================================================

:: Chemin vers Python (par défaut : python.exe dans le PATH)
set "PYTHON_EXE=python.exe"

:: Chemin vers le script principal (ce fichier est dans le même dossier)
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_PATH=%SCRIPT_DIR%radi.py"

:: Nom de l'application
set "APP_NAME=RADI"

:: =============================================================================
:: VÉRIFIER QUE PYTHON EST INSTALLÉ
:: =============================================================================

echo 🔍 Vérification de Python...
%PYTHON_EXE% --version >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ❌ Python n'est pas installé ou n'est pas dans le PATH.
    echo.
    echo    Option 1 : Installer Python depuis https://www.python.org/downloads/
    echo    Option 2 : Modifier PYTHON_EXE dans ce script pour pointer vers python.exe
    echo.
    pause
    exit /b 1
)

:: Vérifier la version de Python (3.10+ recommandé)
for /f "tokens=2 delims== " %%v in ('%PYTHON_EXE% --version 2^>^&1') do set "PYTHON_VERSION=%%v"
echo    Version de Python : %PYTHON_VERSION%

:: Extraire la version majeure
for /f "tokens=1 delims=. " %%a in ('echo %PYTHON_VERSION%') do set "PY_MAJOR=%%a"
if %PY_MAJOR% lss 3 (
    echo.
    echo ❌ Python 3.10 ou supérieur est requis. Version détectée : %PYTHON_VERSION%
    echo.
    pause
    exit /b 1
)

:: =============================================================================
:: VÉRIFIER QUE PYQT6 EST INSTALLÉ
:: =============================================================================

echo.
echo 🔍 Vérification de PyQt6...
%PYTHON_EXE% -c "import PyQt6" >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ⚠️  PyQt6 n'est pas installé. Installation en cours...
    %PYTHON_EXE% -m pip install PyQt6 --user
    if %errorLevel% neq 0 (
        echo.
        echo ❌ Échec de l'installation de PyQt6.
        echo    Essayez : pip install PyQt6
        echo.
        pause
        exit /b 1
    )
    echo    ✅ PyQt6 installé avec succès !
) else (
    echo    ✅ PyQt6 est déjà installé.
)

:: =============================================================================
:: CRÉER LES DOSSIERS NÉCESSAIRES
:: =============================================================================

if not exist "%SCRIPT_DIR%assets" mkdir "%SCRIPT_DIR%assets"
if not exist "%SCRIPT_DIR%data" mkdir "%SCRIPT_DIR%data"

:: Créer un fichier radi.png par défaut s'il n'existe pas
if not exist "%SCRIPT_DIR%assets\radi.png" (
    echo.
    echo 🎨 Création d'un placeholder pour radi.png...
    echo    > "%SCRIPT_DIR%assets\radi_instructions.txt" (
    Pour personnaliser l'apparence de RADI :
    1. Crée une image 'radi.png' (150x150 pixels) dans le dossier 'assets/'
    2. Utilise un outil comme Paint, GIMP ou Photoshop
    3. Exemples d'idées :
       - Un petit robot mignon
       - Un animal (renard, hibou, etc.)
       - Un personnage style pixel art
    
    Format recommandé : PNG avec transparence
    Taille recommandée : 150x150 pixels
    )
)

:: =============================================================================
:: CRÉER UN RACCOURCI DANS LE MENU DÉMARRAGE
:: =============================================================================

echo.
echo 📁 Création du raccourci dans le menu Démarrage...

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\%APP_NAME%.lnk"

:: Utiliser PowerShell pour créer le raccourci (plus fiable)
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%PYTHON_EXE%'; $Shortcut.Arguments = '%SCRIPT_PATH%'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.IconLocation = '%SCRIPT_DIR%assets\radi.png,0'; $Shortcut.Save()"

if exist "%SHORTCUT_PATH%" (
    echo    ✅ Raccourci créé : %SHORTCUT_PATH%
) else (
    echo    ❌ Échec de la création du raccourci.
    echo    Essayez de créer manuellement un raccourci vers : %PYTHON_EXE% %SCRIPT_PATH%
)

:: =============================================================================
:: AJOUTER AU REGISTRE POUR UN DÉMARRAGE PLUS FIABLE
:: =============================================================================

echo.
echo 🔑 Ajout au registre Windows pour un démarrage automatique...

reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%APP_NAME%" /t REG_SZ /d "%PYTHON_EXE% %SCRIPT_PATH%" /f >nul 2>&1

:: Vérifier que l'entrée a bien été ajoutée
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%APP_NAME%" >nul 2>&1
if %errorLevel% equ 0 (
    echo    ✅ Entrée ajoutée au registre.
) else (
    echo    ⚠️  Impossible d'ajouter au registre. Le raccourci dans le menu Démarrage devrait suffire.
)

:: =============================================================================
:: CRÉER UN RACCOURCI SUR LE BUREAU (OPTIONNEL)
:: =============================================================================

echo.
echo 🖥️  Création d'un raccourci sur le bureau (optionnel)...

set "DESKTOP=%PUBLIC%\Desktop"
if not exist "%DESKTOP%" set "DESKTOP=%USERPROFILE%\Desktop"

powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\%APP_NAME%.lnk'); $Shortcut.TargetPath = '%PYTHON_EXE%'; $Shortcut.Arguments = '%SCRIPT_PATH%'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.IconLocation = '%SCRIPT_DIR%assets\radi.png,0'; $Shortcut.Save()"

if exist "%DESKTOP%\%APP_NAME%.lnk" (
    echo    ✅ Raccourci créé sur le bureau.
) else (
    echo    ⚠️  Impossible de créer le raccourci sur le bureau.
)

:: =============================================================================
:: CRÉER UN FICHIER DE DÉSINSTALLATION
:: =============================================================================

echo.
echo 🗑️  Création du script de désinstallation...

(
    echo @echo off
    echo chcp 65001 >nul
    echo.
    echo echo Suppression de RADI du démarrage...
    echo.
    echo :: Supprimer le raccourci dans le menu Démarrage
    echo if exist "%%APPDATA%%\Microsoft\Windows\Start Menu\Programs\Startup\%APP_NAME%.lnk" del "%%APPDATA%%\Microsoft\Windows\Start Menu\Programs\Startup\%APP_NAME%.lnk"
    echo.
    echo :: Supprimer l'entrée du registre
    echo reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%APP_NAME%" /f >nul 2^>&1
    echo.
    echo :: Supprimer le raccourci du bureau
    echo if exist "%%PUBLIC%%\Desktop\%APP_NAME%.lnk" del "%%PUBLIC%%\Desktop\%APP_NAME%.lnk"
    echo if exist "%%USERPROFILE%%\Desktop\%APP_NAME%.lnk" del "%%USERPROFILE%%\Desktop\%APP_NAME%.lnk"
    echo.
    echo echo ✅ RADI a été désinstallé.
    echo pause
) > "%SCRIPT_DIR%uninstall.bat"

echo    ✅ Script de désinstallation créé : uninstall.bat

:: =============================================================================
:: RÉSUMÉ
:: =============================================================================

echo.
echo =========================================================================
echo ✅ INSTALLATION TERMINÉE !
echo =========================================================================
echo.
echo RADI est maintenant installé et se lancera automatiquement au prochain
echo démarrage de Windows.
echo.
echo Pour tester immédiatement :
    echo   1. Double-clique sur "%APP_NAME%.lnk" sur le bureau
    echo   2. Ou exécute : %PYTHON_EXE% %SCRIPT_PATH%
echo.
echo Pour désinstaller :
    echo   Exécute le fichier uninstall.bat dans ce dossier
echo.
echo Dossier d'installation : %SCRIPT_DIR%
echo.
echo =========================================================================

pause
endlocal
