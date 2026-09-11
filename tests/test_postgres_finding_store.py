from datetime import UTC, datetime
from uuid import uuid4

import pytest

from sentinel.infrastructure.finding_store import FindingStore
from sentinel.infrastructure.postgres_finding_store import PostgresFindingStore
from sentinel.scoring.finding import Finding, Severity


class FakeSession:
    def __init__(self) -> None:
        self.records = {}
        self.added = []
        self.committed = False

    def add(self, record) -> None:
        self.added.append(record)
        self.records[record.finding_id] = record

    async def get(self, model, finding_id):
        return self.records.get(finding_id)

    async def execute(self, statement):
        where_column = statement.whereclause.left.key
        where_value = statement.whereclause.right.value

        if where_column == "finding_id":
            records = [
                record
                for record in self.records.values()
                if record.finding_id == where_value
            ]
        elif where_column == "evaluation_id":
            records = [
                record
                for record in self.records.values()
                if record.evaluation_id == where_value
            ]
        else:
            records = []

        class Result:
            def __init__(self, records):
                self.records = records

            def scalar_one_or_none(self):
                return self.records[0] if self.records else None

            def scalars(self):
                class Scalars:
                    def __init__(self, records):
                        self.records = records

                    def all(self):
                        return self.records

                return Scalars(self.records)

        return Result(records)

    async def commit(self) -> None:
        self.committed = True


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
        },
    )


@pytest.mark.asyncio
async def test_postgres_finding_store_saves() -> None:
    session = FakeSession()
    store = PostgresFindingStore(session)

    finding = create_finding()

    await store.save(finding)

    assert len(session.added) == 1
    assert session.added[0].finding_id == finding.finding_id
    assert session.committed is True


@pytest.mark.asyncio
async def test_postgres_finding_store_gets_finding() -> None:
    session = FakeSession()
    store = PostgresFindingStore(session)

    finding = create_finding()

    await store.save(finding)

    result = await store.get(finding.finding_id)

    assert result == finding


@pytest.mark.asyncio
async def test_postgres_finding_store_returns_none_for_unknown_id() -> None:
    session = FakeSession()
    store = PostgresFindingStore(session)

    result = await store.get(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_postgres_finding_store_gets_by_evaluation() -> None:
    session = FakeSession()
    store = PostgresFindingStore(session)

    finding = create_finding()

    await store.save(finding)

    results = await store.get_by_evaluation(
        finding.evaluation_id,
    )

    assert results == [finding]


def test_postgres_finding_store_implements_interface() -> None:
    session = FakeSession()
    store = PostgresFindingStore(session)

    assert isinstance(store, FindingStore)