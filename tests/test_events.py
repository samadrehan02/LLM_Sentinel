from uuid import uuid4

from sentinel.instrumentation.events import Event, EventType


def test_event_creation():
    event = Event(
        evaluation_id=uuid4(),
        run_id=uuid4(),
        trace_id=uuid4(),
        event_type=EventType.ATTACK_STARTED,
        component="attack_orchestrator",
        payload={"attack_id": "A01"},
    )

    assert event.event_type == EventType.ATTACK_STARTED
    assert event.component == "attack_orchestrator"
    assert event.payload["attack_id"] == "A01"
