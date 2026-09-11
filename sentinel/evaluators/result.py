from enum import Enum
from typing import Any

from pydantic import BaseModel


class EvaluationStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    INCONCLUSIVE = "inconclusive"


class EvaluationType(str, Enum):
    ATTACK = "attack"
    BENIGN = "benign"


class EvaluationResult(BaseModel):
    status: EvaluationStatus
    score: float
    evidence: list[str]
    metadata: dict[str, Any]
    evaluation_type: EvaluationType = EvaluationType.ATTACK
