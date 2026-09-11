from uuid import uuid4

from sentinel.instrumentation.event_bus import EventBus
from sentinel.instrumentation.events import Event, EventType
from sentinel.instrumentation.store import InMemoryEventStore


def create_event() -> Event:
    return Event(
        evaluation_id=uuid4(),
        run_id=uuid4(),
        trace_id=uuid4(),
        event_type=EventType.ATTACK_STARTED,
        component="test",
        payload={"attack_id": "PI-001"},
    )


def test_event_bus_persists_events():
    store = InMemoryEventStore()
    event_bus = EventBus(event_store=store)

    event = create_event()

    event_bus.publish(event)

    stored_events = store.get_by_evaluation(
        event.evaluation_id,
    )

    assert len(stored_events) == 1
    assert stored_events[0] == event


def test_event_bus_notifies_subscribers_and_persists():
    store = InMemoryEventStore()
    event_bus = EventBus(event_store=store)

    received = []

    def handler(event):
        received.append(event)

    event_bus.subscribe(
        EventType.ATTACK_STARTED,
        handler,
    )

    event = create_event()

    event_bus.publish(event)

    assert received == [event]

    stored_events = store.get_by_evaluation(
        event.evaluation_id,
    )

    assert stored_events == [event]


def test_event_bus_without_store_still_works():
    event_bus = EventBus()

    received = []

    event_bus.subscribe(
        EventType.ATTACK_STARTED,
        received.append,
    )

    event = create_event()

    event_bus.publish(event)

    assert received == [event]