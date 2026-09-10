import json
from uuid import uuid4

import pytest

from sentinel.defenses.basic_policy import BasicToolPolicy
from sentinel.instrumentation.event_bus import EventBus
from sentinel.instrumentation.events import EventType
from sentinel.models.mock import MockModelRuntime
from target.agent.agent import EnterpriseAgent
from target.agent.tool_gateway import ToolGateway
from target.agent.tools import CustomerLookupTool


@pytest.mark.asyncio
async def test_enterprise_agent_executes_model_tool_request():
    event_bus = EventBus()
    events = []

    event_bus.subscribe(
        EventType.TOOL_REQUESTED,
        events.append,
    )
    event_bus.subscribe(
        EventType.AUTHORIZATION_DECISION,
        events.append,
    )
    event_bus.subscribe(
        EventType.TOOL_EXECUTED,
        events.append,
    )

    model = MockModelRuntime(
        response=json.dumps(
            {
                "type": "tool_call",
                "tool_name": "customer_lookup",
                "arguments": {
                    "customer_id": "CUST-001",
                },
            }
        ),
    )

    gateway = ToolGateway(
        tools={
            "customer_lookup": CustomerLookupTool(),
        },
        policy=BasicToolPolicy(
            allowed_tools={"customer_lookup"},
        ),
        event_bus=event_bus,
        evaluation_id=uuid4(),
    )

    agent = EnterpriseAgent(
        tool_gateway=gateway,
    )

    response = await agent.interact(
        messages=[
            {
                "role": "user",
                "content": "Look up customer CUST-001.",
            }
        ],
        model_runtime=model,
    )

    result = json.loads(response)

    assert result["customer_id"] == "CUST-001"
    assert result["name"] == "Alice Johnson"

    assert len(events) == 3
    assert events[0].event_type == EventType.TOOL_REQUESTED
    assert events[1].event_type == EventType.AUTHORIZATION_DECISION
    assert events[2].event_type == EventType.TOOL_EXECUTED
