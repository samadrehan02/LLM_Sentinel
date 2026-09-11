from uuid import uuid4

import pytest

from sentinel.infrastructure.finding_store import (
    FindingStore,
    InMemoryFindingStore,
)
from sentinel.scoring.finding import Finding, Severity


def create_finding(
    evaluation_id=None,
    attack_id: str = "PI-001",
) -> Finding:
    return Finding(
        evaluation_id=evaluation_id or uuid4(),
        attack_id=attack_id,
        title="Test Finding",
        description="Test security finding.",
        severity=Severity.HIGH,
        score=0.8,
        evidence=["Synthetic evidence"],
        metadata={"source": "test"},
    )


@pytest.mark.asyncio
async def test_in_memory_finding_store_saves_and_gets() -> None:
    store = InMemoryFindingStore()
    finding = create_finding()

    await store.save(finding)

    result = await store.get(finding.finding_id)

    assert result == finding


@pytest.mark.asyncio
async def test_in_memory_finding_store_returns_none_for_unknown_id() -> None:
    store = InMemoryFindingStore()

    result = await store.get(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_in_memory_finding_store_gets_by_evaluation() -> None:
    store = InMemoryFindingStore()
    evaluation_id = uuid4()

    finding_a = create_finding(
        evaluation_id=evaluation_id,
        attack_id="PI-001",
    )
    finding_b = create_finding(
        evaluation_id=evaluation_id,
        attack_id="PI-002",
    )
    unrelated = create_finding(
        evaluation_id=uuid4(),
        attack_id="PI-003",
    )

    await store.save(finding_a)
    await store.save(finding_b)
    await store.save(unrelated)

    results = await store.get_by_evaluation(evaluation_id)

    assert len(results) == 2
    assert {finding.finding_id for finding in results} == {
        finding_a.finding_id,
        finding_b.finding_id,
    }


def test_in_memory_finding_store_implements_interface() -> None:
    store = InMemoryFindingStore()

    assert isinstance(store, FindingStore)