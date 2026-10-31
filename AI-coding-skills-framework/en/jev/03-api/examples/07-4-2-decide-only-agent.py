from typing import Literal
from pydantic import Field
from pydantic_ai import Agent
from pydantic_ai.models.typesafe import TypeSafeModel  # TypeSafeModel
from pydantic_ai.models.fallback import FallbackModel


class Triage(BaseModel):
    """Framing: answer as the support triage desk; evidence is the ticket only."""

    team: Literal["billing", "infra", "bug", "product"] = Field(
        description="Which team should own this ticket?"   # ← the QUESTION
    )
    refund_requested: bool = Field(
        description="Does the customer explicitly ask for money back?"
    )
    urgency: Literal[1, 2, 3] = Field(
        description="Urgency: 1 routine, 2 soon, 3 critical (threat/churn)"
    )


agent = Agent(
    TypeSafeModel("jev-latest"),          # Jev decides…
    output_type=Triage,
    # instructions → FRAMING only; the questions live on the fields
    instructions="Use only the ticket text. Do not speculate about intent.",
)

result = agent.run_sync(
    "Ticket #4821: charged twice, wants $49 back, threatens chargeback by Friday."
)
print(result.output.team)             # "billing"
print(result.output.refund_requested) # True
print(result.output.urgency)          # 3
