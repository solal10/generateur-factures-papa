#!/usr/bin/env python3
"""
Script simple de build et déploiement
"""
import shutil
import os
import zipfile
import subprocess

def sync_versions():
    """Synchronise toutes les versions"""
    print("ÉTAPE 1: Synchronisation des versions...")
    
    source = "pdf_filler.py"
    destinations = [
        "Generateur_Portable/pdf_filler.py",
        "Generateur_Factures_Papa/factures.py"
    ]
    
    if not os.path.exists(source):
        print(f"Erreur: {source} introuvable!")
        return False
    
    for dest in destinations:
        if os.path.exists(os.path.dirname(dest)):
            try:
                shutil.copy2(source, dest)
                print(f"OK: {dest}")
            except Exception as e:
                print(f"Erreur: {dest} - {e}")
                return False
    
    return True

def create_zip():
    """Crée le ZIP portable"""
    print("ÉTAPE 2: Création du ZIP...")
    
    portable_dir = "Generateur_Portable"
    zip_name = "Generateur_Factures_Portable.zip"
    
    if os.path.exists(zip_name):
        os.remove(zip_name)
    
    try:
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(portable_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, os.path.dirname(portable_dir))
                    zipf.write(file_path, arc_name)
        
        print(f"OK: {zip_name} créé")
        return True
    except Exception as e:
        print(f"Erreur ZIP: {e}")
        return False

def git_commit():
    """Commit et push"""
    print("ÉTAPE 3: Git commit...")
    
    try:
        # Check status
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            subprocess.run(['git', 'add', '.'], check=True)
            
            commit_msg = """Update générateur de factures - fixes UI

- Fix espace dans les champs ne fait plus scroller
- Champs numéro facture et date en blanc
- Tableau se remplit du haut vers le bas
- Fix débordement texte libellé
- Script de build automatique

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"""
            
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
            print("OK: Git mis à jour")
        else:
            print("OK: Rien à committer")
            
        return True
    except Exception as e:
        print(f"Erreur Git: {e}")
        return False

def main():
    print("BUILD GÉNÉRATEUR DE FACTURES")
    print("=" * 40)
    
    steps = [sync_versions, create_zip, git_commit]
    
    for step in steps:
        if not step():
            print("\nÉCHEC!")
            return False
    
    print("\n" + "=" * 40)
    print("SUCCÈS!")
    print("- Versions synchronisées")
    print("- ZIP mis à jour") 
    print("- GitHub mis à jour")
    print("\nURL: https://github.com/solal10/generateur-factures-papa")

if __name__ == "__main__":
    main()