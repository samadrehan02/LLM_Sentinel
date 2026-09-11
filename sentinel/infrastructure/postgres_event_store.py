from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sentinel.infrastructure.event_model import EventRecord
from sentinel.instrumentation.events import Event
from sentinel.instrumentation.store import EventStore


class PostgresEventStore(EventStore):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def save(self, event: Event) -> None:
        raise NotImplementedError(
            "PostgresEventStore requires async persistence. "
            "Use save_async() instead."
        )

    async def save_async(self, event: Event) -> None:
        record = EventRecord.from_event(event)

        self.session.add(record)
        await self.session.commit()

    def get_by_evaluation(
        self,
        evaluation_id: UUID,
    ) -> list[Event]:
        raise NotImplementedError(
            "PostgresEventStore requires async retrieval. "
            "Use get_by_evaluation_async() instead."
        )

    async def get_by_evaluation_async(
        self,
        evaluation_id: UUID,
    ) -> list[Event]:
        result = await self.session.execute(
            select(EventRecord)
            .where(
                EventRecord.evaluation_id == evaluation_id,
            )
            .order_by(
                EventRecord.timestamp,
            )
        )

        records = result.scalars().all()

        return [
            Event(
                event_id=record.event_id,
                evaluation_id=record.evaluation_id,
                run_id=record.run_id,
                trace_id=record.trace_id,
                timestamp=record.timestamp,
                event_type=record.event_type,
                component=record.component,
                payload=record.payload,
                schema_version=record.schema_version,
            )
            for record in records
        ]