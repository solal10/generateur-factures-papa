#!/usr/bin/env python3
"""
Portable Invoice Generator for Windows
Works with embedded Python or installed Python
"""

import os
import sys
import subprocess
from datetime import datetime

# Ensure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def install_dependencies():
    """Try to install required dependencies"""
    try:
        import reportlab
        import pdfrw
        return True
    except ImportError:
        print("Installation des librairies PDF...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
                                 'reportlab', 'pdfrw', '--user', '--quiet'])
            print("✅ Librairies installées")
            return True
        except:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
                                     'reportlab', 'pdfrw', '--quiet'])
                return True
            except:
                return False

# Try to install dependencies
deps_ok = install_dependencies()

if deps_ok:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from pdfrw import PdfReader, PdfWriter, PageMerge

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if sys.platform == 'win32' else 'clear')

def get_input(prompt, default=""):
    """Get user input with optional default value"""
    try:
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            return user_input if user_input else default
        return input(f"{prompt}: ").strip()
    except (EOFError, KeyboardInterrupt):
        if default:
            return default
        return ""

def generate_pdf(invoice_data):
    """Generate PDF directly"""
    if not deps_ok:
        print("❌ Impossible de générer le PDF sans les librairies")
        return False
        
    bg_path = "MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf"
    overlay_path = "_text_overlay.pdf"
    invoice_number = invoice_data.get('numero_de_facture', 'SANS_NUMERO')
    out_path = f"FACTURE_{invoice_number}.pdf"
    
    try:
        # Read template
        bg_pdf = PdfReader(bg_path)
        page = bg_pdf.pages[0]
        llx, lly, urx, ury = [float(x) for x in page.MediaBox]
        page_width = urx - llx
        page_height = ury - lly

        # Create overlay
        c = canvas.Canvas(overlay_path, pagesize=(page_width, page_height))
        c.setFont('Helvetica', 9)

        # Position mappings
        positions = {
            "numero_de_facture": (130, 71.5),
            "date": (95, 96.5),
            "nom": (50, 214),
            "adresse": (50, 226),
            "ville": (50, 238),
            "num_rc": (50, 250),
            "tva": (50, 262),
            "document": (355, 203),
            "lieu_d_intervention": (397, 227),
            "debut_du_chantier": (393, 251),
            "fin_du_chantier": (378, 263),
            "total_hors_taxe": (470, 447),
            "tva_5_5_pourcent": (470, 475),
            "tva_10_pourcent": (470, 504),
            "tva_20_pourcent": (470, 529),
            "total_net_de_taxes": (470, 552),
            "acompte_percu": (470, 572),
            "reste_a_payer": (470, 610),
            "en_votre_aimable_reglement_de_la_somme_de": (295, 639),
        }

        # Add text fields
        for field, (x, y) in positions.items():
            value = invoice_data.get(field, '')
            if value:
                c.drawString(x, page_height - y, str(value))

        # Add invoice items
        for i, item in enumerate(invoice_data.get('items', []), 1):
            y_pos = 352 + (4-i) * 25
            if item.get('libelle'):
                c.drawString(60, page_height - y_pos, item['libelle'])
            if item.get('quantite'):
                c.drawString(290, page_height - y_pos, item['quantite'])
            if item.get('prix_unitaire'):
                c.drawString(360, page_height - y_pos, item['prix_unitaire'])
            if item.get('total'):
                c.drawString(465, page_height - y_pos, item['total'])

        c.save()

        # Merge with background
        bg_pdf = PdfReader(bg_path)
        overlay_pdf = PdfReader(overlay_path)
        
        page_bg = bg_pdf.pages[0]
        page_overlay = overlay_pdf.pages[0]
        
        merger = PageMerge(page_bg)
        merger.add(page_overlay).render()
        
        PdfWriter(out_path, trailer=bg_pdf).write()
        
        print(f"\n✅ PDF généré avec succès: {out_path}")
        
        # Cleanup
        if os.path.exists(overlay_path):
            os.remove(overlay_path)
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du PDF: {e}")
        return False

def collect_invoice_data():
    """Collect all invoice data from user"""
    clear_screen()
    print("=== GÉNÉRATEUR DE FACTURES - GLOBAL SOLUTIONS ===\n")
    
    invoice_data = {}
    
    print("📋 INFORMATIONS DE LA FACTURE")
    print("-" * 40)
    invoice_data['numero_de_facture'] = get_input("Numéro de facture")
    invoice_data['date'] = get_input("Date", datetime.now().strftime("%d/%m/%Y"))
    
    print("\n👤 INFORMATIONS CLIENT")
    print("-" * 40)
    invoice_data['nom'] = get_input("Nom")
    invoice_data['adresse'] = get_input("Adresse")
    invoice_data['ville'] = get_input("Ville")
    invoice_data['num_rc'] = get_input("Numéro RC")
    invoice_data['tva'] = get_input("TVA")
    
    print("\n🏗️ INFORMATIONS PROJET")
    print("-" * 40)
    invoice_data['document'] = get_input("Document")
    invoice_data['lieu_d_intervention'] = get_input("Lieu d'intervention")
    invoice_data['debut_du_chantier'] = get_input("Début du chantier")
    invoice_data['fin_du_chantier'] = get_input("Fin du chantier")
    
    print("\n📝 ARTICLES DE LA FACTURE")
    print("-" * 40)
    items = []
    for i in range(1, 5):
        print(f"\nArticle {i}:")
        libelle = get_input(f"  Libellé")
        if not libelle:
            break
            
        quantite = get_input(f"  Quantité", "1")
        prix_unitaire = get_input(f"  Prix unitaire")
        
        try:
            qty = float(quantite) if quantite else 0
            prix = float(prix_unitaire) if prix_unitaire else 0
            total = qty * prix
            
            items.append({
                'libelle': libelle,
                'quantite': quantite,
                'prix_unitaire': prix_unitaire,
                'total': f"{total:.2f}"
            })
            
            print(f"  → Total: {total:.2f} €")
            
        except ValueError:
            print("  ⚠️  Erreur dans les nombres, article ignoré")
    
    invoice_data['items'] = items
    
    print("\n💰 TOTAUX")
    print("-" * 40)
    total_ht = sum(float(item['total']) for item in items)
    print(f"Total H.T. calculé: {total_ht:.2f} €")
    
    invoice_data['total_hors_taxe'] = f"{total_ht:.2f}"
    invoice_data['tva_5_5_pourcent'] = get_input("TVA 5.5%", "0")
    invoice_data['tva_10_pourcent'] = get_input("TVA 10%", "0")
    invoice_data['tva_20_pourcent'] = get_input("TVA 20%", "0")
    
    try:
        tva_total = (float(invoice_data['tva_5_5_pourcent']) + 
                    float(invoice_data['tva_10_pourcent']) + 
                    float(invoice_data['tva_20_pourcent']))
        total_ttc = total_ht + tva_total
        invoice_data['total_net_de_taxes'] = f"{total_ttc:.2f}"
        print(f"Total T.T.C. calculé: {total_ttc:.2f} €")
    except:
        invoice_data['total_net_de_taxes'] = get_input("Total net de taxes")
    
    invoice_data['acompte_percu'] = get_input("Acompte perçu", "0")
    try:
        reste = float(invoice_data['total_net_de_taxes']) - float(invoice_data['acompte_percu'])
        invoice_data['reste_a_payer'] = f"{reste:.2f}"
        print(f"Reste à payer: {reste:.2f} €")
    except:
        invoice_data['reste_a_payer'] = get_input("Reste à payer")
    
    invoice_data['en_votre_aimable_reglement_de_la_somme_de'] = get_input("Montant en lettres")
    
    return invoice_data

def main():
    """Main program"""
    try:
        # Check for template
        if not os.path.exists("MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf"):
            print("❌ Erreur: Le fichier template PDF est introuvable.")
            print("Assurez-vous que 'MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf'")
            print("est dans le même dossier que ce programme.")
            input("\nAppuyez sur Entrée pour quitter...")
            return
        
        # Collect invoice data
        invoice_data = collect_invoice_data()
        
        # Show summary
        clear_screen()
        print("=== RÉSUMÉ DE LA FACTURE ===\n")
        print(f"Facture N°: {invoice_data.get('numero_de_facture', 'N/A')}")
        print(f"Client: {invoice_data.get('nom', 'N/A')}")
        print(f"Total H.T.: {invoice_data.get('total_hors_taxe', '0')} €")
        print(f"Total T.T.C.: {invoice_data.get('total_net_de_taxes', '0')} €")
        print(f"Reste à payer: {invoice_data.get('reste_a_payer', '0')} €")
        
        print("\n" + "="*50)
        confirm = get_input("Générer le PDF? (o/n)", "o").lower()
        
        if confirm in ['o', 'oui', 'y', 'yes', '']:
            generate_pdf(invoice_data)
        else:
            print("Génération annulée.")
            
    except KeyboardInterrupt:
        print("\n\nOpération annulée.")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nAppuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()