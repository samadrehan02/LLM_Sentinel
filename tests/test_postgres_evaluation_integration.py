from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from sentinel.infrastructure.database import (
    create_engine,
    create_session_factory,
    create_tables,
    drop_tables,
)
from sentinel.infrastructure.postgres_evaluation_store import (
    PostgresEvaluationStore,
)
from sentinel.models.evaluation import Evaluation, EvaluationStatus


DATABASE_URL = (
    "postgresql+asyncpg://sentinel:sentinel@localhost:5432/llm_sentinel"
)


def create_evaluation() -> Evaluation:
    return Evaluation(
        evaluation_id=uuid4(),
        campaign_id=uuid4(),
        attack_id="PI-001",
        attack_category="prompt_injection",
        target="enterprise-assistant",
        status=EvaluationStatus.SUCCESS,
        score=0.85,
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
    )


@pytest.mark.asyncio
async def test_postgres_evaluation_store_round_trip() -> None:
    engine = create_engine(DATABASE_URL)
    session_factory = create_session_factory(engine)

    try:
        await drop_tables(engine)
        await create_tables(engine)

        async with session_factory() as session:
            store = PostgresEvaluationStore(session)

            evaluation = create_evaluation()

            await store.save(evaluation)

            loaded = await store.get(
                evaluation.evaluation_id,
            )

            assert loaded is not None
            assert loaded.evaluation_id == evaluation.evaluation_id
            assert loaded.campaign_id == evaluation.campaign_id
            assert loaded.attack_id == evaluation.attack_id
            assert loaded.attack_category == evaluation.attack_category
            assert loaded.target == evaluation.target
            assert loaded.status == evaluation.status
            assert loaded.score == evaluation.score
            assert loaded.started_at == evaluation.started_at
            assert loaded.completed_at == evaluation.completed_at

    finally:
        await drop_tables(engine)
        await engine.dispose()