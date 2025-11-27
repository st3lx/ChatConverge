# src/importer/adapters/whatsapp_adapter.py

from datetime import datetime
import re
from pathlib import Path
from .base_adapter import BaseAdapter
from src.parser.whatsapp_parser import WhatsAppParser

# Heuristic: .txt file, contains " - " separators used by WhatsApp exports.
def _looks_like_whatsapp(text: str) -> bool:
    first = text.strip().splitlines()[0] if text.strip() else ""
    return bool(re.search(r"\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}", first)) and " - " in first

class WhatsAppAdapter(BaseAdapter):
    def __init__(self):
        self.name = "whatsapp"

    def can_handle(self, path: str) -> bool:
        try:
            p = Path(path)
            if p.suffix.lower() != ".txt":
                return False
            with p.open("r", encoding="utf-8", errors="ignore") as f:
                head = f.read(2048)
            return _looks_like_whatsapp(head)
        except Exception:
            return False

    def parse(self, path: str) -> dict:
        """
        Uses existing WhatsAppParser to parse the file and returns normalized structure:
        {
          "platform": "whatsapp",
          "messages": [ {timestamp: str, sender: str, text: str, attachments: []}, ... ]
        }
        """
        parser = WhatsAppParser()
        msgs = parser.parse(path)  # expected list of dicts {"timestamp","sender","text",...}

        normalized = []
        for m in msgs:
            normalized.append({
                "timestamp": m.get("timestamp"),
                "sender": m.get("sender"),
                "text": m.get("text"),
                "attachments": m.get("attachments", [])
            })

        return {"platform": "whatsapp", "messages": normalized}
