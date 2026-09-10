from typing import Any

from sentinel.models.runtime import ModelRuntime
from target.agent.interface import Target


class MockTarget(Target):
    target_id = "mock-target"
    name = "Mock Target"
    description = "Minimal target used for testing."

    def __init__(self, response: str = "Mock target response") -> None:
        self.response = response

    async def interact(
        self,
        messages: list[dict[str, str]],
        model_runtime: ModelRuntime,
        **kwargs: Any,
    ) -> str:
        return await model_runtime.generate(
            messages=messages,
            **kwargs,
        )
