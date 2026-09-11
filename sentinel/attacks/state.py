from typing import Any

from sentinel.attacks.observation import AttackObservation


class AttackState:
    def __init__(self) -> None:
        self.observations: list[AttackObservation] = []

    def add_observation(self, observation: AttackObservation) -> None:
        self.observations.append(observation)

    def latest(self) -> AttackObservation | None:
        if not self.observations:
            return None

        return self.observations[-1]

    def get_response_history(self) -> list[Any]:
        return [
            observation.response
            for observation in self.observations
        ]

    def get_actions(self) -> list[str]:
        return [
            observation.action
            for observation in self.observations
        ]

    @property
    def step_count(self) -> int:
        return len(self.observations)