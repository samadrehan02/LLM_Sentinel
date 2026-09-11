from typing import Any
from uuid import UUID, uuid4

import pytest

from sentinel.attacks.base import Attack
from sentinel.attacks.prompt_injection.benign import BenignPromptAttack
from sentinel.attacks.prompt_injection.direct import DirectPromptInjectionAttack


class DummyAttack(Attack):
    attack_id = "TEST-001"
    name = "Dummy Attack"
    description = "Test attack implementation"

    async def execute(
        self,
        target: Any,
        evaluation_id: UUID,
        run_id: UUID,
        model_runtime: Any,
    ) -> str:
        return "attack executed"


@pytest.mark.asyncio
async def test_attack_interface():
    attack = DummyAttack()

    result = await attack.execute(
        target=None,
        evaluation_id=uuid4(),
        run_id=uuid4(),
        model_runtime=None,
    )

    assert attack.attack_id == "TEST-001"
    assert attack.name == "Dummy Attack"
    assert result == "attack executed"

    def test_direct_prompt_injection_metadata():
        attack = DirectPromptInjectionAttack()

        assert attack.attack_id == "PI-001"
        assert attack.category == "prompt_injection"
        assert attack.severity == "critical"

    def test_benign_prompt_metadata():
        attack = BenignPromptAttack()

        assert attack.attack_id == "PI-000"
        assert attack.category == "benign"
        assert attack.severity == "none"
