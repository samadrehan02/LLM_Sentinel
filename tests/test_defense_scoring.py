from sentinel.scoring.defense import calculate_defense_effectiveness


def test_defense_effectiveness():
    score = calculate_defense_effectiveness(
        attack_success_without_defense=1.0,
        attack_success_with_defense=0.0,
    )

    assert score.attack_success_without_defense == 1.0
    assert score.attack_success_with_defense == 0.0
    assert score.defense_effectiveness == 1.0


def test_partial_defense_effectiveness():
    score = calculate_defense_effectiveness(
        attack_success_without_defense=1.0,
        attack_success_with_defense=0.25,
    )

    assert score.defense_effectiveness == 0.75