# src/security/virustotal_hash.py

import os
import hashlib
import requests
import tkinter as tk
from tkinter import messagebox

VT_API_URL = "https://www.virustotal.com/api/v3/files/"

def compute_sha256(file_path: str) -> str:
    """Compute the SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def ask_user_confirmation(hash_value: str) -> bool:
    """Prompt user whether to check hash on VirusTotal."""
    root = tk.Tk()
    root.withdraw()
    msg = (
        f"Detected attachment.\n\nSHA256:\n{hash_value}\n\n"
        "Would you like to query VirusTotal to check if this file is known as malicious?"
    )
    return messagebox.askyesno("VirusTotal Check", msg)

def query_virustotal(hash_value: str, api_key: str) -> dict:
    """Send the hash to VirusTotal API (no file upload)."""
    headers = {"x-apikey": api_key}
    resp = requests.get(VT_API_URL + hash_value, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    elif resp.status_code == 404:
        return {"data": None, "message": "File hash not found in VirusTotal database."}
    else:
        return {"data": None, "message": f"Error {resp.status_code}: {resp.text}"}

def check_file(file_path: str, api_key: str):
    """Main wrapper: compute hash, ask user, optionally query VT."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    hash_value = compute_sha256(file_path)
    print(f"Computed SHA256: {hash_value}")

    if ask_user_confirmation(hash_value):
        result = query_virustotal(hash_value, api_key)
        root = tk.Tk()
        root.withdraw()

        if result.get("data"):
            stats = result["data"]["attributes"]["last_analysis_stats"]
            messagebox.showinfo(
                "VirusTotal Result",
                f"Results:\n"
                f"Malicious: {stats['malicious']}\n"
                f"Suspicious: {stats['suspicious']}\n"
                f"Undetected: {stats['undetected']}"
            )
        else:
            messagebox.showinfo("VirusTotal Result", result.get("message", "Unknown error."))
