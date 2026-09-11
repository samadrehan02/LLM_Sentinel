import pytest
from uuid import uuid4

from sentinel.attacks.prompt_injection.adaptive import (
    AdaptivePromptInjectionAttack,
)
from sentinel.evaluators.result import EvaluationStatus
from sentinel.evaluators.simple import SimpleEvaluator
from sentinel.models.mock import MockModelRuntime
from target.agent.mock import MockTarget


@pytest.mark.asyncio
async def test_adaptive_prompt_injection_evaluates_as_success() -> None:
    attack = AdaptivePromptInjectionAttack()

    attack_result = await attack.execute(
        target=MockTarget(),
        evaluation_id=uuid4(),
        run_id=uuid4(),
        model_runtime=MockModelRuntime(
            response="Mock target response",
        ),
    )

    evaluation = await SimpleEvaluator().evaluate(attack_result)

    assert evaluation.status == EvaluationStatus.SUCCESS
    assert evaluation.score == 1.0
    assert attack_result.success is True
    assert attack_result.steps == 2


@pytest.mark.asyncio
async def test_adaptive_prompt_injection_evaluates_as_failure() -> None:
    attack = AdaptivePromptInjectionAttack()

    attack_result = await attack.execute(
        target=MockTarget(),
        evaluation_id=uuid4(),
        run_id=uuid4(),
        model_runtime=MockModelRuntime(
            response="I cannot provide that information.",
        ),
    )

    evaluation = await SimpleEvaluator().evaluate(attack_result)

    assert evaluation.status == EvaluationStatus.FAILURE
    assert evaluation.score == 0.0
    assert attack_result.success is False
    assert attack_result.steps == 1