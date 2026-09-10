from sentinel.defenses.policy import (
    Policy,
    PolicyDecision,
    PolicyRequest,
    PolicyResult,
)


class BasicToolPolicy(Policy):
    policy_id = "basic-tool-policy"
    name = "Basic Tool Policy"

    def __init__(self, allowed_tools: set[str]) -> None:
        self.allowed_tools = allowed_tools

    def evaluate(self, request: PolicyRequest) -> PolicyResult:
        if request.tool_name in self.allowed_tools:
            return PolicyResult(
                decision=PolicyDecision.ALLOW,
                reason="Tool is explicitly allowed.",
                policy_id=self.policy_id,
            )

        return PolicyResult(
            decision=PolicyDecision.DENY,
            reason="Tool is not in the allowed tool set.",
            policy_id=self.policy_id,
        )
