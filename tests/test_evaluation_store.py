from uuid import uuid4

import pytest

from sentinel.infrastructure.evaluation_store import (
    EvaluationStore,
    InMemoryEvaluationStore,
)
from sentinel.models.evaluation import (
    Evaluation,
    EvaluationStatus,
)


def create_evaluation() -> Evaluation:
    return Evaluation(
        attack_id="PI-001",
        attack_category="prompt_injection",
        target="enterprise-assistant",
    )


@pytest.mark.asyncio
async def test_in_memory_evaluation_store_saves_and_gets() -> None:
    store = InMemoryEvaluationStore()
    evaluation = create_evaluation()

    await store.save(evaluation)

    result = await store.get(
        evaluation.evaluation_id,
    )

    assert result == evaluation


@pytest.mark.asyncio
async def test_in_memory_evaluation_store_returns_none_for_unknown_id() -> None:
    store = InMemoryEvaluationStore()

    result = await store.get(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_in_memory_evaluation_store_updates_existing_evaluation() -> None:
    store = InMemoryEvaluationStore()
    evaluation = create_evaluation()

    await store.save(evaluation)

    evaluation.status = EvaluationStatus.SUCCESS
    evaluation.score = 1.0

    await store.save(evaluation)

    result = await store.get(
        evaluation.evaluation_id,
    )

    assert result is not None
    assert result.status == EvaluationStatus.SUCCESS
    assert result.score == 1.0


def test_in_memory_evaluation_store_implements_interface() -> None:
    store = InMemoryEvaluationStore()

    assert isinstance(
        store,
        EvaluationStore,
    )