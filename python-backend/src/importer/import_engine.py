from .detectors.whatsapp_detector import WhatsAppDetector
from .detectors.telegram_detector import TelegramDetector
from .detectors.messenger_detector import MessengerDetector

from src.adapters.whatsapp_adapter import WhatsAppAdapter
from src.adapters.telegram_adapter import TelegramAdapter
from src.adapters.messenger_adapter import MessengerAdapter

class ImportEngine:
    def __init__(self):
        self.detectors = [
            (WhatsAppDetector(), WhatsAppAdapter()),
            (TelegramDetector(),  TelegramAdapter()),
            (MessengerDetector(), MessengerAdapter())
        ]

    def import_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        for detector, adapter in self.detectors:
            if detector.matches(text):
                print(f"Detected format: {adapter.__class__.__name__}")
                return adapter.parse(text)

        raise ValueError("Unknown chat export format")
