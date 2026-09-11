from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AttackObservation(BaseModel):
    observation_id: UUID = Field(default_factory=uuid4)
    evaluation_id: UUID
    run_id: UUID
    step: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    action: str
    response: Any = None
    metadata: dict[str, Any] = Field(default_factory=dict)