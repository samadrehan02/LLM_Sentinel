from uuid import uuid4

from sentinel.scoring.finding import Finding, Severity


def test_finding():
    evaluation_id = uuid4()

    finding = Finding(
        evaluation_id=evaluation_id,
        attack_id="PI-001",
        title="Sensitive Data Exposure",
        description=("A prompt injection caused the agent to retrieve protected customer data."),
        severity=Severity.CRITICAL,
        score=1.0,
        evidence=[
            "Customer CUST-001 was accessed.",
            "Synthetic API key was exposed.",
        ],
        metadata={
            "tool": "customer_lookup",
        },
    )

    assert finding.evaluation_id == evaluation_id
    assert finding.attack_id == "PI-001"
    assert finding.severity == Severity.CRITICAL
    assert finding.score == 1.0
    assert len(finding.evidence) == 2
    assert finding.metadata["tool"] == "customer_lookup"
