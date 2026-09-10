from pydantic import BaseModel


class DefenseScore(BaseModel):
    attack_success_without_defense: float
    attack_success_with_defense: float
    defense_effectiveness: float


def calculate_defense_effectiveness(
    attack_success_without_defense: float,
    attack_success_with_defense: float,
) -> DefenseScore:
    effectiveness = (
        attack_success_without_defense
        - attack_success_with_defense
    )

    return DefenseScore(
        attack_success_without_defense=attack_success_without_defense,
        attack_success_with_defense=attack_success_with_defense,
        defense_effectiveness=effectiveness,
    )