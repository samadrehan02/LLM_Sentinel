import pytest

from sentinel.attacks.prompt_injection.direct import (
    DirectPromptInjectionAttack,
)
from sentinel.defenses.basic_policy import BasicToolPolicy
from sentinel.evaluators.result import EvaluationStatus
from sentinel.evaluators.sensitive_data import SensitiveDataEvaluator
from sentinel.instrumentation.event_bus import EventBus
from sentinel.instrumentation.events import EventType
from sentinel.models.mock import MockModelRuntime
from sentinel.orchestrator.runner import EvaluationRunner
from target.agent.agent import EnterpriseAgent


@pytest.mark.asyncio
async def test_prompt_injection_end_to_end():
    event_bus = EventBus()
    events = []

    for event_type in (
        EventType.EVALUATION_STARTED,
        EventType.ATTACK_STARTED,
        EventType.AGENT_REQUEST,
        EventType.LLM_GENERATION,
        EventType.ATTACK_EVALUATED,
        EventType.FINDING_CREATED,
    ):
        event_bus.subscribe(
            event_type,
            events.append,
        )

    model = MockModelRuntime(
        response=(
            "Customer CUST-001 has internal_note information. "
            "The API key is SYNTHETIC-KEY-001-NOT-REAL."
        ),
    )

    runner = EvaluationRunner(
        model_runtime=model,
        target=EnterpriseAgent(),
        evaluator=SensitiveDataEvaluator(),
        policy=BasicToolPolicy(
            allowed_tools={"customer_lookup"},
        ),
        event_bus=event_bus,
    )

    result = await runner.run(
        DirectPromptInjectionAttack(),
    )

    assert result.evaluation.status == EvaluationStatus.SUCCESS
    assert result.evaluation.score == 1.0

    assert result.finding is not None
    assert result.finding.attack_id == "PI-001"

    assert len(events) == 6

    assert events[0].event_type == EventType.EVALUATION_STARTED
    assert events[1].event_type == EventType.ATTACK_STARTED
    assert events[2].event_type == EventType.AGENT_REQUEST
    assert events[3].event_type == EventType.LLM_GENERATION
    assert events[4].event_type == EventType.ATTACK_EVALUATED
    assert events[5].event_type == EventType.FINDING_CREATED
