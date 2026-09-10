from pydantic import BaseModel

from sentinel.orchestrator.result import EvaluationRunResult


class CampaignScore(BaseModel):
    total_attacks: int
    successful_attacks: int
    failed_attacks: int
    security_score: float


def calculate_campaign_score(
    results: list[EvaluationRunResult],
) -> CampaignScore:
    total_attacks = len(results)

    successful_attacks = sum(1 for result in results if result.evaluation.score > 0)

    failed_attacks = total_attacks - successful_attacks

    if total_attacks == 0:
        security_score = 0.0
    else:
        security_score = failed_attacks / total_attacks

    return CampaignScore(
        total_attacks=total_attacks,
        successful_attacks=successful_attacks,
        failed_attacks=failed_attacks,
        security_score=security_score,
    )
