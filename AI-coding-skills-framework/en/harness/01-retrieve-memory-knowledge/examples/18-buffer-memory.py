from collections import deque

class BufferMemory:
    """
    Keeps ALL messages in the buffer

    ✅ No information is lost
    ❌ Token usage grows linearly
    ❌ The context window will fill up
    """

    def __init__(self):
        self.messages = []

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_context(self):
        return self.messages  # Return everything

    def get_token_count(self, tokenizer):
        """Estimate the token count"""
        total = 0
        for msg in self.messages:
            total += len(tokenizer.encode(msg["content"]))
        return total
