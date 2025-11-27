from .base_detector import BaseDetector

class MessengerDetector(BaseDetector):
    def matches(self, text: str) -> bool:
        return '<div class="messages"' in text or "<title>Facebook" in text
