from uuid import uuid4
from datetime import UTC, datetime

from sentinel.infrastructure.postgres_evaluation_store import (
    PostgresEvaluationStore,
)
from collections.abc import AsyncGenerator
from sentinel.models.evaluation import Evaluation, EvaluationStatus
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine

from sentinel.infrastructure.database import (
    Base,
    create_engine,
    create_session_factory,
)
from sentinel.infrastructure.postgres_event_store import PostgresEventStore
from sentinel.infrastructure.settings import DatabaseSettings
from sentinel.instrumentation.events import Event, EventType


@pytest_asyncio.fixture
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    settings = DatabaseSettings()
    engine = create_engine(settings.database_url)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

    await engine.dispose()


def create_test_event(
    evaluation_id=None,
    event_type: EventType = EventType.TOOL_EXECUTED,
    component: str = "integration_test",
    payload: dict | None = None,
) -> Event:
    return Event(
        evaluation_id=evaluation_id or uuid4(),
        run_id=uuid4(),
        trace_id=uuid4(),
        event_type=event_type,
        component=component,
        payload=payload or {},
    )


@pytest.mark.asyncio
async def test_postgres_event_store_round_trip(
    engine: AsyncEngine,
) -> None:
    session_factory = create_session_factory(engine)

    event = create_test_event(
        event_type=EventType.TOOL_EXECUTED,
        payload={
            "tool_name": "customer_lookup",
            "customer_id": "CUST-001",
            "result": "synthetic",
        },
    )

    async with session_factory() as session:
        store = PostgresEventStore(session)

        await store.save(event)

        events = await store.get_by_evaluation(
            event.evaluation_id,
        )

    assert len(events) == 1

    persisted = events[0]

    assert persisted.event_id == event.event_id
    assert persisted.evaluation_id == event.evaluation_id
    assert persisted.run_id == event.run_id
    assert persisted.trace_id == event.trace_id
    assert persisted.event_type == event.event_type
    assert persisted.component == event.component
    assert persisted.payload == event.payload
    assert persisted.schema_version == event.schema_version


@pytest.mark.asyncio
async def test_postgres_event_store_returns_multiple_events(
    engine: AsyncEngine,
) -> None:
    session_factory = create_session_factory(engine)
    evaluation_id = uuid4()

    events_to_save = [
        create_test_event(
            evaluation_id=evaluation_id,
            event_type=EventType.EVALUATION_STARTED,
        ),
        create_test_event(
            evaluation_id=evaluation_id,
            event_type=EventType.ATTACK_STARTED,
        ),
        create_test_event(
            evaluation_id=evaluation_id,
            event_type=EventType.ATTACK_EVALUATED,
        ),
    ]

    async with session_factory() as session:
        store = PostgresEventStore(session)

        for event in events_to_save:
            await store.save(event)

        events = await store.get_by_evaluation(
            evaluation_id,
        )

    assert len(events) == 3
    assert {
        event.event_id
        for event in events
    } == {
        event.event_id
        for event in events_to_save
    }


@pytest.mark.asyncio
async def test_postgres_event_store_isolates_evaluations(
    engine: AsyncEngine,
) -> None:
    session_factory = create_session_factory(engine)

    evaluation_a = uuid4()
    evaluation_b = uuid4()

    event_a = create_test_event(
        evaluation_id=evaluation_a,
        payload={"evaluation": "A"},
    )
    event_b = create_test_event(
        evaluation_id=evaluation_b,
        payload={"evaluation": "B"},
    )

    async with session_factory() as session:
        store = PostgresEventStore(session)

        await store.save(event_a)
        await store.save(event_b)

        events_a = await store.get_by_evaluation(
            evaluation_a,
        )
        events_b = await store.get_by_evaluation(
            evaluation_b,
        )

    assert len(events_a) == 1
    assert events_a[0].payload == {"evaluation": "A"}

    assert len(events_b) == 1
    assert events_b[0].payload == {"evaluation": "B"}


@pytest.mark.asyncio
async def test_postgres_event_store_preserves_event_order(
    engine: AsyncEngine,
) -> None:
    session_factory = create_session_factory(engine)
    evaluation_id = uuid4()

    events_to_save = [
        create_test_event(
            evaluation_id=evaluation_id,
            event_type=EventType.EVALUATION_STARTED,
        ),
        create_test_event(
            evaluation_id=evaluation_id,
            event_type=EventType.ATTACK_STARTED,
        ),
        create_test_event(
            evaluation_id=evaluation_id,
            event_type=EventType.TOOL_REQUESTED,
        ),
        create_test_event(
            evaluation_id=evaluation_id,
            event_type=EventType.TOOL_EXECUTED,
        ),
    ]

    async with session_factory() as session:
        store = PostgresEventStore(session)

        for event in events_to_save:
            await store.save(event)

        persisted_events = await store.get_by_evaluation(
            evaluation_id,
        )

    assert [
        event.event_type
        for event in persisted_events
    ] == [
        EventType.EVALUATION_STARTED,
        EventType.ATTACK_STARTED,
        EventType.TOOL_REQUESTED,
        EventType.TOOL_EXECUTED,
    ]
@pytest.mark.asyncio
async def test_blocked_evaluation_persists_final_state(engine: AsyncEngine) -> None:
    session_factory = create_session_factory(engine)

    async with session_factory() as session:
        store = PostgresEvaluationStore(session)

        evaluation = Evaluation(
            attack_id="TEST-BLOCKED",
            attack_category="tool_abuse",
            target="mock-target",
        )

        await store.save(evaluation)

        evaluation.status = EvaluationStatus.FAILURE
        evaluation.score = 0.0
        evaluation.completed_at = datetime.now(UTC)

        await store.save(evaluation)

    async with session_factory() as session:
        store = PostgresEvaluationStore(session)

        persisted = await store.get(evaluation.evaluation_id)

        assert persisted is not None
        assert persisted.evaluation_id == evaluation.evaluation_id
        assert persisted.attack_id == "TEST-BLOCKED"
        assert persisted.attack_category == "tool_abuse"
        assert persisted.target == "mock-target"
        assert persisted.status == EvaluationStatus.FAILURE
        assert persisted.score == 0.0
        assert persisted.completed_at is not None

    await engine.dispose()