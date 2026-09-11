from datetime import UTC, datetime
from uuid import UUID, uuid4

from sentinel.attacks.base import Attack
from sentinel.defenses.policy import Policy
from sentinel.evaluators.base import Evaluator
from sentinel.evaluators.result import (
    EvaluationResult,
    EvaluationStatus,
    EvaluationType,
)
from sentinel.infrastructure.evaluation_store import EvaluationStore
from sentinel.instrumentation.event_bus import EventBus
from sentinel.instrumentation.events import Event, EventType
from sentinel.models.evaluation import Evaluation
from sentinel.models.instrumented import InstrumentedModelRuntime
from sentinel.models.runtime import ModelRuntime
from sentinel.orchestrator.result import EvaluationRunResult
from sentinel.scoring.finding_builder import build_finding
from target.agent.interface import Target


class EvaluationRunner:
    def __init__(
        self,
        model_runtime: ModelRuntime,
        target: Target,
        evaluator: Evaluator,
        policy: Policy,
        event_bus: EventBus,
        evaluation_store: EvaluationStore | None = None,
    ) -> None:
        self.model_runtime = model_runtime
        self.target = target
        self.evaluator = evaluator
        self.policy = policy
        self.event_bus = event_bus
        self.evaluation_store = evaluation_store

    async def run(
        self,
        attack: Attack,
        evaluation_id: UUID | None = None,
    ) -> EvaluationRunResult:
        evaluation_id = evaluation_id or uuid4()
        run_id = uuid4()
        trace_id = uuid4()

        attack_id = attack.attack_id
        attack_name = getattr(attack, "name", attack_id)
        attack_category = getattr(
            attack,
            "category",
            "unknown",
        )
        attack_severity = getattr(
            attack,
            "severity",
            "unknown",
        )

        record = Evaluation(
            evaluation_id=evaluation_id,
            attack_id=attack_id,
            attack_category=attack_category,
            target="enterprise-assistant",
        )

        if self.evaluation_store is not None:
            await self.evaluation_store.save(record)

        instrumented_runtime = InstrumentedModelRuntime(
            runtime=self.model_runtime,
            event_bus=self.event_bus,
            evaluation_id=evaluation_id,
            run_id=run_id,
            trace_id=trace_id,
        )

        await self.event_bus.publish(
            Event(
                evaluation_id=evaluation_id,
                run_id=run_id,
                trace_id=trace_id,
                event_type=EventType.EVALUATION_STARTED,
                component="evaluation_runner",
                payload={
                    "attack_id": attack_id,
                    "attack_name": attack_name,
                    "attack_category": attack_category,
                },
            )
        )

        await self.event_bus.publish(
            Event(
                evaluation_id=evaluation_id,
                run_id=run_id,
                trace_id=trace_id,
                event_type=EventType.ATTACK_STARTED,
                component="evaluation_runner",
                payload={
                    "attack_id": attack_id,
                    "attack_name": attack_name,
                    "attack_category": attack_category,
                    "attack_severity": attack_severity,
                },
            )
        )

        try:
            attack_result = await attack.execute(
                target=self.target,
                evaluation_id=evaluation_id,
                run_id=run_id,
                model_runtime=instrumented_runtime,
            )

            result = await self.evaluator.evaluate(
                attack_result,
            )

            result.metadata.update(
                {
                    "attack_id": attack_id,
                    "attack_name": attack_name,
                    "attack_category": attack_category,
                    "attack_severity": attack_severity,
                }
            )

            result.evaluation_type = (
                EvaluationType.BENIGN
                if attack_id == "PI-000"
                else EvaluationType.ATTACK
            )

        except PermissionError as exc:
            await self.event_bus.publish(
                Event(
                    evaluation_id=evaluation_id,
                    run_id=run_id,
                    trace_id=trace_id,
                    event_type=EventType.DEFENSE_BLOCKED,
                    component="evaluation_runner",
                    payload={
                        "attack_id": attack_id,
                        "attack_name": attack_name,
                        "attack_category": attack_category,
                        "attack_severity": attack_severity,
                        "reason": str(exc),
                    },
                )
            )

            result = EvaluationResult(
                status=EvaluationStatus.FAILURE,
                score=0.0,
                evidence=[
                    f"Attack blocked by runtime defense: {exc}",
                ],
                metadata={
                    "blocked": True,
                    "defense": "runtime",
                    "attack_id": attack_id,
                    "attack_name": attack_name,
                    "attack_category": attack_category,
                    "attack_severity": attack_severity,
                },
                evaluation_type=EvaluationType.ATTACK,
            )

        record.status = result.status
        record.score = result.score
        record.completed_at = datetime.now(UTC)

        if self.evaluation_store is not None:
            await self.evaluation_store.save(record)

        await self.event_bus.publish(
            Event(
                evaluation_id=evaluation_id,
                run_id=run_id,
                trace_id=trace_id,
                event_type=EventType.ATTACK_EVALUATED,
                component="evaluation_runner",
                payload={
                    "attack_id": attack_id,
                    "attack_name": attack_name,
                    "attack_category": attack_category,
                    "attack_severity": attack_severity,
                    "status": result.status.value,
                    "score": result.score,
                    "evaluation_type": result.evaluation_type.value,
                },
            )
        )

        finding = build_finding(
            evaluation_id=evaluation_id,
            attack_id=attack_id,
            result=result,
        )

        if finding is not None:
            await self.event_bus.publish(
                Event(
                    evaluation_id=evaluation_id,
                    run_id=run_id,
                    trace_id=trace_id,
                    event_type=EventType.FINDING_CREATED,
                    component="evaluation_runner",
                    payload={
                        "finding_id": str(
                            finding.finding_id,
                        ),
                        "attack_id": finding.attack_id,
                        "severity": finding.severity.value,
                        "score": finding.score,
                    },
                )
            )

        events = []

        event_store = self.event_bus.event_store

        if event_store is not None:
            events = await event_store.get_by_evaluation(
                evaluation_id,
            )

        return EvaluationRunResult(
            evaluation=result,
            finding=finding,
            events=events,
            record=record,
        )