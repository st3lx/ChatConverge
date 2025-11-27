# src/importer/adapters/messenger_adapter.py

from pathlib import Path
from src.adapters.base_adapter import BaseAdapter

# We try to import bs4 dynamically; if missing, adapter falls back with clear error.
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except Exception:
    BS4_AVAILABLE = False

class MessengerAdapter(BaseAdapter):
    def __init__(self):
        self.name = "messenger"

    def can_handle(self, path: str) -> bool:
        p = Path(path)
        if p.suffix.lower() not in (".html", ".htm", ".json"):
            return False
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
            return "<div class=\"message\"" in text or "Messages from" in text or "<title>Facebook" in text
        except Exception:
            return False

    def parse(self, path: str) -> dict:
        if not BS4_AVAILABLE:
            raise RuntimeError("beautifulsoup4 is required for Messenger parsing. Install with `pip install beautifulsoup4`.")

        p = Path(path)
        html = p.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")

        messages = []

        # There are different Facebook export formats; we try several heuristics.
        # Common: messages in divs with class "message"
        for div in soup.select("div.message, div._3-96, li.message"):
            # attempt to extract sender, timestamp, and text
            sender_el = div.select_one(".user, .from, ._3-96")
            sender = sender_el.get_text(strip=True) if sender_el else "Unknown"

            time_el = div.select_one("span.meta, abbr, .timestamp")
            timestamp = time_el.get_text(strip=True) if time_el else ""

            content_el = div.select_one(".message_text, ._3-95, .content, p")
            text = content_el.get_text("\n", strip=True) if content_el else div.get_text("\n", strip=True)

            messages.append({
                "timestamp": timestamp,
                "sender": sender,
                "text": text,
                "attachments": []
            })

        # Fallback: look for <div class="thread"> or simple paragraphs
        if not messages:
            for ptag in soup.select("p"):
                txt = ptag.get_text(strip=True)
                if txt:
                    messages.append({"timestamp": "", "sender": "Unknown", "text": txt, "attachments": []})

        return {"platform": "messenger", "messages": messages}

