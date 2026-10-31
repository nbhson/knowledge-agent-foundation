from dataclasses import dataclass
from typing import Dict, List, Optional, Literal
from datetime import datetime

@dataclass
class GraphEvent:
    id: str
    timestamp: datetime
    action: Literal["CREATE_NODE", "CREATE_EDGE", "UPDATE", "DELETE", "MERGE"]
    payload: Dict
    actor: str  # "user:alice" | "pipeline:etl" | "loop:daily-triage"
    prev_state: Optional[Dict] = None  # for rollback

class GraphAuditLog:
    def __init__(self):
        self.events: List[GraphEvent] = []
    
    def log(self, event: GraphEvent):
        self.events.append(event)
        print(f"  [Audit] {event.action}: {event.payload} by {event.actor}")
    
    def rollback(self, event_id: str, graph):
        """Roll back to before event_id."""
        idx = next(i for i, e in enumerate(self.events) if e.id == event_id)
        target_event = self.events[idx]
        if target_event.prev_state:
            # Restore the prev_state
            print(f"  Rolling back {event_id}: restoring {target_event.prev_state}")
        # Remove events after it
        self.events = self.events[:idx]
    
    def history(self, node_name: str) -> List[GraphEvent]:
        """History of one node."""
        return [e for e in self.events if e.payload.get("name") == node_name or
                e.payload.get("source") == node_name or e.payload.get("target") == node_name]
