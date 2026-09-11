from uuid import uuid4

from sentinel.attacks.observation import AttackObservation
from sentinel.attacks.outcome import AttackOutcome
from sentinel.attacks.result import AttackResult


def test_attack_result_defaults_to_empty_observations() -> None:
    result = AttackResult(
        attack_id="PI-002",
        outcome=AttackOutcome(
            success=False,
            objective="sensitive_data_disclosure",
        ),
    )

    assert result.attack_id == "PI-002"
    assert result.success is False
    assert result.observations == []
    assert result.metadata == {}
    assert result.steps == 0


def test_attack_result_preserves_outcome_observations_and_metadata() -> None:
    evaluation_id = uuid4()
    run_id = uuid4()

    observations = [
        AttackObservation(
            evaluation_id=evaluation_id,
            run_id=run_id,
            step=1,
            action="initial_prompt",
            response="Mock target response",
        ),
        AttackObservation(
            evaluation_id=evaluation_id,
            run_id=run_id,
            step=2,
            action="escalation_prompt",
            response="Sensitive information",
        ),
    ]

    outcome = AttackOutcome(
        success=True,
        objective="sensitive_data_disclosure",
        evidence=[
            "Sensitive information appeared in the response.",
        ],
    )

    result = AttackResult(
        attack_id="PI-002",
        outcome=outcome,
        observations=observations,
        metadata={"steps": 2},
    )

    assert result.success is True
    assert result.steps == 2
    assert result.outcome == outcome
    assert result.observations == observations
    assert result.metadata == {"steps": 2}