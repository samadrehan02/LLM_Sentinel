from uuid import uuid4

import pytest

from sentinel.defenses.basic_policy import BasicToolPolicy
from sentinel.instrumentation.event_bus import EventBus
from target.agent.agent import EnterpriseAgent
from target.agent.tool_gateway import ToolGateway
from target.agent.tools import CustomerLookupTool


@pytest.mark.asyncio
async def test_enterprise_agent_can_use_tool():
    gateway = ToolGateway(
        tools={
            "customer_lookup": CustomerLookupTool(),
        },
        policy=BasicToolPolicy(
            allowed_tools={"customer_lookup"},
        ),
        event_bus=EventBus(),
        evaluation_id=uuid4(),
    )

    agent = EnterpriseAgent(
        tool_gateway=gateway,
    )

    result = await agent.use_tool(
        tool_name="customer_lookup",
        arguments={
            "customer_id": "CUST-001",
        },
    )

    assert result is not None
    assert result["customer_id"] == "CUST-001"
