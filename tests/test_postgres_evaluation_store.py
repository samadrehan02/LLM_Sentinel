from datetime import UTC, datetime
from uuid import uuid4

import pytest

from sentinel.infrastructure.evaluation_store import EvaluationStore
from sentinel.infrastructure.postgres_evaluation_store import (
    PostgresEvaluationStore,
)
from sentinel.models.evaluation import Evaluation, EvaluationStatus


class FakeSession:
    def __init__(self) -> None:
        self.records = {}
        self.added = []
        self.committed = False

    def add(self, record) -> None:
        self.added.append(record)
        self.records[record.evaluation_id] = record

    async def get(self, model, evaluation_id):
        return self.records.get(evaluation_id)

    async def execute(self, statement):
        evaluation_id = statement.whereclause.right.value
        record = self.records.get(evaluation_id)

        class Result:
            def __init__(self, record):
                self.record = record

            def scalar_one_or_none(self):
                return self.record

        return Result(record)

    async def commit(self) -> None:
        self.committed = True


def create_evaluation() -> Evaluation:
    return Evaluation(
        evaluation_id=uuid4(),
        campaign_id=uuid4(),
        attack_id="PI-001",
        attack_category="prompt_injection",
        target="enterprise-assistant",
        status=EvaluationStatus.SUCCESS,
        score=1.0,
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
    )


@pytest.mark.asyncio
async def test_postgres_evaluation_store_saves() -> None:
    session = FakeSession()
    store = PostgresEvaluationStore(session)

    evaluation = create_evaluation()

    await store.save(evaluation)

    assert len(session.added) == 1
    assert session.added[0].evaluation_id == evaluation.evaluation_id
    assert session.committed is True


@pytest.mark.asyncio
async def test_postgres_evaluation_store_gets_evaluation() -> None:
    session = FakeSession()
    store = PostgresEvaluationStore(session)

    evaluation = create_evaluation()

    await store.save(evaluation)

    result = await store.get(
        evaluation.evaluation_id,
    )

    assert result == evaluation


@pytest.mark.asyncio
async def test_postgres_evaluation_store_returns_none_for_unknown_id() -> None:
    session = FakeSession()
    store = PostgresEvaluationStore(session)

    result = await store.get(uuid4())

    assert result is None


def test_postgres_evaluation_store_implements_interface() -> None:
    session = FakeSession()
    store = PostgresEvaluationStore(session)

    assert isinstance(
        store,
        EvaluationStore,
    )