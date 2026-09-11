from abc import abstractmethod
from typing import Any
from uuid import UUID

from sentinel.attacks.base import Attack
from sentinel.attacks.observation import AttackObservation
from sentinel.attacks.state import AttackState


class AdaptiveAttack(Attack):
    @abstractmethod
    async def choose_next_action(
        self,
        state: AttackState,
        model_runtime: Any,
    ) -> str | None:
        """Choose the next attack action from the current state."""
        raise NotImplementedError

    @abstractmethod
    async def execute_action(
        self,
        action: str,
        state: AttackState,
        target: Any,
        model_runtime: Any,
        evaluation_id: UUID,
        run_id: UUID,
    ) -> AttackObservation:
        """Execute one selected attack action and return its observation."""
        raise NotImplementedError