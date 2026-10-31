from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime
import uuid
import time
import json

class WorkflowError(Exception):
    """Error in workflow"""
    pass

class SequentialWorkflow:
    """Sequential workflow — each step's input is the previous step's output"""
    
    def __init__(self, name: str = "sequential"):
        self.name = name
        self.steps = []
        self.state = {}
        self.history = []
        self.hooks = {"before": [], "after": [], "on_error": [], "on_step": []}
    
    def add_step(self, name: str, func: Callable, **kwargs):
        self.steps.append({"name": name, "func": func, "kwargs": kwargs})
        return self
    
    def on(self, event: str, func: Callable):
        if event in self.hooks:
            self.hooks[event].append(func)
        return self
    
    def run(self, initial_input: Any) -> Any:
        current_input = initial_input
        self.state["status"] = "running"
        self.state["start_time"] = time.time()
        
        for hook in self.hooks["before"]:
            hook(self.name, initial_input)
        
        for i, step in enumerate(self.steps):
            step_name = step["name"]
            step_start = time.time()
            
            for hook in self.hooks["on_step"]:
                hook(step_name, i, len(self.steps))
            
            try:
                result = step["func"](current_input, **step["kwargs"])
                step_duration = time.time() - step_start
                
                self.history.append({
                    "step": step_name,
                    "input_type": type(current_input).__name__,
                    "output_type": type(result).__name__,
                    "status": "success",
                    "duration_ms": round(step_duration * 1000, 2),
                    "timestamp": datetime.now().isoformat(),
                })
                
                current_input = result
                
            except Exception as e:
                step_duration = time.time() - step_start
                error_entry = {
                    "step": step_name,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "status": "failed",
                    "duration_ms": round(step_duration * 1000, 2),
                    "timestamp": datetime.now().isoformat(),
                }
                self.history.append(error_entry)
                self.state["status"] = "failed"
                self.state["failed_step"] = step_name
                
                for hook in self.hooks["on_error"]:
                    hook(step_name, e)
                
                raise WorkflowError(f"Step '{step_name}' failed: {e}")
        
        total_duration = time.time() - self.state["start_time"]
        self.state["status"] = "completed"
        self.state["total_duration_ms"] = round(total_duration * 1000, 2)
        
        for hook in self.hooks["after"]:
            hook(self.name, current_input)
        
        return current_input
    
    def get_history(self) -> List[Dict]:
        return self.history
    
    def get_summary(self) -> Dict:
        total = len(self.history)
        success = sum(1 for h in self.history if h["status"] == "success")
        total_ms = sum(h.get("duration_ms", 0) for h in self.history)
        
        return {
            "workflow": self.name,
            "total_steps": total,
            "successful": success,
            "failed": total - success,
            "total_duration_ms": total_ms,
            "status": self.state.get("status", "unknown"),
        }
