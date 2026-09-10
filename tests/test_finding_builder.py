from uuid import uuid4

from sentinel.evaluators.result import EvaluationResult, EvaluationStatus
from sentinel.scoring.finding import Severity
from sentinel.scoring.finding_builder import build_finding


def test_build_finding_from_successful_evaluation():
    evaluation_id = uuid4()

    result = EvaluationResult(
        status=EvaluationStatus.SUCCESS,
        score=1.0,
        evidence=[
            "Synthetic API key was exposed.",
        ],
        metadata={
            "exposed_markers": [
                "SYNTHETIC-KEY-001-NOT-REAL",
            ],
        },
    )

    finding = build_finding(
        evaluation_id=evaluation_id,
        attack_id="PI-001",
        result=result,
    )

    assert finding is not None
    assert finding.evaluation_id == evaluation_id
    assert finding.attack_id == "PI-001"
    assert finding.severity == Severity.CRITICAL
    assert finding.score == 1.0
    assert finding.evidence == result.evidence
    assert finding.metadata == result.metadata


def test_no_finding_for_failed_evaluation():
    result = EvaluationResult(
        status=EvaluationStatus.FAILURE,
        score=0.0,
        evidence=[
            "No sensitive data exposed.",
        ],
        metadata={},
    )

    finding = build_finding(
        evaluation_id=uuid4(),
        attack_id="PI-001",
        result=result,
    )

    assert finding is None
