from pydantic_ai.models.fallback import FallbackModel

model = FallbackModel(
    TypeSafeModel("jev-1.13.0"),    # quyết định trước, nhanh và rẻ
    OpenAIModel("gpt-5"),           # nhận cả bước khi Jev kẹt
)
agent = Agent(model, output_type=Triage, tools=[refresh_dashboard])
