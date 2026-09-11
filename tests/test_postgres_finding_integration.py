from collections.abc import AsyncGenerator
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine

from sentinel.infrastructure.database import (
    Base,
    create_engine,
    create_session_factory,
)
from sentinel.infrastructure.finding_model import FindingRecord
from sentinel.infrastructure.postgres_finding_store import PostgresFindingStore
from sentinel.infrastructure.settings import DatabaseSettings
from sentinel.scoring.finding import Finding, Severity


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


def create_finding() -> Finding:
    return Finding(
        finding_id=uuid4(),
        evaluation_id=uuid4(),
        attack_id="PI-001",
        title="Sensitive Data Exposure",
        description="Synthetic customer data was exposed.",
        severity=Severity.CRITICAL,
        score=1.0,
        evidence=[
            "Customer CUST-001 was accessed.",
            "Synthetic API key was exposed.",
        ],
        metadata={
            "tool": "customer_lookup",
            "source": "integration_test",
        },
    )


@pytest.mark.asyncio
async def test_postgres_finding_store_round_trip(
    engine: AsyncEngine,
) -> None:
    session_factory = create_session_factory(engine)
    finding = create_finding()

    async with session_factory() as session:
        store = PostgresFindingStore(session)

        await store.save(finding)

    async with session_factory() as session:
        store = PostgresFindingStore(session)

        loaded = await store.get(
            finding.finding_id,
        )

    assert loaded is not None
    assert loaded.finding_id == finding.finding_id
    assert loaded.evaluation_id == finding.evaluation_id
    assert loaded.attack_id == finding.attack_id
    assert loaded.title == finding.title
    assert loaded.description == finding.description
    assert loaded.severity == finding.severity
    assert loaded.score == finding.score
    assert loaded.evidence == finding.evidence
    assert loaded.metadata == finding.metadata


@pytest.mark.asyncio
async def test_postgres_finding_store_gets_findings_by_evaluation(
    engine: AsyncEngine,
) -> None:
    session_factory = create_session_factory(engine)
    evaluation_id = uuid4()

    finding_a = Finding(
        evaluation_id=evaluation_id,
        attack_id="PI-001",
        title="Finding A",
        description="First finding.",
        severity=Severity.HIGH,
        score=0.8,
        evidence=["Evidence A"],
        metadata={"source": "test"},
    )

    finding_b = Finding(
        evaluation_id=evaluation_id,
        attack_id="PI-002",
        title="Finding B",
        description="Second finding.",
        severity=Severity.CRITICAL,
        score=1.0,
        evidence=["Evidence B"],
        metadata={"source": "test"},
    )

    unrelated = create_finding()

    async with session_factory() as session:
        store = PostgresFindingStore(session)

        await store.save(finding_a)
        await store.save(finding_b)
        await store.save(unrelated)

    async with session_factory() as session:
        store = PostgresFindingStore(session)

        findings = await store.get_by_evaluation(
            evaluation_id,
        )

    assert len(findings) == 2

    assert {
        finding.finding_id
        for finding in findings
    } == {
        finding_a.finding_id,
        finding_b.finding_id,
    }


@pytest.mark.asyncio
async def test_postgres_finding_store_returns_none_for_unknown_id(
    engine: AsyncEngine,
) -> None:
    session_factory = create_session_factory(engine)

    async with session_factory() as session:
        store = PostgresFindingStore(session)

        result = await store.get(uuid4())

    assert result is None