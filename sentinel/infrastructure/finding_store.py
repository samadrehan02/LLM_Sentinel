from abc import ABC, abstractmethod
from uuid import UUID

from sentinel.scoring.finding import Finding


class FindingStore(ABC):
    @abstractmethod
    async def save(self, finding: Finding) -> None:
        ...

    @abstractmethod
    async def get(self, finding_id: UUID) -> Finding | None:
        ...

    @abstractmethod
    async def get_by_evaluation(
        self,
        evaluation_id: UUID,
    ) -> list[Finding]:
        ...


class InMemoryFindingStore(FindingStore):
    def __init__(self) -> None:
        self._findings: dict[UUID, Finding] = {}

    async def save(self, finding: Finding) -> None:
        self._findings[finding.finding_id] = finding

    async def get(self, finding_id: UUID) -> Finding | None:
        return self._findings.get(finding_id)

    async def get_by_evaluation(
        self,
        evaluation_id: UUID,
    ) -> list[Finding]:
        return [
            finding
            for finding in self._findings.values()
            if finding.evaluation_id == evaluation_id
        ]