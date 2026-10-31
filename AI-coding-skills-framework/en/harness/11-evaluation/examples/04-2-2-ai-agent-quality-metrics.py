from dataclasses import dataclass
from typing import Dict, List

@dataclass
class AgentQualityMetrics:
    """
    Metrics specific to an AI coding agent.
    
    Unlike ordinary code quality,
    agent metrics measure the entire GENERATION PROCESS,
    not just the final result.
    """
    
    # === PROCESS METRICS ===
    
    # 1. First-Attempt Success Rate
    # Rate of code correct on the first attempt (no retry needed)
    first_attempt_success: float = 0.0
    
    # 2. Iteration Efficiency
    # Average number of retries to complete a task
    avg_iterations: float = 0.0
    
    # 3. Token Efficiency
    # Tokens used vs optimal (lower = better)
    token_efficiency: float = 0.0
    
    # 4. Time to First Good Output
    # Time from prompt to the first valid output
    time_to_first_output: float = 0.0
    
    # === OUTPUT METRICS ===
    
    # 5. Code Correctness
    # Test pass rate
    test_pass_rate: float = 0.0
    
    # 6. Edit Precision
    # Ratio of edits that were truly necessary / total edits
    edit_precision: float = 0.0
    
    # 7. Context Relevance
    # Was the right context used (no hallucination)
    context_relevance: float = 0.0
    
    # 8. Instruction Following
    # Was the task done as requested
    instruction_following: float = 0.0
    
    # === SAFETY METRICS ===
    
    # 9. No Regressions
    # Does not break existing functionality
    regression_free_rate: float = 0.0
    
    # 10. Security Compliance
    # Does not introduce vulnerabilities
    security_compliance: float = 0.0
    
    def calculate_composite_score(self) -> float:
        """Compute the composite score from all metrics"""
        weights = {
            "first_attempt_success": 0.15,
            "test_pass_rate": 0.25,
            "edit_precision": 0.10,
            "context_relevance": 0.10,
            "instruction_following": 0.15,
            "regression_free_rate": 0.15,
            "token_efficiency": 0.10,
        }
        
        total = 0.0
        for metric, weight in weights.items():
            value = getattr(self, metric, 0.0)
            total += value * weight
        
        return total * 100  # Scale to 0-100
