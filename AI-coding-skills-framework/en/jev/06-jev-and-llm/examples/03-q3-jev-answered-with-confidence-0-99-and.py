jev_model = TypeSafeModel("jev-latest")       # threshold default 0.6 — retune it
llm_model = FallbackModel("gpt-class", "claude-class")
agent = Agent(FallbackModel(jev_model, llm_model))   # fallback always present
