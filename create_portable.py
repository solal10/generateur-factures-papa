"""
Create a portable Python app that doesn't need installation
"""
import shutil
import os
import zipfile

def create_portable_app():
    # Create portable directory
    portable_dir = "Generateur_Portable"
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    
    os.makedirs(portable_dir)
    
    # Copy main script
    shutil.copy("pdf_filler.py", os.path.join(portable_dir, "pdf_filler.py"))
    
    # Copy PDF template
    shutil.copy("MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf", portable_dir)
    
    # Copy requirements
    shutil.copy("requirements.txt", portable_dir)
    
    # Create batch file for Windows
    batch_content = '''@echo off
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
'''
    
    with open(os.path.join(portable_dir, "Lancer_Factures.bat"), 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    # Create installation instructions
    instructions = '''GÉNÉRATEUR DE FACTURES - INSTALLATION FACILE
=====================================================

ÉTAPE 1: Installer Python (si pas déjà fait)
1. Va sur: https://www.python.org/downloads/
2. Télécharge la dernière version de Python
3. IMPORTANT: Coche "Add Python to PATH" pendant l'installation

ÉTAPE 2: Lancer le programme
1. Double-clique sur "Lancer_Factures.bat"
2. Le script installera automatiquement les dépendances
3. Le programme s'ouvrira

C'EST TOUT!

Le fichier .bat vérifie Python, installe les dépendances si nécessaire,
et lance le programme automatiquement.

PROBLÈME?
- Si Python n'est pas reconnu, redémarre ton ordinateur après installation
- Ou appelle Solal pour aide :)

Générateur créé avec ❤️ pour Papa
'''
    
    with open(os.path.join(portable_dir, "LIRE_MOI.txt"), 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    # Create zip file
    with zipfile.ZipFile("Generateur_Factures_Portable.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(portable_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, os.path.dirname(portable_dir))
                zipf.write(file_path, arc_name)
    
    print(f"Application portable créée dans: {portable_dir}")
    print(f"Archive ZIP créée: Generateur_Factures_Portable.zip")
    print("\nTon père peut maintenant:")
    print("1. Extraire le ZIP")
    print("2. Double-cliquer sur 'Lancer_Factures.bat'")
    print("3. Profiter!")

if __name__ == "__main__":
    create_portable_app()