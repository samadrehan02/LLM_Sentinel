import pytest

from sentinel.attacks.base import Attack
from sentinel.attacks.prompt_injection.direct import DirectPromptInjectionAttack
from sentinel.attacks.registry import AttackRegistry


class DummyAttack(Attack):
    attack_id = "TEST-REGISTRY-001"
    name = "Registry Test Attack"
    description = "Attack used to test the registry."

    async def execute(
        self,
        target,
        evaluation_id,
        run_id,
        model_runtime,
    ):
        return True


def test_register_and_get_attack():
    registry = AttackRegistry()
    attack = DummyAttack()

    registry.register(attack)

    result = registry.get("TEST-REGISTRY-001")

    assert result is attack


def test_list_attacks():
    registry = AttackRegistry()
    attack = DummyAttack()

    registry.register(attack)

    attacks = registry.list()

    assert len(attacks) == 1
    assert attacks[0] is attack


def test_duplicate_attack_registration():
    registry = AttackRegistry()
    attack = DummyAttack()

    registry.register(attack)

    with pytest.raises(
        ValueError,
        match="Attack already registered",
    ):
        registry.register(attack)


def test_unknown_attack():
    registry = AttackRegistry()

    with pytest.raises(
        KeyError,
        match="Unknown attack",
    ):
        registry.get("DOES-NOT-EXIST")


def test_attack_registry_metadata():
    registry = AttackRegistry()
    attack = DirectPromptInjectionAttack()

    registry.register(attack)

    metadata = registry.metadata("PI-001")

    assert metadata["attack_id"] == "PI-001"
    assert metadata["name"] == "Direct Prompt Injection"
    assert metadata["category"] == "prompt_injection"
    assert metadata["severity"] == "critical"
    assert metadata["description"] == (
        "Attempts to override the agent's instructions through user input."
    )