# Générateur de Factures - Global Solutions

Un générateur de factures PDF simple et efficace pour Windows et macOS.

## 🎯 Objectif

Application créée pour générer facilement des factures PDF en utilisant un template pré-défini. Interface en ligne de commande simple, particulièrement adaptée aux utilisateurs non-techniques.

## 📦 Contenu

### Pour Windows (Recommandé)
- `GenerateurFactures_Windows.zip` - Package complet pour Windows
  - `LANCEUR_FACTURES.bat` - Lanceur automatique
  - `GenerateurFactures_Portable.pyw` - Application Python
  - Template PDF inclus

### Pour macOS
- `simple_invoice.py` - Version texte compatible macOS
- `Lancer_Factures_Simple.command` - Lanceur macOS

## 🚀 Installation

### Windows
1. Téléchargez `GenerateurFactures_Windows.zip`
2. Extrayez le contenu
3. Double-cliquez sur `LANCEUR_FACTURES.bat`
4. Si Python n'est pas installé, suivez les instructions à l'écran

### macOS
1. Téléchargez les fichiers
2. Double-cliquez sur `Lancer_Factures_Simple.command`
3. Ou exécutez : `python3 simple_invoice.py`

## 💼 Utilisation

L'application vous guide étape par étape :

1. **Informations de facture** : Numéro, date
2. **Client** : Nom, adresse, ville, RC, TVA
3. **Projet** : Document, lieu, dates de chantier
4. **Articles** : Jusqu'à 4 articles avec calcul automatique
5. **Totaux** : TVA, acompte, reste à payer

Les factures sont générées au format : `FACTURE_[numéro].pdf`

## 🛠️ Prérequis

- **Windows** : Python 3.x (installé automatiquement si nécessaire)
- **macOS** : Python 3.x avec pip
- **Librairies Python** : reportlab, pdfrw (installées automatiquement)

## 📝 Fonctionnalités

- ✅ Calculs automatiques des totaux
- ✅ Support TVA multiple (5.5%, 10%, 20%)
- ✅ Gestion des acomptes
- ✅ Interface entièrement en français
- ✅ Génération PDF professionnelle
- ✅ Utilise un template PDF existant

## 🔧 Développement

### Structure des fichiers

```
papa pdf/
├── GenerateurFactures_Windows.zip   # Package Windows
├── simple_invoice.py                 # Version macOS/Linux
├── simple_invoice_windows.py         # Version Windows
├── GenerateurFactures_Portable.pyw  # Version portable
├── MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf  # Template
└── Lanceurs (.bat, .command)        # Scripts de lancement
```

### Créer un exécutable Windows

Sur une machine Windows :
```bash
pip install pyinstaller
pyinstaller --onefile GenerateurFactures_Portable.pyw
```

## 📄 License

Projet privé - Usage familial

## 👨‍💻 Auteur

Créé pour faciliter la gestion des factures de Papa.

## 🆘 Support

En cas de problème :
1. Vérifiez que tous les fichiers sont dans le même dossier
2. Assurez-vous que Python est installé
3. Vérifiez que le template PDF est présent

---

*Application développée avec ❤️ pour simplifier la vie administrative*