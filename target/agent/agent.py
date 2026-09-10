import json
from typing import Any

from sentinel.defenses.middleware import PromptInjectionMiddleware
from sentinel.models.runtime import ModelRuntime
from target.agent.config import AgentConfig
from target.agent.interface import Target
from target.agent.tool_gateway import ToolGateway


class EnterpriseAgent(Target):
    target_id = "enterprise-assistant"
    name = "Enterprise Assistant"
    description = "Deliberately vulnerable enterprise LLM agent."

    def __init__(
        self,
        config: AgentConfig | None = None,
        tool_gateway: ToolGateway | None = None,
        prompt_injection_middleware: PromptInjectionMiddleware | None = None,
    ) -> None:
        self.config = config or AgentConfig()
        self.tool_gateway = tool_gateway
        self.prompt_injection_middleware = prompt_injection_middleware

    async def interact(
        self,
        messages: list[dict[str, str]],
        model_runtime: ModelRuntime,
        **kwargs: Any,
    ) -> str:
        for message in messages:
            if message.get("role") == "user":
                content = message.get("content", "")

                if self.prompt_injection_middleware is not None:
                    self.prompt_injection_middleware.inspect(content)

        system_message = {
            "role": "system",
            "content": self.config.system_prompt,
        }

        full_messages = [
            system_message,
            *messages,
        ]

        response = await model_runtime.generate(
            messages=full_messages,
            **kwargs,
        )

        tool_request = self._parse_tool_request(response)

        if tool_request is None:
            return response

        tool_result = await self.use_tool(
            tool_name=tool_request["tool_name"],
            arguments=tool_request["arguments"],
        )

        return json.dumps(tool_result)

    async def use_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> Any:
        if self.tool_gateway is None:
            raise RuntimeError("Tool gateway is not configured.")

        return await self.tool_gateway.execute(
            tool_name=tool_name,
            arguments=arguments,
        )

    @staticmethod
    def _parse_tool_request(
        response: str,
    ) -> dict[str, Any] | None:
        try:
            parsed = json.loads(response)
        except json.JSONDecodeError:
            return None

        if not isinstance(parsed, dict):
            return None

        if parsed.get("type") != "tool_call":
            return None

        tool_name = parsed.get("tool_name")
        arguments = parsed.get("arguments")

        if not isinstance(tool_name, str):
            return None

        if not isinstance(arguments, dict):
            return None

        return {
            "tool_name": tool_name,
            "arguments": arguments,
        }