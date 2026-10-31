from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional
from enum import Enum
import time


class TestCategory(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    PERFORMANCE = "performance"
    SECURITY = "security"


@dataclass
class TestCase:
    name: str
    category: TestCategory
    handler: Callable
    timeout_seconds: int = 60
    tags: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)


@dataclass
class TestResult:
    test_name: str
    status: str            # passed, failed, skipped, error
    duration_seconds: float
    error_message: Optional[str] = None
    stdout: str = ""


class AutomatedTestRunner:
    """
    Automated test runner với parallel execution,
    categorization, và reporting.
    """
    
    def __init__(self):
        self.test_cases: List[TestCase] = []
        self.results: List[TestResult] = []
        self.coverage_threshold: float = 80.0
    
    def register(self, test: TestCase):
        self.test_cases.append(test)
    
    def run(self, categories: List[TestCategory] = None,
            tags: List[str] = None) -> Dict:
        """Run tests with optional filtering"""
        
        # Filter tests
        tests_to_run = self.test_cases
        if categories:
            tests_to_run = [t for t in tests_to_run if t.category in categories]
        if tags:
            tests_to_run = [t for t in tests_to_run 
                           if any(tag in t.tags for tag in tags)]
        
        self.results = []
        total_start = time.time()
        
        for test in tests_to_run:
            start = time.time()
            try:
                test.handler()
                self.results.append(TestResult(
                    test_name=test.name,
                    status="passed",
                    duration_seconds=time.time() - start,
                ))
            except AssertionError as e:
                self.results.append(TestResult(
                    test_name=test.name,
                    status="failed",
                    duration_seconds=time.time() - start,
                    error_message=str(e),
                ))
            except Exception as e:
                self.results.append(TestResult(
                    test_name=test.name,
                    status="error",
                    duration_seconds=time.time() - start,
                    error_message=str(e),
                ))
        
        total_duration = time.time() - total_start
        
        return self._generate_report(total_duration)
    
    def _generate_report(self, total_duration: float) -> Dict:
        """Generate test report"""
        passed = sum(1 for r in self.results if r.status == "passed")
        failed = sum(1 for r in self.results if r.status == "failed")
        errors = sum(1 for r in self.results if r.status == "error")
        total = len(self.results)
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
            "duration_seconds": total_duration,
            "results": [
                {
                    "name": r.test_name,
                    "status": r.status,
                    "duration": r.duration_seconds,
                    "error": r.error_message,
                }
                for r in self.results
            ],
            "gate_passed": failed == 0 and errors == 0,
        }
