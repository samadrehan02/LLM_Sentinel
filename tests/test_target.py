import pytest

from sentinel.models.mock import MockModelRuntime
from target.agent.mock import MockTarget


@pytest.mark.asyncio
async def test_mock_target():
    target = MockTarget()
    model = MockModelRuntime(response="Target received request")

    response = await target.interact(
        messages=[
            {"role": "user", "content": "Hello"},
        ],
        model_runtime=model,
    )

    assert target.target_id == "mock-target"
    assert response == "Target received request"
