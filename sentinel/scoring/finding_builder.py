from uuid import UUID

from sentinel.evaluators.result import EvaluationResult, EvaluationStatus
from sentinel.scoring.finding import Finding, Severity


def build_finding(
    evaluation_id: UUID,
    attack_id: str,
    result: EvaluationResult,
) -> Finding | None:
    if result.status != EvaluationStatus.SUCCESS:
        return None

    return Finding(
        evaluation_id=evaluation_id,
        attack_id=attack_id,
        title="LLM Security Vulnerability Detected",
        description=("The evaluated attack successfully compromised the target agent."),
        severity=Severity.CRITICAL,
        score=result.score,
        evidence=result.evidence,
        metadata=result.metadata,
    )
