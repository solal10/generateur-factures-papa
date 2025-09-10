@echo off
title Générateur de Factures - Global Solutions

echo ========================================
echo   GÉNÉRATEUR DE FACTURES - PAPA
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé!
    echo.
    echo Télécharge Python sur: https://www.python.org/downloads/
    echo N'oublie pas de cocher "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo Python trouvé! Vérification des dépendances...

REM Install dependencies if needed
pip install -q reportlab pdfrw

if errorlevel 1 (
    echo Installation des dépendances...
    pip install reportlab pdfrw
    if errorlevel 1 (
        echo ERREUR: Impossible d'installer les dépendances
        echo Essaie manuellement: pip install reportlab pdfrw
        pause
        exit /b 1
    )
)

echo Lancement du générateur de factures...
echo.
python pdf_filler.py

if errorlevel 1 (
    echo.
    echo ERREUR lors du lancement!
    pause
)
