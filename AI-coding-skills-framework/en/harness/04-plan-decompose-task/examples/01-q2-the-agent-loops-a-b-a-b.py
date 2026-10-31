class Task:                      # guardrails nằm trên từng task
    max_retries = 3; timeout_seconds = 300
    token_budget = None; tools_allowed = []

class ReActAgent:
    def __init__(self, tools, llm_func, max_steps=10):
        self.max_steps = max_steps   # outer loop guardrail
