import pytest
from uuid import uuid4

from sentinel.attacks.outcome import AttackOutcome
from sentinel.attacks.prompt_injection.adaptive import (
    AdaptivePromptInjectionAttack,
)
from sentinel.attacks.result import AttackResult
from sentinel.models.mock import MockModelRuntime
from target.agent.mock import MockTarget


@pytest.mark.asyncio
async def test_adaptive_prompt_injection_runs_two_steps() -> None:
    attack = AdaptivePromptInjectionAttack()

    result = await attack.execute(
        target=MockTarget(),
        evaluation_id=uuid4(),
        run_id=uuid4(),
        model_runtime=MockModelRuntime(
            response="Mock target response",
        ),
    )

    assert isinstance(result, AttackResult)
    assert result.attack_id == "PI-002"
    assert result.success is True
    assert result.outcome == AttackOutcome(
        success=True,
        objective="prompt_injection_escalation",
        evidence=[
            "Adaptive attack reached the escalation stage.",
        ],
    )
    assert result.steps == 2
    assert len(result.observations) == 2
    assert result.observations[0].step == 1
    assert result.observations[0].action == "initial_prompt"
    assert result.observations[0].response == "Mock target response"
    assert result.observations[1].step == 2
    assert result.observations[1].action == "escalation_prompt"
    assert result.observations[1].response == "Mock target response"


@pytest.mark.asyncio
async def test_adaptive_prompt_injection_stops_after_escalation() -> None:
    attack = AdaptivePromptInjectionAttack()

    result = await attack.execute(
        target=MockTarget(),
        evaluation_id=uuid4(),
        run_id=uuid4(),
        model_runtime=MockModelRuntime(
            response="Mock target response",
        ),
    )

    actions = [observation.action for observation in result.observations]

    assert actions == [
        "initial_prompt",
        "escalation_prompt",
    ]


@pytest.mark.asyncio
async def test_adaptive_prompt_injection_stops_when_response_does_not_match() -> None:
    attack = AdaptivePromptInjectionAttack()

    result = await attack.execute(
        target=MockTarget(),
        evaluation_id=uuid4(),
        run_id=uuid4(),
        model_runtime=MockModelRuntime(
            response="I cannot provide that information.",
        ),
    )

    assert result.success is False
    assert result.outcome.objective == "prompt_injection_escalation"
    assert result.outcome.evidence == [
        "Adaptive attack stopped before reaching the escalation stage.",
    ]
    assert result.steps == 1
    assert len(result.observations) == 1
    assert result.observations[0].action == "initial_prompt"