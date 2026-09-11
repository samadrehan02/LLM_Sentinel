from sentinel.evaluators.result import EvaluationResult
from sentinel.instrumentation.events import Event
from sentinel.scoring.finding import Finding


class EvaluationRunResult:
    def __init__(
        self,
        evaluation: EvaluationResult,
        finding: Finding | None,
        events: list[Event] | None = None,
    ) -> None:
        self.evaluation = evaluation
        self.finding = finding
        self.events = events or []