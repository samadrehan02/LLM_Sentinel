import pytest

from sentinel.attacks.outcome import AttackOutcome
from sentinel.attacks.result import AttackResult
from sentinel.evaluators.result import EvaluationStatus
from sentinel.evaluators.simple import SimpleEvaluator


@pytest.mark.asyncio
async def test_simple_evaluator_success() -> None:
    evaluator = SimpleEvaluator()

    result = await evaluator.evaluate(True)

    assert result.status == EvaluationStatus.SUCCESS
    assert result.score == 1.0


@pytest.mark.asyncio
async def test_simple_evaluator_failure() -> None:
    evaluator = SimpleEvaluator()

    result = await evaluator.evaluate(False)

    assert result.status == EvaluationStatus.FAILURE
    assert result.score == 0.0


@pytest.mark.asyncio
async def test_simple_evaluator_dict_result_is_failure() -> None:
    evaluator = SimpleEvaluator()

    result = await evaluator.evaluate(
        {
            "attack_id": "PI-001",
            "response": "Mock response",
        }
    )

    assert result.status == EvaluationStatus.FAILURE
    assert result.score == 0.0


@pytest.mark.asyncio
async def test_simple_evaluator_attack_result_success() -> None:
    evaluator = SimpleEvaluator()

    result = await evaluator.evaluate(
        AttackResult(
            attack_id="PI-002",
            outcome=AttackOutcome(
                success=True,
                objective="prompt_injection_escalation",
                evidence=[
                    "Adaptive attack reached the escalation stage.",
                ],
                metadata={
                    "objective_confidence": 0.9,
                },
            ),
            metadata={
                "steps": 2,
            },
        )
    )

    assert result.status == EvaluationStatus.SUCCESS
    assert result.score == 1.0
    assert result.evidence == [
        "Adaptive attack reached the escalation stage.",
    ]
    assert result.metadata == {
        "steps": 2,
        "objective_confidence": 0.9,
    }


@pytest.mark.asyncio
async def test_simple_evaluator_attack_result_failure() -> None:
    evaluator = SimpleEvaluator()

    result = await evaluator.evaluate(
        AttackResult(
            attack_id="PI-002",
            outcome=AttackOutcome(
                success=False,
                objective="prompt_injection_escalation",
                evidence=[
                    "Adaptive attack stopped before reaching the escalation stage.",
                ],
            ),
            metadata={
                "steps": 1,
            },
        )
    )

    assert result.status == EvaluationStatus.FAILURE
    assert result.score == 0.0
    assert result.evidence == [
        "Adaptive attack stopped before reaching the escalation stage.",
    ]
    assert result.metadata == {
        "steps": 1,
    }