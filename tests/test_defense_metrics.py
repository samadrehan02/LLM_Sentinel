from uuid import uuid4

from sentinel.evaluators.result import (
    EvaluationResult,
    EvaluationStatus,
    EvaluationType,
)
from sentinel.orchestrator.campaign_result import CampaignResult
from sentinel.orchestrator.result import EvaluationRunResult
from sentinel.scoring.campaign import CampaignScore
from sentinel.scoring.defense import calculate_campaign_defense_score
from sentinel.scoring.finding import Finding, Severity


def test_evaluation_type_defaults_to_attack():
    result = EvaluationResult(
        status=EvaluationStatus.SUCCESS,
        score=1.0,
        evidence=["Attack succeeded."],
        metadata={},
    )

    assert result.evaluation_type == EvaluationType.ATTACK


def test_benign_evaluation_type():
    result = EvaluationResult(
        status=EvaluationStatus.FAILURE,
        score=0.0,
        evidence=["Benign request completed normally."],
        metadata={},
        evaluation_type=EvaluationType.BENIGN,
    )

    assert result.evaluation_type == EvaluationType.BENIGN


def test_campaign_defense_score():
    evaluation_id = uuid4()

    baseline_results = [
        EvaluationRunResult(
            evaluation=EvaluationResult(
                status=EvaluationStatus.SUCCESS,
                score=1.0,
                evidence=["Attack succeeded."],
                metadata={"attack_id": "PI-001"},
            ),
            finding=Finding(
                evaluation_id=evaluation_id,
                attack_id="PI-001",
                title="Prompt Injection",
                description="Attack succeeded.",
                severity=Severity.CRITICAL,
                score=1.0,
            ),
        ),
        EvaluationRunResult(
            evaluation=EvaluationResult(
                status=EvaluationStatus.FAILURE,
                score=0.0,
                evidence=["Benign request did not expose data."],
                metadata={"attack_id": "PI-000"},
            ),
            finding=None,
        ),
    ]

    defended_results = [
        EvaluationRunResult(
            evaluation=EvaluationResult(
                status=EvaluationStatus.FAILURE,
                score=0.0,
                evidence=["Attack blocked."],
                metadata={
                    "attack_id": "PI-001",
                    "blocked": True,
                },
            ),
            finding=None,
        ),
        EvaluationRunResult(
            evaluation=EvaluationResult(
                status=EvaluationStatus.FAILURE,
                score=0.0,
                evidence=["Benign request was not blocked."],
                metadata={"attack_id": "PI-000"},
            ),
            finding=None,
        ),
    ]

    baseline = CampaignResult(
        results=baseline_results,
        score=CampaignScore(
            total_attacks=2,
            successful_attacks=1,
            failed_attacks=1,
            security_score=0.5,
        ),
    )

    defended = CampaignResult(
        results=defended_results,
        score=CampaignScore(
            total_attacks=2,
            successful_attacks=0,
            failed_attacks=2,
            security_score=1.0,
        ),
    )

    score = calculate_campaign_defense_score(
        baseline=baseline,
        defended=defended,
    )

    assert score.attack_success_without_defense == 0.5
    assert score.attack_success_with_defense == 0.0
    assert score.defense_effectiveness == 0.5
    assert score.detection_rate == 0.5
    assert score.block_rate == 0.5
    assert score.false_positive_rate == 0.0


from sentinel.scoring.defense import (
    calculate_block_rate,
    calculate_defense_score,
    calculate_detection_rate,
    calculate_false_positive_rate,
)


def test_complete_defense_score():
    score = calculate_defense_score(
        attack_success_without_defense=1.0,
        attack_success_with_defense=0.1,
        detected_attacks=9,
        total_attacks=10,
        blocked_attacks=8,
        false_positives=1,
        total_benign_requests=20,
    )

    assert score.attack_success_without_defense == 1.0
    assert score.attack_success_with_defense == 0.1
    assert score.defense_effectiveness == 0.9
    assert score.detection_rate == 0.9
    assert score.block_rate == 0.8
    assert score.false_positive_rate == 0.05


def test_detection_rate():
    assert (
        calculate_detection_rate(
            detected_attacks=8,
            total_attacks=10,
        )
        == 0.8
    )


def test_block_rate():
    assert (
        calculate_block_rate(
            blocked_attacks=9,
            total_attacks=10,
        )
        == 0.9
    )


def test_false_positive_rate():
    assert (
        calculate_false_positive_rate(
            false_positives=1,
            total_benign_requests=20,
        )
        == 0.05
    )


def test_detection_rate_with_no_attacks():
    assert (
        calculate_detection_rate(
            detected_attacks=0,
            total_attacks=0,
        )
        == 0.0
    )


def test_block_rate_with_no_attacks():
    assert (
        calculate_block_rate(
            blocked_attacks=0,
            total_attacks=0,
        )
        == 0.0
    )


def test_false_positive_rate_with_no_benign_requests():
    assert (
        calculate_false_positive_rate(
            false_positives=0,
            total_benign_requests=0,
        )
        == 0.0
    )
