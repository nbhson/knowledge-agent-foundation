import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List
from datetime import datetime

@dataclass
class BenchmarkResult:
    """Benchmark result for a task"""
    task_id: str
    task_description: str
    tokens_used: int = 0
    execution_time_s: float = 0.0
    success: bool = False
    quality_score: float = 0.0
    attempts: int = 0
    error_message: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )


class BenchmarkSuite:
    """
    Benchmark suite for an AI coding agent.
    
    Run many tasks, collect metrics, and compare
    across runs/models/configurations.
    """
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.results: List[BenchmarkResult] = []
        self.tasks: List[Dict] = []
    
    def add_task(self, task_id: str, description: str,
                 input_data: Any = None,
                 expected_output: Any = None,
                 validator: Callable = None):
        """Add a task to the benchmark suite"""
        self.tasks.append({
            "id": task_id,
            "description": description,
            "input": input_data,
            "expected": expected_output,
            "validator": validator,
        })
    
    def run(self, agent_func: Callable, max_retries: int = 3):
        """
        Run the benchmark — run the agent on each task.
        
        agent_func: function(task) -> (output, tokens_used)
        """
        for task in self.tasks:
            result = BenchmarkResult(
                task_id=task["id"],
                task_description=task["description"],
            )
            
            start_time = time.time()
            
            for attempt in range(max_retries):
                try:
                    output, tokens = agent_func(task)
                    result.execution_time_s = time.time() - start_time
                    result.tokens_used = tokens
                    result.attempts = attempt + 1
                    
                    # Validate
                    if task.get("validator"):
                        result.success = task["validator"](output)
                    elif task.get("expected"):
                        result.success = output == task["expected"]
                    else:
                        result.success = True
                    
                    if result.success:
                        break
                        
                except Exception as e:
                    result.error_message = str(e)
                    result.attempts = attempt + 1
            
            self.results.append(result)
        
        return self.get_summary()
    
    def get_summary(self) -> Dict:
        """Summarize the benchmark results"""
        if not self.results:
            return {"total": 0}
        
        successful = [r for r in self.results if r.success]
        failed = [r for r in self.results if not r.success]
        
        total_tokens = sum(r.tokens_used for r in self.results)
        total_time = sum(r.execution_time_s for r in self.results)
        
        return {
            "suite": self.name,
            "total_tasks": len(self.results),
            "successful": len(successful),
            "failed": len(failed),
            "success_rate": len(successful) / len(self.results),
            "total_tokens": total_tokens,
            "avg_tokens": total_tokens / len(self.results),
            "total_time_s": total_time,
            "avg_time_s": total_time / len(self.results),
            "avg_attempts": sum(
                r.attempts for r in self.results
            ) / len(self.results),
        }
    
    def compare_with(self, other_suite: "BenchmarkSuite") -> Dict:
        """Compare two benchmark suites"""
        s1 = self.get_summary()
        s2 = other_suite.get_summary()
        
        return {
            self.name: s1,
            other_suite.name: s2,
            "improvements": {
                "success_rate": (
                    s1["success_rate"] - s2["success_rate"]
                ),
                "avg_tokens": (
                    s2["avg_tokens"] - s1["avg_tokens"]
                ),
                "avg_time": (
                    s2["avg_time_s"] - s1["avg_time_s"]
                ),
            },
        }
