from typing import Callable, Dict, List
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class EvalConfig:
    """Cấu hình evaluation"""
    dimensions: List[str] = field(default_factory=lambda: [
        "correctness", "quality", "efficiency", 
        "safety", "completeness"
    ])
    weights: Dict[str, float] = field(default_factory=lambda: {
        "correctness": 0.25,
        "quality": 0.20,
        "efficiency": 0.15,
        "safety": 0.15,
        "completeness": 0.15,
        "speed": 0.10,
    })
    auto_evaluate: bool = True
    human_review: bool = False


class EvaluationPipeline:
    """
    Pipeline đánh giá tự động cho AI coding output.
    
    Steps:
    1. Static Analysis (lint, complexity, naming)
    2. Dynamic Testing (run tests, check output)
    3. Security Scan (vulnerability check)
    4. Quality Scoring (weighted dimensions)
    5. Report Generation
    """
    
    def __init__(self, config: EvalConfig = None):
        self.config = config or EvalConfig()
        self.checks: List[Callable] = []
        self.results: List[EvaluationResult] = []
    
    def add_check(self, name: str, check_func: Callable,
                  dimension: str, weight: float = 1.0):
        """Thêm một check vào pipeline"""
        self.checks.append({
            "name": name,
            "func": check_func,
            "dimension": dimension,
            "weight": weight,
        })
    
    def evaluate(self, task_id: str, code: str, 
                 context: Dict = None) -> EvaluationResult:
        """Chạy evaluation trên code"""
        result = EvaluationResult(task_id=task_id)
        
        for check in self.checks:
            try:
                score = check["func"](code, context or {})
                result.add_score(
                    check["name"],
                    score * check["weight"],
                    f"Auto-evaluated by {check['name']}"
                )
            except Exception as e:
                result.add_score(
                    check["name"], 0.0,
                    f"Evaluation failed: {str(e)}"
                )
        
        result.calculate_total(self.config.weights)
        self.results.append(result)
        return result
    
    def get_average_scores(self) -> Dict[str, float]:
        """Tính average scores qua tất cả evaluations"""
        if not self.results:
            return {}
        
        dim_scores = {}
        for result in self.results:
            for dim, score in result.scores.items():
                if dim not in dim_scores:
                    dim_scores[dim] = []
                dim_scores[dim].append(score)
        
        return {
            dim: sum(scores) / len(scores)
            for dim, scores in dim_scores.items()
        }


# Standard checks
def check_test_passes(code: str, context: Dict) -> float:
    """Kiểm tra code có chạy qua tests không"""
    tests = context.get("tests", [])
    if not tests:
        return 50.0  # No tests = neutral score
    # Would execute tests and return pass rate
    return 80.0

def check_no_lint_errors(code: str, context: Dict) -> float:
    """Kiểm tra lint"""
    return 90.0  # Simplified

def check_complexity(code: str, context: Dict) -> float:
    """Kiểm tra complexity"""
    analyzer = CodeQualityAnalyzer()
    report = analyzer.analyze(code)
    return min(100, max(0, 100 - report.cyclomatic_complexity * 5))
