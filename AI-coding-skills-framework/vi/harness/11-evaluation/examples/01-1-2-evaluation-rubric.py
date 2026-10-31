from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class Rating(Enum):
    EXCELLENT = 5
    GOOD = 4
    ACCEPTABLE = 3
    POOR = 2
    FAILED = 1


@dataclass
class EvaluationDimension:
    """Một chiều đánh giá"""
    name: str
    weight: float              # 0.0 - 1.0
    description: str
    criteria: Dict[Rating, str] = field(default_factory=dict)


@dataclass
class EvaluationResult:
    """Kết quả đánh giá cho một task"""
    task_id: str
    scores: Dict[str, float] = field(default_factory=dict)
    notes: Dict[str, str] = field(default_factory=dict)
    total_score: float = 0.0
    
    def add_score(self, dimension: str, score: float, 
                  note: str = ""):
        self.scores[dimension] = score
        if note:
            self.notes[dimension] = note
    
    def calculate_total(self, weights: Dict[str, float]) -> float:
        """Tính tổng điểm weighted"""
        total = 0.0
        total_weight = 0.0
        
        for dim, weight in weights.items():
            if dim in self.scores:
                total += self.scores[dim] * weight
                total_weight += weight
        
        self.total_score = total / total_weight if total_weight else 0
        return self.total_score


# Define standard rubric
STANDARD_RUBRIC = [
    EvaluationDimension(
        name="correctness",
        weight=0.25,
        description="Code runs correctly, handles edge cases",
        criteria={
            Rating.EXCELLENT: "All tests pass, edge cases handled",
            Rating.GOOD: "Most tests pass, minor edge case missed",
            Rating.ACCEPTABLE: "Core functionality works, some gaps",
            Rating.POOR: "Partially working, key issues remain",
            Rating.FAILED: "Does not work or breaks existing code",
        }
    ),
    EvaluationDimension(
        name="quality",
        weight=0.20,
        description="Code is clean, readable, maintainable",
        criteria={
            Rating.EXCELLENT: "Follows all conventions, self-documenting",
            Rating.GOOD: "Clean code, minor style issues",
            Rating.ACCEPTABLE: "Readable but could be improved",
            Rating.POOR: "Messy but understandable",
            Rating.FAILED: "Unreadable or extremely messy",
        }
    ),
    EvaluationDimension(
        name="efficiency",
        weight=0.15,
        description="Performance is appropriate for the use case",
        criteria={
            Rating.EXCELLENT: "Optimal complexity, minimal resources",
            Rating.GOOD: "Good performance, minor optimizations possible",
            Rating.ACCEPTABLE: "Acceptable for most cases",
            Rating.POOR: "Performance concerns for scale",
            Rating.FAILED: "Severe performance issues",
        }
    ),
    EvaluationDimension(
        name="safety",
        weight=0.15,
        description="Code handles errors and is secure",
        criteria={
            Rating.EXCELLENT: "Comprehensive error handling, no vulnerabilities",
            Rating.GOOD: "Good error handling, minor security notes",
            Rating.ACCEPTABLE: "Basic error handling present",
            Rating.POOR: "Minimal error handling",
            Rating.FAILED: "No error handling, security risks",
        }
    ),
    EvaluationDimension(
        name="completeness",
        weight=0.15,
        description="All requirements are addressed",
        criteria={
            Rating.EXCELLENT: "All requirements + bonus improvements",
            Rating.GOOD: "All requirements met",
            Rating.ACCEPTABLE: "Core requirements met, some missing",
            Rating.POOR: "Partially completed",
            Rating.FAILED: "Major requirements missing",
        }
    ),
    EvaluationDimension(
        name="speed",
        weight=0.10,
        description="Token efficiency and time to completion",
        criteria={
            Rating.EXCELLENT: "Minimal tokens, fast completion",
            Rating.GOOD: "Reasonable token usage",
            Rating.ACCEPTABLE: "Average token usage",
            Rating.POOR: "High token usage, slow",
            Rating.FAILED: "Extremely inefficient",
        }
    ),
]
