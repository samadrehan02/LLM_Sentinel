from sentinel.defenses.prompt_injection import PromptInjectionDetector


class PromptInjectionMiddleware:
    def __init__(
        self,
        detector: PromptInjectionDetector,
    ) -> None:
        self.detector = detector

    def inspect(self, text: str) -> None:
        if self.detector.detect(text):
            raise PermissionError("Request blocked by prompt injection defense.")
