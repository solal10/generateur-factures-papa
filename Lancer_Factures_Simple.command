#!/bin/bash

# Change to the script directory
cd "$(dirname "$0")"

echo "=== GÉNÉRATEUR DE FACTURES - VERSION SIMPLE ==="
echo "Timestamp: $(date)"
echo ""

# Check if template exists
if [ ! -f "MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf" ]; then
    echo "❌ Erreur: Le fichier template 'MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf' est introuvable."
    echo "Veuillez le placer dans le même dossier que ce script."
    echo ""
    echo "Appuyez sur Entrée pour fermer..."
    read
    exit 1
fi

# Check Python
echo "=== VÉRIFICATION PYTHON ==="
echo "which python3: $(which python3)"
echo "python3 version: $(python3 --version 2>&1)"
echo ""

# Install PDF libraries if needed
echo "=== INSTALLATION DES LIBRAIRIES PDF ==="
echo "Installation de reportlab et pdfrw..."

python3 -m pip install --user reportlab pdfrw --break-system-packages --quiet 2>/dev/null || {
    python3 -m pip install --user reportlab pdfrw --quiet 2>/dev/null || {
        echo "⚠️  Installation des librairies échouée, tentative avec le script..."
    }
}

# Test if PDF libraries work
echo "Test des librairies PDF..."
if python3 -c "from reportlab.pdfgen import canvas; from pdfrw import PdfReader; print('✅ Librairies PDF OK')" 2>/dev/null; then
    echo "✅ Les librairies PDF sont prêtes"
else
    echo "❌ Problème avec les librairies PDF"
    echo "Le script va essayer de continuer..."
fi

echo ""
echo "=== LANCEMENT DU GÉNÉRATEUR DE FACTURES ==="
echo "Interface en mode texte (pas de fenêtre graphique)"
echo ""

# Run the simple invoice generator
python3 simple_invoice.py

echo ""
echo "=== FIN ==="
echo "Appuyez sur Entrée pour fermer..."
read