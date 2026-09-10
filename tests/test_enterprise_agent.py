import pytest

from sentinel.models.mock import MockModelRuntime
from target.agent.agent import EnterpriseAgent


@pytest.mark.asyncio
async def test_enterprise_agent_sends_system_prompt():
    model = MockModelRuntime(
        response="Mock response",
    )

    agent = EnterpriseAgent()

    response = await agent.interact(
        messages=[
            {
                "role": "user",
                "content": "Hello",
            }
        ],
        model_runtime=model,
    )

    assert response == "Mock response"

    assert model.last_messages is not None
    assert model.last_messages[0]["role"] == "system"
    assert "internal enterprise assistant" in model.last_messages[0]["content"]

    assert model.last_messages[1]["role"] == "user"
    assert model.last_messages[1]["content"] == "Hello"
