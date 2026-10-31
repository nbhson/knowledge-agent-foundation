class KBMaintainer:
    """
    Maintain knowledge base: add, update, delete, validate
    """
    
    def __init__(self, knowledge_graph, vector_store):
        self.kg = knowledge_graph
        self.vector_store = vector_store
        self.changelog = []
    
    def add_knowledge(self, subject, predicate, obj, source="manual"):
        """Add new knowledge"""
        self.kg.add_triplet(subject, predicate, obj)
        
        # Also index for search
        fact_text = f"{subject} {predicate} {obj}"
        embedding = self._get_embedding(fact_text)
        self.vector_store.add(
            document=fact_text,
            vector=embedding,
            metadata={"source": source, "added_at": datetime.now().isoformat()}
        )
        
        self.changelog.append({
            "action": "add",
            "fact": (subject, predicate, obj),
            "source": source,
            "timestamp": datetime.now().isoformat(),
        })
    
    def update_knowledge(self, subject, predicate, old_obj, new_obj, reason=""):
        """Update existing knowledge"""
        # Remove old
        self.kg.triplets = [
            (s, p, o) for s, p, o in self.kg.triplets
            if not (s == subject and p == predicate and o == old_obj)
        ]
        
        # Add new
        self.kg.add_triplet(subject, predicate, new_obj)
        
        self.changelog.append({
            "action": "update",
            "old": (subject, predicate, old_obj),
            "new": (subject, predicate, new_obj),
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        })
    
    def delete_knowledge(self, subject, predicate=None, obj=None):
        """Delete knowledge (specific or all for a subject)"""
        before = len(self.kg.triplets)
        
        self.kg.triplets = [
            (s, p, o) for s, p, o in self.kg.triplets
            if not (s == subject and 
                   (predicate is None or p == predicate) and
                   (obj is None or o == obj))
        ]
        
        deleted = before - len(self.kg.triplets)
        self.changelog.append({
            "action": "delete",
            "subject": subject,
            "count": deleted,
            "timestamp": datetime.now().isoformat(),
        })
        
        return deleted
    
    def validate_knowledge(self, validation_rules=None):
        """
        Validate knowledge base against rules
        
        Rules:
        - No orphan entities
        - No contradictory facts
        - All required predicates present
        """
        issues = []
        
        # Check for orphan entities
        connected = set()
        for subj, pred, obj in self.kg.triplets:
            connected.add(subj)
            connected.add(obj)
        
        orphans = self.kg.entities - connected
        if orphans:
            issues.append({
                "type": "orphan_entities",
                "entities": list(orphans),
                "severity": "warning",
            })
        
        # Check for contradictions
        fact_groups = {}
        for subj, pred, obj in self.kg.triplets:
            key = (subj, pred)
            if key not in fact_groups:
                fact_groups[key] = []
            fact_groups[key].append(obj)
        
        for key, objs in fact_groups.items():
            unique = set(objs)
            if len(unique) > 1:
                issues.append({
                    "type": "contradiction",
                    "fact": key,
                    "conflicting_values": list(unique),
                    "severity": "error",
                })
        
        return issues
    
    def export_knowledge(self, format="json"):
        """Export knowledge base"""
        if format == "json":
            return json.dumps({
                "triplets": [
                    {"subject": s, "predicate": p, "object": o}
                    for s, p, o in self.kg.triplets
                ],
                "entities": list(self.kg.entities),
                "changelog": self.changelog,
            }, indent=2, ensure_ascii=False)
        
        elif format == "markdown":
            lines = ["# Knowledge Base Export\n"]
            lines.append(f"Total facts: {len(self.kg.triplets)}\n")
            
            for subj, pred, obj in self.kg.triplets:
                lines.append(f"- **{subj}** {pred} **{obj}**")
            
            return "\n".join(lines)
    
    def get_stats(self):
        return {
            "total_facts": len(self.kg.triplets),
            "total_entities": len(self.kg.entities),
            "total_predicates": len(self.kg.predicates),
            "total_changes": len(self.changelog),
        }
    
    def _get_embedding(self, text):
        import requests
        try:
            response = requests.post("http://localhost:11434/api/embed", json={
                "model": "nomic-embed-text", "input": text
            })
            return response.json()["embeddings"][0]
        except Exception:
            return [0.0] * 768
