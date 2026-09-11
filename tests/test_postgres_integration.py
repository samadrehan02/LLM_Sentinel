from uuid import uuid4

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
async def engine() -> AsyncEngine:
    settings = DatabaseSettings()
    engine = create_engine(settings.database_url)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.mark.asyncio
async def test_postgres_event_store_round_trip(
    engine: AsyncEngine,
) -> None:
    session_factory = create_session_factory(engine)

    evaluation_id = uuid4()
    run_id = uuid4()
    trace_id = uuid4()

    event = Event(
        evaluation_id=evaluation_id,
        run_id=run_id,
        trace_id=trace_id,
        event_type=EventType.TOOL_EXECUTED,
        component="integration_test",
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
            evaluation_id,
        )

    assert len(events) == 1

    persisted = events[0]

    assert persisted.event_id == event.event_id
    assert persisted.evaluation_id == event.evaluation_id
    assert persisted.run_id == event.run_id
    assert persisted.trace_id == event.trace_id
    assert persisted.event_type == EventType.TOOL_EXECUTED
    assert persisted.component == "integration_test"
    assert persisted.payload == event.payload
    assert persisted.schema_version == "1.0"