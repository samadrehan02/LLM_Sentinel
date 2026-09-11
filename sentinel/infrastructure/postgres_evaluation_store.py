from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sentinel.infrastructure.evaluation_model import EvaluationRecord
from sentinel.infrastructure.evaluation_store import EvaluationStore
from sentinel.models.evaluation import Evaluation, EvaluationStatus


class PostgresEvaluationStore(EvaluationStore):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(
        self,
        evaluation: Evaluation,
    ) -> None:
        record = EvaluationRecord.from_evaluation(
            evaluation,
        )

        existing = await self.session.get(
            EvaluationRecord,
            evaluation.evaluation_id,
        )

        if existing is None:
            self.session.add(record)
        else:
            existing.campaign_id = record.campaign_id
            existing.attack_id = record.attack_id
            existing.attack_category = record.attack_category
            existing.target = record.target
            existing.status = record.status
            existing.score = record.score
            existing.started_at = record.started_at
            existing.completed_at = record.completed_at

        await self.session.commit()

    async def get(
        self,
        evaluation_id: UUID,
    ) -> Evaluation | None:
        result = await self.session.execute(
            select(EvaluationRecord).where(
                EvaluationRecord.evaluation_id == evaluation_id,
            )
        )

        record = result.scalar_one_or_none()

        if record is None:
            return None

        return Evaluation(
            evaluation_id=record.evaluation_id,
            campaign_id=record.campaign_id,
            attack_id=record.attack_id,
            attack_category=record.attack_category,
            target=record.target,
            status=EvaluationStatus(record.status),
            score=record.score,
            started_at=record.started_at,
            completed_at=record.completed_at,
        )