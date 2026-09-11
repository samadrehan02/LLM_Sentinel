from typing import Any

from pydantic import BaseModel, Field


class AttackOutcome(BaseModel):
    success: bool
    objective: str
    evidence: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)