from dataclasses import dataclass
from typing import Dict, List

@dataclass
class CostEstimate:
    """Cost estimate for multi-agent execution"""
    task_name: str
    single_agent_tokens: int
    multi_agent_tokens: int
    quality_improvement_pct: float  # Estimated quality gain
    
    @property
    def cost_ratio(self) -> float:
        """Multi/single cost ratio"""
        return self.multi_agent_tokens / max(self.single_agent_tokens, 1)
    
    @property
    def roi(self) -> float:
        """
        ROI estimate.
        Positive = multi-agent is worth the cost.
        """
        quality_value = self.quality_improvement_pct * 100
        cost_increase = (self.cost_ratio - 1) * 100
        return quality_value - cost_increase
    
    def recommendation(self) -> str:
        if self.roi > 20:
            return "✅ RECOMMEND: Multi-agent (strong ROI)"
        elif self.roi > 0:
            return "💡 CONSIDER: Multi-agent (marginal ROI)"
        else:
            return "❌ AVOID: Single agent is more cost-effective"


# Example cost estimates
COST_ESTIMATES = [
    CostEstimate("Simple bug fix", 5000, 15000, 10),
    CostEstimate("Code review", 8000, 16000, 35),
    CostEstimate("Feature development", 15000, 45000, 25),
    CostEstimate("Security audit", 10000, 20000, 40),
    CostEstimate("Multi-file refactor", 20000, 60000, 35),
    CostEstimate("Documentation", 5000, 20000, 5),
]

print("Multi-Agent Cost-Benefit Analysis:")
print("=" * 60)
for est in COST_ESTIMATES:
    print(f"\n{est.task_name}:")
    print(f"  Single agent: {est.single_agent_tokens:,} tokens")
    print(f"  Multi agent:  {est.multi_agent_tokens:,} tokens")
    print(f"  Cost ratio:   {est.cost_ratio:.1f}×")
    print(f"  Quality gain: +{est.quality_improvement_pct:.0f}%")
    print(f"  ROI:          {est.roi:+.0f}")
    print(f"  → {est.recommendation()}")
