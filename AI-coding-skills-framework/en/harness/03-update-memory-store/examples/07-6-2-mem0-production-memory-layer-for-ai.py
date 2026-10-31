"""
Mem0 Architecture — Production Memory Management

Features:
- Multi-user memory with namespacing
- Automatic fact extraction from conversations
- Temporal decay + relevance scoring
- Memory deduplication and conflict resolution
"""

class Mem0ProductionMemory:
    """
    Production memory system inspired by Mem0 architecture
    """
    
    def __init__(self, vector_store, graph_store=None, llm_func=None):
        self.vector_store = vector_store
        self.graph = graph_store
        self.llm = llm_func
        self.user_memories = {}  # user_id -> [memories]
    
    # ═══════════════════════════════════════════
    # EXTRACT: Auto-extract facts from conversation
    # ═══════════════════════════════════════════
    def extract_and_store(self, messages, user_id, agent_id=None):
        """
        Extract facts from conversation and store them
        
        Pipeline:
        1. LLM extracts facts from conversation
        2. Deduplicate against existing memories
        3. Resolve conflicts with existing facts
        4. Store new unique facts
        """
        
        # Step 1: Extract facts using LLM
        facts = self._extract_facts(messages)
        
        # Step 2: Get existing memories
        existing = self.get_memories(user_id, agent_id)
        
        # Step 3: Deduplicate and resolve conflicts
        new_facts = self._deduplicate(facts, existing)
        conflicts = self._find_conflicts(facts, existing)
        
        # Step 4: Resolve conflicts
        resolved = self._resolve_conflicts(conflicts)
        
        # Step 5: Store new facts
        stored = []
        for fact in new_facts:
            memory = self._store_memory(fact, user_id, agent_id)
            stored.append(memory)
        
        # Step 6: Update graph relationships
        if self.graph:
            for fact in stored:
                self._update_graph(fact)
        
        return {
            "extracted": len(facts),
            "new_stored": len(stored),
            "conflicts_found": len(conflicts),
            "conflicts_resolved": len(resolved),
            "memories": stored
        }
    
    def _extract_facts(self, messages):
        """
        Use LLM to extract factual information from messages
        """
        conversation = "\n".join(
            f"{m['role']}: {m['content']}" for m in messages
        )
        
        prompt = f"""Extract all factual information from this conversation.
For each fact, provide:
- Category: (personal_info, preference, knowledge, event, decision)
- Fact: The factual statement
- Confidence: 0.0-1.0

Conversation:
{conversation}

Return as JSON array:
[{{"category": "...", "fact": "...", "confidence": 0.9}}]"""
        
        if self.llm:
            response = self.llm(prompt)
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return []
        return []
    
    # ═══════════════════════════════════════════
    # DEDUPLICATE: Remove redundant memories
    # ═══════════════════════════════════════════
    def _deduplicate(self, new_facts, existing_memories):
        """
        Remove new facts that are already covered by existing memories
        """
        unique = []
        
        for fact in new_facts:
            is_duplicate = False
            
            for existing in existing_memories:
                similarity = self._compute_similarity(
                    fact['fact'], existing['content']
                )
                
                if similarity > 0.85:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique.append(fact)
        
        return unique
    
    # ═══════════════════════════════════════════
    # CONFLICT RESOLUTION
    # ═══════════════════════════════════════════
    def _find_conflicts(self, new_facts, existing_memories):
        """
        Find cases where new facts contradict existing memories
        """
        conflicts = []
        
        for fact in new_facts:
            for existing in existing_memories:
                # Check if same topic but different value
                if self._is_contradiction(fact['fact'], existing['content']):
                    conflicts.append({
                        "new_fact": fact,
                        "existing_memory": existing,
                        "conflict_type": "contradiction"
                    })
        
        return conflicts
    
    def _resolve_conflicts(self, conflicts):
        """
        Resolve conflicts between new and existing memories
        
        Strategies:
        1. TEMPORAL: Newer information wins
        2. CONFIDENCE: Higher confidence wins
        3. FREQUENCY: More frequently mentioned wins
        4. MANUAL: Ask user to resolve
        """
        resolved = []
        
        for conflict in conflicts:
            new = conflict["new_fact"]
            existing = conflict["existing_memory"]
            
            # Strategy: Temporal + Confidence
            new_score = new.get("confidence", 0.5)
            existing_score = existing.get("confidence", 0.5)
            
            # Newer facts get a slight boost
            if new.get("timestamp", "") > existing.get("timestamp", ""):
                new_score += 0.1
            
            if new_score > existing_score:
                # New fact wins — update existing
                self._update_memory(
                    existing["id"], 
                    new["fact"],
                    reason="temporal_update"
                )
                resolved.append({
                    "action": "updated",
                    "old": existing["content"],
                    "new": new["fact"]
                })
            else:
                # Existing wins — ignore new
                resolved.append({
                    "action": "kept_existing",
                    "existing": existing["content"],
                    "ignored": new["fact"]
                })
        
        return resolved
    
    # ═══════════════════════════════════════════
    # STORAGE
    # ═══════════════════════════════════════════
    def _store_memory(self, fact, user_id, agent_id):
        """Store a fact as a memory"""
        memory = {
            "id": f"mem_{uuid4().hex[:8]}",
            "user_id": user_id,
            "agent_id": agent_id,
            "content": fact["fact"],
            "category": fact.get("category", "unknown"),
            "confidence": fact.get("confidence", 0.5),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "access_count": 0,
            "last_accessed": None,
        }
        
        # Store in vector DB
        embedding = self._get_embedding(fact["fact"])
        self.vector_store.add(
            document=fact["fact"],
            vector=embedding,
            metadata=memory
        )
        
        # Track in user namespace
        key = f"{user_id}:{agent_id}" if agent_id else user_id
        if key not in self.user_memories:
            self.user_memories[key] = []
        self.user_memories[key].append(memory)
        
        return memory
    
    def get_memories(self, user_id, agent_id=None, query=None, limit=20):
        """
        Retrieve memories for a user, optionally filtered by query
        """
        key = f"{user_id}:{agent_id}" if agent_id else user_id
        
        if query:
            # Semantic search
            embedding = self._get_embedding(query)
            results = self.vector_store.search(
                embedding, 
                top_k=limit,
                filter={"user_id": user_id}
            )
            
            # Apply temporal decay
            for r in results:
                age_days = (datetime.now() - 
                           datetime.fromisoformat(r["created_at"])).days
                r["decayed_score"] = r["score"] * (0.99 ** age_days)
            
            # Re-rank by decayed score
            results.sort(key=lambda x: x["decayed_score"], reverse=True)
            
            # Update access count
            for r in results:
                r["access_count"] = r.get("access_count", 0) + 1
                r["last_accessed"] = datetime.now().isoformat()
            
            return results[:limit]
        
        # No query: return all user memories
        return self.user_memories.get(key, [])[:limit]
    
    # ═══════════════════════════════════════════
    # HELPERS
    # ═══════════════════════════════════════════
    def _compute_similarity(self, text1, text2):
        emb1 = self._get_embedding(text1)
        emb2 = self._get_embedding(text2)
        
        import numpy as np
        a, b = np.array(emb1), np.array(emb2)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    
    def _is_contradiction(self, fact1, fact2):
        """Check if two facts contradict each other"""
        # Simple heuristic: same subject, different numbers
        import re
        nums1 = set(re.findall(r'\d+\.?\d*', fact1))
        nums2 = set(re.findall(r'\d+\.?\d*', fact2))
        
        # If same topic words but different numbers → likely contradiction
        words1 = set(fact1.lower().split())
        words2 = set(fact2.lower().split())
        topic_overlap = len(words1 & words2) / max(len(words1 | words2), 1)
        
        return topic_overlap > 0.6 and nums1 != nums2 and len(nums1) > 0
    
    def _get_embedding(self, text):
        import requests
        try:
            resp = requests.post("http://localhost:11434/api/embed", json={
                "model": "nomic-embed-text", "input": text
            })
            return resp.json()["embeddings"][0]
        except Exception:
            return [0.0] * 768
    
    def _update_graph(self, fact):
        """Update knowledge graph with new fact"""
        if self.graph:
            category = fact.get("category", "general")
            self.graph.add_triplet(
                fact["user_id"],
                f"has_{category}",
                fact["content"]
            )
