from uuid import uuid4

from sentinel.instrumentation.event_bus import EventBus
from sentinel.instrumentation.events import Event, EventType


def test_event_bus_publishes_to_subscriber():
    bus = EventBus()
    received: list[Event] = []

    def handler(event: Event) -> None:
        received.append(event)

    bus.subscribe(EventType.ATTACK_STARTED, handler)

    event = Event(
        evaluation_id=uuid4(),
        run_id=uuid4(),
        trace_id=uuid4(),
        event_type=EventType.ATTACK_STARTED,
        component="test",
        payload={"attack_id": "A01"},
    )

    bus.publish(event)

    assert len(received) == 1
    assert received[0] == event
