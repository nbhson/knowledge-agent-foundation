@dataclass
class PipelineEvent:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    type: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class PipelineResult:
    success: bool
    data: Any = None
    errors: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)


class Pipeline:
    """
    Advanced Pipeline with branching, transforms, filters, and sinks.
    
    Features:
    - Transform chain
    - Conditional branching
    - Fan-out / Fan-in
    - Error handling per stage
    - Metrics collection
    """
    
    def __init__(self, name: str):
        self.name = name
        self.stages: List[Dict] = []
        self.hooks = {"before": [], "after": [], "on_error": [], "on_stage": []}
        self.metrics = PipelineMetrics()
    
    def add_transform(self, func: Callable, name: str = None) -> "Pipeline":
        self.stages.append({
            "type": "transform",
            "name": name or func.__name__,
            "func": func,
        })
        return self
    
    def add_filter(self, func: Callable, name: str = None) -> "Pipeline":
        self.stages.append({
            "type": "filter",
            "name": name or "filter",
            "func": func,
        })
        return self
    
    def add_branch(self, condition: Callable, true_pipeline: "Pipeline", 
                   false_pipeline: Optional["Pipeline"] = None, name: str = "branch") -> "Pipeline":
        self.stages.append({
            "type": "branch",
            "name": name,
            "condition": condition,
            "true_pipeline": true_pipeline,
            "false_pipeline": false_pipeline,
        })
        return self
    
    def add_fan_out(self, tasks: List[Dict], aggregator: Callable = None) -> "Pipeline":
        """Fan-out: split into parallel tasks, then aggregate"""
        self.stages.append({
            "type": "fan_out",
            "name": "fan_out",
            "tasks": tasks,
            "aggregator": aggregator or (lambda results: results),
        })
        return self
    
    def add_sink(self, func: Callable, name: str = None) -> "Pipeline":
        self.stages.append({
            "type": "sink",
            "name": name or func.__name__,
            "func": func,
        })
        return self
    
    def add_validator(self, func: Callable, name: str = None) -> "Pipeline":
        self.stages.append({
            "type": "validator",
            "name": name or "validate",
            "func": func,
        })
        return self
    
    def on(self, event: str, func: Callable) -> "Pipeline":
        if event in self.hooks:
            self.hooks[event].append(func)
        return self
    
    def run(self, data: Any) -> PipelineResult:
        start_time = time.time()
        errors = []
        
        for hook in self.hooks["before"]:
            hook(self.name, data)
        
        try:
            for stage in self.stages:
                stage_start = time.time()
                stage_name = stage["name"]
                
                for hook in self.hooks["on_stage"]:
                    hook(stage_name, data)
                
                try:
                    if stage["type"] == "transform":
                        data = stage["func"](data)
                    
                    elif stage["type"] == "filter":
                        if not stage["func"](data):
                            return PipelineResult(
                                success=False,
                                errors=[f"Filter '{stage_name}' rejected data"],
                                metrics=self.metrics.get_summary(),
                            )
                    
                    elif stage["type"] == "branch":
                        condition_result = stage["condition"](data)
                        if condition_result and stage["true_pipeline"]:
                            result = stage["true_pipeline"].run(data)
                            data = result.data
                        elif not condition_result and stage["false_pipeline"]:
                            result = stage["false_pipeline"].run(data)
                            data = result.data
                    
                    elif stage["type"] == "fan_out":
                        task_results = {}
                        with ThreadPoolExecutor(max_workers=4) as executor:
                            futures = {}
                            for task in stage["tasks"]:
                                f = executor.submit(task["func"], data)
                                futures[f] = task["name"]
                            for f in as_completed(futures):
                                task_results[futures[f]] = f.result()
                        data = stage["aggregator"](task_results)
                    
                    elif stage["type"] == "validator":
                        valid = stage["func"](data)
                        if not valid:
                            return PipelineResult(
                                success=False,
                                errors=[f"Validation '{stage_name}' failed"],
                                metrics=self.metrics.get_summary(),
                            )
                    
                    elif stage["type"] == "sink":
                        stage["func"](data)
                    
                    stage_duration = (time.time() - stage_start) * 1000
                    self.metrics.record(stage_name, stage_duration, True)
                    
                except Exception as e:
                    stage_duration = (time.time() - stage_start) * 1000
                    self.metrics.record(stage_name, stage_duration, False)
                    errors.append(f"{stage_name}: {str(e)}")
                    
                    for hook in self.hooks["on_error"]:
                        hook(stage_name, e)
                    
                    if stage["type"] != "sink":
                        raise WorkflowError(f"Pipeline stage '{stage_name}' failed: {e}")
            
            total_duration = (time.time() - start_time) * 1000
            
            for hook in self.hooks["after"]:
                hook(self.name, data)
            
            return PipelineResult(
                success=True,
                data=data,
                metrics=self.metrics.get_summary(),
            )
            
        except Exception as e:
            return PipelineResult(
                success=False,
                errors=errors or [str(e)],
                metrics=self.metrics.get_summary(),
            )


class PipelineMetrics:
    def __init__(self):
        self.stages: Dict[str, Dict] = {}
    
    def record(self, stage_name: str, duration_ms: float, success: bool):
        if stage_name not in self.stages:
            self.stages[stage_name] = {
                "runs": 0, "success": 0, "fail": 0, "total_ms": 0
            }
        s = self.stages[stage_name]
        s["runs"] += 1
        s["total_ms"] += duration_ms
        if success:
            s["success"] += 1
        else:
            s["fail"] += 1
    
    def get_summary(self) -> Dict:
        return {
            stage: {
                "runs": s["runs"],
                "avg_ms": round(s["total_ms"] / s["runs"], 2) if s["runs"] else 0,
                "success_rate": round(s["success"] / s["runs"], 2) if s["runs"] else 0,
            }
            for stage, s in self.stages.items()
        }
