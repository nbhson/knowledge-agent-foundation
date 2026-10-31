from threading import Lock
from typing import Any, Dict, List, Optional
from datetime import datetime

class SharedMemoryManager:
    """
    Thread-safe shared memory for multi-agent systems.
    
    Layers:
    - Global: Project-wide state, accessible by all agents
    - Agent-private: Each agent's own context
    - Artifact store: Files, code, test results
    """
    
    def __init__(self):
        self._lock = Lock()
        self.global_state: Dict[str, Any] = {
            "project_files": [],
            "task_queue": [],
            "completed_tasks": [],
            "decisions": [],
        }
        self.agent_memory: Dict[str, Dict[str, Any]] = {}
        self.artifacts: Dict[str, Any] = {}
        self.change_log: List[Dict] = []
    
    def read_global(self, key: str) -> Any:
        """Read from global memory"""
        with self._lock:
            return self.global_state.get(key)
    
    def write_global(self, key: str, value: Any, 
                     agent_id: str = "system"):
        """Write to global memory"""
        with self._lock:
            old_value = self.global_state.get(key)
            self.global_state[key] = value
            
            self.change_log.append({
                "timestamp": datetime.now().isoformat(),
                "agent": agent_id,
                "key": key,
                "action": "write",
                "old": str(old_value)[:200],
                "new": str(value)[:200],
            })
    
    def update_global(self, key: str, updater: Callable,
                      agent_id: str = "system"):
        """Atomic update — read-modify-write inside the lock"""
        with self._lock:
            current = self.global_state.get(key, {})
            new_value = updater(current)
            self.global_state[key] = new_value
            
            self.change_log.append({
                "timestamp": datetime.now().isoformat(),
                "agent": agent_id,
                "key": key,
                "action": "update",
            })
    
    def get_agent_memory(self, agent_id: str) -> Dict[str, Any]:
        """Get an agent's private memory"""
        with self._lock:
            if agent_id not in self.agent_memory:
                self.agent_memory[agent_id] = {
                    "context": "",
                    "working_set": [],
                    "notes": [],
                }
            return self.agent_memory[agent_id]
    
    def store_artifact(self, name: str, content: Any,
                       agent_id: str = "system"):
        """Store an artifact (file content, test result, etc.)"""
        with self._lock:
            self.artifacts[name] = {
                "content": content,
                "stored_by": agent_id,
                "timestamp": datetime.now().isoformat(),
            }
    
    def get_artifact(self, name: str) -> Optional[Any]:
        """Get an artifact"""
        artifact = self.artifacts.get(name)
        return artifact["content"] if artifact else None
    
    def log_decision(self, decision: str, rationale: str,
                     agent_id: str):
        """Log a technical decision"""
        with self._lock:
            self.global_state["decisions"].append({
                "decision": decision,
                "rationale": rationale,
                "agent": agent_id,
                "timestamp": datetime.now().isoformat(),
            })
    
    def get_summary(self) -> str:
        """Summarize shared memory status"""
        return (
            f"Global keys: {len(self.global_state)}\n"
            f"Agents: {len(self.agent_memory)}\n"
            f"Artifacts: {len(self.artifacts)}\n"
            f"Decisions: {len(self.global_state['decisions'])}\n"
            f"Changes logged: {len(self.change_log)}"
        )
