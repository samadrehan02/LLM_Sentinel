import pytest

from sentinel.attacks.prompt_injection.benign import BenignPromptAttack
from sentinel.models.mock import MockModelRuntime
from target.agent.agent import EnterpriseAgent


@pytest.mark.asyncio
async def test_benign_prompt_attack():
    attack = BenignPromptAttack()

    model = MockModelRuntime(
        response="The company provides enterprise software services.",
    )

    result = await attack.execute(
        target=EnterpriseAgent(),
        evaluation_id=None,
        run_id=None,
        model_runtime=model,
    )

    assert result["attack_id"] == "PI-000"
    assert "company provide" in result["prompt"]
    assert "enterprise software services" in result["response"]
