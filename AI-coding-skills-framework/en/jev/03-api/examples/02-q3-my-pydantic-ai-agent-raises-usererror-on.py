class Triage(BaseModel):
    """Framing: answer as the support triage desk; evidence is the ticket only."""
    team: Literal["billing", "infra", "bug"] = Field(
        description="Which team should own this ticket?"
    )
    risky: bool = Field(
        description="Does this change remove a safety guardrail?"
    )
