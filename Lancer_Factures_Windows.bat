@echo off
chcp 65001 >nul
title Générateur de Factures - Global Solutions

echo ===================================
echo    GÉNÉRATEUR DE FACTURES
echo    GLOBAL SOLUTIONS
echo ===================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if template exists
if not exist "MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf" (
    echo ❌ ERREUR: Template PDF manquant!
    echo.
    echo Le fichier "MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf"
    echo doit être dans le même dossier que ce programme.
    echo.
    pause
    exit /b 1
)

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo.
    echo Veuillez installer Python depuis: https://python.org
    echo Assurez-vous de cocher "Add to PATH" lors de l'installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python trouvé
python --version

REM Install PDF libraries
echo.
echo 📦 Vérification des librairies PDF...
python -c "import reportlab, pdfrw" >nul 2>&1
if errorlevel 1 (
    echo Installation des librairies PDF en cours...
    python -m pip install reportlab pdfrw --user --quiet
    if errorlevel 1 (
        echo ⚠️ Installation échouée, tentative sans --user
        python -m pip install reportlab pdfrw --quiet
    )
)

REM Test PDF libraries
python -c "import reportlab, pdfrw; print('✅ Librairies PDF OK')" 2>nul
if errorlevel 1 (
    echo ❌ Problème avec les librairies PDF
    echo Le programme va essayer de continuer...
)

echo.
echo 🚀 Lancement du générateur de factures...
echo.

REM Run the invoice generator
python simple_invoice_windows.py

echo.
echo Programme terminé.
pause