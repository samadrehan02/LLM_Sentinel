from uuid import uuid4

from sentinel.attacks.observation import AttackObservation
from sentinel.attacks.state import AttackState


def create_observation(
    step: int,
    action: str,
    response: str,
) -> AttackObservation:
    return AttackObservation(
        evaluation_id=uuid4(),
        run_id=uuid4(),
        step=step,
        action=action,
        response=response,
    )


def test_attack_state_starts_empty() -> None:
    state = AttackState()

    assert state.observations == []
    assert state.latest() is None
    assert state.get_response_history() == []
    assert state.get_actions() == []
    assert state.step_count == 0


def test_attack_state_adds_observations() -> None:
    state = AttackState()

    first = create_observation(
        step=1,
        action="prompt",
        response="I cannot help with that.",
    )

    second = create_observation(
        step=2,
        action="follow_up_prompt",
        response="I can provide general information.",
    )

    state.add_observation(first)
    state.add_observation(second)

    assert state.observations == [first, second]
    assert state.latest() is second
    assert state.step_count == 2


def test_attack_state_tracks_response_history() -> None:
    state = AttackState()

    state.add_observation(
        create_observation(
            step=1,
            action="prompt",
            response="First response",
        )
    )

    state.add_observation(
        create_observation(
            step=2,
            action="follow_up",
            response="Second response",
        )
    )

    assert state.get_response_history() == [
        "First response",
        "Second response",
    ]


def test_attack_state_tracks_action_history() -> None:
    state = AttackState()

    state.add_observation(
        create_observation(
            step=1,
            action="prompt",
            response="Response",
        )
    )

    state.add_observation(
        create_observation(
            step=2,
            action="tool_request",
            response="Denied",
        )
    )

    assert state.get_actions() == [
        "prompt",
        "tool_request",
    ]