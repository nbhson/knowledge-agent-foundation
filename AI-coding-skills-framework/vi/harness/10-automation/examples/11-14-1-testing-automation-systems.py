import time
import json
import hashlib
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from enum import Enum
from pathlib import Path


class AutomationTestType(Enum):
    """Các loại test cho automation systems"""
    PIPELINE_CONFIG = "pipeline_config"      # Validate pipeline configs
    STEP_EXECUTION = "step_execution"        # Test individual steps
    ROLLBACK = "rollback"                    # Test rollback mechanisms
    CIRCUIT_BREAKER = "circuit_breaker"      # Test circuit breaker
    INTEGRATION = "integration"              # End-to-end pipeline test
    CHAOS = "chaos"                          # Chaos testing
    PERFORMANCE = "performance"              # Throughput & latency


@dataclass
class AutomationTest:
    """Một test case cho automation system"""
    name: str
    test_type: AutomationTestType
    description: str
    handler: Callable
    setup: Optional[Callable] = None
    teardown: Optional[Callable] = None
    timeout: int = 60
    tags: List[str] = field(default_factory=list)
    expected_result: Optional[Any] = None


class AutomationTestHarness:
    """
    Harness để test các automation components.
    
    Features:
    - Pipeline config validation
    - Step execution testing
    - Rollback verification
    - Circuit breaker testing
    - Chaos engineering
    - Performance benchmarks
    """
    
    def __init__(self):
        self.tests: List[AutomationTest] = []
        self.results: List[Dict] = []
        self.suite_metrics: Dict[str, Any] = {}
    
    def register(self, test: AutomationTest):
        """Register một automation test"""
        self.tests.append(test)
    
    def run_all(self) -> Dict:
        """Chạy toàn bộ automation tests"""
        self.results = []
        start_time = time.time()
        
        for test in self.tests:
            result = self._run_single(test)
            self.results.append(result)
        
        total_time = time.time() - start_time
        
        return self._generate_report(total_time)
    
    def run_by_type(self, test_type: AutomationTestType) -> Dict:
        """Chạy tests theo type"""
        self.results = []
        start_time = time.time()
        
        for test in self.tests:
            if test.test_type == test_type:
                result = self._run_single(test)
                self.results.append(result)
        
        total_time = time.time() - start_time
        return self._generate_report(total_time)
    
    def _run_single(self, test: AutomationTest) -> Dict:
        """Chạy một test case"""
        # Setup
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
        
        # Execute
        start = time.time()
        try:
            result = test.handler()
            duration = time.time() - start
            
            # Verify expected result
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
            # Teardown
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

def test_pipeline_config_valid():
    """Test that pipeline config is valid YAML with required fields"""
    config_path = Path(".github/workflows/ci.yml")
    assert config_path.exists(), "CI workflow file must exist"
    content = config_path.read_text()
    assert "name:" in content, "Workflow must have a name"
    assert "on:" in content, "Workflow must have triggers"
    assert "jobs:" in content, "Workflow must have jobs"

def test_circuit_breaker_opens_on_failure():
    """Test circuit breaker opens after threshold failures"""
    cb = CircuitBreaker(failure_threshold=3)
    for _ in range(3):
        cb.record_failure()
    assert cb.state == "open"

def test_rollback_reverts_changes():
    """Test that rollback properly reverts deployment"""
    deployer = Deployer()
    deployer.deploy("v1.0")
    deployer.deploy("v2.0")
    deployer.rollback()
    assert deployer.current_version == "v1.0"


# Register tests
harness = AutomationTestHarness()

harness.register(AutomationTest(
    name="CI Config Valid",
    test_type=AutomationTestType.PIPELINE_CONFIG,
    description="Validates GitHub Actions CI workflow config",
    handler=test_pipeline_config_valid,
    tags=["ci", "config"],
))

harness.register(AutomationTest(
    name="Circuit Breaker Opens",
    test_type=AutomationTestType.CIRCUIT_BREAKER,
    description="Circuit breaker opens after 3 failures",
    handler=test_circuit_breaker_opens_on_failure,
    tags=["reliability"],
))

harness.register(AutomationTest(
    name="Rollback Works",
    test_type=AutomationTestType.ROLLBACK,
    description="Deployment rollback reverts to previous version",
    handler=test_rollback_reverts_changes,
    tags=["deploy", "rollback"],
))

# Run
# report = harness.run_all()
# print(json.dumps(report, indent=2))
