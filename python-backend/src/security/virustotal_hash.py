import hashlib
import requests
from dotenv import load_dotenv
import os

load_dotenv()   # loads .env from project root

VT_API_KEY = os.getenv("VT_API_KEY")

if not VT_API_KEY:
    raise RuntimeError(
        "VirusTotal API key not found. Please create a .env file with:\n"
        "VT_API_KEY=your_api_key_here"
    )

API_URL = "https://www.virustotal.com/api/v3/files/{}"


def compute_file_hash(path: str) -> str:
    """Return the SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()


def check_file_with_virustotal(path: str) -> dict:
    """Upload hash to VirusTotal and return report."""
    file_hash = compute_file_hash(path)

    headers = {"x-apikey": VT_API_KEY}

    response = requests.get(API_URL.format(file_hash), headers=headers)

    if response.status_code == 404:
        return {"found": False, "hash": file_hash}

    response.raise_for_status()

    data = response.json()
    malicious = data["data"]["attributes"]["last_analysis_stats"]["malicious"]

    return {"found": True, "malicious": malicious, "hash": file_hash}
