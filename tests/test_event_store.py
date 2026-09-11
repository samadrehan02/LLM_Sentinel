from uuid import uuid4

from sentinel.instrumentation.events import Event, EventType
from sentinel.instrumentation.store import InMemoryEventStore


def create_event(evaluation_id):
    return Event(
        evaluation_id=evaluation_id,
        run_id=uuid4(),
        trace_id=uuid4(),
        event_type=EventType.ATTACK_STARTED,
        component="test",
        payload={"attack_id": "PI-001"},
    )


def test_event_store_saves_event():
    store = InMemoryEventStore()
    evaluation_id = uuid4()

    event = create_event(evaluation_id)

    store.save(event)

    events = store.get_by_evaluation(evaluation_id)

    assert len(events) == 1
    assert events[0] == event


def test_event_store_filters_by_evaluation():
    store = InMemoryEventStore()

    evaluation_a = uuid4()
    evaluation_b = uuid4()

    event_a = create_event(evaluation_a)
    event_b = create_event(evaluation_b)

    store.save(event_a)
    store.save(event_b)

    events = store.get_by_evaluation(evaluation_a)

    assert len(events) == 1
    assert events[0].evaluation_id == evaluation_a


def test_event_store_returns_empty_for_unknown_evaluation():
    store = InMemoryEventStore()

    events = store.get_by_evaluation(uuid4())

    assert events == []