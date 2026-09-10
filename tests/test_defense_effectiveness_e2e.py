import json
from uuid import uuid4

import pytest

from sentinel.attacks.prompt_injection.direct import (
    DirectPromptInjectionAttack,
)
from sentinel.defenses.basic_policy import BasicToolPolicy
from sentinel.defenses.middleware import PromptInjectionMiddleware
from sentinel.defenses.prompt_injection import PromptInjectionDetector
from sentinel.evaluators.sensitive_data import SensitiveDataEvaluator
from sentinel.instrumentation.event_bus import EventBus
from sentinel.instrumentation.events import EventType
from sentinel.models.mock import MockModelRuntime
from sentinel.orchestrator.runner import EvaluationRunner
from sentinel.scoring.defense import calculate_defense_effectiveness
from target.agent.agent import EnterpriseAgent
from target.agent.tool_gateway import ToolGateway
from target.agent.tools import CustomerLookupTool


@pytest.mark.asyncio
async def test_prompt_injection_defense_effectiveness():
    attack = DirectPromptInjectionAttack()

    model = MockModelRuntime(
        response=json.dumps(
            {
                "type": "tool_call",
                "tool_name": "customer_lookup",
                "arguments": {
                    "customer_id": "CUST-001",
                },
            }
        ),
    )

    evaluator = SensitiveDataEvaluator()

    vulnerable_agent = EnterpriseAgent(
        tool_gateway=ToolGateway(
            tools={
                "customer_lookup": CustomerLookupTool(),
            },
            policy=BasicToolPolicy(
                allowed_tools={"customer_lookup"},
            ),
            event_bus=EventBus(),
            evaluation_id=uuid4(),
        ),
    )

    vulnerable_runner = EvaluationRunner(
        model_runtime=model,
        target=vulnerable_agent,
        evaluator=evaluator,
        policy=BasicToolPolicy(
            allowed_tools={"customer_lookup"},
        ),
        event_bus=EventBus(),
    )

    vulnerable_result = await vulnerable_runner.run(
        attack,
    )

    assert vulnerable_result.evaluation.status.value == "success"
    assert vulnerable_result.evaluation.score == 1.0
    assert vulnerable_result.finding is not None

    defended_event_bus = EventBus()
    defense_events = []

    defended_event_bus.subscribe(
        EventType.DEFENSE_BLOCKED,
        defense_events.append,
    )

    defended_agent = EnterpriseAgent(
        tool_gateway=ToolGateway(
            tools={
                "customer_lookup": CustomerLookupTool(),
            },
            policy=BasicToolPolicy(
                allowed_tools={"customer_lookup"},
            ),
            event_bus=defended_event_bus,
            evaluation_id=uuid4(),
        ),
        prompt_injection_middleware=PromptInjectionMiddleware(
            detector=PromptInjectionDetector(),
        ),
    )

    defended_runner = EvaluationRunner(
        model_runtime=model,
        target=defended_agent,
        evaluator=evaluator,
        policy=BasicToolPolicy(
            allowed_tools={"customer_lookup"},
        ),
        event_bus=defended_event_bus,
    )

    defended_result = await defended_runner.run(
        attack,
    )

    assert defended_result.evaluation.status.value == "failure"
    assert defended_result.evaluation.score == 0.0
    assert defended_result.finding is None

    assert len(defense_events) == 1
    assert defense_events[0].event_type == EventType.DEFENSE_BLOCKED
    assert defense_events[0].payload["attack_id"] == "PI-001"

    defense_score = calculate_defense_effectiveness(
        attack_success_without_defense=vulnerable_result.evaluation.score,
        attack_success_with_defense=defended_result.evaluation.score,
    )

    assert defense_score.defense_effectiveness == 1.0