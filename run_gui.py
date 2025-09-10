#!/usr/bin/env python3
"""
GUI wrapper to ensure the PDF filler application launches properly from app bundles.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Paths to required files
    pdf_filler_path = os.path.join(script_dir, "pdf_filler.py")
    venv_python = os.path.join(script_dir, "venv", "bin", "python")
    
    # Check if files exist
    if not os.path.exists(pdf_filler_path):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erreur", f"pdf_filler.py non trouvé dans:\n{script_dir}")
        return
        
    if not os.path.exists(venv_python):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erreur", f"Environnement virtuel non trouvé dans:\n{script_dir}")
        return
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Run the PDF filler with the virtual environment Python
    try:
        subprocess.run([venv_python, pdf_filler_path], check=True)
    except subprocess.CalledProcessError as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erreur", f"Erreur lors du lancement:\n{str(e)}")
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erreur", f"Erreur inattendue:\n{str(e)}")

if __name__ == "__main__":
    main()