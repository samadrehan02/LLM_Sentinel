from collections.abc import Callable
from typing import Any

from sentinel.instrumentation.events import Event, EventType

EventHandler = Callable[[Event], Any]


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[EventType, list[EventHandler]] = {}

    def subscribe(
        self,
        event_type: EventType,
        handler: EventHandler,
    ) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event: Event) -> None:
        handlers = self._handlers.get(event.event_type, [])

        for handler in handlers:
            handler(event)
