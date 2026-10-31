class ABTestFramework:
    """
    A/B testing for prompt engineering.
    
    Compare 2 versions of a prompt/harness
    on the same benchmark suite.
    
    Like A/B testing on the web,
    but applied to AI agent configuration.
    """
    
    def __init__(self, benchmark_suite: BenchmarkSuite):
        self.suite = benchmark_suite
        self.results = {"A": None, "B": None}
    
    def run_variant(self, variant: str, 
                    agent_func: Callable) -> Dict:
        """Run one variant"""
        self.results[variant] = self.suite.run(agent_func)
        return self.results[variant]
    
    def analyze(self) -> Dict:
        """
        Analyze the A/B test results.
        
        Use a statistical significance test
        to decide which variant is better.
        """
        if not all(self.results.values()):
            return {"error": "Both variants must be run first"}
        
        a_summary = self.results["A"]
        b_summary = self.results["B"]
        
        # Simple comparison
        metrics = {}
        for key in a_summary:
            if isinstance(a_summary[key], (int, float)):
                a_val = a_summary[key]
                b_val = b_summary.get(key, 0)
                metrics[key] = {
                    "A": a_val,
                    "B": b_val,
                    "delta": b_val - a_val,
                    "winner": "A" if a_val > b_val else "B",
                }
        
        # Overall winner (by success rate)
        a_rate = a_summary.get("success_rate", 0)
        b_rate = b_summary.get("success_rate", 0)
        
        return {
            "metrics": metrics,
            "overall_winner": "A" if a_rate >= b_rate else "B",
            "confidence": "high" if abs(a_rate - b_rate) > 0.1 else "low",
        }
