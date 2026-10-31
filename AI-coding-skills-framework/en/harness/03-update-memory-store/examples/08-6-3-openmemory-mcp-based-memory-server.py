"""
OpenMemory Pattern: Memory as a Service via MCP Protocol

Memory operations exposed as MCP tools:
- create_memory(content, metadata)
- search_memory(query, user_id)
- update_memory(memory_id, content)
- delete_memory(memory_id)
- list_memories(user_id, category)
"""

class OpenMemoryServer:
    """
    Memory server following MCP protocol pattern
    Exposes memory operations as tools
    """
    
    def __init__(self, storage_backend):
        self.storage = storage_backend
        self.tools = {
            "create_memory": self.create_memory,
            "search_memory": self.search_memory,
            "update_memory": self.update_memory,
            "delete_memory": self.delete_memory,
            "list_memories": self.list_memories,
            "consolidate_memories": self.consolidate,
        }
    
    def create_memory(self, content, user_id, category="general",
                       metadata=None):
        """Create a new memory entry"""
        memory = {
            "id": str(uuid4()),
            "content": content,
            "user_id": user_id,
            "category": category,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "embedding": self._get_embedding(content)
        }
        
        # Store with vector index
        self.storage.insert(memory)
        
        return {
            "success": True,
            "memory_id": memory["id"],
            "message": f"Memory created: {content[:50]}..."
        }
    
    def search_memory(self, query, user_id=None, 
                       category=None, limit=10):
        """Semantic search over memories"""
        query_embedding = self._get_embedding(query)
        
        filters = {}
        if user_id:
            filters["user_id"] = user_id
        if category:
            filters["category"] = category
        
        results = self.storage.search(
            embedding=query_embedding,
            filters=filters,
            top_k=limit
        )
        
        # Apply relevance scoring
        for r in results:
            r["relevance"] = self._score_relevance(r, query)
        
        results.sort(key=lambda x: x["relevance"], reverse=True)
        
        return {
            "memories": results,
            "count": len(results),
            "query": query
        }
    
    def update_memory(self, memory_id, content, 
                       reason="user_update"):
        """Update an existing memory"""
        old = self.storage.get(memory_id)
        if not old:
            return {"success": False, "error": "Memory not found"}
        
        # Archive old version
        self.storage.archive_version(memory_id, old)
        
        # Update
        old["content"] = content
        old["embedding"] = self._get_embedding(content)
        old["updated_at"] = datetime.now().isoformat()
        old["update_reason"] = reason
        
        self.storage.update(memory_id, old)
        
        return {
            "success": True,
            "memory_id": memory_id,
            "previous_content": old["content"]
        }
    
    def delete_memory(self, memory_id, soft=True):
        """Delete a memory (soft or hard)"""
        if soft:
            # Soft delete: mark as deleted but keep in storage
            self.storage.update(memory_id, {
                "deleted": True,
                "deleted_at": datetime.now().isoformat()
            })
        else:
            # Hard delete: permanently remove
            self.storage.delete(memory_id)
        
        return {"success": True, "memory_id": memory_id, "type": "soft" if soft else "hard"}
    
    def consolidate(self, user_id, similarity_threshold=0.85):
        """
        Consolidate memories: merge duplicates, resolve conflicts
        """
        memories = self.storage.get_all(user_id=user_id)
        
        # Find duplicates
        duplicates = self._find_duplicates(memories, similarity_threshold)
        
        # Merge duplicates
        merged = 0
        for group in duplicates:
            primary = group[0]  # Keep the oldest
            for dup in group[1:]:
                # Merge content
                primary["content"] = self._merge_content(
                    primary["content"], dup["content"]
                )
                # Delete duplicate
                self.storage.delete(dup["id"])
                merged += 1
        
        # Find conflicts
        conflicts = self._find_all_conflicts(memories)
        
        return {
            "memories_before": len(memories),
            "duplicates_merged": merged,
            "conflicts_found": len(conflicts),
            "memories_after": len(memories) - merged
        }
    
    def _score_relevance(self, memory, query):
        """Score memory relevance considering multiple factors"""
        # Base: vector similarity
        base_score = memory.get("score", 0)
        
        # Recency boost (newer = more relevant)
        age_days = (datetime.now() - 
                   datetime.fromisoformat(memory["created_at"])).days
        recency = max(0, 1 - age_days / 365)
        
        # Access frequency boost
        access_freq = memory.get("access_count", 0) / 10
        
        # Combined score
        return (base_score * 0.6 + 
                recency * 0.2 + 
                min(access_freq, 0.2))
    
    def _find_duplicates(self, memories, threshold):
        """Group similar memories together"""
        groups = []
        used = set()
        
        for i, m1 in enumerate(memories):
            if i in used or m1.get("deleted"):
                continue
            
            group = [m1]
            for j, m2 in enumerate(memories[i+1:], i+1):
                if j in used or m2.get("deleted"):
                    continue
                
                sim = self._compute_similarity(
                    m1["content"], m2["content"]
                )
                if sim > threshold:
                    group.append(m2)
                    used.add(j)
            
            if len(group) > 1:
                groups.append(group)
                used.add(i)
        
        return groups
