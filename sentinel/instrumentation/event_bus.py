from collections.abc import Callable
from typing import Any

from sentinel.instrumentation.events import Event, EventType
from sentinel.instrumentation.store import EventStore

EventHandler = Callable[[Event], Any]


class EventBus:
    def __init__(
        self,
        event_store: EventStore | None = None,
    ) -> None:
        self._handlers: dict[EventType, list[EventHandler]] = {}
        self.event_store = event_store

    def subscribe(
        self,
        event_type: EventType,
        handler: EventHandler,
    ) -> None:
        self._handlers.setdefault(
            event_type,
            [],
        ).append(handler)

    def publish(self, event: Event) -> None:
        if self.event_store is not None:
            self.event_store.save(event)

        handlers = self._handlers.get(
            event.event_type,
            [],
        )

        for handler in handlers:
            handler(event)