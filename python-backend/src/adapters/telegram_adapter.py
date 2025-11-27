# src/importer/adapters/telegram_adapter.py

import json
from pathlib import Path
from datetime import datetime
from src.adapters.base_adapter import BaseAdapter

class TelegramAdapter(BaseAdapter):
    def __init__(self):
        self.name = "telegram"

    def can_handle(self, path: str) -> bool:
        p = Path(path)
        if p.suffix.lower() not in (".json", ".txt"):
            return False
        try:
            with p.open("r", encoding="utf-8", errors="ignore") as f:
                txt = f.read(8192)
            data = json.loads(txt)
            return isinstance(data, dict) and "messages" in data
        except Exception:
            return False

    def _parse_date(self, d):
        # Telegram export often uses ISO format; fall back where needed
        try:
            return datetime.fromisoformat(d).isoformat()
        except Exception:
            return d

    def parse(self, path: str) -> dict:
        p = Path(path)
        with p.open("r", encoding="utf-8", errors="ignore") as f:
            data = json.load(f)

        messages = []
        for m in data.get("messages", []):
            if m.get("type") != "message":
                continue
            txt = m.get("text", "")
            # text in telegram export may be a list/dict; normalize to string
            if isinstance(txt, list):
                parts = []
                for el in txt:
                    if isinstance(el, str):
                        parts.append(el)
                    elif isinstance(el, dict) and "text" in el:
                        parts.append(el.get("text"))
                txt = "".join(parts)
            messages.append({
                "timestamp": self._parse_date(m.get("date", "")),
                "sender": m.get("from", m.get("actor", "Unknown")),
                "text": txt,
                "attachments": m.get("photo", []) + m.get("media", []) if isinstance(m, dict) else []
            })

        return {"platform": "telegram", "messages": messages}
