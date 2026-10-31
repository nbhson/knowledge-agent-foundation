class Triage(BaseModel):
    """Phân loại theo đội sở hữu chính, không theo nhắc đầu tiên."""
    team: Team = Field(description="Team nào sở hữu ticket này?")
    refund_requested: bool = Field(
        description="Khách có yêu cầu hoàn tiền không?"   # bắt buộc với bool
    )
