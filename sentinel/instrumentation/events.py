from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class EventType(str, Enum):
    EVALUATION_STARTED = "evaluation.started"
    ATTACK_STARTED = "attack.started"
    AGENT_REQUEST = "agent.request"
    LLM_GENERATION = "llm.generation"
    RETRIEVAL = "retrieval"
    TOOL_REQUESTED = "tool.requested"
    AUTHORIZATION_DECISION = "authorization.decision"
    TOOL_EXECUTED = "tool.executed"
    AGENT_RESPONSE = "agent.response"
    ATTACK_EVALUATED = "attack.evaluated"
    DEFENSE_BLOCKED = "defense.blocked"
    FINDING_CREATED = "finding.created"


class Event(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    evaluation_id: UUID
    run_id: UUID
    trace_id: UUID
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )
    event_type: EventType
    component: str
    payload: dict[str, Any] = Field(default_factory=dict)
    schema_version: str = "1.0"