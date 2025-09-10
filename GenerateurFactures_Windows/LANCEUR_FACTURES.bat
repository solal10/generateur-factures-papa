@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
title Générateur de Factures - Global Solutions
color 0A

echo ========================================
echo    GÉNÉRATEUR DE FACTURES
echo    GLOBAL SOLUTIONS
echo ========================================
echo.

cd /d "%~dp0"

:: Check if template exists
if not exist "MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf" (
    echo ❌ ERREUR: Template PDF manquant!
    echo.
    echo Le fichier "MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf"
    echo doit être dans le même dossier.
    echo.
    pause
    exit /b 1
)

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Python n'est pas installé!
        echo.
        echo INSTALLATION RAPIDE:
        echo 1. Allez sur https://www.python.org/downloads/
        echo 2. Téléchargez Python pour Windows
        echo 3. IMPORTANT: Cochez "Add Python to PATH"
        echo 4. Installez et relancez ce programme
        echo.
        pause
        exit /b 1
    ) else (
        set PYTHON=py
    )
) else (
    set PYTHON=python
)

echo ✅ Python trouvé
%PYTHON% --version

:: Install dependencies silently
echo.
echo Vérification des librairies...
%PYTHON% -c "import reportlab, pdfrw" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installation en cours...
    %PYTHON% -m pip install --upgrade pip >nul 2>&1
    %PYTHON% -m pip install reportlab pdfrw --user >nul 2>&1
    if %errorlevel% neq 0 (
        %PYTHON% -m pip install reportlab pdfrw >nul 2>&1
    )
)

:: Verify installation
%PYTHON% -c "import reportlab, pdfrw; print('✅ Librairies OK')" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️ Problème avec les librairies
    echo Tentative de lancement quand même...
)

echo.
echo 🚀 Lancement du générateur...
echo ========================================
echo.

:: Run the generator
if exist "GenerateurFactures_Portable.pyw" (
    %PYTHON% GenerateurFactures_Portable.pyw
) else if exist "simple_invoice_windows.py" (
    %PYTHON% simple_invoice_windows.py
) else (
    echo ❌ Fichier programme introuvable!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Programme terminé.
pause