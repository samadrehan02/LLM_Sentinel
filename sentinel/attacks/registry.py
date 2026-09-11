from typing import Any

from sentinel.attacks.base import Attack


class AttackRegistry:
    def __init__(self) -> None:
        self._attacks: dict[str, Attack] = {}

    def register(self, attack: Attack) -> None:
        if attack.attack_id in self._attacks:
            raise ValueError(f"Attack already registered: {attack.attack_id}")

        self._attacks[attack.attack_id] = attack

    def get(self, attack_id: str) -> Attack:
        try:
            return self._attacks[attack_id]
        except KeyError as exc:
            raise KeyError(f"Unknown attack: {attack_id}") from exc

    def list(self) -> list[Attack]:
        return list(self._attacks.values())

    def metadata(self, attack_id: str) -> dict[str, Any]:
        attack = self.get(attack_id)

        return {
            "attack_id": attack.attack_id,
            "name": attack.name,
            "description": attack.description,
            "category": attack.category,
            "severity": attack.severity,
        }
