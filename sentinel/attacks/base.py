from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class Attack(ABC):
    attack_id: str
    name: str
    description: str
    category: str
    severity: str

    @abstractmethod
    async def execute(
        self,
        target: Any,
        evaluation_id: UUID,
        run_id: UUID,
        model_runtime: Any,
    ) -> Any:
        """Execute the attack against the target."""
        raise NotImplementedError
