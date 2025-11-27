import os
import sys
from tkinter import Tk, filedialog
import tkinter as tk

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello"}


# Ensure project root path
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(ROOT))

from src.ui.consent_dialog import ConsentDialog
from src.ui.vt_settings import VirusTotalSettings
from src.importer.import_engine import ImportEngine


try:
    from src.security.virustotal_hash import check_file_with_virustotal
    VT_AVAILABLE = True
except ImportError:
    VT_AVAILABLE = False


def pick_chat_file():
    root = Tk()
    root.withdraw()
    file = filedialog.askopenfilename(
        title="Select Chat File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    root.destroy()
    return file


def main():
    # === 1. Consent dialog ===
    consent = ConsentDialog()
    if not consent.run():
        print("User declined consent. Exiting.")
        return

    print("=== ChatConverge ===")

    # === 2. Select chat file ===
    chat_file = pick_chat_file()
    if not chat_file:
        print("No chat file selected.")
        return

    print(f"Selected file: {chat_file}")

    # === 3. Universal importer ===
    engine = ImportEngine()
    try:
        records = engine.import_file(chat_file)
    except Exception as e:
        print(f"[Error] Import failed: {e}")
        return

    print(f"Imported {len(records)} normalized messages.")

    # TODO: Save records into your FTS search DB here

    # === 4. VirusTotal ===
    print("\nVirusTotal Options:")
    print("1. Scan file hash")
    print("2. Open VirusTotal settings (enter API key)")
    print("3. Skip")

    choice = input("Choose an option (1/2/3): ").strip()

    if choice == "2":
        import tkinter as tk
        settings_win = tk.Toplevel()
        VirusTotalSettings(settings_win)
        settings_win.grab_set()      # makes it modal
        settings_win.wait_window()   # block until closed
        return

    
    if choice == "1":
        if not VT_AVAILABLE:
            print("[Error] virustotal_hash.py missing.")
            return

        if os.getenv("VT_API_KEY") is None:
            print("[Error] VirusTotal API key missing. Open settings.")
            return

        print("\n[+] Scanning file hash with VirusTotal…")
        result = check_file_with_virustotal(chat_file)
        print("Result:", result)

    print("\nDone.")


if __name__ == "__main__":
    main()

