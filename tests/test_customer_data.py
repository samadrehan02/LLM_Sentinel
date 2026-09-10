from target.data.customers import get_customer


def test_get_customer():
    customer = get_customer("CUST-001")

    assert customer is not None
    assert customer["customer_id"] == "CUST-001"
    assert customer["name"] == "Alice Johnson"
    assert customer["api_key"] == "SYNTHETIC-KEY-001-NOT-REAL"


def test_unknown_customer():
    assert get_customer("DOES-NOT-EXIST") is None
