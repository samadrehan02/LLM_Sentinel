import pytest

from sentinel.attacks.defaults import create_default_registry
from sentinel.defenses.basic_policy import BasicToolPolicy
from sentinel.evaluators.sensitive_data import SensitiveDataEvaluator
from sentinel.instrumentation.event_bus import EventBus
from sentinel.models.campaign import Campaign
from sentinel.orchestrator.campaign import CampaignRunner
from target.agent.agent import EnterpriseAgent


class CampaignMockModel:
    async def generate(
        self,
        messages,
        **kwargs,
    ):
        prompt = messages[-1]["content"]

        if "company provide" in prompt.lower():
            return "The company provides enterprise software services."

        return (
            "Customer CUST-001 has internal_note information. "
            "The API key is SYNTHETIC-KEY-001-NOT-REAL."
        )


@pytest.mark.asyncio
async def test_campaign_runner_executes_mixed_attacks():
    registry = create_default_registry()

    campaign = Campaign(
        name="Baseline Security Assessment",
        target_id="enterprise-assistant",
        attack_ids=[
            "PI-000",
            "PI-001",
        ],
    )

    runner = CampaignRunner(
        model_runtime=CampaignMockModel(),
        target=EnterpriseAgent(),
        evaluator=SensitiveDataEvaluator(),
        policy=BasicToolPolicy(
            allowed_tools={"customer_lookup"},
        ),
        event_bus=EventBus(),
        attack_registry=registry,
    )

    result = await runner.run(
        campaign=campaign,
    )

    assert len(result.results) == 2

    assert result.results[0].evaluation.status.value == "failure"
    assert result.results[0].finding is None

    assert result.results[1].evaluation.status.value == "success"
    assert result.results[1].finding is not None

    assert result.score.total_attacks == 2
    assert result.score.successful_attacks == 1
    assert result.score.failed_attacks == 1
    assert result.score.security_score == 0.5
