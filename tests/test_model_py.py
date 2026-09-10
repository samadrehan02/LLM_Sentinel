import pytest

from sentinel.models.mock import MockModelRuntime


@pytest.mark.asyncio
async def test_mock_model_runtime():
    model = MockModelRuntime(
        response="Hello from Sentinel",
    )

    messages = [
        {
            "role": "user",
            "content": "Hello",
        }
    ]

    response = await model.generate(messages=messages)

    assert response == "Hello from Sentinel"
    assert model.last_messages == messages
