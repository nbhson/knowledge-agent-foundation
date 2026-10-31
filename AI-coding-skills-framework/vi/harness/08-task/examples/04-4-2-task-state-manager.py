from enum import Enum
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime

class TaskStatus(Enum):
    PENDING = "pending"
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    TESTING = "testing"
    REVIEW = "review"
    DONE = "done"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskState:
    """Trạng thái hiện tại của task"""
    task_id: str
    status: TaskStatus = TaskStatus.PENDING
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    progress: float = 0.0        # 0.0 → 1.0
    attempts: int = 0
    last_error: Optional[str] = None
    notes: List[str] = field(default_factory=list)


class TaskStateManager:
    """
    Quản lý lifecycle của tasks — tracks status changes,
    enforces valid transitions, và emits events.
    """
    
    VALID_TRANSITIONS = {
        TaskStatus.PENDING: [
            TaskStatus.PLANNING, TaskStatus.CANCELLED
        ],
        TaskStatus.PLANNING: [
            TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED
        ],
        TaskStatus.IN_PROGRESS: [
            TaskStatus.TESTING, TaskStatus.BLOCKED,
            TaskStatus.FAILED, TaskStatus.DONE,
        ],
        TaskStatus.BLOCKED: [
            TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED,
            TaskStatus.PENDING,
        ],
        TaskStatus.TESTING: [
            TaskStatus.REVIEW, TaskStatus.IN_PROGRESS,
            TaskStatus.FAILED,
        ],
        TaskStatus.REVIEW: [
            TaskStatus.DONE, TaskStatus.IN_PROGRESS,
            TaskStatus.FAILED,
        ],
        TaskStatus.FAILED: [
            TaskStatus.PENDING, TaskStatus.CANCELLED,
        ],
    }
    
    def __init__(self):
        self.states: Dict[str, TaskState] = {}
        self.listeners: List[Callable] = []
    
    def create(self, task_id: str) -> TaskState:
        state = TaskState(task_id=task_id)
        self.states[task_id] = state
        return state
    
    def transition(self, task_id: str, new_status: TaskStatus,
                   note: str = "") -> TaskState:
        """Chuyển trạng thái task — kiểm tra validity"""
        state = self.states.get(task_id)
        if not state:
            raise ValueError(f"Task {task_id} not found")
        
        valid = self.VALID_TRANSITIONS.get(state.status, [])
        if new_status not in valid:
            raise InvalidTransitionError(
                f"Cannot transition from {state.status.value} "
                f"to {new_status.value}"
            )
        
        old_status = state.status
        state.status = new_status
        
        if new_status == TaskStatus.IN_PROGRESS and not state.started_at:
            state.started_at = datetime.now().isoformat()
            state.attempts += 1
        
        if new_status in (TaskStatus.DONE, TaskStatus.FAILED, 
                         TaskStatus.CANCELLED):
            state.completed_at = datetime.now().isoformat()
        
        if note:
            state.notes.append(
                f"[{datetime.now().isoformat()}] {note}"
            )
        
        # Notify listeners
        for listener in self.listeners:
            listener(task_id, old_status, new_status)
        
        return state
    
    def on_transition(self, callback: Callable):
        self.listeners.append(callback)


class InvalidTransitionError(Exception):
    pass
