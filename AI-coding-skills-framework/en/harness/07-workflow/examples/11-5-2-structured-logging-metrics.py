class WorkflowLogger:
    """Structured logger for workflow"""
    
    def __init__(self, workflow_name: str, log_file: str = None):
        self.workflow_name = workflow_name
        self.logs = []
        self.log_file = log_file
    
    def log_step(self, step: str, status: str, data: Dict = None, duration: float = None):
        entry = {
            "workflow": self.workflow_name,
            "step": step,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "duration_ms": round(duration * 1000, 2) if duration else None,
            "data": data or {},
        }
        self.logs.append(entry)
        
        if self.log_file:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
    
    @contextmanager
    def track(self, step_name: str):
        start = time.time()
        self.log_step(step_name, "start")
        try:
            yield
            duration = time.time() - start
            self.log_step(step_name, "success", duration=duration)
        except Exception as e:
            duration = time.time() - start
            self.log_step(step_name, "error", data={"error": str(e)}, duration=duration)
            raise
    
    def export_json(self, path: str = None) -> str:
        output = json.dumps(self.logs, indent=2, ensure_ascii=False)
        if path:
            with open(path, "w") as f:
                f.write(output)
        return output


class MetricsCollector:
    """Collects and aggregates metrics"""
    
    def __init__(self):
        self.counters: Dict[str, int] = {}
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = {}
    
    def counter(self, name: str, value: int = 1):
        self.counters[name] = self.counters.get(name, 0) + value
    
    def gauge(self, name: str, value: float):
        self.gauges[name] = value
    
    def histogram(self, name: str, value: float):
        if name not in self.histograms:
            self.histograms[name] = []
        self.histograms[name].append(value)
    
    def get_summary(self) -> Dict:
        summary = {
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "histograms": {},
        }
        
        for name, values in self.histograms.items():
            sorted_vals = sorted(values)
            n = len(sorted_vals)
            summary["histograms"][name] = {
                "count": n,
                "min": sorted_vals[0] if n else 0,
                "max": sorted_vals[-1] if n else 0,
                "mean": sum(sorted_vals) / n if n else 0,
                "p50": sorted_vals[n // 2] if n else 0,
                "p95": sorted_vals[int(n * 0.95)] if n else 0,
                "p99": sorted_vals[int(n * 0.99)] if n else 0,
            }
        
        return summary
