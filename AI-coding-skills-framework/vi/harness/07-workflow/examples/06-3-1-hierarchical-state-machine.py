from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Callable, Optional, List, Any

class AgentState(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    PLANNING = "planning"
    READING_CODE = "reading_code"
    WRITING_CODE = "writing_code"
    RUNNING_TESTS = "running_tests"
    FIXING_ERRORS = "fixing_errors"
    REVIEWING = "reviewing"
    COMMITTING = "committing"
    DONE = "done"
    ERROR = "error"
    WAITING_APPROVAL = "waiting_approval"
    ROLLING_BACK = "rolling_back"


@dataclass
class Transition:
    from_state: AgentState
    to_state: AgentState
    condition: Callable[[Dict], bool]
    action: Optional[Callable] = None
    guard: Optional[Callable] = None  # Extra validation
    name: str = ""


class HierarchicalStateMachine:
    """
    Finite State Machine nâng cao cho AI coding agent.
    
    Features:
    - Hierarchical states (parent/child)
    - Guards on transitions
    - Actions on transitions
    - History tracking
    - Max iteration protection
    - State timeout handling
    """
    
    def __init__(self, name: str = "agent"):
        self.name = name
        self.state = AgentState.IDLE
        self.transitions: List[Transition] = []
        self.history: List[Dict] = []
        self.context: Dict = {}
        self.max_history = 100
        self._state_enter_time = time.time()
        self._state_timeouts: Dict[AgentState, float] = {}
    
    def set_timeout(self, state: AgentState, seconds: float):
        """Set timeout for a state (auto-transition to ERROR)"""
        self._state_timeouts[state] = seconds
    
    def add_transition(self, transition: Transition):
        self.transitions.append(transition)
        return self
    
    def can_transition(self, to_state: AgentState) -> bool:
        """Check if transition to target state is possible"""
        for t in self.transitions:
            if t.from_state == self.state and t.to_state == to_state:
                if t.guard and not t.guard(self.context):
                    return False
                return t.condition(self.context)
        return False
    
    def transition(self) -> Optional[Transition]:
        """Try all transitions from current state"""
        for t in self.transitions:
            if t.from_state == self.state and t.condition(self.context):
                # Check guard
                if t.guard and not t.guard(self.context):
                    continue
                
                old_state = self.state
                
                # Execute action
                if t.action:
                    t.action(self.context)
                
                # Record history
                entry = {
                    "from": old_state.value,
                    "to": t.to_state.value,
                    "transition": t.name or f"{old_state.value} → {t.to_state.value}",
                    "context_keys": list(self.context.keys()),
                    "timestamp": datetime.now().isoformat(),
                    "state_duration_ms": round((time.time() - self._state_enter_time) * 1000, 2),
                }
                self.history.append(entry)
                
                # Enforce history limit
                if len(self.history) > self.max_history:
                    self.history = self.history[-self.max_history:]
                
                self.state = t.to_state
                self._state_enter_time = time.time()
                return t
        
        return None
    
    def check_timeout(self) -> bool:
        """Check if current state has timed out"""
        if self.state in self._state_timeouts:
            elapsed = time.time() - self._state_enter_time
            if elapsed > self._state_timeouts[self.state]:
                self.context["error"] = f"State {self.state.value} timed out after {elapsed:.1f}s"
                self.state = AgentState.ERROR
                return True
        return False
    
    def run(self, task: Dict, max_iterations: int = 50) -> Any:
        """Run FSM until DONE or ERROR"""
        self.context["task"] = task
        self._state_enter_time = time.time()
        
        for i in range(max_iterations):
            # Check timeout
            if self.check_timeout():
                break
            
            if self.state == AgentState.DONE:
                return self.context.get("result")
            
            if self.state == AgentState.ERROR:
                raise RuntimeError(f"Agent error: {self.context.get('error')}")
            
            transition = self.transition()
            if not transition:
                break
        
        return self.context.get("result")
    
    def get_state_path(self) -> List[str]:
        """Get the path of states visited"""
        return [h["from"] for h in self.history] + [self.state.value]
    
    def get_stats(self) -> Dict:
        transitions_count = len(self.history)
        state_counts = {}
        for h in self.history:
            state = h["from"]
            state_counts[state] = state_counts.get(state, 0) + 1
        
        return {
            "current_state": self.state.value,
            "total_transitions": transitions_count,
            "state_visits": state_counts,
            "avg_transition_ms": (
                sum(h.get("state_duration_ms", 0) for h in self.history) / transitions_count
                if transitions_count else 0
            ),
        }
