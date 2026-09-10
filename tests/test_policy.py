from sentinel.defenses.basic_policy import BasicToolPolicy
from sentinel.defenses.policy import (
    PolicyDecision,
    PolicyRequest,
)


def test_policy_allows_explicitly_allowed_tool():
    policy = BasicToolPolicy(
        allowed_tools={"search_documents"},
    )

    request = PolicyRequest(
        agent_id="test-agent",
        tool_name="search_documents",
        arguments={"query": "annual report"},
    )

    result = policy.evaluate(request)

    assert result.decision == PolicyDecision.ALLOW


def test_policy_denies_unapproved_tool():
    policy = BasicToolPolicy(
        allowed_tools={"search_documents"},
    )

    request = PolicyRequest(
        agent_id="test-agent",
        tool_name="delete_customer",
        arguments={"customer_id": "123"},
    )

    result = policy.evaluate(request)

    assert result.decision == PolicyDecision.DENY
