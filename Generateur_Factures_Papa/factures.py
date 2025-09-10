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
            
            # Add formatting for prix unitaire field
            def make_prix_formatter(field_var):
                def format_on_focus_out(event):
                    try:
                        value = field_var.get().strip()
                        # Remove existing euro symbol if present
                        value = value.replace(' €', '').replace('€', '').strip()
                        if value and value != "0":
                            formatted_value = f"{float(value):.2f} €"
                            field_var.set(formatted_value)
                    except ValueError:
                        pass
                return format_on_focus_out
            
            prix_formatter = make_prix_formatter(prix_var)
            prix_entry.bind("<FocusOut>", prix_formatter)
            
            # Total (auto-calculated)
            total_var = tk.StringVar()
            total_entry = ttk.Entry(row_frame, textvariable=total_var, width=12)
            total_entry.grid(row=0, column=3, padx=(6, 2), sticky="ew")
            self.fields[f"total_net_{i}"] = total_var
            
            # Add formatting for total field
            def make_total_formatter(field_var):
                def format_on_focus_out(event):
                    try:
                        value = field_var.get().strip()
                        # Remove existing euro symbol if present
                        value = value.replace(' €', '').replace('€', '').strip()
                        if value and value != "0":
                            formatted_value = f"{float(value):.2f} €"
                            field_var.set(formatted_value)
                    except ValueError:
                        pass
                return format_on_focus_out
            
            total_formatter = make_total_formatter(total_var)
            total_entry.bind("<FocusOut>", total_formatter)
            
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
                        # Strip euro symbols before calculating
                        price_str = self.fields[f"prix_unitaire_{i}"].get() or "0"
                        price_str = price_str.replace(' €', '').replace('€', '').strip()
                        price = float(price_str or 0)
                        total = qty * price
                        if total > 0:
                            self.fields[f"total_net_{i}"].set(f"{total:.2f} €")
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
            ("en_votre_aimable_reglement_de_la_somme_de", "Confirmation somme"),
        ]
        
        for field_name, label_text in totals_config:
            row_frame = ttk.Frame(fields_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            label = ttk.Label(row_frame, text=label_text + ":", width=20, anchor="e")
            label.pack(side=tk.LEFT, padx=(0, 10))
            
            var = tk.StringVar()
            entry = ttk.Entry(row_frame, textvariable=var, width=15, justify="right")
            entry.pack(side=tk.RIGHT)
            
            # Add formatting for all monetary fields
            if field_name in ["acompte_percu", "tva_5_5_pourcent", "tva_10_pourcent", "tva_20_pourcent", 
                             "total_hors_taxe", "total_net_de_taxes", "reste_a_payer"]:
                def make_formatter(field_var):
                    def format_on_focus_out(event):
                        try:
                            value = field_var.get().strip()
                            # Remove existing euro symbol if present
                            value = value.replace(' €', '').replace('€', '').strip()
                            if value and value != "0":
                                formatted_value = f"{float(value):.2f} €"
                                field_var.set(formatted_value)
                        except ValueError:
                            pass
                    return format_on_focus_out
                
                formatter = make_formatter(var)
                entry.bind("<FocusOut>", formatter)
            
            # Special formatting for confirmation somme field
            if field_name == "en_votre_aimable_reglement_de_la_somme_de":
                def make_confirmation_formatter(field_var):
                    def format_on_focus_out(event):
                        try:
                            value = field_var.get().strip()
                            # Remove existing formatting if present
                            value = value.replace(',00 €', '').replace(' €', '').replace('€', '').replace(',00', '').strip()
                            if value and value != "0":
                                formatted_value = f"{float(value):.0f},00 €"
                                field_var.set(formatted_value)
                        except ValueError:
                            pass
                    return format_on_focus_out
                
                confirmation_formatter = make_confirmation_formatter(var)
                entry.bind("<FocusOut>", confirmation_formatter)
            
            self.fields[field_name] = var
    
    def update_totals(self):
        """Update total HT automatically"""
        try:
            total_ht = 0
            for i in range(1, 5):
                total_str = self.fields[f"total_net_{i}"].get()
                if total_str:
                    # Strip euro symbols before calculating
                    clean_total = total_str.replace(' €', '').replace('€', '').strip()
                    total_ht += float(clean_total)
            
            if total_ht > 0:
                self.fields["total_hors_taxe"].set(f"{total_ht:.2f} €")
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
                    # Strip euro symbols before calculating
                    clean_total = total_str.replace(' €', '').replace('€', '').strip()
                    total_ht += float(clean_total)
            
            self.fields["total_hors_taxe"].set(f"{total_ht:.2f} €")
            
            # Calculate taxes (you can modify these rates as needed)
            def get_clean_value(field_name):
                value = self.fields[field_name].get() or "0"
                return float(value.replace(' €', '').replace('€', '').strip() or 0)
            
            tva_5_5 = get_clean_value("tva_5_5_pourcent")
            tva_10 = get_clean_value("tva_10_pourcent")
            tva_20 = get_clean_value("tva_20_pourcent")
            
            total_ttc = total_ht + tva_5_5 + tva_10 + tva_20
            self.fields["total_net_de_taxes"].set(f"{total_ttc:.2f} €")
            
            # Calculate remaining amount
            acompte = get_clean_value("acompte_percu")
            reste = total_ttc - acompte
            self.fields["reste_a_payer"].set(f"{reste:.2f} €")
            
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
        script_lines.append("")
        script_lines.append("# Register Roboto font (using Helvetica as fallback)")
        script_lines.append("try:")
        script_lines.append("    from reportlab.pdfbase import pdfutils")
        script_lines.append("    from reportlab.pdfbase.ttfonts import TTFont")
        script_lines.append("    # Try to use Roboto, fallback to Helvetica")
        script_lines.append("    font_name = 'Helvetica'  # Default fallback")
        script_lines.append("except:")
        script_lines.append("    font_name = 'Helvetica'")
        script_lines.append("")
        
        # Generate text placement for each filled field
        for field_name, var in self.fields.items():
            value = var.get().strip()
            if value:
                # Clean the value for PDF output (remove euro symbols for processing)
                clean_value = value.replace(' €', '').replace('€', '').strip()
                escaped_value = clean_value.replace('"', '\\"').replace('\\', '\\\\')
                x, y = self.get_field_position(field_name)
                if x is not None and y is not None:
                    # Determine font size based on field position
                    font_size = self.get_font_size_for_field(field_name)
                    script_lines.append(f'c.setFont(font_name, {font_size})')
                    
                    # Set text color for specific fields
                    if field_name in ["numero_de_facture", "date"]:
                        script_lines.append('c.setFillColorRGB(1, 1, 1)  # White text')
                    else:
                        script_lines.append('c.setFillColorRGB(0, 0, 0)  # Black text')
                    
                    # Handle text wrapping for libelle fields
                    if field_name.startswith("libelle_") and len(value) > 35:
                        # Split long libelle text into multiple lines
                        script_lines.append(f'# Handle long libelle text for {field_name}')
                        script_lines.append(f'text = "{escaped_value}"')
                        script_lines.append(f'max_width = 225  # Maximum width for libelle field')
                        script_lines.append(f'words = text.split(" ")')
                        script_lines.append(f'lines = []')
                        script_lines.append(f'current_line = ""')
                        script_lines.append(f'for word in words:')
                        script_lines.append(f'    test_line = current_line + (" " if current_line else "") + word')
                        script_lines.append(f'    if c.stringWidth(test_line, font_name, {font_size}) <= max_width:')
                        script_lines.append(f'        current_line = test_line')
                        script_lines.append(f'    else:')
                        script_lines.append(f'        if current_line:')
                        script_lines.append(f'            lines.append(current_line)')
                        script_lines.append(f'        current_line = word')
                        script_lines.append(f'if current_line:')
                        script_lines.append(f'    lines.append(current_line)')
                        script_lines.append(f'# Draw each line with 12pt spacing')
                        script_lines.append(f'for i, line in enumerate(lines):')
                        script_lines.append(f'    c.drawString({x}, page_height - {y} - (i * 12), line)')
                    else:
                        # Check if field is monetary and needs right alignment
                        is_monetary = (field_name.startswith(("prix_unitaire_", "total_net_")) or 
                                     field_name in ["total_hors_taxe", "tva_5_5_pourcent", "tva_10_pourcent", 
                                                   "tva_20_pourcent", "total_net_de_taxes", "acompte_percu", "reste_a_payer"])
                        
                        if is_monetary:
                            # Add euro symbol and right-align
                            script_lines.append(f'text_with_euro = "{escaped_value} €"')
                            script_lines.append(f'text_width = c.stringWidth(text_with_euro, font_name, {font_size})')
                            script_lines.append(f'c.drawRightString({x} + 80, page_height - {y}, text_with_euro)')
                        elif field_name == "en_votre_aimable_reglement_de_la_somme_de":
                            # Special formatting for confirmation field: bold, with ,00 and euro
                            script_lines.append(f'c.setFont(font_name + "-Bold", {font_size})')
                            script_lines.append(f'formatted_amount = "{escaped_value},00 €"')
                            script_lines.append(f'c.drawString({x}, page_height - {y}, formatted_amount)')
                            script_lines.append(f'c.setFont(font_name, {font_size})  # Reset to normal font')
                        else:
                            # Normal single line text
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
    
    def get_font_size_for_field(self, field_name):
        """Get font size based on field position in form"""
        # Fields before table (size 12): header and client info fields
        before_table_fields = [
            "numero_de_facture", "date", "nom", "adresse", "ville", 
            "num_rc", "tva", "document", "lieu_d_intervention", 
            "debut_du_chantier", "fin_du_chantier"
        ]
        
        # Table and after table fields (size 8): libelle, quantities, totals
        table_and_after_fields = [
            "libelle_", "quantite_", "prix_unitaire_", "total_net_",
            "total_hors_taxe", "tva_5_5_pourcent", "tva_10_pourcent", 
            "tva_20_pourcent", "total_net_de_taxes", "acompte_percu", 
            "reste_a_payer", "en_votre_aimable_reglement_de_la_somme_de"
        ]
        
        # Check if field is in table or after table (size 10)
        for pattern in table_and_after_fields:
            if field_name.startswith(pattern) or field_name == pattern:
                return 10
                
        # Check if field is before table (size 12)  
        if field_name in before_table_fields:
            return 12
            
        # Default fallback
        return 9
    
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
            "total_hors_taxe": (465, 447),
            "tva_5_5_pourcent": (465, 475),
            "tva_10_pourcent": (465, 504),
            "tva_20_pourcent": (465, 529),
            "total_net_de_taxes": (465, 552),
            "acompte_percu": (465, 572),
            "reste_a_payer": (465, 610),
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