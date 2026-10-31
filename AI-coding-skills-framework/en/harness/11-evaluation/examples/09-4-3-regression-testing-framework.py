class RegressionTestSuite:
    """
    Regression testing framework for an AI coding agent.
    
    Purpose: Ensure the agent doesn't "forget" how to do
    things correctly after an update / new prompt.
    
    Concept:
    - Each task has a verified "golden answer"
    - When the agent is updated, re-run all tasks
    - If the score drops -> REGRESSION
    """
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.test_cases: List[Dict] = []
        self.baselines: Dict[str, float] = {}
    
    def add_test_case(self, task_id: str, prompt: str,
                      golden_output: str, 
                      validator: Callable = None,
                      category: str = "general"):
        """Add a test case with a golden output"""
        self.test_cases.append({
            "id": task_id,
            "prompt": prompt,
            "golden": golden_output,
            "validator": validator,
            "category": category,
        })
    
    def set_baseline(self, results: Dict[str, float]):
        """Set the baseline score for each test case"""
        self.baselines = results
    
    def run_and_check(self, agent_func: Callable) -> Dict:
        """
        Run the agent and check for regressions.
        
        agent_func: function(prompt) -> output
        
        Returns:
        {
            "total": N,
            "passed": N,
            "regressions": [...],
            "improvements": [...],
            "score_delta": float,
        }
        """
        results = {}
        regressions = []
        improvements = []
        
        for test in self.test_cases:
            output = agent_func(test["prompt"])
            
            # Score against golden
            if test["validator"]:
                score = 100.0 if test["validator"](output) else 0.0
            else:
                score = self._similarity_score(output, test["golden"])
            
            results[test["id"]] = score
            
            # Check regression
            baseline = self.baselines.get(test["id"], 50.0)
            if score < baseline - 10:  # 10% threshold
                regressions.append({
                    "id": test["id"],
                    "baseline": baseline,
                    "current": score,
                    "delta": score - baseline,
                })
            elif score > baseline + 10:
                improvements.append({
                    "id": test["id"],
                    "baseline": baseline,
                    "current": score,
                    "delta": score - baseline,
                })
        
        # Calculate overall
        avg_score = sum(results.values()) / len(results) if results else 0
        avg_baseline = sum(self.baselines.values()) / len(self.baselines) if self.baselines else 50
        
        return {
            "total": len(self.test_cases),
            "passed": sum(1 for s in results.values() if s >= 70),
            "regressions": regressions,
            "improvements": improvements,
            "avg_score": avg_score,
            "score_delta": avg_score - avg_baseline,
            "has_regression": len(regressions) > 0,
        }
    
    def _similarity_score(self, actual: str, expected: str) -> float:
        """Simple text similarity score"""
        actual_words = set(actual.lower().split())
        expected_words = set(expected.lower().split())
        
        if not expected_words:
            return 100.0
        
        intersection = actual_words & expected_words
        return (len(intersection) / len(expected_words)) * 100
