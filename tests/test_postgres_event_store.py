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


def test_postgres_event_store_requires_async_save():
    store = PostgresEventStore(session=None)

    event = create_event()

    try:
        store.save(event)
    except NotImplementedError as exc:
        assert "save_async" in str(exc)
    else:
        raise AssertionError(
            "PostgresEventStore.save() should require async persistence."
        )


def test_postgres_event_store_requires_async_retrieval():
    store = PostgresEventStore(session=None)

    evaluation_id = uuid4()

    try:
        store.get_by_evaluation(evaluation_id)
    except NotImplementedError as exc:
        assert "get_by_evaluation_async" in str(exc)
    else:
        raise AssertionError(
            "PostgresEventStore.get_by_evaluation() should require "
            "async retrieval."
        )