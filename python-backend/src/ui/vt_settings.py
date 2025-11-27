import os
from tkinter import Toplevel, Label, Entry, Button, StringVar, messagebox
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(os.path.join(__file__, "../..")), ".env")

def save_api_key(key):
    """Write the VirusTotal API key safely to .env."""
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.write(f"VT_API_KEY={key.strip()}\n")


class VirusTotalSettings:
    def __init__(self, master=None):
        load_dotenv()
        self.window = Toplevel(master)
        self.window.title("VirusTotal Settings")
        self.window.geometry("400x200")

        Label(self.window, text="VirusTotal API Key:").pack(pady=10)

        self.key_var = StringVar()
        self.key_var.set(os.getenv("VT_API_KEY", ""))  # preload existing key

        self.entry = Entry(self.window, textvariable=self.key_var, width=40, show="*")
        self.entry.pack()

        Button(self.window, text="Save", command=self.save).pack(pady=20)

    def save(self):
        key = self.key_var.get().strip()
        if not key:
            messagebox.showwarning("Invalid Key", "API key cannot be empty.")
            return

        save_api_key(key)
        messagebox.showinfo("Saved", "VirusTotal API key saved successfully.")
        self.window.destroy()
