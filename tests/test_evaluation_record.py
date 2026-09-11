from datetime import UTC, datetime
from uuid import uuid4

from sentinel.infrastructure.evaluation_model import EvaluationRecord
from sentinel.models.evaluation import (
    Evaluation,
    EvaluationStatus,
)


def test_evaluation_record_table_name() -> None:
    assert EvaluationRecord.__tablename__ == "evaluations"


def test_evaluation_record_from_domain_model() -> None:
    evaluation_id = uuid4()
    campaign_id = uuid4()
    started_at = datetime.now(UTC)
    completed_at = datetime.now(UTC)

    evaluation = Evaluation(
        evaluation_id=evaluation_id,
        campaign_id=campaign_id,
        attack_id="PI-001",
        attack_category="prompt_injection",
        target="enterprise-assistant",
        status=EvaluationStatus.SUCCESS,
        score=1.0,
        started_at=started_at,
        completed_at=completed_at,
    )

    record = EvaluationRecord.from_evaluation(
        evaluation,
    )

    assert record.evaluation_id == evaluation_id
    assert record.campaign_id == campaign_id
    assert record.attack_id == "PI-001"
    assert record.attack_category == "prompt_injection"
    assert record.target == "enterprise-assistant"
    assert record.status == "success"
    assert record.score == 1.0
    assert record.started_at == started_at
    assert record.completed_at == completed_at


def test_evaluation_record_supports_running_evaluation() -> None:
    evaluation = Evaluation(
        attack_id="PI-001",
        attack_category="prompt_injection",
        target="enterprise-assistant",
    )

    record = EvaluationRecord.from_evaluation(
        evaluation,
    )

    assert record.status == "running"
    assert record.score is None
    assert record.completed_at is None