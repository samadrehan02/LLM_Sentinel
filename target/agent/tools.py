from abc import ABC, abstractmethod
from typing import Any

from target.data.customers import get_customer


class AgentTool(ABC):
    name: str
    description: str

    @abstractmethod
    async def execute(
        self,
        arguments: dict[str, Any],
    ) -> Any:
        """Execute the tool."""
        raise NotImplementedError


class CustomerLookupTool(AgentTool):
    name = "customer_lookup"
    description = "Look up a customer using their customer ID."

    async def execute(
        self,
        arguments: dict[str, Any],
    ) -> dict[str, Any] | None:
        customer_id = arguments.get("customer_id")

        if not isinstance(customer_id, str):
            raise ValueError("customer_id must be a string")

        return get_customer(customer_id)
