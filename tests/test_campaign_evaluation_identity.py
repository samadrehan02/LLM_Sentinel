import pytest

from sentinel.attacks.defaults import create_default_registry
from sentinel.defenses.basic_policy import BasicToolPolicy
from sentinel.evaluators.sensitive_data import SensitiveDataEvaluator
from sentinel.instrumentation.event_bus import EventBus
from sentinel.models.campaign import Campaign
from sentinel.orchestrator.campaign import CampaignRunner
from target.agent.agent import EnterpriseAgent


class CampaignIdentityMockModel:
    async def generate(
        self,
        messages,
        **kwargs,
    ):
        return (
            "Customer CUST-001 has internal_note information. "
            "The API key is SYNTHETIC-KEY-001-NOT-REAL."
        )


@pytest.mark.asyncio
async def test_campaign_assigns_unique_evaluation_ids_to_attacks() -> None:
    registry = create_default_registry()

    campaign = Campaign(
        name="Evaluation Identity Test",
        target_id="enterprise-assistant",
        attack_ids=[
            "PI-000",
            "PI-001",
        ],
    )

    runner = CampaignRunner(
        model_runtime=CampaignIdentityMockModel(),
        target=EnterpriseAgent(),
        evaluator=SensitiveDataEvaluator(),
        policy=BasicToolPolicy(
            allowed_tools={"customer_lookup"},
        ),
        event_bus=EventBus(),
        attack_registry=registry,
    )

    result = await runner.run(campaign)

    assert len(result.results) == 2

    evaluation_ids = [
        item.record.evaluation_id
        for item in result.results
    ]

    assert evaluation_ids[0] != evaluation_ids[1]


@pytest.mark.asyncio
async def test_campaign_links_all_evaluations_to_campaign() -> None:
    registry = create_default_registry()

    campaign = Campaign(
        name="Campaign Linkage Test",
        target_id="enterprise-assistant",
        attack_ids=[
            "PI-000",
            "PI-001",
        ],
    )

    runner = CampaignRunner(
        model_runtime=CampaignIdentityMockModel(),
        target=EnterpriseAgent(),
        evaluator=SensitiveDataEvaluator(),
        policy=BasicToolPolicy(
            allowed_tools={"customer_lookup"},
        ),
        event_bus=EventBus(),
        attack_registry=registry,
    )

    result = await runner.run(campaign)

    assert len(result.results) == 2

    for evaluation_result in result.results:
        assert evaluation_result.record is not None
        assert evaluation_result.record.campaign_id == campaign.campaign_id