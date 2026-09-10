from sentinel.attacks.prompt_injection.benign import BenignPromptAttack
from sentinel.attacks.prompt_injection.direct import DirectPromptInjectionAttack
from sentinel.attacks.registry import AttackRegistry


def create_default_registry() -> AttackRegistry:
    registry = AttackRegistry()

    registry.register(
        BenignPromptAttack(),
    )

    registry.register(
        DirectPromptInjectionAttack(),
    )

    return registry
