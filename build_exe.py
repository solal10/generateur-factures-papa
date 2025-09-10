#!/usr/bin/env python3
"""
Build script to create Windows .exe using PyInstaller
"""

import os
import sys
import subprocess

def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        import PyInstaller
        print("✅ PyInstaller déjà installé")
        return True
    except ImportError:
        print("📦 Installation de PyInstaller...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("✅ PyInstaller installé avec succès")
            return True
        except subprocess.CalledProcessError:
            print("❌ Échec de l'installation de PyInstaller")
            return False

def build_exe():
    """Build the .exe file"""
    if not install_pyinstaller():
        return False
    
    print("🔨 Construction de l'exécutable...")
    
    # PyInstaller command - fix syntax for cross-platform
    template_data = 'MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf' + os.pathsep + '.'
    
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',                    # Single executable file
        '--console',                    # Keep console window
        '--name', 'GenerateurFactures', # Name of the executable
        '--add-data', template_data,    # Include template
        '--hidden-import', 'reportlab.pdfgen.canvas',
        '--hidden-import', 'reportlab.lib.pagesizes', 
        '--hidden-import', 'pdfrw',
        'simple_invoice_windows.py'
    ]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Exécutable créé avec succès!")
            print("📁 Fichier: dist/GenerateurFactures.exe")
            return True
        else:
            print("❌ Erreur lors de la construction:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def create_spec_file():
    """Create a detailed .spec file for more control"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['simple_invoice_windows.py'],
    pathex=[],
    binaries=[],
    datas=[('MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf', '.')],
    hiddenimports=[
        'reportlab.pdfgen.canvas',
        'reportlab.lib.pagesizes',
        'reportlab.lib.units',
        'reportlab.platypus',
        'pdfrw',
        'pdfrw.pdfwriter',
        'pdfrw.pdfreader',
        'pdfrw.pagemerge',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GenerateurFactures',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open('generateur_factures.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Fichier .spec créé: generateur_factures.spec")

if __name__ == "__main__":
    print("=== CONSTRUCTION DE L'EXÉCUTABLE WINDOWS ===")
    print()
    
    # Check if template exists
    if not os.path.exists("MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf"):
        print("❌ Template PDF manquant!")
        print("Assurez-vous que 'MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf' est présent")
        sys.exit(1)
    
    # Check if source exists
    if not os.path.exists("simple_invoice_windows.py"):
        print("❌ Fichier source manquant!")
        print("Assurez-vous que 'simple_invoice_windows.py' est présent")
        sys.exit(1)
    
    # Create spec file
    create_spec_file()
    
    # Build executable
    success = build_exe()
    
    if success:
        print()
        print("🎉 SUCCÈS!")
        print("📁 L'exécutable se trouve dans: dist/GenerateurFactures.exe")
        print("📦 Copiez ce fichier avec le template PDF sur l'ordinateur Windows de votre père")
    else:
        print("❌ La construction a échoué")
        sys.exit(1)