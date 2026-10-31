from dataclasses import dataclass
from typing import Dict, List

@dataclass
class AgentQualityMetrics:
    """
    Metrics đặc thù cho AI coding agent.
    
    Khác với code quality thông thường,
    agent metrics đo cả QUÁ TRÌNH generate,
    không chỉ kết quả cuối cùng.
    """
    
    # === PROCESS METRICS ===
    
    # 1. First-Attempt Success Rate
    # Tỷ lệ code đúng ngay lần đầu (không cần retry)
    first_attempt_success: float = 0.0
    
    # 2. Iteration Efficiency
    # Số lần retry trung bình để hoàn thành task
    avg_iterations: float = 0.0
    
    # 3. Token Efficiency
    # Token sử dụng so với optimal (thấp hơn = tốt hơn)
    token_efficiency: float = 0.0
    
    # 4. Time to First Good Output
    # Thời gian từ prompt đến output hợp lệ đầu tiên
    time_to_first_output: float = 0.0
    
    # === OUTPUT METRICS ===
    
    # 5. Code Correctness
    # Tỷ lệ tests pass
    test_pass_rate: float = 0.0
    
    # 6. Edit Precision
    # Tỷ lệ edits thực sự cần thiết / total edits
    edit_precision: float = 0.0
    
    # 7. Context Relevance
    # Có dùng đúng context không (không hallucinate)
    context_relevance: float = 0.0
    
    # 8. Instruction Following
    # Có làm đúng theo yêu cầu không
    instruction_following: float = 0.0
    
    # === SAFETY METRICS ===
    
    # 9. No Regressions
    # Không phá vỡ existing functionality
    regression_free_rate: float = 0.0
    
    # 10. Security Compliance
    # Không introduce vulnerabilities
    security_compliance: float = 0.0
    
    def calculate_composite_score(self) -> float:
        """Tính composite score từ tất cả metrics"""
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
