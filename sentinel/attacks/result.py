from typing import Any

from pydantic import BaseModel, Field

from sentinel.attacks.observation import AttackObservation
from sentinel.attacks.outcome import AttackOutcome


class AttackResult(BaseModel):
    attack_id: str
    outcome: AttackOutcome
    observations: list[AttackObservation] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def success(self) -> bool:
        return self.outcome.success

    @property
    def steps(self) -> int:
        return len(self.observations)