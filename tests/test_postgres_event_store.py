import pytest
from uuid import uuid4

from sentinel.infrastructure.event_model import EventRecord
from sentinel.infrastructure.postgres_event_store import PostgresEventStore
from sentinel.instrumentation.events import Event, EventType


def create_event() -> Event:
    return Event(
        evaluation_id=uuid4(),
        run_id=uuid4(),
        trace_id=uuid4(),
        event_type=EventType.ATTACK_STARTED,
        component="evaluation_runner",
        payload={
            "attack_id": "PI-001",
        },
    )


class FakeSession:
    def __init__(self) -> None:
        self.added = []
        self.committed = False

    def add(self, record) -> None:
        self.added.append(record)

    async def commit(self) -> None:
        self.committed = True

    async def execute(self, statement):
        raise NotImplementedError


@pytest.mark.asyncio
async def test_postgres_event_store_saves_event():
    session = FakeSession()
    store = PostgresEventStore(session=session)

    event = create_event()

    await store.save(event)

    assert len(session.added) == 1
    assert session.added[0].event_id == event.event_id
    assert session.added[0].evaluation_id == event.evaluation_id
    assert session.added[0].event_type == "attack.started"
    assert session.committed is True


def test_event_record_can_be_created_for_postgres_store():
    event = create_event()

    record = EventRecord.from_event(event)

    assert record.event_id == event.event_id
    assert record.evaluation_id == event.evaluation_id
    assert record.run_id == event.run_id
    assert record.trace_id == event.trace_id
    assert record.event_type == event.event_type.value
    assert record.component == event.component
    assert record.payload == event.payload


def test_postgres_event_store_is_event_store():
    from sentinel.instrumentation.store import EventStore

    session = FakeSession()
    store = PostgresEventStore(session=session)

    assert isinstance(store, EventStore)