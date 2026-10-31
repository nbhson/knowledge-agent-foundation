class MemoryConsolidator:
    """
    Consolidate and merge memories to reduce redundancy
    and keep knowledge up-to-date
    """
    
    def __init__(self, vector_store, knowledge_graph, llm_func=None):
        self.vector_store = vector_store
        self.kg = knowledge_graph
        self.llm = llm_func
    
    def consolidate_facts(self, similarity_threshold=0.85):
        """
        Step 1: Find and merge duplicate/similar facts
        """
        if not self.kg or not self.kg.triplets:
            return {"merged": 0, "deleted": 0}
        
        merged = 0
        deleted = 0
        
        # Group facts by subject
        facts_by_subject = {}
        for subj, pred, obj in self.kg.triplets:
            key = (subj, pred)
            if key not in facts_by_subject:
                facts_by_subject[key] = []
            facts_by_subject[key].append(obj)
        
        # For each group, keep only the latest/most complete
        for (subj, pred), objs in facts_by_subject.items():
            if len(objs) <= 1:
                continue
            
            # Find duplicates using text similarity
            unique_objs = []
            for obj in objs:
                is_dup = False
                for unique in unique_objs:
                    if self._text_similarity(obj, unique) > similarity_threshold:
                        is_dup = True
                        break
                if not is_dup:
                    unique_objs.append(obj)
            
            deleted += len(objs) - len(unique_objs)
        
        return {"merged": merged, "deleted": deleted}
    
    def temporal_consolidation(self, max_age_days=30):
        """
        Step 2: Remove outdated facts based on age
        
        Facts older than max_age_days may be outdated
        """
        from datetime import datetime, timedelta
        
        cutoff = datetime.now() - timedelta(days=max_age_days)
        removed = 0
        
        if not self.kg:
            return {"removed": removed}
        
        # Filter by timestamp (if stored in metadata)
        # Simplified: just count for demo
        return {"removed": removed}
    
    def summarize_entities(self, entity_name, llm_func=None):
        """
        Step 3: Generate summary for all facts about an entity
        
        Useful for building entity profiles
        """
        if not self.kg:
            return ""
        
        facts = self.kg.query_entity(entity_name, max_hops=1)
        
        if not facts:
            return f"No information found about {entity_name}"
        
        facts_text = "\n".join(
            f"- {subj} {pred} {obj}" 
            for subj, pred, obj, _ in facts
        )
        
        if llm_func or self.llm:
            func = llm_func or self.llm
            summary = func(
                f"Summarize information about {entity_name}:\n\n{facts_text}\n\nSummary:"
            )
            return summary
        
        return facts_text
    
    def conflict_resolution(self):
        """
        Step 4: Resolve conflicting facts
        
        Strategy: Most recent wins (temporal)
        Alternative: Most trusted source wins (source-based)
        """
        conflicts = []
        
        if not self.kg:
            return conflicts
        
        # Group by subject+predicate
        fact_groups = {}
        for subj, pred, obj in self.kg.triplets:
            key = (subj, pred)
            if key not in fact_groups:
                fact_groups[key] = []
            fact_groups[key].append(obj)
        
        # Find conflicts (same subject+predicate, different objects)
        for key, objs in fact_groups.items():
            if len(set(objs)) > 1:
                conflicts.append({
                    "subject": key[0],
                    "predicate": key[1],
                    "conflicting_values": list(set(objs)),
                    "resolution": "keep_latest",  # or "merge", "manual"
                })
        
        return conflicts
    
    def generate_memory_report(self, llm_func=None):
        """
        Generate a report of current memory state
        
        Useful for debugging and auditing
        """
        report = []
        report.append("=" * 50)
        report.append("MEMORY CONSOLIDATION REPORT")
        report.append("=" * 50)
        
        if self.kg:
            report.append(f"\nTotal triplets: {len(self.kg.triplets)}")
            report.append(f"Unique entities: {len(self.kg.entities)}")
            report.append(f"Predicates: {len(self.kg.predicates)}")
            
            # Community detection
            communities = self.kg.community_detection()
            report.append(f"Communities: {len(communities)}")
            
            for i, comm in enumerate(communities[:5]):
                report.append(f"  Community {i+1}: {', '.join(comm[:5])}")
        
        # Conflicts
        conflicts = self.conflict_resolution()
        report.append(f"\nConflicts found: {len(conflicts)}")
        for c in conflicts[:5]:
            report.append(f"  {c['subject']} → {c['conflicting_values']}")
        
        return "\n".join(report)
    
    def _text_similarity(self, text1, text2):
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        return len(words1 & words2) / len(words1 | words2)
