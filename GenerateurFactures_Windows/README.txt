=== GÉNÉRATEUR DE FACTURES POUR WINDOWS ===

MÉTHODE 1 - PLUS SIMPLE (Recommandé)
=====================================
1. Double-cliquez sur LANCEUR_FACTURES.bat
2. Si Python n'est pas installé, suivez les instructions
3. Le programme s'occupera du reste automatiquement

MÉTHODE 2 - SI LA MÉTHODE 1 NE MARCHE PAS
==========================================
1. Installez Python depuis https://www.python.org
   IMPORTANT: Cochez "Add Python to PATH" lors de l'installation
   
2. Ouvrez l'invite de commandes (cmd)
   - Appuyez sur Windows+R
   - Tapez "cmd" et Entrée
   
3. Naviguez vers ce dossier:
   cd "chemin\vers\ce\dossier"
   
4. Installez les librairies:
   python -m pip install reportlab pdfrw
   
5. Lancez le programme:
   python GenerateurFactures_Portable.pyw

FICHIERS NÉCESSAIRES
====================
✅ LANCEUR_FACTURES.bat (pour lancer facilement)
✅ GenerateurFactures_Portable.pyw (le programme)
✅ MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf (template)

CES 3 FICHIERS DOIVENT RESTER ENSEMBLE

UTILISATION
===========
Le programme vous demande:
- Numéro de facture
- Date (Entrée = aujourd'hui)
- Client (nom, adresse, etc.)
- Projet (lieu, dates)
- Articles (jusqu'à 4)
- TVA et totaux

Les factures sont générées dans le même dossier:
FACTURE_[numéro].pdf

SUPPORT
=======
Si ça ne marche pas:
1. Vérifiez que Python est installé
2. Vérifiez que les 3 fichiers sont ensemble
3. Essayez de faire clic-droit sur LANCEUR_FACTURES.bat
   et choisir "Exécuter en tant qu'administrateur"

Bon travail!