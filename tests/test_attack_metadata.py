from sentinel.attacks.prompt_injection.benign import BenignPromptAttack
from sentinel.attacks.prompt_injection.direct import DirectPromptInjectionAttack


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
