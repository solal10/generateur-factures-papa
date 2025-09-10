#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import subprocess
import os

class InvoiceFillerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Générateur de Factures - Global Solutions")
        self.root.geometry("900x1000")
        
        # Create main frame with scrollbar
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Dictionary to store all field variables
        self.fields = {}
        
        # Title
        title_label = ttk.Label(scrollable_frame, text="Global Solutions - Générateur de Factures", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Create field groups
        self.create_header_fields(scrollable_frame)
        self.create_client_fields(scrollable_frame)
        self.create_project_fields(scrollable_frame)
        self.create_invoice_items(scrollable_frame)
        self.create_totals_fields(scrollable_frame)
        
        # Buttons frame
        buttons_frame = ttk.Frame(scrollable_frame)
        buttons_frame.pack(pady=20, fill=tk.X)
        
        # Generate PDF button
        generate_btn = ttk.Button(buttons_frame, text="Générer la Facture PDF", 
                                 command=self.generate_pdf)
        generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear all button
        clear_btn = ttk.Button(buttons_frame, text="Effacer Tout", 
                              command=self.clear_all_fields)
        clear_btn.pack(side=tk.LEFT)
        
        # Auto-calculate button
        calc_btn = ttk.Button(buttons_frame, text="Calculer Totaux", 
                             command=self.auto_calculate_totals)
        calc_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Store canvas reference for scrolling
        self.canvas = canvas
        
        # Optimized scrolling for Mac with smooth motion
        def _on_scroll(event):
            try:
                if hasattr(event, 'delta') and event.delta is not None:
                    delta = event.delta
                    
                    # Handle large negative values (two's complement issues)
                    if delta < -32768:
                        delta = delta + 65536
                    elif delta > 32768:
                        delta = delta - 65536
                    
                    # Use fractional scrolling for smoothness
                    scroll_amount = -delta * 0.3  # Smooth scaling factor
                    
                    # Clamp to reasonable values
                    scroll_amount = max(-30, min(30, scroll_amount))
                    
                    # Use yview_moveto for pixel-perfect scrolling
                    if scroll_amount != 0:
                        current = self.canvas.yview()[0]
                        canvas_height = self.canvas.winfo_height()
                        scroll_region = self.canvas.cget('scrollregion')
                        if scroll_region:
                            total_height = int(scroll_region.split()[3])
                            if total_height > canvas_height:
                                # Calculate new position
                                scroll_fraction = scroll_amount / total_height
                                new_pos = current + scroll_fraction
                                new_pos = max(0.0, min(1.0, new_pos))
                                self.canvas.yview_moveto(new_pos)
                    
                    return "break"  # Prevent default scrolling
            except Exception:
                pass
            
            return "break"
        
        # Bind scroll events globally to catch all scroll attempts
        root.bind_all("<MouseWheel>", _on_scroll)
        root.bind_all("<Button-4>", lambda e: _on_scroll(e))
        root.bind_all("<Button-5>", lambda e: _on_scroll(e))
        
        # Bind TouchpadScroll for Mac trackpads
        try:
            root.bind_all("<TouchpadScroll>", _on_scroll)
        except:
            pass
        
        # Enable keyboard scrolling (only when not in entry fields)
        def _on_key(event):
            # Don't scroll if focus is on an Entry widget
            focused_widget = self.root.focus_get()
            if isinstance(focused_widget, ttk.Entry):
                return
                
            if event.keysym in ['Up', 'k']:
                self.canvas.yview_scroll(-3, "units")
                return "break"
            elif event.keysym in ['Down', 'j']:
                self.canvas.yview_scroll(3, "units")
                return "break"
            elif event.keysym in ['Page_Up']:
                self.canvas.yview_scroll(-10, "units")
                return "break"
            elif event.keysym in ['Page_Down']:
                self.canvas.yview_scroll(10, "units")
                return "break"
            # Remove space from scroll triggers to allow typing in fields
        
        root.bind("<KeyPress>", _on_key)
        
    def create_field_group(self, parent, title, fields_config):
        """Create a group of fields with a title"""
        group_frame = ttk.LabelFrame(parent, text=title, padding=10)
        group_frame.pack(fill=tk.X, pady=(0, 15))
        
        for field_name, label_text, default_value, width in fields_config:
            row_frame = ttk.Frame(group_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            label = ttk.Label(row_frame, text=label_text + ":", width=25, anchor="w")
            label.pack(side=tk.LEFT, padx=(0, 10))
            
            var = tk.StringVar(value=default_value)
            
            # Special styling for header fields (invoice number and date)
            if field_name in ["numero_de_facture", "date"]:
                entry = tk.Entry(row_frame, textvariable=var, width=width, 
                               bg="white", fg="black", insertbackground="black")
            else:
                entry = ttk.Entry(row_frame, textvariable=var, width=width)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            self.fields[field_name] = var
    
    def create_header_fields(self, parent):
        """Create header fields"""
        fields_config = [
            ("numero_de_facture", "Numéro de facture", "", 40),
            ("date", "Date", datetime.now().strftime("%d/%m/%Y"), 40),
        ]
        self.create_field_group(parent, "En-tête de facture", fields_config)
    
    def create_client_fields(self, parent):
        """Create client information fields"""
        fields_config = [
            ("nom", "Nom", "", 40),
            ("adresse", "Adresse", "", 40),
            ("ville", "Ville", "", 40),
            ("num_rc", "Numéro RC", "", 40),
            ("tva", "TVA", "", 40),
        ]
        self.create_field_group(parent, "Informations Client", fields_config)
    
    def create_project_fields(self, parent):
        """Create project fields"""
        fields_config = [
            ("document", "Document", "", 40),
            ("lieu_d_intervention", "Lieu d'intervention", "", 40),
            ("debut_du_chantier", "Début du chantier", "", 40),
            ("fin_du_chantier", "Fin du chantier", "", 40),
        ]
        self.create_field_group(parent, "Informations Projet", fields_config)
    
    def create_invoice_items(self, parent):
        """Create invoice line items"""
        items_frame = ttk.LabelFrame(parent, text="Articles de la facture", padding=10)
        items_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Create a grid-based layout for better alignment
        # Headers row
        headers_frame = ttk.Frame(items_frame)
        headers_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Use grid for precise alignment with padding to shift right
        ttk.Label(headers_frame, text="Libellé", font=("Arial", 9, "bold")).grid(row=0, column=0, padx=(2, 2), sticky="w")
        ttk.Label(headers_frame, text="Qté", font=("Arial", 9, "bold")).grid(row=0, column=1, padx=(8, 2), sticky="w")
        ttk.Label(headers_frame, text="Prix Unit.", font=("Arial", 9, "bold")).grid(row=0, column=2, padx=(8, 2), sticky="w")
        ttk.Label(headers_frame, text="Total", font=("Arial", 9, "bold")).grid(row=0, column=3, padx=(8, 2), sticky="w")
        
        # Configure column widths to match entry fields
        headers_frame.grid_columnconfigure(0, minsize=265)  # Libellé column (increased)
        headers_frame.grid_columnconfigure(1, minsize=80)   # Qté column  
        headers_frame.grid_columnconfigure(2, minsize=95)   # Prix Unit. column
        headers_frame.grid_columnconfigure(3, minsize=95)   # Total column
        
        # Create 4 rows for invoice items
        for i in range(1, 5):
            row_frame = ttk.Frame(items_frame)
            row_frame.pack(fill=tk.X, pady=1)
            
            # Use grid for entries to match header alignment
            # Libellé - with text wrapping/truncation
            libelle_var = tk.StringVar()
            libelle_entry = ttk.Entry(row_frame, textvariable=libelle_var, width=35)
            libelle_entry.grid(row=0, column=0, padx=(0, 2), sticky="w")  # Use 'w' instead of 'ew'
            self.fields[f"libelle_{i}"] = libelle_var
            
            # Quantité
            quantite_var = tk.StringVar()
            quantite_entry = ttk.Entry(row_frame, textvariable=quantite_var, width=10)
            quantite_entry.grid(row=0, column=1, padx=(6, 2), sticky="ew")
            self.fields[f"quantite_{i}"] = quantite_var
            
            # Prix unitaire
            prix_var = tk.StringVar()
            prix_entry = ttk.Entry(row_frame, textvariable=prix_var, width=12)
            prix_entry.grid(row=0, column=2, padx=(6, 2), sticky="ew")
            self.fields[f"prix_unitaire_{i}"] = prix_var
            
            # Total (auto-calculated)
            total_var = tk.StringVar()
            total_entry = ttk.Entry(row_frame, textvariable=total_var, width=12)
            total_entry.grid(row=0, column=3, padx=(6, 2), sticky="ew")
            self.fields[f"total_net_{i}"] = total_var
            
            # Configure grid columns with proper sizing
            row_frame.grid_columnconfigure(0, minsize=265, weight=0)  # Fixed width for libelle
            row_frame.grid_columnconfigure(1, minsize=80, weight=0)
            row_frame.grid_columnconfigure(2, minsize=95, weight=0)
            row_frame.grid_columnconfigure(3, minsize=95, weight=1)   # Allow last column to expand
            
            # Bind calculation
            def make_calculator(i):
                def calculate_total(*args):
                    try:
                        qty = float(self.fields[f"quantite_{i}"].get() or 0)
                        price = float(self.fields[f"prix_unitaire_{i}"].get() or 0)
                        total = qty * price
                        if total > 0:
                            self.fields[f"total_net_{i}"].set(f"{total:.2f}")
                        else:
                            self.fields[f"total_net_{i}"].set("")
                        self.update_totals()
                    except ValueError:
                        self.fields[f"total_net_{i}"].set("")
                return calculate_total
            
            calculator = make_calculator(i)
            quantite_var.trace_add("write", calculator)
            prix_var.trace_add("write", calculator)
    
    def create_totals_fields(self, parent):
        """Create totals and tax fields aligned with Total column"""
        totals_frame = ttk.LabelFrame(parent, text="Totaux et Taxes", padding=10)
        totals_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Create a frame to align with the table's Total column
        container_frame = ttk.Frame(totals_frame)
        container_frame.pack(fill=tk.X)
        
        # Add spacer to align with Total column (same as table layout)
        spacer_frame = ttk.Frame(container_frame)
        spacer_frame.pack(side=tk.LEFT)
        spacer_frame.configure(width=535)  # Width to align with Total column (265+80+95+95 = 535)
        
        # Right-aligned fields frame for the totals
        fields_frame = ttk.Frame(container_frame)
        fields_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Totals fields 
        totals_config = [
            ("total_hors_taxe", "Total H.T."),
            ("tva_5_5_pourcent", "TVA 5.5%"),
            ("tva_10_pourcent", "TVA 10%"),
            ("tva_20_pourcent", "TVA 20%"),
            ("total_net_de_taxes", "Total Net de Taxes"),
            ("acompte_percu", "Acompte perçu"),
            ("reste_a_payer", "Reste à payer"),
            ("en_votre_aimable_reglement_de_la_somme_de", "En lettres"),
        ]
        
        for field_name, label_text in totals_config:
            row_frame = ttk.Frame(fields_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            label = ttk.Label(row_frame, text=label_text + ":", width=20, anchor="e")
            label.pack(side=tk.LEFT, padx=(0, 10))
            
            var = tk.StringVar()
            entry = ttk.Entry(row_frame, textvariable=var, width=15, justify="right")
            entry.pack(side=tk.RIGHT)
            
            self.fields[field_name] = var
    
    def update_totals(self):
        """Update total HT automatically"""
        try:
            total_ht = 0
            for i in range(1, 5):
                total_str = self.fields[f"total_net_{i}"].get()
                if total_str:
                    total_ht += float(total_str)
            
            if total_ht > 0:
                self.fields["total_hors_taxe"].set(f"{total_ht:.2f}")
            else:
                self.fields["total_hors_taxe"].set("")
                
        except ValueError:
            pass
    
    def auto_calculate_totals(self):
        """Auto-calculate all totals and taxes"""
        try:
            # Calculate total HT
            total_ht = 0
            for i in range(1, 5):
                total_str = self.fields[f"total_net_{i}"].get()
                if total_str:
                    total_ht += float(total_str)
            
            self.fields["total_hors_taxe"].set(f"{total_ht:.2f}")
            
            # Calculate taxes (you can modify these rates as needed)
            tva_5_5 = float(self.fields["tva_5_5_pourcent"].get() or 0)
            tva_10 = float(self.fields["tva_10_pourcent"].get() or 0)
            tva_20 = float(self.fields["tva_20_pourcent"].get() or 0)
            
            total_ttc = total_ht + tva_5_5 + tva_10 + tva_20
            self.fields["total_net_de_taxes"].set(f"{total_ttc:.2f}")
            
            # Calculate remaining amount
            acompte = float(self.fields["acompte_percu"].get() or 0)
            reste = total_ttc - acompte
            self.fields["reste_a_payer"].set(f"{reste:.2f}")
            
        except ValueError as e:
            messagebox.showwarning("Erreur de calcul", "Vérifiez que tous les montants sont des nombres valides.")
    
    def clear_all_fields(self):
        """Clear all form fields"""
        if messagebox.askyesno("Confirmer", "Êtes-vous sûr de vouloir effacer tous les champs ?"):
            for field_name, var in self.fields.items():
                if field_name != "date":  # Keep current date
                    var.set("")
    
    def generate_pdf(self):
        """Generate the PDF invoice"""
        try:
            # Check if required fields are filled
            if not self.fields["numero_de_facture"].get().strip():
                messagebox.showwarning("Champ manquant", "Le numéro de facture est obligatoire.")
                return
            
            # Generate the filled form Python script
            script_content = self.create_filled_form_script()
            
            # Write temporary script
            with open("temp_filled_form.py", "w", encoding="utf-8") as f:
                f.write(script_content)
            
            # Execute the script
            result = subprocess.run(["python", "temp_filled_form.py"], 
                                  cwd=".", capture_output=True, text=True)
            
            if result.returncode == 0:
                # Clean up temp file
                os.remove("temp_filled_form.py")
                # Get the filename that was generated
                invoice_number = self.fields["numero_de_facture"].get().strip()
                if invoice_number:
                    output_filename = f"FACTURE_{invoice_number}.pdf"
                else:
                    output_filename = "FACTURE_SANS_NUMERO.pdf"
                
                messagebox.showinfo("Succès", 
                                  f"La facture PDF a été générée avec succès!\n\nFichier: {output_filename}")
            else:
                messagebox.showerror("Erreur", 
                                   f"Erreur lors de la génération du PDF:\n{result.stderr}")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite:\n{str(e)}")
    
    def create_filled_form_script(self):
        """Create a script that overlays text on the existing acroform PDF"""
        script_lines = []
        script_lines.append("# Generated filled form script")
        script_lines.append("from reportlab.pdfgen import canvas")
        script_lines.append("from reportlab.lib.pagesizes import A4")
        script_lines.append("from pdfrw import PdfReader, PdfWriter, PageMerge")
        script_lines.append("")
        # Get invoice number for filename
        invoice_number = self.fields["numero_de_facture"].get().strip()
        if invoice_number:
            output_filename = f"FACTURE_{invoice_number}.pdf"
        else:
            output_filename = "FACTURE_SANS_NUMERO.pdf"
        
        script_lines.append('bg_path = "MODELE FACTURE GLOBAL SOLUTIONS A REMPLIR.pdf"')
        script_lines.append('overlay_path = "_text_overlay.pdf"')
        script_lines.append(f'out_path = "{output_filename}"')
        script_lines.append("")
        script_lines.append("# Read background PDF to get dimensions")
        script_lines.append("bg_pdf = PdfReader(bg_path)")
        script_lines.append("page = bg_pdf.pages[0]")
        script_lines.append("llx, lly, urx, ury = [float(x) for x in page.MediaBox]")
        script_lines.append("page_width = urx - llx")
        script_lines.append("page_height = ury - lly")
        script_lines.append("")
        script_lines.append("# Create canvas for text overlay")
        script_lines.append("c = canvas.Canvas(overlay_path, pagesize=(page_width, page_height))")
        script_lines.append("c.setFont('Helvetica', 9)")
        script_lines.append("")
        
        # Generate text placement for each filled field
        for field_name, var in self.fields.items():
            value = var.get().strip()
            if value:
                escaped_value = value.replace('"', '\\"').replace('\\', '\\\\')
                # Use the same positioning as acroform.py
                x, y = self.get_field_position(field_name)
                if x is not None and y is not None:
                    script_lines.append(f'c.drawString({x}, page_height - {y}, "{escaped_value}")')
        
        script_lines.append("")
        script_lines.append("c.save()")
        script_lines.append("")
        script_lines.append("# Merge text overlay with the acroform PDF")
        script_lines.append("bg_pdf = PdfReader(bg_path)")
        script_lines.append("overlay_pdf = PdfReader(overlay_path)")
        script_lines.append("")
        script_lines.append("page_bg = bg_pdf.pages[0]")
        script_lines.append("page_overlay = overlay_pdf.pages[0]")
        script_lines.append("")
        script_lines.append("merger = PageMerge(page_bg)")
        script_lines.append("merger.add(page_overlay).render()")
        script_lines.append("")
        script_lines.append("PdfWriter(out_path, trailer=bg_pdf).write()")
        script_lines.append("print('PDF generated successfully!')")
        
        return "\n".join(script_lines)
    
    def get_field_position(self, field_name):
        """Get the position for a field based on acroform.py positioning"""
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
        
        # Add line items positions - fill from top to bottom
        for i in range(1, 5):
            # Use (i-1) to fill from top: line 1 at top, line 4 at bottom
            y_pos = 352 + (i-1) * 25
            positions[f"libelle_{i}"] = (60, y_pos)
            positions[f"quantite_{i}"] = (290, y_pos) 
            positions[f"prix_unitaire_{i}"] = (360, y_pos)
            positions[f"total_net_{i}"] = (465, y_pos)
        
        return positions.get(field_name, (None, None))

def main():
    import os
    
    # Bypass macOS version check for older systems
    os.environ['SYSTEM_VERSION_COMPAT'] = '1'
    
    root = tk.Tk()
    
    # Ensure the window appears properly when launched from app bundle
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(lambda: root.attributes('-topmost', False))
    root.focus_force()
    
    app = InvoiceFillerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()