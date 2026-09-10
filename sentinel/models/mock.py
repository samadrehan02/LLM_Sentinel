from typing import Any

from sentinel.models.runtime import ModelRuntime


class MockModelRuntime(ModelRuntime):
    def __init__(self, response: str = "Mock model response") -> None:
        self.response = response
        self.last_messages: list[dict[str, str]] | None = None

    async def generate(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> str:
        self.last_messages = messages
        return self.response
