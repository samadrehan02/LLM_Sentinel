import json
from uuid import uuid4

import pytest

from sentinel.attacks.prompt_injection.direct import (
    DirectPromptInjectionAttack,
)
from sentinel.defenses.basic_policy import BasicToolPolicy
from sentinel.instrumentation.event_bus import EventBus
from sentinel.instrumentation.events import EventType
from sentinel.models.mock import MockModelRuntime
from target.agent.agent import EnterpriseAgent
from target.agent.tool_gateway import ToolGateway
from target.agent.tools import CustomerLookupTool


@pytest.mark.asyncio
async def test_prompt_injection_tool_chain_is_traced():
    event_bus = EventBus()
    events = []

    for event_type in (
        EventType.TOOL_REQUESTED,
        EventType.AUTHORIZATION_DECISION,
        EventType.TOOL_EXECUTED,
    ):
        event_bus.subscribe(
            event_type,
            events.append,
        )

    evaluation_id = uuid4()

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
        evaluation_id=evaluation_id,
    )

    agent = EnterpriseAgent(
        tool_gateway=gateway,
    )

    attack = DirectPromptInjectionAttack()

    result = await attack.execute(
        target=agent,
        evaluation_id=evaluation_id,
        run_id=uuid4(),
        model_runtime=model,
    )

    assert result["attack_id"] == "PI-001"

    assert len(events) == 3

    assert events[0].event_type == EventType.TOOL_REQUESTED
    assert events[1].event_type == EventType.AUTHORIZATION_DECISION
    assert events[2].event_type == EventType.TOOL_EXECUTED

    for event in events:
        assert event.evaluation_id == evaluation_id
        assert event.run_id == events[0].run_id
        assert event.trace_id == events[0].trace_id

    assert events[0].payload["tool_name"] == "customer_lookup"
    assert events[0].payload["arguments"]["customer_id"] == "CUST-001"

    assert events[1].payload["decision"] == "allow"

    assert events[2].payload["result"]["api_key"] == "SYNTHETIC-KEY-001-NOT-REAL"
