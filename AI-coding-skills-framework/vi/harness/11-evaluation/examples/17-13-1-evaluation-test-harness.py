import time
import json
import statistics
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from enum import Enum


class EvalHarnessTestType(Enum):
    """Các loại test cho evaluation harness"""
    METRIC_ACCURACY = "metric_accuracy"       # Metric outputs correct values
    BENCHMARK_VALIDITY = "benchmark_validity"  # Benchmark has expected structure
    REPRODUCIBILITY = "reproducibility"        # Same input → same output
    COST_TRACKING = "cost_tracking"           # Costs are accurate
    REGRESSION_DETECTION = "regression_detection"  # Detects quality drops
    HUMAN_CALIBRATION = "human_calibration"    # Aligns with human judgment
    EDGE_CASE_HANDLING = "edge_case_handling"  # Handles edge cases


@dataclass
class EvalHarnessTest:
    """Một test case cho evaluation harness"""
    name: str
    test_type: EvalHarnessTestType
    description: str
    handler: Callable
    setup: Optional[Callable] = None
    teardown: Optional[Callable] = None
    timeout: int = 120
    tags: List[str] = field(default_factory=list)
    expected_result: Optional[Any] = None


class EvaluationTestHarness:
    """
    Harness để test evaluation systems itself.
    
    Features:
    - Metric accuracy verification
    - Benchmark validity checks
    - Reproducibility testing
    - Cost tracking validation
    - Regression detection testing
    - Human calibration checks
    """
    
    def __init__(self):
        self.tests: List[EvalHarnessTest] = []
        self.results: List[Dict] = []
    
    def register(self, test: EvalHarnessTest):
        """Register một eval harness test"""
        self.tests.append(test)
    
    def run_all(self) -> Dict:
        """Chạy toàn bộ eval harness tests"""
        self.results = []
        start_time = time.time()
        
        for test in self.tests:
            result = self._run_single(test)
            self.results.append(result)
        
        total_time = time.time() - start_time
        return self._generate_report(total_time)
    
    def run_by_type(self, test_type: EvalHarnessTestType) -> Dict:
        """Chạy tests theo type"""
        self.results = []
        start_time = time.time()
        
        for test in self.tests:
            if test.test_type == test_type:
                result = self._run_single(test)
                self.results.append(result)
        
        total_time = time.time() - start_time
        return self._generate_report(total_time)
    
    def _run_single(self, test: EvalHarnessTest) -> Dict:
        """Chạy một test case"""
        if test.setup:
            try:
                test.setup()
            except Exception as e:
                return {
                    "name": test.name,
                    "type": test.test_type.value,
                    "status": "setup_error",
                    "error": str(e),
                    "duration": 0,
                }
        
        start = time.time()
        try:
            result = test.handler()
            duration = time.time() - start
            
            passed = True
            if test.expected_result is not None:
                passed = result == test.expected_result
            
            return {
                "name": test.name,
                "type": test.test_type.value,
                "status": "passed" if passed else "failed",
                "duration": duration,
                "output": result,
                "expected": test.expected_result,
                "tags": test.tags,
            }
        except AssertionError as e:
            return {
                "name": test.name,
                "type": test.test_type.value,
                "status": "failed",
                "duration": time.time() - start,
                "error": str(e),
                "tags": test.tags,
            }
        except Exception as e:
            return {
                "name": test.name,
                "type": test.test_type.value,
                "status": "error",
                "duration": time.time() - start,
                "error": str(e),
                "tags": test.tags,
            }
        finally:
            if test.teardown:
                try:
                    test.teardown()
                except Exception:
                    pass
    
    def _generate_report(self, total_time: float) -> Dict:
        """Tạo test report"""
        passed = sum(1 for r in self.results if r["status"] == "passed")
        failed = sum(1 for r in self.results if r["status"] == "failed")
        errors = sum(1 for r in self.results if r["status"] == "error")
        
        return {
            "summary": {
                "total": len(self.results),
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "pass_rate": f"{(passed / len(self.results) * 100):.1f}%",
                "total_duration": f"{total_time:.2f}s",
            },
            "by_type": self._group_by_type(),
            "results": self.results,
            "gate_passed": failed == 0 and errors == 0,
        }
    
    def _group_by_type(self) -> Dict:
        """Group results by test type"""
        groups: Dict[str, List] = {}
        for result in self.results:
            t = result["type"]
            if t not in groups:
                groups[t] = []
            groups[t].append(result)
        
        return {
            t: {
                "total": len(results),
                "passed": sum(1 for r in results if r["status"] == "passed"),
            }
            for t, results in groups.items()
        }


# ═══════════════════════════════════════════════════════════════
# Usage Example
# ═══════════════════════════════════════════════════════════════

def test_metric_accuracy():
    """Test that pass@k metric computes correctly"""
    evaluator = PassAtKEvaluator()
    # 3 correct out of 5 → pass@1 should be 0.6
    result = evaluator.compute(k=1, total=5, correct=3)
    assert abs(result - 0.6) < 0.01, f"Expected 0.6, got {result}"

def test_benchmark_reproducibility():
    """Test that running same benchmark twice gives same results"""
    bench = SimpleBenchmark(seed=42)
    result1 = bench.run(tasks=["task1", "task2"])
    result2 = bench.run(tasks=["task1", "task2"])
    assert result1 == result2, "Benchmark results not reproducible"

def test_cost_tracking():
    """Test that cost tracking is accurate"""
    tracker = CostTracker(model="gpt-4o")
    tracker.record(input_tokens=1000, output_tokens=500)
    assert tracker.total_cost > 0
    assert tracker.total_cost < 0.01  # Should be very small for this usage


# Register tests
harness = EvaluationTestHarness()

harness.register(EvalHarnessTest(
    name="Pass@K Accuracy",
    test_type=EvalHarnessTestType.METRIC_ACCURACY,
    description="Verify pass@k metric computation",
    handler=test_metric_accuracy,
    tags=["metric", "correctness"],
))

harness.register(EvalHarnessTest(
    name="Benchmark Reproducibility",
    test_type=EvalHarnessTestType.REPRODUCIBILITY,
    description="Verify benchmark produces consistent results",
    handler=test_benchmark_reproducibility,
    tags=["benchmark", "reliability"],
))

harness.register(EvalHarnessTest(
    name="Cost Tracking Accuracy",
    test_type=EvalHarnessTestType.COST_TRACKING,
    description="Verify cost tracking is accurate",
    handler=test_cost_tracking,
    tags=["cost", "tracking"],
))

# Run
# report = harness.run_all()
# print(json.dumps(report, indent=2))
