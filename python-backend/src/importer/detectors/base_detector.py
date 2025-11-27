class BaseDetector:
    def matches(self, text: str) -> bool:
        raise NotImplementedError
