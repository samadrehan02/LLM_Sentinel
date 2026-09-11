from sentinel.attacks.outcome import AttackOutcome


def test_attack_outcome_defaults() -> None:
    outcome = AttackOutcome(
        success=False,
        objective="sensitive_data_disclosure",
    )

    assert outcome.success is False
    assert outcome.objective == "sensitive_data_disclosure"
    assert outcome.evidence == []
    assert outcome.metadata == {}


def test_attack_outcome_preserves_evidence_and_metadata() -> None:
    outcome = AttackOutcome(
        success=True,
        objective="sensitive_data_disclosure",
        evidence=[
            "Synthetic customer record appeared in response.",
        ],
        metadata={
            "customer_id": "CUST-001",
        },
    )

    assert outcome.success is True
    assert outcome.objective == "sensitive_data_disclosure"
    assert outcome.evidence == [
        "Synthetic customer record appeared in response.",
    ]
    assert outcome.metadata == {
        "customer_id": "CUST-001",
    }