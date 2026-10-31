class SummaryMemory:
    """
    Summarizes older messages, keeps the most recent ones

    ✅ Balances information and token usage
    ❌ The summary may lose details
    ❌ Requires an LLM to summarize
    """

    def __init__(self, window_size=5, llm_func=None):
        self.window_size = window_size
        self.messages = deque(maxlen=window_size)
        self.summary = ""
        self.llm = llm_func

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_context(self):
        context = []

        if self.summary:
            context.append({
                "role": "system",
                "content": f"Summary of the previous conversation:\n{self.summary}"
            })

        context.extend(list(self.messages))
        return context

    def update_summary(self):
        """Summarize all messages except the recent window"""
        if len(self.messages) <= self.window_size:
            return

        # Messages to summarize
        old_messages = list(self.messages)[:-self.window_size]

        conversation = "\n".join([
            f"{m['role']}: {m['content']}" for m in old_messages
        ])

        if self.llm:
            self.summary = self.llm(
                f"Summarize concisely:\n{conversation}\n\nSummary:"
            )
