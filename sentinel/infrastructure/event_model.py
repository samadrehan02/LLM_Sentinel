from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String, Text, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from sentinel.instrumentation.events import Event
from sentinel.infrastructure.database import Base


class EventRecord(Base):
    __tablename__ = "security_events"

    event_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
    )

    evaluation_id: Mapped[UUID] = mapped_column(
        Uuid,
        index=True,
        nullable=False,
    )

    run_id: Mapped[UUID] = mapped_column(
        Uuid,
        index=True,
        nullable=False,
    )

    trace_id: Mapped[UUID] = mapped_column(
        Uuid,
        index=True,
        nullable=False,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
    )

    component: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    payload: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    schema_version: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="1.0",
    )

    @classmethod
    def from_event(cls, event: Event) -> "EventRecord":
        return cls(
            event_id=event.event_id,
            evaluation_id=event.evaluation_id,
            run_id=event.run_id,
            trace_id=event.trace_id,
            timestamp=event.timestamp,
            event_type=event.event_type.value,
            component=event.component,
            payload=event.payload,
            schema_version=event.schema_version,
        )