from uuid import uuid4

import pytest

from sentinel.instrumentation.event_bus import EventBus
from sentinel.instrumentation.events import EventType
from sentinel.models.instrumented import InstrumentedModelRuntime
from sentinel.models.mock import MockModelRuntime


@pytest.mark.asyncio
async def test_instrumented_model_runtime():
    event_bus = EventBus()
    events = []

    def capture_event(event):
        events.append(event)

    event_bus.subscribe(EventType.AGENT_REQUEST, capture_event)
    event_bus.subscribe(EventType.LLM_GENERATION, capture_event)

    runtime = InstrumentedModelRuntime(
        runtime=MockModelRuntime(
            response="Mock response",
        ),
        event_bus=event_bus,
        evaluation_id=uuid4(),
        run_id=uuid4(),
        trace_id=uuid4(),
    )

    messages = [
        {
            "role": "user",
            "content": "Hello",
        }
    ]

    response = await runtime.generate(messages=messages)

    assert response == "Mock response"
    assert len(events) == 2

    assert events[0].event_type == EventType.AGENT_REQUEST
    assert events[0].payload["messages"] == messages

    assert events[1].event_type == EventType.LLM_GENERATION
    assert events[1].payload["response"] == "Mock response"
