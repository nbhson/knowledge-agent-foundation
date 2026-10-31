class WindowMemory:
    """
    Giữ N messages gần nhất
    
    ✅ Token usage cố định
    ✅ Simple implementation
    ❌ Mất context từ messages cũ
    """
    
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.messages = deque(maxlen=window_size)
    
    def add(self, role, content):
        self.messages.append({"role": role, "content": content})
    
    def get_context(self):
        return list(self.messages)
