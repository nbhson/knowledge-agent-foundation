class EnsemblePattern:
    """
    Ensemble pattern — run N agents in parallel,
    pick the best output.
    
    Like ensembles in ML:
    - Multiple diverse agents → diverse outputs
    - Judge/voting system → pick best
    - Reduces risk of single-agent failure
    
    Pros:
    - Higher quality ceiling
    - More robust (one agent fails, others compensate)
    - Diverse solutions → better exploration
    
    Cons:
    - N× cost
    - Need a good judge/voting mechanism
    """
    
    def __init__(self, n_agents: int = 3):
        self.n_agents = n_agents
    
    def run_ensemble(self, task: str,
                     agent_func: Callable,
                     judge_func: Callable) -> Dict:
        """
        Run N agents and pick the best output.
        
        agent_func: function(task) -> code
        judge_func: function(code, task) -> float
        """
        outputs = []
        
        for i in range(self.n_agents):
            output = agent_func(task)
            score = judge_func(output, task)
            
            outputs.append({
                "agent_index": i,
                "output": output,
                "score": score,
                "lines": len(output.split("\n")) if isinstance(output, str) else 0,
            })
        
        # Sort by score
        outputs.sort(key=lambda x: x["score"], reverse=True)
        
        best = outputs[0]
        worst = outputs[-1]
        
        return {
            "best_output": best["output"],
            "best_score": best["score"],
            "best_agent": best["agent_index"],
            "worst_score": worst["score"],
            "score_variance": self._variance([o["score"] for o in outputs]),
            "all_outputs": outputs,
            "recommendation": self._generate_recommendation(outputs),
        }
    
    def _variance(self, scores: List[float]) -> float:
        """Calculate the variance of the scores"""
        if len(scores) < 2:
            return 0.0
        mean = sum(scores) / len(scores)
        return sum((s - mean) ** 2 for s in scores) / len(scores)
    
    def _generate_recommendation(self, outputs: List[Dict]) -> str:
        """Recommend based on ensemble results"""
        scores = [o["score"] for o in outputs]
        variance = self._variance(scores)
        
        if variance < 0.01:
            return "Low variance: All agents agree. High confidence."
        elif variance < 0.05:
            return "Moderate variance: Minor differences. Best output likely reliable."
        else:
            return "High variance: Agents disagree significantly. Consider reviewing all outputs."
