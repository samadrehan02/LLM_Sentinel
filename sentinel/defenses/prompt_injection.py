import re


class PromptInjectionDetector:
    def __init__(self) -> None:
        self.patterns = [
            re.compile(
                r"ignore\s+(all\s+)?previous\s+instructions",
                re.IGNORECASE,
            ),
            re.compile(
                r"ignore\s+(all\s+)?prior\s+instructions",
                re.IGNORECASE,
            ),
            re.compile(
                r"you\s+are\s+now\s+operating\s+in\s+administrator\s+mode",
                re.IGNORECASE,
            ),
            re.compile(
                r"reveal\s+(the\s+)?system\s+prompt",
                re.IGNORECASE,
            ),
        ]

    def detect(self, text: str) -> bool:
        return any(
            pattern.search(text)
            for pattern in self.patterns
        )