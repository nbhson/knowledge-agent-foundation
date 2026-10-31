class MemoryManager:
    """
    Complete memory system combining multiple strategies
    """
    
    def __init__(self, llm_model="gemma3:12b"):
        self.llm_model = llm_model
        self.ollama_url = "http://localhost:11434"
        
        # Different memory types
        self.core_memory = {}  # Always in context
        self.conversation = deque(maxlen=20)  # Short-term
        self.summary = ""  # Compressed history
        self.entity_memory = EntityMemory()  # Entities
        self.semantic_memory = None  # Vector store (optional)
        
        # Stats
        self.stats = {
            "total_messages": 0,
            "total_tokens_used": 0,
        }
    
    def update_core_memory(self, key, value):
        """Update core memory (always in context)"""
        self.core_memory[key] = value
    
    def add_message(self, role, content):
        """Add message to conversation"""
        self.conversation.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })
        self.stats["total_messages"] += 1
        
        # Extract entities
        if role == "user":
            self.entity_memory.extract_and_update(content, self._llm_call)
    
    def get_context(self, strategy="smart"):
        """
        Get context based on strategy
        
        Strategies:
        - buffer: All messages
        - window: Last N messages
        - summary: Summary + recent
        - smart: Dynamic based on token budget
        """
        context = []
        
        # Core memory (always)
        if self.core_memory:
            core_text = "\n".join(
                f"- {k}: {v}" for k, v in self.core_memory.items()
            )
            context.append({
                "role": "system",
                "content": f"Core Memory:\n{core_text}"
            })
        
        # Entity memory
        entity_context = self.entity_memory.get_context_string()
        if entity_context:
            context.append({
                "role": "system",
                "content": f"Known Entities:\n{entity_context}"
            })
        
        # Conversation strategy
        if strategy == "buffer":
            context.extend(list(self.conversation))
        elif strategy == "window":
            context.extend(list(self.conversation)[-10:])
        elif strategy == "summary":
            if self.summary:
                context.append({
                    "role": "system",
                    "content": f"Previous context summary:\n{self.summary}"
                })
            context.extend(list(self.conversation)[-5:])
        elif strategy == "smart":
            # Dynamic strategy based on token budget
            budget_remaining = 8000  # tokens for conversation
            
            # Start with recent messages
            recent = list(self.conversation)[-10:]
            recent_tokens = sum(
                len(m["content"].split()) for m in recent
            ) * 1.3  # rough token estimate
            
            if recent_tokens < budget_remaining:
                context.extend(recent)
                
                # Add summary if we have budget
                if self.summary and budget_remaining - recent_tokens > 200:
                    context.insert(-len(recent), {
                        "role": "system",
                        "content": f"Summary:\n{self.summary}"
                    })
            else:
                # Too many messages, use summary
                if self.summary:
                    context.append({
                        "role": "system",
                        "content": f"Summary:\n{self.summary}"
                    })
                context.extend(list(self.conversation)[-5:])
        
        return context
    
    def update_summary(self):
        """Update conversation summary"""
        if len(self.conversation) < 10:
            return
        
        old_messages = list(self.conversation)[:-5]
        conversation_text = "\n".join(
            f"{m['role']}: {m['content'][:200]}" for m in old_messages
        )
        
        prompt = f"""Tóm tắt cuộc hội thoại sau trong 3-5 câu:

{conversation_text}

Tóm tắt:"""
        
        self.summary = self._llm_call(prompt)
    
    def _llm_call(self, prompt):
        """Call LLM"""
        response = requests.post(f"{self.ollama_url}/api/generate", json={
            "model": self.llm_model,
            "prompt": prompt,
            "stream": False
        })
        return response.json()["response"]
    
    def get_stats(self):
        """Return memory statistics"""
        return {
            **self.stats,
            "core_memory_size": len(self.core_memory),
            "conversation_length": len(self.conversation),
            "entity_count": len(self.entity_memory.entities),
            "has_summary": bool(self.summary),
        }
