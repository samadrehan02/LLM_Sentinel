from sentinel.attacks.prompt_injection.adaptive import AdaptivePromptInjectionAttack
from sentinel.attacks.prompt_injection.benign import BenignPromptAttack
from sentinel.attacks.prompt_injection.direct import DirectPromptInjectionAttack
from sentinel.attacks.registry import AttackRegistry


def create_default_registry() -> AttackRegistry:
    registry = AttackRegistry()

    registry.register(BenignPromptAttack())
    registry.register(DirectPromptInjectionAttack())
    registry.register(AdaptivePromptInjectionAttack())

    return registry