"""
Consolidation Pipeline: Background process to maintain memory quality.

Runs periodically to:
1. Deduplicate memories
2. Resolve conflicts
3. Apply temporal decay
4. Archive old memories
5. Generate memory statistics
"""

class MemoryConsolidationPipeline:
    """
    Automated pipeline for memory maintenance
    """
    
    def __init__(self, memory_store, config=None):
        self.store = memory_store
        self.config = config or {
            "dedup_threshold": 0.85,
            "conflict_strategy": "temporal",  # temporal, confidence, manual
            "archive_after_days": 90,
            "decay_rate": 0.01,
            "min_confidence": 0.3
        }
        self.stats = {
            "runs": 0,
            "deduped": 0,
            "conflicts_resolved": 0,
            "archived": 0,
            "low_confidence_removed": 0
        }
    
    def run_full_consolidation(self):
        """
        Run complete consolidation pipeline
        
        Returns: ConsolidationReport
        """
        start_time = time.time()
        report = {"stages": {}}
        
        # Stage 1: Deduplication
        dedup_result = self._stage_deduplicate()
        report["stages"]["dedup"] = dedup_result
        
        # Stage 2: Conflict Resolution
        conflict_result = self._stage_resolve_conflicts()
        report["stages"]["conflicts"] = conflict_result
        
        # Stage 3: Temporal Decay
        decay_result = self._stage_apply_decay()
        report["stages"]["decay"] = decay_result
        
        # Stage 4: Archive Old Memories
        archive_result = self._stage_archive()
        report["stages"]["archive"] = archive_result
        
        # Stage 5: Remove Low Confidence
        cleanup_result = self._stage_cleanup()
        report["stages"]["cleanup"] = cleanup_result
        
        # Final report
        elapsed = time.time() - start_time
        report["total_time_ms"] = elapsed * 1000
        report["total_memories"] = self.store.count()
        report["stats"] = self.stats
        self.stats["runs"] += 1
        
        return report
    
    def _stage_deduplicate(self):
        """Remove duplicate memories"""
        memories = self.store.get_all()
        
        # Group by similarity
        duplicates_found = 0
        removed = 0
        
        for i, m1 in enumerate(memories):
            if m1.get("archived") or m1.get("deleted"):
                continue
            
            for m2 in memories[i+1:]:
                if m2.get("archived") or m2.get("deleted"):
                    continue
                
                similarity = self._compute_similarity(
                    m1["content"], m2["content"]
                )
                
                if similarity > self.config["dedup_threshold"]:
                    # Keep the one with higher confidence
                    if m1.get("confidence", 0) >= m2.get("confidence", 0):
                        self.store.soft_delete(m2["id"])
                    else:
                        self.store.soft_delete(m1["id"])
                    removed += 1
        
        self.stats["deduped"] += removed
        return {"duplicates_found": duplicates_found, "removed": removed}
    
    def _stage_resolve_conflicts(self):
        """Resolve conflicting memories"""
        memories = self.store.get_all()
        
        # Group by topic (simplified: same first 5 words)
        topic_groups = {}
        for m in memories:
            if m.get("deleted"):
                continue
            topic_key = " ".join(m["content"].split()[:5])
            if topic_key not in topic_groups:
                topic_groups[topic_key] = []
            topic_groups[topic_key].append(m)
        
        conflicts_resolved = 0
        
        for topic, group in topic_groups.items():
            if len(group) <= 1:
                continue
            
            # Check for actual contradictions
            values = set()
            for m in group:
                values.add(m["content"])
            
            if len(values) > 1:
                # Conflict found — resolve by strategy
                if self.config["conflict_strategy"] == "temporal":
                    # Keep newest
                    group.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
                    for m in group[1:]:
                        self.store.soft_delete(m["id"])
                        conflicts_resolved += 1
                elif self.config["conflict_strategy"] == "confidence":
                    # Keep highest confidence
                    group.sort(key=lambda x: x.get("confidence", 0), reverse=True)
                    for m in group[1:]:
                        self.store.soft_delete(m["id"])
                        conflicts_resolved += 1
        
        self.stats["conflicts_resolved"] += conflicts_resolved
        return {"conflicts_found": len(topic_groups), "resolved": conflicts_resolved}
    
    def _stage_apply_decay(self):
        """Apply temporal decay to memory confidence"""
        memories = self.store.get_all()
        
        decayed = 0
        for m in memories:
            if m.get("deleted") or m.get("archived"):
                continue
            
            age_days = (datetime.now() - 
                       datetime.fromisoformat(m.get("created_at", 
                           datetime.now().isoformat()))).days
            
            # Apply exponential decay
            decay_factor = (1 - self.config["decay_rate"]) ** age_days
            new_confidence = m.get("confidence", 1.0) * decay_factor
            
            if abs(new_confidence - m.get("confidence", 1.0)) > 0.01:
                self.store.update(m["id"], {"confidence": new_confidence})
                decayed += 1
        
        return {"memories_decayed": decayed}
    
    def _stage_archive(self):
        """Archive old, low-access memories"""
        cutoff = datetime.now() - timedelta(
            days=self.config["archive_after_days"]
        )
        
        archived = 0
        memories = self.store.get_all()
        
        for m in memories:
            if m.get("deleted") or m.get("archived"):
                continue
            
            last_accessed = m.get("last_accessed", m.get("updated_at"))
            if last_accessed and datetime.fromisoformat(last_accessed) < cutoff:
                # Archive: move to cold storage
                self.store.archive(m["id"])
                archived += 1
        
        self.stats["archived"] += archived
        return {"archived": archived}
    
    def _stage_cleanup(self):
        """Remove very low confidence memories"""
        removed = 0
        memories = self.store.get_all()
        
        for m in memories:
            if m.get("deleted") or m.get("archived"):
                continue
            
            if m.get("confidence", 1.0) < self.config["min_confidence"]:
                self.store.soft_delete(m["id"])
                removed += 1
        
        self.stats["low_confidence_removed"] += removed
        return {"low_confidence_removed": removed}
    
    def _compute_similarity(self, text1, text2):
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        return len(words1 & words2) / len(words1 | words2)
