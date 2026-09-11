from uuid import uuid4

from sentinel.infrastructure.finding_model import FindingRecord
from sentinel.scoring.finding import Finding, Severity


def create_finding() -> Finding:
    return Finding(
        finding_id=uuid4(),
        evaluation_id=uuid4(),
        attack_id="PI-001",
        title="Sensitive Data Exposure",
        description="Synthetic customer data was exposed.",
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


def test_finding_record_from_finding() -> None:
    finding = create_finding()

    record = FindingRecord.from_finding(finding)

    assert record.finding_id == finding.finding_id
    assert record.evaluation_id == finding.evaluation_id
    assert record.attack_id == finding.attack_id
    assert record.title == finding.title
    assert record.description == finding.description
    assert record.severity == finding.severity.value
    assert record.score == finding.score
    assert record.evidence == finding.evidence
    assert record.metadata_ == finding.metadata


def test_finding_record_table_name() -> None:
    assert FindingRecord.__tablename__ == "findings"


def test_finding_record_primary_key() -> None:
    primary_keys = FindingRecord.__table__.primary_key.columns

    assert list(primary_keys)[0].name == "finding_id"