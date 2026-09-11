from sentinel.attacks.defaults import create_default_registry


def test_default_registry_lists_attacks():
    registry = create_default_registry()

    attacks = registry.list()

    assert len(attacks) == 3
    assert {attack.attack_id for attack in attacks} == {
        "PI-000",
        "PI-001",
        "PI-002",
    }


def test_default_registry_returns_attack_by_id():
    registry = create_default_registry()

    attack = registry.get("PI-001")

    assert attack.attack_id == "PI-001"
    assert attack.category == "prompt_injection"
    
def test_default_registry_exposes_adaptive_attack_metadata():
    registry = create_default_registry()

    metadata = registry.metadata("PI-002")

    assert metadata == {
        "attack_id": "PI-002",
        "name": "Adaptive Prompt Injection",
        "description": (
            "A multi-step prompt injection attack that escalates "
            "based on the target's previous response."
        ),
        "category": "prompt_injection",
        "severity": "critical",
    }