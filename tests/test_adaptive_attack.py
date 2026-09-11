from uuid import uuid4

import pytest

from sentinel.attacks.adaptive import AdaptiveAttack
from sentinel.attacks.observation import AttackObservation
from sentinel.attacks.state import AttackState


class DummyAdaptiveAttack(AdaptiveAttack):
    attack_id = "TEST-ADAPTIVE-001"
    name = "Dummy Adaptive Attack"
    description = "Adaptive attack used to test the interface."
    category = "test"
    severity = "low"

    async def execute(
        self,
        target,
        evaluation_id,
        run_id,
        model_runtime,
    ):
        state = AttackState()

        action = await self.choose_next_action(
            state=state,
            model_runtime=model_runtime,
        )

        if action is None:
            return False

        observation = await self.execute_action(
            action=action,
            state=state,
            target=target,
            model_runtime=model_runtime,
        )

        state.add_observation(observation)

        return True

    async def choose_next_action(
        self,
        state,
        model_runtime,
    ):
        if state.step_count == 0:
            return "initial_prompt"

        return None

    async def execute_action(
        self,
        action,
        state,
        target,
        model_runtime,
    ):
        return AttackObservation(
            evaluation_id=uuid4(),
            run_id=uuid4(),
            step=state.step_count + 1,
            action=action,
            response="Mock response",
        )


@pytest.mark.asyncio
async def test_adaptive_attack_selects_initial_action():
    attack = DummyAdaptiveAttack()
    state = AttackState()

    action = await attack.choose_next_action(
        state=state,
        model_runtime=None,
    )

    assert action == "initial_prompt"


@pytest.mark.asyncio
async def test_adaptive_attack_stops_when_no_action_available():
    attack = DummyAdaptiveAttack()
    state = AttackState()

    observation = AttackObservation(
        evaluation_id=uuid4(),
        run_id=uuid4(),
        step=1,
        action="initial_prompt",
        response="Mock response",
    )

    state.add_observation(observation)

    action = await attack.choose_next_action(
        state=state,
        model_runtime=None,
    )

    assert action is None


@pytest.mark.asyncio
async def test_adaptive_attack_executes_action():
    attack = DummyAdaptiveAttack()
    state = AttackState()

    observation = await attack.execute_action(
        action="initial_prompt",
        state=state,
        target=None,
        model_runtime=None,
    )

    assert observation.step == 1
    assert observation.action == "initial_prompt"
    assert observation.response == "Mock response"


@pytest.mark.asyncio
async def test_adaptive_attack_integrates_with_state():
    attack = DummyAdaptiveAttack()
    state = AttackState()

    action = await attack.choose_next_action(
        state=state,
        model_runtime=None,
    )

    observation = await attack.execute_action(
        action=action,
        state=state,
        target=None,
        model_runtime=None,
    )

    state.add_observation(observation)

    assert state.step_count == 1
    assert state.latest() is observation