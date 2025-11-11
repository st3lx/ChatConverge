import sys, os
sys.path.append(os.path.dirname(__file__))  # Add src/ to path

from src.parsers.whatsapp_parser import WhatsAppParser
from src.ui.consent_dialog import ConsentDialog
from db.fts_builder import FTSDatabase

import tkinter as tk
from tkinter import filedialog

def main():
    print("=== ChatConverge ===")

    # Step 1: Show consent dialog
    consent = ConsentDialog()
    if not consent.get_consent():
        print("User did not consent. Exiting.")
        return

    # Step 2: Let user select exported WhatsApp chat file
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename(
        title="Select WhatsApp Chat .txt",
        filetypes=[("Text files", "*.txt")]
    )
    if not filepath:
        print("No file selected. Exiting.")
        return

    # Step 3: Parse and build DB
    print(f"Parsing messages from: {filepath}")
    parser = WhatsAppParser()
    messages = parser.parse(filepath)
    print(f"Parsed {len(messages)} messages.")

    db = FTSDatabase("chatconverge.db")
    db.insert_messages(messages)
    print("Messages saved to chatconverge.db (FTS5 search enabled).")

    from src.security.virustotal_hash import check_file

    # Suppose your attachments folder:
    attachments = ["path/to/photo.jpg", "path/to/video.mp4"]

    VT_API_KEY = "YOUR_VIRUSTOTAL_API_KEY"  # You can set this via .env later

    for f in attachments:
       check_file(f, VT_API_KEY)


    # Step 4: Query loop
    while True:
        q = input("\nSearch messages (or 'exit'): ").strip()
        if q.lower() == "exit":
            break
        results = db.search(q)
        for ts, sender, text in results:
            print(f"[{ts}] {sender}: {text}")

if __name__ == "__main__":
    main()
