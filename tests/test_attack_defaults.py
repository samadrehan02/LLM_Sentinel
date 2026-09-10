from sentinel.attacks.defaults import create_default_registry


def test_default_registry_contains_direct_prompt_injection():
    registry = create_default_registry()

    attack = registry.get("PI-001")

    assert attack.attack_id == "PI-001"
    assert attack.name == "Direct Prompt Injection"


def test_default_registry_lists_attacks():
    registry = create_default_registry()

    attacks = registry.list()

    assert len(attacks) == 2
    assert attacks[0].attack_id == "PI-000"
    assert attacks[1].attack_id == "PI-001"
