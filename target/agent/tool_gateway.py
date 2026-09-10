from typing import Any
from uuid import UUID, uuid4

from sentinel.defenses.policy import (
    Policy,
    PolicyDecision,
    PolicyRequest,
)
from sentinel.instrumentation.event_bus import EventBus
from sentinel.instrumentation.events import Event, EventType
from target.agent.tools import AgentTool


class ToolGateway:
    def __init__(
        self,
        tools: dict[str, AgentTool],
        policy: Policy,
        event_bus: EventBus,
        evaluation_id: UUID,
        run_id: UUID | None = None,
        trace_id: UUID | None = None,
    ) -> None:
        self.tools = tools
        self.policy = policy
        self.event_bus = event_bus
        self.evaluation_id = evaluation_id
        self.run_id = run_id or uuid4()
        self.trace_id = trace_id or uuid4()

    async def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> Any:
        tool = self.tools.get(tool_name)

        if tool is None:
            raise ValueError(f"Unknown tool: {tool_name}")

        self.event_bus.publish(
            Event(
                evaluation_id=self.evaluation_id,
                run_id=self.run_id,
                trace_id=self.trace_id,
                event_type=EventType.TOOL_REQUESTED,
                component="tool_gateway",
                payload={
                    "tool_name": tool_name,
                    "arguments": arguments,
                },
            )
        )

        policy_result = self.policy.evaluate(
            PolicyRequest(
                agent_id="enterprise-assistant",
                tool_name=tool_name,
                arguments=arguments,
            )
        )

        self.event_bus.publish(
            Event(
                evaluation_id=self.evaluation_id,
                run_id=self.run_id,
                trace_id=self.trace_id,
                event_type=EventType.AUTHORIZATION_DECISION,
                component="tool_gateway",
                payload={
                    "tool_name": tool_name,
                    "decision": policy_result.decision.value,
                    "reason": policy_result.reason,
                    "policy_id": policy_result.policy_id,
                },
            )
        )

        if policy_result.decision != PolicyDecision.ALLOW:
            raise PermissionError(f"Tool execution denied: {policy_result.reason}")

        result = await tool.execute(arguments)

        self.event_bus.publish(
            Event(
                evaluation_id=self.evaluation_id,
                run_id=self.run_id,
                trace_id=self.trace_id,
                event_type=EventType.TOOL_EXECUTED,
                component="tool_gateway",
                payload={
                    "tool_name": tool_name,
                    "arguments": arguments,
                    "result": result,
                },
            )
        )

        return result
