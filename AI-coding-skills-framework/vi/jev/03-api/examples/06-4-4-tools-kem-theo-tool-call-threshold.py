from pydantic_ai.models.fallback import FallbackModel
from pydantic_ai.models.typesafe import TypeSafeModel
from pydantic_ai.models.openai import OpenAIModel

# Jev phía trước (nhanh, rẻ, decide tool/threshold);
# LLM phía sau cho các step cần sinh text / tool arguments
model = FallbackModel(
    TypeSafeModel("jev-1.13.0"),
    OpenAIModel("gpt-5"),                  # fallback khi ToolCallProposed
)

agent = Agent(model, output_type=Triage, tools=[lookup_user, refund_flow])
