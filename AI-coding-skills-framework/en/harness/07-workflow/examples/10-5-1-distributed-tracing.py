import time
import uuid
from contextlib import contextmanager
from typing import Dict, List, Any, Optional

class Span:
    """A single unit of work in a trace"""
    
    def __init__(self, name: str, trace_id: str, parent_span_id: str = None):
        self.name = name
        self.span_id = str(uuid.uuid4())[:8]
        self.trace_id = trace_id
        self.parent_span_id = parent_span_id
        self.start_time = time.time()
        self.end_time = None
        self.attributes: Dict[str, Any] = {}
        self.events: List[Dict] = []
        self.status = "OK"
    
    def set_attribute(self, key: str, value: Any):
        self.attributes[key] = value
    
    def add_event(self, name: str, attributes: Dict = None):
        self.events.append({
            "name": name,
            "attributes": attributes or {},
            "timestamp": datetime.now().isoformat(),
        })
    
    def finish(self, status: str = "OK"):
        self.end_time = time.time()
        self.status = status
    
    @property
    def duration_ms(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time) * 1000
        return (time.time() - self.start_time) * 1000
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "span_id": self.span_id,
            "trace_id": self.trace_id,
            "parent_span_id": self.parent_span_id,
            "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
            "end_time": datetime.fromtimestamp(self.end_time).isoformat() if self.end_time else None,
            "duration_ms": round(self.duration_ms, 2),
            "status": self.status,
            "attributes": self.attributes,
            "events": self.events,
        }


class Tracer:
    """
    Distributed tracing system for workflow observability.
    
    Creates traces with nested spans, enabling:
    - End-to-end latency tracking
    - Bottleneck identification
    - Error attribution
    """
    
    _current_trace_id: Optional[str] = None
    _current_span_id: Optional[str] = None
    
    def __init__(self):
        self.traces: Dict[str, List[Span]] = {}
    
    def start_trace(self, name: str) -> str:
        trace_id = str(uuid.uuid4())[:12]
        span = Span(name, trace_id)
        self.traces[trace_id] = [span]
        Tracer._current_trace_id = trace_id
        Tracer._current_span_id = span.span_id
        return trace_id
    
    @contextmanager
    def span(self, name: str, attributes: Dict = None):
        trace_id = Tracer._current_trace_id or str(uuid.uuid4())[:12]
        parent_id = Tracer._current_span_id
        
        new_span = Span(name, trace_id, parent_id)
        if attributes:
            for k, v in attributes.items():
                new_span.set_attribute(k, v)
        
        if trace_id not in self.traces:
            self.traces[trace_id] = []
        self.traces[trace_id].append(new_span)
        
        old_span_id = Tracer._current_span_id
        Tracer._current_span_id = new_span.span_id
        
        try:
            yield new_span
            new_span.finish("OK")
        except Exception as e:
            new_span.set_attribute("error", str(e))
            new_span.finish("ERROR")
            raise
        finally:
            Tracer._current_span_id = old_span_id
    
    def get_trace(self, trace_id: str) -> List[Dict]:
        spans = self.traces.get(trace_id, [])
        return [s.to_dict() for s in sorted(spans, key=lambda s: s.start_time)]
    
    def get_trace_summary(self, trace_id: str) -> Dict:
        spans = self.traces.get(trace_id, [])
        if not spans:
            return {"error": "Trace not found"}
        
        root = min(spans, key=lambda s: s.start_time)
        total_duration = max(s.end_time or time.time() for s in spans) - root.start_time
        
        return {
            "trace_id": trace_id,
            "root_span": root.name,
            "total_spans": len(spans),
            "total_duration_ms": round(total_duration * 1000, 2),
            "errors": sum(1 for s in spans if s.status == "ERROR"),
            "spans": [s.to_dict() for s in spans],
        }
