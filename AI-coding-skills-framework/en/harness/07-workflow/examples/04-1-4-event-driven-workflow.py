import queue
from typing import Callable, Dict, List, Optional
from datetime import datetime

class EventDrivenWorkflow:
    """
    Workflow reacts to events.
    
    Events trigger handlers, which may emit new events.
    Supports: pub/sub, event filtering, event chains.
    """
    
    def __init__(self, name: str = "event-driven"):
        self.name = name
        self.handlers: Dict[str, List[Callable]] = {}
        self.event_log: List[Dict] = []
        self.event_queue = queue.Queue()
        self._running = False
        self._max_events = 1000
    
    def on(self, event_type: str, handler: Callable):
        """Register handler for event type"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        return self
    
    def emit(self, event_type: str, data: Any = None):
        """Emit an event"""
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "id": str(uuid.uuid4())[:8],
        }
        self.event_queue.put(event)
        self.event_log.append(event)
    
    def process_event(self, event: Dict):
        """Process a single event"""
        event_type = event["type"]
        handlers = self.handlers.get(event_type, [])
        
        if not handlers:
            self.event_log.append({
                **event,
                "status": "unhandled",
                "timestamp": datetime.now().isoformat(),
            })
            return
        
        for handler in handlers:
            try:
                result = handler(event["data"])
                self.event_log.append({
                    **event,
                    "handler": handler.__name__,
                    "status": "processed",
                    "result": str(result)[:200] if result else None,
                    "timestamp": datetime.now().isoformat(),
                })
            except Exception as e:
                self.event_log.append({
                    **event,
                    "handler": handler.__name__,
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                })
    
    def run(self):
        """Process all queued events"""
        self._running = True
        event_count = 0
        
        while self._running and not self.event_queue.empty():
            if event_count >= self._max_events:
                break
            
            try:
                event = self.event_queue.get(timeout=1)
                self.process_event(event)
                event_count += 1
            except queue.Empty:
                break
        
        self._running = False
    
    def stop(self):
        self._running = False
    
    def get_stats(self) -> Dict:
        total = len(self.event_log)
        processed = sum(1 for e in self.event_log if e.get("status") == "processed")
        errors = sum(1 for e in self.event_log if e.get("status") == "error")
        
        event_types = {}
        for e in self.event_log:
            t = e.get("type", "unknown")
            event_types[t] = event_types.get(t, 0) + 1
        
        return {
            "total_events": total,
            "processed": processed,
            "errors": errors,
            "event_types": event_types,
            "queue_size": self.event_queue.qsize(),
        }
