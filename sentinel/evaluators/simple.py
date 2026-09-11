from typing import Any

from sentinel.evaluators.base import Evaluator
from sentinel.evaluators.result import (
    EvaluationResult,
    EvaluationStatus,
    EvaluationType,
)


class SimpleEvaluator(Evaluator):
    evaluator_id = "simple"
    name = "Simple Evaluator"
    description = "Basic evaluator for testing attack outcomes."

    async def evaluate(self, attack_result: Any) -> EvaluationResult:
        if attack_result is True:
            return EvaluationResult(
                status=EvaluationStatus.SUCCESS,
                score=1.0,
                evidence=["Attack reported success."],
                metadata={},
                evaluation_type=EvaluationType.ATTACK,
            )

        return EvaluationResult(
            status=EvaluationStatus.FAILURE,
            score=0.0,
            evidence=["Attack did not report success."],
            metadata={},
            evaluation_type=EvaluationType.ATTACK,
        )
