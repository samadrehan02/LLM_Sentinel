from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sentinel.infrastructure.finding_model import FindingRecord
from sentinel.infrastructure.finding_store import FindingStore
from sentinel.scoring.finding import Finding, Severity


class PostgresFindingStore(FindingStore):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, finding: Finding) -> None:
        record = FindingRecord.from_finding(finding)

        existing = await self.session.get(
            FindingRecord,
            finding.finding_id,
        )

        if existing is not None:
            existing.evaluation_id = record.evaluation_id
            existing.attack_id = record.attack_id
            existing.title = record.title
            existing.description = record.description
            existing.severity = record.severity
            existing.score = record.score
            existing.evidence = record.evidence
            existing.metadata_ = record.metadata_
        else:
            self.session.add(record)

        await self.session.commit()

    async def get(self, finding_id: UUID) -> Finding | None:
        result = await self.session.execute(
            select(FindingRecord).where(
                FindingRecord.finding_id == finding_id,
            )
        )

        record = result.scalar_one_or_none()

        if record is None:
            return None

        return Finding(
            finding_id=record.finding_id,
            evaluation_id=record.evaluation_id,
            attack_id=record.attack_id,
            title=record.title,
            description=record.description,
            severity=Severity(record.severity),
            score=record.score,
            evidence=record.evidence,
            metadata=record.metadata_,
        )

    async def get_by_evaluation(
        self,
        evaluation_id: UUID,
    ) -> list[Finding]:
        result = await self.session.execute(
            select(FindingRecord)
            .where(
                FindingRecord.evaluation_id == evaluation_id,
            )
            .order_by(FindingRecord.finding_id)
        )

        records = result.scalars().all()

        return [
            Finding(
                finding_id=record.finding_id,
                evaluation_id=record.evaluation_id,
                attack_id=record.attack_id,
                title=record.title,
                description=record.description,
                severity=Severity(record.severity),
                score=record.score,
                evidence=record.evidence,
                metadata=record.metadata_,
            )
            for record in records
        ]