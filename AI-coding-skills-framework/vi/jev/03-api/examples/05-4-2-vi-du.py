from enum import Enum
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.typesafe import TypeSafeModel

class Team(str, Enum):
    BILLING = "billing"
    TECH = "tech"
    ACCOUNT = "account"
    OTHER = "other"

class Triage(BaseModel):
    """Classify by the PRIMARY owning team, not the first mention."""

    team: Team = Field(
        description="Which team owns this ticket?"     # ← câu hỏi
    )
    refund_requested: bool = Field(
        description="Does the customer explicitly request a refund?"
    )
    urgency: int = Field(
        description="Urgency of handling this ticket",
        # score levels do TypeSafeModel map từ schema/config
    )

agent = Agent(TypeSafeModel("jev-1.13.0"), output_type=Triage)

result = agent.run_sync(
    "Ticket #4821: charged twice, want refund, very frustrated."
)
print(result.output.team)             # Team.BILLING — typed, closed
print(result.output.refund_requested) # True
