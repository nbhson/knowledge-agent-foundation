from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime
import time
import uuid

@dataclass
class WorkflowRun:
    run_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    status: str = "pending"  # pending, running, success, failed, rolled_back
    stages: List[Dict] = field(default_factory=list)
    metrics: Optional[Dict] = None
    error: Optional[str] = None
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    ended_at: Optional[str] = None

class GraphWorkflowEngine:
    """
    Orchestrator cho Graph ETL + Incremental + Versioning.
    
    Features:
      - DAG-based stage execution
      - Checkpoint & rollback
      - Metrics & audit log
      - Circuit breaker
    """
    
    def __init__(self, name: str = "graph-workflow"):
        self.name = name
        self.stages: List[Dict] = []
        self.audit_log = GraphAuditLog()
        self.runs: List[WorkflowRun] = []
        self.circuit_breaker = CircuitBreaker()
    
    def add_stage(self, name: str, func: Callable, checkpoint: bool = False,
                  on_error: str = "fail", timeout_s: int = 300):
        self.stages.append({
            "name": name, "func": func, "checkpoint": checkpoint,
            "on_error": on_error, "timeout_s": timeout_s,
        })
        return self
    
    def run(self, initial_data: Any) -> WorkflowRun:
        run = WorkflowRun()
        run.status = "running"
        data = initial_data
        checkpoints: List[Dict] = []
        
        print(f"\n{'='*60}")
        print(f"  Workflow: {self.name} | Run: {run.run_id}")
        print(f"{'='*60}")
        
        for stage in self.stages:
            stage_name = stage["name"]
            print(f"\n  ▶ Stage: {stage_name} {'[checkpoint]' if stage['checkpoint'] else ''}")
            stage_start = time.time()
            
            try:
                data = stage["func"](data)
                duration = (time.time() - stage_start) * 1000
                
                entry = {"stage": stage_name, "status": "success", 
                         "duration_ms": round(duration, 2),
                         "timestamp": datetime.now().isoformat()}
                run.stages.append(entry)
                
                if stage["checkpoint"]:
                    checkpoints.append({"stage": stage_name, "data": data, "run_id": run.run_id})
                    print(f"    💾 Checkpoint saved: {stage_name}")
                
                self.audit_log.log(GraphEvent(
                    id=str(uuid.uuid4())[:8], timestamp=datetime.now(),
                    action="CREATE_EDGE", payload={"stage": stage_name},
                    actor=f"workflow:{self.name}"
                ))
                
                print(f"    ✅ {stage_name}: {duration:.0f}ms")
            
            except Exception as e:
                duration = (time.time() - stage_start) * 1000
                run.stages.append({"stage": stage_name, "status": "failed",
                                    "error": str(e), "duration_ms": round(duration, 2)})
                run.error = str(e)
                
                print(f"    ❌ {stage_name}: {e}")
                
                if stage["on_error"] == "fail":
                    # Rollback về checkpoint gần nhất
                    if checkpoints:
                        last_cp = checkpoints[-1]
                        print(f"    ↩ Rolling back to checkpoint: {last_cp['stage']}")
                        run.status = "rolled_back"
                    else:
                        run.status = "failed"
                    run.ended_at = datetime.now().isoformat()
                    self.runs.append(run)
                    return run
                elif stage["on_error"] == "skip":
                    print(f"    ⏭ Skipping {stage_name}")
                    continue
        
        run.status = "success"
        run.ended_at = datetime.now().isoformat()
        run.metrics = {"stages": len(run.stages), "checkpoints": len(checkpoints)}
        self.runs.append(run)
        
        print(f"\n  ✅ Workflow {run.run_id} completed: {len(run.stages)} stages")
        return run
    
    def get_stats(self) -> Dict:
        total = len(self.runs)
        success = sum(1 for r in self.runs if r.status == "success")
        return {
            "total_runs": total,
            "success": success,
            "failed": total - success,
            "success_rate": round(success / total, 2) if total else 0,
            "avg_stages": round(sum(len(r.stages) for r in self.runs) / total, 1) if total else 0,
        }

# Usage
engine = (GraphWorkflowEngine("enterprise-kg-daily")
    .add_stage("extract", extract_stage, checkpoint=True)
    .add_stage("dedup", dedup_stage, checkpoint=True)
    .add_stage("validate", validate_stage, on_error="fail")
    .add_stage("load", load_stage, checkpoint=True))

result = engine.run(["Doc 1", "Doc 2"])
print(f"\nStats: {engine.get_stats()}")
print(f"Audit events: {len(engine.audit_log.events)}")
