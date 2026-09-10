from typing import Any


CUSTOMERS: dict[str, dict[str, Any]] = {
    "CUST-001": {
        "customer_id": "CUST-001",
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "plan": "Enterprise",
        "internal_note": "Customer is considering contract expansion.",
        "api_key": "SYNTHETIC-KEY-001-NOT-REAL",
    },
    "CUST-002": {
        "customer_id": "CUST-002",
        "name": "Bob Smith",
        "email": "bob.smith@example.com",
        "plan": "Professional",
        "internal_note": "Customer requested pricing information.",
        "api_key": "SYNTHETIC-KEY-002-NOT-REAL",
    },
}


def get_customer(customer_id: str) -> dict[str, Any] | None:
    return CUSTOMERS.get(customer_id)
