from typing import Any

from sentinel.attacks.result import AttackResult
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
        if isinstance(attack_result, AttackResult):
            if attack_result.success:
                evidence = list(attack_result.outcome.evidence)

                if not evidence:
                    evidence = [
                        f"Attack {attack_result.attack_id} reached its success condition."
                    ]

                return EvaluationResult(
                    status=EvaluationStatus.SUCCESS,
                    score=1.0,
                    evidence=evidence,
                    metadata={
                        **attack_result.metadata,
                        **attack_result.outcome.metadata,
                    },
                    evaluation_type=EvaluationType.ATTACK,
                )

            evidence = list(attack_result.outcome.evidence)

            if not evidence:
                evidence = [
                    f"Attack {attack_result.attack_id} did not reach its success condition."
                ]

            return EvaluationResult(
                status=EvaluationStatus.FAILURE,
                score=0.0,
                evidence=evidence,
                metadata={
                    **attack_result.metadata,
                    **attack_result.outcome.metadata,
                },
                evaluation_type=EvaluationType.ATTACK,
            )

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