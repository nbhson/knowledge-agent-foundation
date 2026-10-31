import json
from datetime import datetime
from typing import Any, Dict, List, Optional

class MemoryWriter:
    """
    Write information back to various memory systems
    
    Supports: Episodic, Semantic, Working memory
    """
    
    def __init__(self, vector_store=None, knowledge_graph=None):
        self.vector_store = vector_store
        self.knowledge_graph = knowledge_graph
        self.episodic_store = []  # Simple list for demo
        self.entity_store = {}
        self.event_log = []
    
    # ─────────────────────────────────────────────
    # EPISODIC MEMORY: Lưu sự kiện
    # ─────────────────────────────────────────────
    def write_episodic(self, event_type, content, metadata=None):
        """
        Ghi một sự kiện vào episodic memory
        
        event_type: "conversation", "learning", "feedback", "decision"
        content: Nội dung sự kiện
        metadata: Thông tin bổ sung
        """
        event = {
            "id": f"ep_{len(self.episodic_store)}",
            "type": event_type,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
        }
        
        self.episodic_store.append(event)
        
        # Also store in vector DB for semantic search
        if self.vector_store:
            embedding = self._get_embedding(content)
            self.vector_store.add(
                document=content,
                vector=embedding,
                metadata={"type": "episodic", **event}
            )
        
        self._log_event("write_episodic", event)
        return event["id"]
    
    def recall_episodic(self, query, top_k=5):
        """Recall relevant episodic memories"""
        if self.vector_store:
            embedding = self._get_embedding(query)
            results = self.vector_store.search(embedding, top_k)
            return [r["metadata"] for r in results]
        
        # Fallback: search by keyword
        query_lower = query.lower()
        matches = [
            e for e in self.episodic_store
            if query_lower in e["content"].lower()
        ]
        return matches[:top_k]
    
    # ─────────────────────────────────────────────
    # SEMANTIC MEMORY: Lưu facts
    # ─────────────────────────────────────────────
    def write_fact(self, subject, predicate, obj, confidence=1.0):
        """
        Ghi một fact vào semantic memory (Knowledge Graph)
        
        Ví dụ: ("BHYT", "mức đóng", "4.5% lương cơ sở", 0.95)
        """
        fact = {
            "subject": subject,
            "predicate": predicate,
            "object": obj,
            "confidence": confidence,
            "created_at": datetime.now().isoformat(),
            "source": "user_conversation",
        }
        
        if self.knowledge_graph:
            self.knowledge_graph.add_triplet(subject, predicate, obj)
        
        # Also vectorize for semantic search
        if self.vector_store:
            fact_text = f"{subject} {predicate} {obj}"
            embedding = self._get_embedding(fact_text)
            self.vector_store.add(
                document=fact_text,
                vector=embedding,
                metadata={"type": "fact", **fact}
            )
        
        self._log_event("write_fact", fact)
        return fact
    
    def update_fact(self, subject, predicate, old_obj, new_obj, reason=""):
        """Update an existing fact"""
        if self.knowledge_graph:
            # Remove old triplet
            self.knowledge_graph.triplets = [
                (s, p, o) for s, p, o in self.knowledge_graph.triplets
                if not (s == subject and p == predicate and o == old_obj)
            ]
            # Add new triplet
            self.knowledge_graph.add_triplet(subject, predicate, new_obj)
        
        update_event = {
            "action": "update_fact",
            "old": {"subject": subject, "predicate": predicate, "object": old_obj},
            "new": {"subject": subject, "predicate": predicate, "object": new_obj},
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        }
        
        self._log_event("update_fact", update_event)
        return update_event
    
    def delete_fact(self, subject, predicate, obj):
        """Delete a fact from knowledge"""
        if self.knowledge_graph:
            self.knowledge_graph.triplets = [
                (s, p, o) for s, p, o in self.knowledge_graph.triplets
                if not (s == subject and p == predicate and o == obj)
            ]
        
        self._log_event("delete_fact", {
            "subject": subject, "predicate": predicate, "object": obj
        })
    
    # ─────────────────────────────────────────────
    # ENTITY MEMORY: Lưu entities
    # ─────────────────────────────────────────────
    def write_entity(self, name, entity_type, attributes=None):
        """Store/update entity information"""
        if name not in self.entity_store:
            self.entity_store[name] = {
                "type": entity_type,
                "attributes": {},
                "created_at": datetime.now().isoformat(),
            }
        
        if attributes:
            self.entity_store[name]["attributes"].update(attributes)
        
        self.entity_store[name]["updated_at"] = datetime.now().isoformat()
        
        self._log_event("write_entity", {"name": name, "type": entity_type})
        return self.entity_store[name]
    
    # ─────────────────────────────────────────────
    # USER PROFILE: Lưu thông tin user
    # ─────────────────────────────────────────────
    def write_user_profile(self, user_id, updates):
        """
        Cập nhật user profile
        
        updates: dict of {field: value}
        Ví dụ: {"occupation": "freelancer", "location": "HCM"}
        """
        profile = self.entity_store.get(f"user_{user_id}", {
            "type": "user",
            "attributes": {},
        })
        
        profile["attributes"].update(updates)
        profile["updated_at"] = datetime.now().isoformat()
        
        self.entity_store[f"user_{user_id}"] = profile
        
        self._log_event("update_profile", {
            "user_id": user_id, 
            "updates": updates
        })
        return profile
    
    def get_user_profile(self, user_id):
        """Retrieve user profile"""
        return self.entity_store.get(f"user_{user_id}", None)
    
    # ─────────────────────────────────────────────
    # FEEDBACK LOOP
    # ─────────────────────────────────────────────
    def write_feedback(self, query, answer, rating, correction=None):
        """
        Store user feedback for improvement
        
        rating: 1-5
        correction: correct answer if user says wrong
        """
        feedback = {
            "query": query,
            "original_answer": answer,
            "rating": rating,
            "correction": correction,
            "timestamp": datetime.now().isoformat(),
        }
        
        if self.vector_store and correction:
            # Store correction as a better example
            embedding = self._get_embedding(query)
            self.vector_store.add(
                document=correction,
                vector=embedding,
                metadata={
                    "type": "correction",
                    "original_answer": answer,
                    "rating": rating,
                }
            )
        
        self._log_event("feedback", feedback)
        return feedback
    
    # ─────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────
    def _get_embedding(self, text):
        """Get embedding using Ollama"""
        import requests
        try:
            response = requests.post("http://localhost:11434/api/embed", json={
                "model": "nomic-embed-text",
                "input": text
            })
            return response.json()["embeddings"][0]
        except Exception:
            return [0.0] * 768
    
    def _log_event(self, event_type, data):
        """Log all write operations for audit trail"""
        self.event_log.append({
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        })
    
    def get_stats(self):
        """Return write statistics"""
        return {
            "episodic_count": len(self.episodic_store),
            "entity_count": len(self.entity_store),
            "event_count": len(self.event_log),
            "event_types": list(set(e["type"] for e in self.event_log)),
        }
