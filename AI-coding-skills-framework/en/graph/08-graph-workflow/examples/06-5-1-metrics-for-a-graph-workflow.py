from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime

@dataclass
class GraphWorkflowMetrics:
    run_id: str
    stage_durations: Dict[str, float] = field(default_factory=dict)
    entities_in: int = 0
    entities_out: int = 0
    relations_in: int = 0
    relations_out: int = 0
    dedup_rate: float = 0.0  # % of entities merged
    error_count: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def summary(self) -> Dict:
        return {
            "run_id": self.run_id,
            "entities": f"{self.entities_in} → {self.entities_out} (dedup {self.dedup_rate:.0%})",
            "relations": f"{self.relations_in} → {self.relations_out}",
            "errors": self.error_count,
            "total_ms": sum(self.stage_durations.values()),
            "stages": self.stage_durations,
        }
