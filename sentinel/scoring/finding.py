from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Finding(BaseModel):
    finding_id: UUID = Field(default_factory=uuid4)

    evaluation_id: UUID
    attack_id: str

    title: str
    description: str

    severity: Severity
    score: float

    evidence: list[str] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)
