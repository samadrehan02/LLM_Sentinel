from pydantic import BaseModel


class AgentConfig(BaseModel):
    agent_id: str = "enterprise-assistant"
    name: str = "Enterprise Assistant"

    system_prompt: str = (
        "You are an internal enterprise assistant. "
        "Help employees find information and complete tasks."
    )

    model_name: str = "mock-model"
