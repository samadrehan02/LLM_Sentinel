from sentinel.evaluators.result import EvaluationResult
from sentinel.scoring.finding import Finding


class EvaluationRunResult:
    def __init__(
        self,
        evaluation: EvaluationResult,
        finding: Finding | None,
    ) -> None:
        self.evaluation = evaluation
        self.finding = finding
