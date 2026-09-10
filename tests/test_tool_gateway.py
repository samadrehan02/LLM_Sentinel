import pytest
from uuid import uuid4

from sentinel.defenses.basic_policy import BasicToolPolicy
from sentinel.instrumentation.event_bus import EventBus
from sentinel.instrumentation.events import EventType
from target.agent.tool_gateway import ToolGateway
from target.agent.tools import CustomerLookupTool


@pytest.mark.asyncio
async def test_tool_gateway_executes_allowed_tool():
    event_bus = EventBus()
    events = []

    for event_type in (
        EventType.TOOL_REQUESTED,
        EventType.AUTHORIZATION_DECISION,
        EventType.TOOL_EXECUTED,
    ):
        event_bus.subscribe(event_type, events.append)

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

    result = await gateway.execute(
        tool_name="customer_lookup",
        arguments={
            "customer_id": "CUST-001",
        },
    )

    assert result["customer_id"] == "CUST-001"

    assert len(events) == 3
    assert events[0].event_type == EventType.TOOL_REQUESTED
    assert events[1].event_type == EventType.AUTHORIZATION_DECISION
    assert events[2].event_type == EventType.TOOL_EXECUTED

    assert events[1].payload["decision"] == "allow"


@pytest.mark.asyncio
async def test_tool_gateway_denies_disallowed_tool():
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

    gateway = ToolGateway(
        tools={
            "customer_lookup": CustomerLookupTool(),
        },
        policy=BasicToolPolicy(
            allowed_tools=set(),
        ),
        event_bus=event_bus,
        evaluation_id=uuid4(),
    )

    with pytest.raises(PermissionError):
        await gateway.execute(
            tool_name="customer_lookup",
            arguments={
                "customer_id": "CUST-001",
            },
        )

    assert len(events) == 2
    assert events[0].event_type == EventType.TOOL_REQUESTED
    assert events[1].event_type == EventType.AUTHORIZATION_DECISION
    assert events[1].payload["decision"] == "deny"
