import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

# Add project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

from src.parser.whatsapp_parser import WhatsAppParser
from src.ui.consent_dialog import ConsentDialog
from src.ui.vt_settings import VirusTotalSettings

try:
    from src.security.virustotal_hash import check_file_with_virustotal
    VT_AVAILABLE = True
except:
    VT_AVAILABLE = False


def open_file():
    filepath = filedialog.askopenfilename(
        title="Select WhatsApp Chat Export",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return

    parser = WhatsAppParser()
    messages = parser.parse(filepath)
    parser.save_to_db(messages)

    messagebox.showinfo("Success", f"Imported {len(messages)} messages.")


def open_settings():
    root = tk.Toplevel()
    VirusTotalSettings(root)


def run_virustotal_scan():
    if not VT_AVAILABLE:
        messagebox.showerror("Error", "VirusTotal module missing.")
        return

    api_key = os.getenv("VT_API_KEY")
    if not api_key:
        messagebox.showwarning("Missing API Key", "Please configure VirusTotal settings first.")
        return

    filepath = filedialog.askopenfilename(
        title="Select file to scan",
        filetypes=[("All Files", "*.*")]
    )
    if not filepath:
        return

    result = check_file_with_virustotal(filepath)
    messagebox.showinfo("VirusTotal Result", str(result))


def create_gui():
    root = tk.Tk()
    root.title("ChatConverge")

    # --- Menubar ---
    menu = tk.Menu(root)

    file_menu = tk.Menu(menu, tearoff=False)
    file_menu.add_command(label="Import Chat", command=open_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    vt_menu = tk.Menu(menu, tearoff=False)
    vt_menu.add_command(label="Scan File...", command=run_virustotal_scan)
    vt_menu.add_command(label="VirusTotal Settings", command=open_settings)

    menu.add_cascade(label="File", menu=file_menu)
    menu.add_cascade(label="VirusTotal", menu=vt_menu)

    root.config(menu=menu)

    # --- Start with consent dialog ---
    consent = ConsentDialog()
    if not consent.run():
        root.destroy()
        return

    root.mainloop()


if __name__ == "__main__":
    create_gui()
