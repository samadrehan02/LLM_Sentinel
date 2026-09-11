import pytest

from sentinel.attacks.base import Attack
from sentinel.defenses.basic_policy import BasicToolPolicy
from sentinel.evaluators.simple import SimpleEvaluator
from sentinel.instrumentation.event_bus import EventBus
from sentinel.models.mock import MockModelRuntime
from sentinel.orchestrator.runner import EvaluationRunner
from target.agent.mock import MockTarget


class RecordTestAttack(Attack):
    attack_id = "TEST-RECORD"
    name = "Record Test Attack"
    description = "Attack used to test evaluation records."
    category = "test"
    severity = "low"

    async def execute(
        self,
        target,
        evaluation_id,
        run_id,
        model_runtime,
    ) -> bool:
        return True


def create_runner() -> EvaluationRunner:
    return EvaluationRunner(
        model_runtime=MockModelRuntime(
            response="Mock target response",
        ),
        target=MockTarget(),
        evaluator=SimpleEvaluator(),
        policy=BasicToolPolicy(
            allowed_tools={"search_documents"},
        ),
        event_bus=EventBus(),
    )


@pytest.mark.asyncio
async def test_runner_returns_completed_evaluation_record() -> None:
    runner = create_runner()
    attack = RecordTestAttack()

    result = await runner.run(attack)

    assert result.record is not None
    assert result.record.evaluation_id is not None
    assert result.record.attack_id == attack.attack_id
    assert result.record.attack_category == attack.category
    assert result.record.target == "enterprise-assistant"
    assert result.record.status.value == result.evaluation.status.value
    assert result.record.score == result.evaluation.score
    assert result.record.completed_at is not None


@pytest.mark.asyncio
async def test_runner_record_has_completed_status() -> None:
    runner = create_runner()

    result = await runner.run(
        RecordTestAttack(),
    )

    assert result.record is not None
    assert result.record.status.value == "success"
    assert result.record.score == 1.0
    assert result.record.completed_at is not None