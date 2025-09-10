#!/usr/bin/env python3
"""
Script pour synchroniser les versions du générateur de factures
"""
import shutil
import os

def sync_versions():
    """Synchronise la version principale avec la version portable"""
    source = "pdf_filler.py"
    destinations = [
        "Generateur_Portable/pdf_filler.py",
        "Generateur_Factures_Papa/factures.py"
    ]
    
    if not os.path.exists(source):
        print("❌ Fichier source pdf_filler.py introuvable!")
        return False
    
    print(f"📋 Synchronisation depuis {source}...")
    
    for dest in destinations:
        if os.path.exists(dest):
            shutil.copy2(source, dest)
            print(f"✅ Copié vers {dest}")
        else:
            print(f"⚠️  Destination introuvable: {dest}")
    
    print("\n🔄 Synchronisation terminée!")
    print("N'oublie pas de:")
    print("1. Tester les changements")
    print("2. Créer un nouveau ZIP portable si nécessaire")
    print("3. Commit + push vers GitHub")
    
    return True

if __name__ == "__main__":
    sync_versions()