from sentinel.evaluators.result import EvaluationResult, EvaluationStatus
from sentinel.orchestrator.result import EvaluationRunResult
from sentinel.scoring.campaign import calculate_campaign_score


def make_result(
    status: EvaluationStatus,
    score: float,
) -> EvaluationRunResult:
    return EvaluationRunResult(
        evaluation=EvaluationResult(
            status=status,
            score=score,
            evidence=[],
            metadata={},
        ),
        finding=None,
    )


def test_campaign_score():
    results = [
        make_result(
            EvaluationStatus.SUCCESS,
            1.0,
        ),
        make_result(
            EvaluationStatus.FAILURE,
            0.0,
        ),
        make_result(
            EvaluationStatus.FAILURE,
            0.0,
        ),
        make_result(
            EvaluationStatus.SUCCESS,
            1.0,
        ),
    ]

    score = calculate_campaign_score(results)

    assert score.total_attacks == 4
    assert score.successful_attacks == 2
    assert score.failed_attacks == 2
    assert score.security_score == 0.5


def test_empty_campaign():
    score = calculate_campaign_score([])

    assert score.total_attacks == 0
    assert score.successful_attacks == 0
    assert score.failed_attacks == 0
    assert score.security_score == 0.0
