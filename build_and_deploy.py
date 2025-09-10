#!/usr/bin/env python3
"""
Script automatique de build et déploiement du générateur de factures
"""
import shutil
import os
import zipfile
import subprocess
import sys
from datetime import datetime

def print_step(step, description):
    """Print a formatted step"""
    print(f"\n{'='*50}")
    print(f"ÉTAPE {step}: {description}")
    print(f"{'='*50}")

def sync_versions():
    """Synchronise toutes les versions"""
    print_step(1, "SYNCHRONISATION DES VERSIONS")
    
    source = "pdf_filler.py"
    destinations = [
        "Generateur_Portable/pdf_filler.py",
        "Generateur_Factures_Papa/factures.py"
    ]
    
    if not os.path.exists(source):
        print(f"Erreur: {source} introuvable!")
        return False
    
    print(f"Synchronisation depuis {source}...")
    
    success = True
    for dest in destinations:
        if os.path.exists(os.path.dirname(dest)):
            try:
                shutil.copy2(source, dest)
                print(f"Copié vers {dest}")
            except Exception as e:
                print(f"Erreur copie vers {dest}: {e}")
                success = False
        else:
            print(f"Dossier destination manquant: {os.path.dirname(dest)}")
            success = False
    
    return success

def create_portable_zip():
    """Crée le ZIP portable"""
    print_step(2, "CRÉATION DU ZIP PORTABLE")
    
    portable_dir = "Generateur_Portable"
    zip_name = "Generateur_Factures_Portable.zip"
    
    if not os.path.exists(portable_dir):
        print(f"❌ Erreur: Dossier {portable_dir} introuvable!")
        return False
    
    # Remove old zip
    if os.path.exists(zip_name):
        os.remove(zip_name)
        print(f"🗑️  Ancien ZIP supprimé")
    
    try:
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(portable_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, os.path.dirname(portable_dir))
                    zipf.write(file_path, arc_name)
                    print(f"📦 Ajouté: {arc_name}")
        
        size = os.path.getsize(zip_name)
        print(f"✅ ZIP créé: {zip_name} ({size:,} bytes)")
        return True
    
    except Exception as e:
        print(f"❌ Erreur création ZIP: {e}")
        return False

def run_tests():
    """Test basic functionality"""
    print_step(3, "TESTS BASIQUES")
    
    try:
        # Test import
        sys.path.insert(0, '.')
        import pdf_filler
        print("✅ Import du module principal: OK")
        
        # Test portable version
        if os.path.exists("Generateur_Portable/pdf_filler.py"):
            print("✅ Version portable: OK")
        else:
            print("❌ Version portable: MANQUANTE")
            return False
            
        return True
    
    except Exception as e:
        print(f"❌ Erreur tests: {e}")
        return False

def git_operations():
    """Opérations Git"""
    print_step(4, "MISE À JOUR GIT")
    
    try:
        # Check git status
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            print("📝 Changements détectés, commit en cours...")
            
            # Add changes
            subprocess.run(['git', 'add', '.'], check=True)
            print("✅ Fichiers ajoutés au staging")
            
            # Commit with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            commit_msg = f"""Update générateur de factures - {timestamp}

Corrections appliquées:
- Fix problème espace dans les champs (scroll)  
- Champs numéro facture et date en blanc
- Tableau se remplit du haut vers le bas
- Fix débordement texte libellé

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"""
            
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            print("✅ Commit créé")
            
            # Push to remote
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
            print("✅ Poussé vers GitHub")
            
            return True
        else:
            print("ℹ️  Aucun changement à committer")
            return True
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur Git: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue Git: {e}")
        return False

def main():
    """Build et déploiement automatique"""
    print("GÉNÉRATEUR DE FACTURES - BUILD AUTOMATIQUE")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    steps = [
        ("Synchronisation", sync_versions),
        ("Création ZIP", create_portable_zip),
        ("Tests", run_tests),
        ("Git", git_operations)
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\nERREUR à l'étape: {step_name}")
            print("BUILD ARRÊTÉ")
            return False
    
    print(f"\n{'='*50}")
    print("BUILD TERMINÉ AVEC SUCCÈS!")
    print(f"{'='*50}")
    print("\nRÉSUMÉ:")
    print("- Toutes les versions synchronisées")
    print("- ZIP portable mis à jour")  
    print("- Tests passés")
    print("- GitHub mis à jour")
    print("\nTon père peut maintenant télécharger la dernière version!")
    print("URL: https://github.com/solal10/generateur-factures-papa")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)