from uuid import uuid4

from sentinel.attacks.observation import AttackObservation


def test_attack_observation_defaults() -> None:
    evaluation_id = uuid4()
    run_id = uuid4()

    observation = AttackObservation(
        evaluation_id=evaluation_id,
        run_id=run_id,
        step=1,
        action="prompt",
        response="I cannot comply.",
    )

    assert observation.observation_id is not None
    assert observation.evaluation_id == evaluation_id
    assert observation.run_id == run_id
    assert observation.step == 1
    assert observation.action == "prompt"
    assert observation.response == "I cannot comply."
    assert observation.metadata == {}
    assert observation.timestamp.tzinfo is not None


def test_attack_observation_preserves_metadata() -> None:
    observation = AttackObservation(
        evaluation_id=uuid4(),
        run_id=uuid4(),
        step=2,
        action="tool_request",
        response={"status": "denied"},
        metadata={
            "tool": "customer_lookup",
            "authorized": False,
        },
    )

    assert observation.metadata == {
        "tool": "customer_lookup",
        "authorized": False,
    }