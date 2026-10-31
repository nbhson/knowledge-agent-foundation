from typing import Dict, List, Tuple
from enum import Enum

class ConflictType(Enum):
    CODE_CONFLICT = "code_conflict"
    APPROACH_CONFLICT = "approach_conflict"
    RESOURCE_CONFLICT = "resource_conflict"
    STATE_CONFLICT = "state_conflict"
    OUTPUT_CONFLICT = "output_conflict"


class ConflictResolutionManager:
    """
    Detects and resolves conflicts between agents.
    """
    
    def __init__(self):
        self.file_locks: Dict[str, str] = {}  # file -> agent_id
        self.conflict_log: List[Dict] = []
    
    def acquire_file_lock(self, file_path: str, 
                          agent_id: str) -> bool:
        """Agent requests a lock on a file before modifying it"""
        if file_path in self.file_locks:
            current_holder = self.file_locks[file_path]
            if current_holder != agent_id:
                self.conflict_log.append({
                    "type": ConflictType.CODE_CONFLICT,
                    "file": file_path,
                    "agents": [current_holder, agent_id],
                    "resolution": "blocked",
                })
                return False
        
        self.file_locks[file_path] = agent_id
        return True
    
    def release_file_lock(self, file_path: str, agent_id: str):
        """Agent releases a file lock when done"""
        if self.file_locks.get(file_path) == agent_id:
            del self.file_locks[file_path]
    
    def resolve_approach_conflict(
        self,
        agent_a: Dict,   # {"id": str, "approach": str, "rationale": str}
        agent_b: Dict,
        authority: str = "orchestrator",
    ) -> Dict:
        """
        Resolve a disagreement between 2 agents on approach.
        Uses structured debate with evidence.
        """
        # Score each approach
        score_a = self._score_approach(agent_a)
        score_b = self._score_approach(agent_b)
        
        winner = agent_a if score_a >= score_b else agent_b
        loser = agent_b if score_a >= score_b else agent_a
        
        resolution = {
            "type": ConflictType.APPROACH_CONFLICT,
            "agents": [agent_a["id"], agent_b["id"]],
            "winner": winner["id"],
            "chosen_approach": winner["approach"],
            "scores": {agent_a["id"]: score_a, agent_b["id"]: score_b},
            "resolved_by": authority,
        }
        
        self.conflict_log.append(resolution)
        return resolution
    
    def _score_approach(self, agent: Dict) -> float:
        """Score approach based on rationale quality"""
        rationale = agent.get("rationale", "")
        score = 0.0
        
        # More specific rationale = higher score
        if "because" in rationale.lower():
            score += 0.3
        if "trade-off" in rationale.lower():
            score += 0.2
        if "tested" in rationale.lower() or "proven" in rationale.lower():
            score += 0.3
        if len(rationale) > 100:
            score += 0.2
        
        return min(score, 1.0)
    
    def get_conflict_report(self) -> str:
        """Report conflicts that have occurred"""
        if not self.conflict_log:
            return "No conflicts recorded."
        
        lines = ["=== Conflict Report ==="]
        for i, conflict in enumerate(self.conflict_log, 1):
            lines.append(
                f"\n#{i} [{conflict['type'].value}] "
                f"Agents: {conflict['agents']} "
                f"→ Resolution: {conflict.get('resolution', conflict.get('winner', 'N/A'))}"
            )
        
        return "\n".join(lines)
