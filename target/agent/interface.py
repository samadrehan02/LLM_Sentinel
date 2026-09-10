from abc import ABC, abstractmethod
from typing import Any


class Target(ABC):
    target_id: str
    name: str
    description: str

    @abstractmethod
    async def interact(
        self,
        messages: list[dict[str, str]],
        model_runtime: Any,
        **kwargs: Any,
    ) -> str:
        """Send an interaction to the target agent."""
        raise NotImplementedError
