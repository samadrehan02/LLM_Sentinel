from datetime import datetime, UTC
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Campaign(BaseModel):
    campaign_id: UUID = Field(default_factory=uuid4)

    name: str
    target_id: str

    attack_ids: list[str] = Field(default_factory=list)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )
