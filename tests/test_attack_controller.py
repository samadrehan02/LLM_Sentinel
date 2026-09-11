import pytest
from uuid import uuid4

from sentinel.attacks.adaptive import AdaptiveAttack
from sentinel.attacks.controller import AdaptiveAttackController
from sentinel.attacks.observation import AttackObservation
from sentinel.attacks.state import AttackState


class ControllerTestAttack(AdaptiveAttack):
    attack_id = "TEST-ADAPTIVE"
    name = "Controller Test Attack"
    description = "Attack used to test the adaptive controller."
    category = "test"
    severity = "low"

    async def execute(
        self,
        target,
        evaluation_id,
        run_id,
        model_runtime,
    ):
        raise NotImplementedError(
            "ControllerTestAttack is only used to test the controller."
        )

    async def choose_next_action(
        self,
        state: AttackState,
        model_runtime,
    ) -> str | None:
        if state.step_count >= 2:
            return None

        return f"action-{state.step_count + 1}"

    async def execute_action(
        self,
        action: str,
        state: AttackState,
        target,
        model_runtime,
        evaluation_id,
        run_id,
    ) -> AttackObservation:
        return AttackObservation(
            evaluation_id=evaluation_id,
            run_id=run_id,
            step=state.step_count + 1,
            action=action,
            response=f"response-{state.step_count + 1}",
        )


@pytest.mark.asyncio
async def test_controller_runs_until_attack_stops() -> None:
    attack = ControllerTestAttack()
    controller = AdaptiveAttackController(attack)

    evaluation_id = uuid4()
    run_id = uuid4()

    state = await controller.run(
        target=None,
        model_runtime=None,
        evaluation_id=evaluation_id,
        run_id=run_id,
    )

    assert state.step_count == 2
    assert state.get_actions() == [
        "action-1",
        "action-2",
    ]
    assert state.get_response_history() == [
        "response-1",
        "response-2",
    ]

    assert all(
        observation.evaluation_id == evaluation_id
        for observation in state.observations
    )
    assert all(
        observation.run_id == run_id
        for observation in state.observations
    )


@pytest.mark.asyncio
async def test_controller_respects_max_steps() -> None:
    attack = ControllerTestAttack()
    controller = AdaptiveAttackController(
        attack,
        max_steps=2,
    )

    evaluation_id = uuid4()
    run_id = uuid4()

    state = await controller.run(
        target=None,
        model_runtime=None,
        evaluation_id=evaluation_id,
        run_id=run_id,
    )

    assert state.step_count == 2


@pytest.mark.asyncio
async def test_controller_rejects_invalid_max_steps() -> None:
    attack = ControllerTestAttack()

    with pytest.raises(ValueError, match="max_steps must be at least 1"):
        AdaptiveAttackController(
            attack,
            max_steps=0,
        )