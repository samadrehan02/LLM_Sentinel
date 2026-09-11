from uuid import UUID

from sentinel.attacks.adaptive import AdaptiveAttack
from sentinel.attacks.observation import AttackObservation
from sentinel.attacks.state import AttackState


class AdaptiveAttackController:
    def __init__(
        self,
        attack: AdaptiveAttack,
        max_steps: int = 10,
    ) -> None:
        if max_steps < 1:
            raise ValueError("max_steps must be at least 1")

        self.attack = attack
        self.max_steps = max_steps

    async def run(
        self,
        target,
        model_runtime,
        evaluation_id: UUID,
        run_id: UUID,
    ) -> AttackState:
        state = AttackState()

        for _ in range(self.max_steps):
            action = await self.attack.choose_next_action(
                state=state,
                model_runtime=model_runtime,
            )

            if action is None:
                break

            observation = await self.attack.execute_action(
                action=action,
                state=state,
                target=target,
                model_runtime=model_runtime,
                evaluation_id=evaluation_id,
                run_id=run_id,
            )

            state.add_observation(observation)

        return state