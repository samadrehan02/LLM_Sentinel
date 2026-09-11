from typing import Any
from uuid import UUID

from sqlalchemy import Float, String, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from sentinel.infrastructure.database import Base
from sentinel.scoring.finding import Finding, Severity


class FindingRecord(Base):
    __tablename__ = "findings"

    finding_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
    )

    evaluation_id: Mapped[UUID] = mapped_column(
        Uuid,
        index=True,
        nullable=False,
    )

    attack_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    severity: Mapped[str] = mapped_column(
        String(20),
        index=True,
        nullable=False,
    )

    score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    evidence: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    metadata_: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSONB,
        nullable=False,
        default=dict,
    )

    @classmethod
    def from_finding(cls, finding: Finding) -> "FindingRecord":
        return cls(
            finding_id=finding.finding_id,
            evaluation_id=finding.evaluation_id,
            attack_id=finding.attack_id,
            title=finding.title,
            description=finding.description,
            severity=finding.severity.value,
            score=finding.score,
            evidence=finding.evidence,
            metadata_=finding.metadata,
        )