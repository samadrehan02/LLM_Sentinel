from uuid import uuid4

from sentinel.instrumentation.events import Event, EventType
from sentinel.infrastructure.event_model import EventRecord


def test_event_record_from_event():
    event = Event(
        evaluation_id=uuid4(),
        run_id=uuid4(),
        trace_id=uuid4(),
        event_type=EventType.ATTACK_STARTED,
        component="evaluation_runner",
        payload={
            "attack_id": "PI-001",
        },
    )

    record = EventRecord.from_event(event)

    assert record.event_id == event.event_id
    assert record.evaluation_id == event.evaluation_id
    assert record.run_id == event.run_id
    assert record.trace_id == event.trace_id
    assert record.timestamp == event.timestamp
    assert record.event_type == "attack.started"
    assert record.component == "evaluation_runner"
    assert record.payload == event.payload
    assert record.schema_version == "1.0"


def test_event_record_table_name():
    assert EventRecord.__tablename__ == "security_events"