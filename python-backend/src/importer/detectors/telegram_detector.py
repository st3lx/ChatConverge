import json
from .base_detector import BaseDetector

class TelegramDetector(BaseDetector):
    def matches(self, text: str) -> bool:
        try:
            data = json.loads(text)
            return "messages" in data
        except:
            return False
