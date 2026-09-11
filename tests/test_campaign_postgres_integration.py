import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine
from collections.abc import AsyncGenerator

from sentinel.attacks.defaults import create_default_registry
from sentinel.defenses.basic_policy import BasicToolPolicy
from sentinel.evaluators.sensitive_data import SensitiveDataEvaluator
from sentinel.infrastructure.database import (
    Base,
    create_engine,
    create_session_factory,
)
from sentinel.infrastructure.evaluation_model import EvaluationRecord
from sentinel.infrastructure.postgres_evaluation_store import (
    PostgresEvaluationStore,
)
from sentinel.infrastructure.settings import DatabaseSettings
from sentinel.instrumentation.event_bus import EventBus
from sentinel.models.campaign import Campaign
from sentinel.models.evaluation import EvaluationStatus
from sentinel.orchestrator.campaign import CampaignRunner
from target.agent.agent import EnterpriseAgent


@pytest_asyncio.fixture
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    settings = DatabaseSettings()
    engine = create_engine(settings.database_url)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

    await engine.dispose()


class CampaignPostgresMockModel:
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
async def test_campaign_persists_separate_evaluations(
    engine: AsyncEngine,
) -> None:
    session_factory = create_session_factory(engine)

    campaign = Campaign(
        name="Postgres Campaign Integration",
        target_id="enterprise-assistant",
        attack_ids=[
            "PI-000",
            "PI-001",
        ],
    )

    registry = create_default_registry()

    async with session_factory() as session:
        evaluation_store = PostgresEvaluationStore(session)

        runner = CampaignRunner(
            model_runtime=CampaignPostgresMockModel(),
            target=EnterpriseAgent(),
            evaluator=SensitiveDataEvaluator(),
            policy=BasicToolPolicy(
                allowed_tools={"customer_lookup"},
            ),
            event_bus=EventBus(),
            attack_registry=registry,
            evaluation_store=evaluation_store,
        )

        result = await runner.run(campaign)

    assert len(result.results) == 2

    evaluation_ids = [
        item.record.evaluation_id
        for item in result.results
    ]

    assert evaluation_ids[0] != evaluation_ids[1]

    async with session_factory() as session:
        rows = await session.execute(
            select(EvaluationRecord)
            .where(
                EvaluationRecord.campaign_id == campaign.campaign_id,
            )
            .order_by(EvaluationRecord.attack_id)
        )

        records = rows.scalars().all()

    assert len(records) == 2

    assert {
        record.evaluation_id
        for record in records
    } == set(evaluation_ids)

    assert all(
        record.campaign_id == campaign.campaign_id
        for record in records
    )

    assert all(
        record.status == EvaluationStatus.SUCCESS.value
        for record in records
    )

    assert all(
        record.score is not None
        for record in records
    )

    assert all(
        record.completed_at is not None
        for record in records
    )