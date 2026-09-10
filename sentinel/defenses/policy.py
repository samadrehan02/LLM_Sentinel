from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from pydantic import BaseModel


class PolicyDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_REVIEW = "require_review"


class PolicyRequest(BaseModel):
    agent_id: str
    tool_name: str
    arguments: dict[str, Any]
    context: dict[str, Any] = {}


class PolicyResult(BaseModel):
    decision: PolicyDecision
    reason: str
    policy_id: str


class Policy(ABC):
    policy_id: str
    name: str

    @abstractmethod
    def evaluate(self, request: PolicyRequest) -> PolicyResult:
        """Determine whether an agent action is permitted."""
        raise NotImplementedError
