from typing import Dict, List, Tuple

class ImprovementTracker:
    """
    Track improvement across iterations.
    
    Tracks:
    - Benchmark scores over time
    - Regression detection
    - Improvement suggestions
    """
    
    def __init__(self):
        self.iterations: List[Dict] = []
        self.baselines: Dict[str, float] = {}
    
    def set_baseline(self, benchmark_name: str, scores: Dict):
        """Set a baseline for the benchmark"""
        self.baselines[benchmark_name] = scores
    
    def record_iteration(self, iteration_id: str,
                         benchmark_name: str,
                         scores: Dict[str, float]):
        """Record an iteration's results"""
        self.iterations.append({
            "id": iteration_id,
            "benchmark": benchmark_name,
            "scores": scores,
            "timestamp": datetime.now().isoformat(),
        })
    
    def analyze_trend(self, benchmark_name: str) -> Dict:
        """Analyze the trend across iterations"""
        relevant = [
            i for i in self.iterations 
            if i["benchmark"] == benchmark_name
        ]
        
        if len(relevant) < 2:
            return {"trend": "insufficient_data"}
        
        # Compare first and last
        first = relevant[0]["scores"]
        last = relevant[-1]["scores"]
        
        improvements = {}
        regressions = {}
        
        for metric in last:
            if metric in first:
                change = last[metric] - first[metric]
                if change > 0:
                    improvements[metric] = change
                elif change < 0:
                    regressions[metric] = abs(change)
        
        return {
            "iterations": len(relevant),
            "improvements": improvements,
            "regressions": regressions,
            "overall_trend": "improving" if not regressions else "mixed",
        }
    
    def suggest_improvements(self, 
                              eval_results: List[EvaluationResult]
                              ) -> List[str]:
        """Suggest improvements based on evaluation results"""
        suggestions = []
        
        # Find consistently low scores
        dim_avgs = {}
        for result in eval_results:
            for dim, score in result.scores.items():
                if dim not in dim_avgs:
                    dim_avgs[dim] = []
                dim_avgs[dim].append(score)
        
        for dim, scores in dim_avgs.items():
            avg = sum(scores) / len(scores)
            if avg < 60:
                suggestions.append(
                    f"⚠️ {dim}: Average score {avg:.1f}/100. "
                    f"Consider improving prompts or adding "
                    f"specific rules for {dim}."
                )
            elif avg < 80:
                suggestions.append(
                    f"💡 {dim}: Score {avg:.1f}/100. "
                    f"Room for improvement with "
                    f"better context or examples."
                )
        
        return suggestions
