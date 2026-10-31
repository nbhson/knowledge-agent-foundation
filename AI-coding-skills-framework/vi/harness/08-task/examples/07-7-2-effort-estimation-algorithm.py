from enum import Enum
from typing import Dict, List, Tuple

class EffortEstimator:
    """
    ước lượng effort cho coding tasks dựa trên historical data
    và task characteristics.
    """
    
    # Base tokens per complexity level
    BASE_TOKENS = {
        TaskComplexity.TRIVIAL: 500,
        TaskComplexity.SIMPLE: 2000,
        TaskComplexity.MODERATE: 5000,
        TaskComplexity.COMPLEX: 12000,
        TaskComplexity.EPIC: 25000,
    }
    
    # Multipliers per category
    CATEGORY_MULTIPLIERS = {
        TaskCategory.GENERATION: 1.0,
        TaskCategory.MODIFICATION: 0.8,
        TaskCategory.ANALYSIS: 0.6,
        TaskCategory.DOCUMENTATION: 0.4,
        TaskCategory.TESTING: 0.7,
    }
    
    # File involvement bonus
    FILE_BONUS_PER_FILE = 500
    
    def estimate_tokens(self, task: Task) -> int:
        """Ước lượng số tokens cần thiết"""
        base = self.BASE_TOKENS.get(task.complexity, 2000)
        multiplier = self.CATEGORY_MULTIPLIERS.get(task.category, 1.0)
        file_bonus = len(task.files_involved) * self.FILE_BONUS_PER_FILE
        
        return int(base * multiplier + file_bonus)
    
    def estimate_duration(self, task: Task) -> Dict[str, float]:
        """
        ước lượng thời gian thực hiện (phút).
        Giả định: ~100 tokens/minute processing speed.
        """
        tokens = self.estimate_tokens(task)
        processing_minutes = tokens / 100
        
        # Add overhead for coordination, review
        overhead = 1.2 if len(task.dependencies) > 2 else 1.1
        
        total_minutes = processing_minutes * overhead
        
        return {
            "processing_minutes": processing_minutes,
            "overhead_factor": overhead,
            "total_minutes": total_minutes,
            "total_hours": total_minutes / 60,
        }
    
    def estimate_batch(self, tasks: List[Task]) -> Dict[str, float]:
        """Ước lượng cho cả batch tasks"""
        total_tokens = sum(self.estimate_tokens(t) for t in tasks)
        estimates = [self.estimate_duration(t) for t in tasks]
        
        return {
            "total_tokens": total_tokens,
            "total_minutes": sum(e["total_minutes"] for e in estimates),
            "task_count": len(tasks),
            "avg_tokens_per_task": total_tokens / len(tasks) if tasks else 0,
        }
