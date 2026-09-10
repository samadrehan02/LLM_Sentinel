from sentinel.orchestrator.result import EvaluationRunResult
from sentinel.scoring.campaign import CampaignScore


class CampaignResult:
    def __init__(
        self,
        results: list[EvaluationRunResult],
        score: CampaignScore,
    ) -> None:
        self.results = results
        self.score = score
