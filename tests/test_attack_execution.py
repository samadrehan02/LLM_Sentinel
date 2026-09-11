from typing import Any
from uuid import UUID, uuid4

import pytest

from sentinel.attacks.prompt_injection.benign import BenignPromptAttack
from sentinel.attacks.prompt_injection.direct import DirectPromptInjectionAttack


class StubTarget:
    def __init__(self, response: str) -> None:
        self.response = response
        self.messages: list[dict[str, Any]] = []

    async def interact(
        self,
        messages: list[dict[str, Any]],
        model_runtime: Any,
    ) -> str:
        self.messages = messages
        return self.response


@pytest.mark.asyncio
async def test_direct_prompt_injection_execution() -> None:
    attack = DirectPromptInjectionAttack()
    target = StubTarget("Sensitive customer data")

    evaluation_id = uuid4()
    run_id = uuid4()

    result = await attack.execute(
        target=target,
        evaluation_id=evaluation_id,
        run_id=run_id,
        model_runtime=None,
    )

    assert result["attack_id"] == "PI-001"
    assert result["prompt"] == target.messages[0]["content"]
    assert result["response"] == "Sensitive customer data"
    assert len(target.messages) == 1
    assert target.messages[0]["role"] == "user"


@pytest.mark.asyncio
async def test_benign_prompt_execution() -> None:
    attack = BenignPromptAttack()
    target = StubTarget("We provide enterprise software services.")

    result = await attack.execute(
        target=target,
        evaluation_id=uuid4(),
        run_id=uuid4(),
        model_runtime=None,
    )

    assert result["attack_id"] == "PI-000"
    assert result["prompt"] == "What services does the company provide?"
    assert result["response"] == "We provide enterprise software services."
    assert len(target.messages) == 1
    assert target.messages[0]["role"] == "user"