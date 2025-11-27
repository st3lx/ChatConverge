import re
from .base_detector import BaseDetector

class WhatsAppDetector(BaseDetector):
    pattern = re.compile(r"^\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} (AM|PM) - .+: .+")

    def matches(self, text: str) -> bool:
        return bool(self.pattern.match(text.splitlines()[0]))
