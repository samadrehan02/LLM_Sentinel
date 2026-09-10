import pytest

from target.agent.tools import CustomerLookupTool


@pytest.mark.asyncio
async def test_customer_lookup_tool():
    tool = CustomerLookupTool()

    result = await tool.execute(
        {
            "customer_id": "CUST-001",
        }
    )

    assert result is not None
    assert result["customer_id"] == "CUST-001"
    assert result["name"] == "Alice Johnson"


@pytest.mark.asyncio
async def test_customer_lookup_unknown_customer():
    tool = CustomerLookupTool()

    result = await tool.execute(
        {
            "customer_id": "DOES-NOT-EXIST",
        }
    )

    assert result is None


@pytest.mark.asyncio
async def test_customer_lookup_requires_string_id():
    tool = CustomerLookupTool()

    with pytest.raises(ValueError, match="customer_id must be a string"):
        await tool.execute(
            {
                "customer_id": 123,
            }
        )
