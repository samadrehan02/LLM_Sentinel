from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Float, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from sentinel.infrastructure.database import Base
from sentinel.models.evaluation import Evaluation


class EvaluationRecord(Base):
    __tablename__ = "evaluations"

    evaluation_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
    )
    campaign_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        index=True,
        nullable=True,
    )
    attack_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
    )
    attack_category: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
    )
    target: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    @classmethod
    def from_evaluation(
        cls,
        evaluation: Evaluation,
    ) -> "EvaluationRecord":
        return cls(
            evaluation_id=evaluation.evaluation_id,
            campaign_id=evaluation.campaign_id,
            attack_id=evaluation.attack_id,
            attack_category=evaluation.attack_category,
            target=evaluation.target,
            status=evaluation.status.value,
            score=evaluation.score,
            started_at=evaluation.started_at,
            completed_at=evaluation.completed_at,
        )