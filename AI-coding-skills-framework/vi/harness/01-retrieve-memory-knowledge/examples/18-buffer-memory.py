from collections import deque

class BufferMemory:
    """
    Giữ TẤT CẢ messages trong buffer
    
    ✅ Không mất thông tin
    ❌ Token usage tăng linear
    ❌ Context window sẽ đầy
    """
    
    def __init__(self):
        self.messages = []
    
    def add(self, role, content):
        self.messages.append({"role": role, "content": content})
    
    def get_context(self):
        return self.messages  # Return ALL
    
    def get_token_count(self, tokenizer):
        """Estimate token count"""
        total = 0
        for msg in self.messages:
            total += len(tokenizer.encode(msg["content"]))
        return total
