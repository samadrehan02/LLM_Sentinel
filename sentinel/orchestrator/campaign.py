from uuid import UUID

from sentinel.attacks.registry import AttackRegistry
from sentinel.defenses.policy import Policy
from sentinel.evaluators.base import Evaluator
from sentinel.infrastructure.evaluation_store import EvaluationStore
from sentinel.instrumentation.event_bus import EventBus
from sentinel.models.campaign import Campaign
from sentinel.models.runtime import ModelRuntime
from sentinel.orchestrator.campaign_result import CampaignResult
from sentinel.orchestrator.runner import EvaluationRunner
from sentinel.scoring.campaign import calculate_campaign_score
from target.agent.interface import Target


class CampaignRunner:
    def __init__(
        self,
        model_runtime: ModelRuntime,
        target: Target,
        evaluator: Evaluator,
        policy: Policy,
        event_bus: EventBus,
        attack_registry: AttackRegistry,
        evaluation_store: EvaluationStore | None = None,
    ) -> None:
        self.attack_registry = attack_registry

        self.evaluation_runner = EvaluationRunner(
            model_runtime=model_runtime,
            target=target,
            evaluator=evaluator,
            policy=policy,
            event_bus=event_bus,
            evaluation_store=evaluation_store,
        )

    async def run(
        self,
        campaign: Campaign,
    ) -> CampaignResult:
        results = []

        for attack_id in campaign.attack_ids:
            attack = self.attack_registry.get(attack_id)

            result = await self.evaluation_runner.run(
                attack=attack,
                campaign_id=campaign.campaign_id,
            )

            results.append(result)

        score = calculate_campaign_score(results)

        return CampaignResult(
            results=results,
            score=score,
        )