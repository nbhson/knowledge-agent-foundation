from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from enum import Enum
import time


class TriggerType(Enum):
    EVENT = "event"
    SCHEDULED = "scheduled"
    CONDITIONAL = "conditional"
    MANUAL = "manual"


class PipelineStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class PipelineStep:
    """A step in an automation pipeline"""
    name: str
    handler: Callable
    retry_count: int = 2
    timeout_seconds: int = 300
    gate: bool = False              # True = must pass to continue
    rollback: Optional[Callable] = None
    on_failure: Optional[Callable] = None
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineResult:
    """Result of a pipeline run"""
    status: PipelineStatus
    steps_completed: List[str]
    failed_step: Optional[str] = None
    error_message: Optional[str] = None
    duration_seconds: float = 0.0
    artifacts: Dict[str, Any] = field(default_factory=dict)


class AutomationPipeline:
    """
    Framework for automation pipelines with:
    - Sequential steps with gates
    - Automatic retry on failure
    - Rollback support
    - Duration tracking
    """
    
    def __init__(self, name: str):
        self.name = name
        self.steps: List[PipelineStep] = []
        self.pre_hooks: List[Callable] = []
        self.post_hooks: List[Callable] = []
        self.on_failure_hooks: List[Callable] = []
    
    def add_step(self, step: PipelineStep) -> "AutomationPipeline":
        """Add a step to the pipeline (chainable)"""
        self.steps.append(step)
        return self
    
    def step(self, name: str, handler: Callable, 
             gate: bool = False, **kwargs) -> "AutomationPipeline":
        """Shorthand to add a step"""
        self.steps.append(PipelineStep(
            name=name, handler=handler, gate=gate, **kwargs
        ))
        return self
    
    def before(self, hook: Callable) -> "AutomationPipeline":
        """Add a pre-execution hook"""
        self.pre_hooks.append(hook)
        return self
    
    def after(self, hook: Callable) -> "AutomationPipeline":
        """Add a post-execution hook"""
        self.post_hooks.append(hook)
        return self
    
    def on_failure(self, hook: Callable) -> "AutomationPipeline":
        """Add a failure hook"""
        self.on_failure_hooks.append(hook)
        return self
    
    def execute(self, context: Dict[str, Any] = None) -> PipelineResult:
        """Execute the entire pipeline"""
        context = context or {}
        start_time = time.time()
        completed_steps = []
        artifacts = {}
        
        # Run pre-hooks
        for hook in self.pre_hooks:
            hook(context)
        
        for step in self.steps:
            success = False
            last_error = None
            
            for attempt in range(step.retry_count + 1):
                try:
                    result = step.handler(context, artifacts)
                    artifacts[step.name] = result
                    completed_steps.append(step.name)
                    success = True
                    break
                except Exception as e:
                    last_error = str(e)
                    if attempt < step.retry_count:
                        time.sleep(1 * (attempt + 1))  # Backoff
            
            if not success:
                # Gate step failure = pipeline failure
                if step.gate:
                    for hook in self.on_failure_hooks:
                        hook(step.name, last_error, context)
                    
                    # Execute rollback for completed steps
                    for completed_name in reversed(completed_steps):
                        for s in self.steps:
                            if s.name == completed_name and s.rollback:
                                try:
                                    s.rollback(context, artifacts)
                                except Exception:
                                    pass
                    
                    return PipelineResult(
                        status=PipelineStatus.FAILED,
                        steps_completed=completed_steps,
                        failed_step=step.name,
                        error_message=last_error,
                        duration_seconds=time.time() - start_time,
                        artifacts=artifacts,
                    )
        
        # Run post-hooks
        for hook in self.post_hooks:
            hook(context, artifacts)
        
        return PipelineResult(
            status=PipelineStatus.SUCCESS,
            steps_completed=completed_steps,
            duration_seconds=time.time() - start_time,
            artifacts=artifacts,
        )
