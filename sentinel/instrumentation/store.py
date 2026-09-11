from abc import ABC, abstractmethod
from uuid import UUID

from sentinel.instrumentation.events import Event


class EventStore(ABC):
    @abstractmethod
    def save(self, event: Event) -> None:
        """Persist an event."""
        raise NotImplementedError

    @abstractmethod
    def get_by_evaluation(
        self,
        evaluation_id: UUID,
    ) -> list[Event]:
        """Return all events for an evaluation."""
        raise NotImplementedError


class InMemoryEventStore(EventStore):
    def __init__(self) -> None:
        self._events: list[Event] = []

    def save(self, event: Event) -> None:
        self._events.append(event)

    def get_by_evaluation(
        self,
        evaluation_id: UUID,
    ) -> list[Event]:
        return [
            event
            for event in self._events
            if event.evaluation_id == evaluation_id
        ]