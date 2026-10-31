from pydantic_ai.models.typesafe import TypeSafeModel
agent = Agent(TypeSafeModel("jev-1.13.0"), output_type=Triage)
