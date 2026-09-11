from uuid import UUID, uuid4

import pytest

from sentinel.evaluators.result import (
    EvaluationResult,
    EvaluationStatus,
)
from sentinel.infrastructure.evaluation_store import InMemoryEvaluationStore
from sentinel.instrumentation.event_bus import EventBus
from sentinel.models.evaluation import EvaluationStatus as RecordStatus
from sentinel.orchestrator.runner import EvaluationRunner


class FakeAttack:
    attack_id = "TEST-001"
    name = "Persistence Test Attack"
    category = "prompt_injection"
    severity = "high"

    async def execute(
        self,
        target,
        evaluation_id,
        run_id,
        model_runtime,
    ):
        return {"success": True}


class FakeModelRuntime:
    async def generate(self, *args, **kwargs):
        return "test response"


class FakeTarget:
    pass


class FakeEvaluator:
    async def evaluate(self, attack_result):
        return EvaluationResult(
            status=EvaluationStatus.SUCCESS,
            score=0.9,
            evidence=["Test attack succeeded"],
            metadata={},
        )


class FakePolicy:
    pass


class RecordingEvaluationStore(InMemoryEvaluationStore):
    def __init__(self) -> None:
        super().__init__()
        self.saved_statuses: list[RecordStatus] = []

    async def save(self, evaluation) -> None:
        self.saved_statuses.append(evaluation.status)
        await super().save(evaluation)


@pytest.mark.asyncio
async def test_runner_persists_running_and_final_evaluation() -> None:
    store = RecordingEvaluationStore()

    runner = EvaluationRunner(
        model_runtime=FakeModelRuntime(),
        target=FakeTarget(),
        evaluator=FakeEvaluator(),
        policy=FakePolicy(),
        event_bus=EventBus(),
        evaluation_store=store,
    )

    result = await runner.run(FakeAttack())

    assert result.record is not None

    assert store.saved_statuses == [
        RecordStatus.RUNNING,
        result.record.status,
    ]

    persisted = await store.get(result.record.evaluation_id)

    assert persisted is not None
    assert persisted.evaluation_id == result.record.evaluation_id
    assert persisted.attack_id == "TEST-001"
    assert persisted.attack_category == "prompt_injection"
    assert persisted.status == RecordStatus.SUCCESS
    assert persisted.score == 0.9
    assert persisted.completed_at is not None


@pytest.mark.asyncio
async def test_runner_works_without_evaluation_store() -> None:
    runner = EvaluationRunner(
        model_runtime=FakeModelRuntime(),
        target=FakeTarget(),
        evaluator=FakeEvaluator(),
        policy=FakePolicy(),
        event_bus=EventBus(),
    )

    result = await runner.run(FakeAttack())

    assert result.record is not None
    assert isinstance(result.record.evaluation_id, UUID)
    assert result.record.status == RecordStatus.SUCCESS
    assert result.record.score == 0.9
    assert result.record.completed_at is not None