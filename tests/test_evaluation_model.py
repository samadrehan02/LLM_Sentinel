from uuid import uuid4

from sentinel.models.evaluation import (
    Evaluation,
    EvaluationStatus,
)


def test_evaluation_defaults_to_running() -> None:
    evaluation = Evaluation(
        attack_id="PI-001",
        attack_category="prompt_injection",
        target="enterprise-assistant",
    )

    assert evaluation.status == EvaluationStatus.RUNNING
    assert evaluation.score is None
    assert evaluation.completed_at is None


def test_evaluation_generates_id() -> None:
    evaluation = Evaluation(
        attack_id="PI-001",
        attack_category="prompt_injection",
        target="enterprise-assistant",
    )

    assert evaluation.evaluation_id is not None


def test_evaluation_accepts_campaign_id() -> None:
    campaign_id = uuid4()

    evaluation = Evaluation(
        campaign_id=campaign_id,
        attack_id="PI-001",
        attack_category="prompt_injection",
        target="enterprise-assistant",
    )

    assert evaluation.campaign_id == campaign_id


def test_evaluation_can_be_completed() -> None:
    evaluation = Evaluation(
        attack_id="PI-001",
        attack_category="prompt_injection",
        target="enterprise-assistant",
        status=EvaluationStatus.SUCCESS,
        score=1.0,
    )

    assert evaluation.status == EvaluationStatus.SUCCESS
    assert evaluation.score == 1.0