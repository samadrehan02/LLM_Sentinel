from typing import Any
from uuid import UUID

from sentinel.instrumentation.event_bus import EventBus
from sentinel.instrumentation.events import Event, EventType
from sentinel.models.runtime import ModelRuntime


class InstrumentedModelRuntime(ModelRuntime):
    def __init__(
        self,
        runtime: ModelRuntime,
        event_bus: EventBus,
        evaluation_id: UUID,
        run_id: UUID,
        trace_id: UUID,
    ) -> None:
        self.runtime = runtime
        self.event_bus = event_bus
        self.evaluation_id = evaluation_id
        self.run_id = run_id
        self.trace_id = trace_id

    async def generate(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> str:
        self.event_bus.publish(
            Event(
                evaluation_id=self.evaluation_id,
                run_id=self.run_id,
                trace_id=self.trace_id,
                event_type=EventType.AGENT_REQUEST,
                component="model_runtime",
                payload={
                    "messages": messages,
                },
            )
        )

        response = await self.runtime.generate(
            messages=messages,
            **kwargs,
        )

        self.event_bus.publish(
            Event(
                evaluation_id=self.evaluation_id,
                run_id=self.run_id,
                trace_id=self.trace_id,
                event_type=EventType.LLM_GENERATION,
                component="model_runtime",
                payload={
                    "response": response,
                },
            )
        )

        return response
