from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable
from datetime import datetime
import time

@dataclass
class ETLResult:
    success: bool
    entities_in: int = 0
    entities_out: int = 0
    relations_in: int = 0
    relations_out: int = 0
    errors: List[str] = field(default_factory=list)
    duration_ms: float = 0

class GraphETLPipeline:
    """
    ETL Pipeline cho Knowledge Graph.
    
    Stages: Extract → Transform (dedup) → Validate → Load
    Mỗi stage có error handling + metrics.
    """
    
    def __init__(self, name: str = "graph-etl"):
        self.name = name
        self.stages: List[Dict] = []
        self.metrics: Dict[str, Dict] = {}
    
    def add_stage(self, name: str, func: Callable, on_error: str = "fail"):
        """
        on_error: "fail" (dừng pipeline) | "skip" (bỏ qua stage) | "retry"
        """
        self.stages.append({"name": name, "func": func, "on_error": on_error})
        return self
    
    def run(self, data: Any) -> ETLResult:
        start = time.time()
        result = ETLResult(success=True)
        
        for stage in self.stages:
            stage_start = time.time()
            stage_name = stage["name"]
            print(f"  ▶ Stage: {stage_name}")
            
            try:
                data = stage["func"](data)
                duration = (time.time() - stage_start) * 1000
                self.metrics[stage_name] = {"status": "success", "duration_ms": round(duration, 2)}
                print(f"    ✅ {stage_name}: {duration:.0f}ms")
            
            except Exception as e:
                duration = (time.time() - stage_start) * 1000
                self.metrics[stage_name] = {"status": "failed", "error": str(e), "duration_ms": round(duration, 2)}
                result.errors.append(f"{stage_name}: {e}")
                print(f"    ❌ {stage_name}: {e}")
                
                if stage["on_error"] == "fail":
                    result.success = False
                    result.duration_ms = (time.time() - start) * 1000
                    return result
                elif stage["on_error"] == "skip":
                    print(f"    ⏭ Skipping {stage_name}")
                    continue
        
        result.duration_ms = (time.time() - start) * 1000
        return result

# Usage: định nghĩa pipeline
def extract_stage(data: List[str]) -> Dict:
    all_entities, all_relations = [], []
    for doc in data:
        # Gọi LLM extraction (từ 02-knowledge-graph)
        # entities = extract_entities(doc)
        # relations = extract_relations(doc, entities)
        entities = [{"name": "Alice", "type": "Person"}]  # mock
        relations = [{"source": "Alice", "target": "Phoenix", "type": "WORKS_ON"}]
        all_entities.extend(entities)
        all_relations.extend(relations)
    return {"entities": all_entities, "relations": all_relations, "raw_count": len(data)}

def dedup_stage(data: Dict) -> Dict:
    # Deduplicate (từ 02-knowledge-graph)
    # canonical, mapping = deduplicate_entities(data["entities"])
    print(f"    Dedup: {len(data['entities'])} -> {len(data['entities'])} entities")
    return data

def validate_stage(data: Dict) -> Dict:
    # Validate against ontology (từ 02-knowledge-graph)
    print(f"    Validate: {len(data['entities'])} entities, {len(data['relations'])} relations")
    return data

def load_stage(data: Dict) -> Dict:
    # Load vào Neo4j/Kuzu (từ 03-graph-storage)
    print(f"    Load: {len(data['entities'])} entities → Neo4j")
    return data

pipeline = (GraphETLPipeline("enterprise-kg")
    .add_stage("extract", extract_stage)
    .add_stage("dedup", dedup_stage)
    .add_stage("validate", validate_stage)
    .add_stage("load", load_stage))

result = pipeline.run(["Doc 1: Alice works on Phoenix", "Doc 2: Bob manages Carol"])
print(f"Pipeline: success={result.success}, duration={result.duration_ms:.0f}ms")
print(f"Metrics: {pipeline.metrics}")
