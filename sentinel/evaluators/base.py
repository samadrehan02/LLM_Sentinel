from abc import ABC, abstractmethod
from typing import Any


class Evaluator(ABC):
    evaluator_id: str
    name: str
    description: str

    @abstractmethod
    async def evaluate(
        self,
        attack_result: Any,
    ) -> Any:
        """Evaluate whether an attack succeeded."""
        raise NotImplementedError
