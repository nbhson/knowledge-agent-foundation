import random
from typing import List, Dict, Callable

class PromptABTest:
    """
    A/B testing framework for prompts
    
    Flow:
    1. Define variants
    2. Randomly assign users to variant
    3. Measure outcomes
    4. Statistical significance test
    5. Declare winner
    """
    
    def __init__(self, test_name: str):
        self.test_name = test_name
        self.variants: Dict[str, Dict] = {}
        self.assignments: Dict[str, str] = {}  # user_id -> variant
        self.results: Dict[str, List[Dict]] = {}  # variant -> [results]
        self.start_time = datetime.now().isoformat()
    
    def add_variant(self, name: str, prompt_template: str, traffic_pct: float = 50):
        """Add a variant"""
        self.variants[name] = {
            "template": prompt_template,
            "traffic_pct": traffic_pct,
        }
        self.results[name] = []
    
    def assign(self, user_id: str) -> str:
        """Assign user to variant"""
        if user_id in self.assignments:
            return self.assignments[user_id]
        
        # Weighted random selection
        rand = random.random() * 100
        cumulative = 0
        
        for name, variant in self.variants.items():
            cumulative += variant["traffic_pct"]
            if rand <= cumulative:
                self.assignments[user_id] = name
                return name
        
        # Fallback to first variant
        first_name = list(self.variants.keys())[0]
        self.assignments[user_id] = first_name
        return first_name
    
    def record_result(self, user_id: str, metrics: Dict):
        """Record result for a user"""
        variant = self.assignments.get(user_id)
        if variant:
            self.results[variant].append({
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "metrics": metrics,
            })
    
    def analyze(self) -> Dict:
        """Analyze test results"""
        analysis = {}
        
        for variant_name, results in self.results.items():
            if not results:
                analysis[variant_name] = {"status": "no_data"}
                continue
            
            # Calculate metrics
            all_metrics = [r["metrics"] for r in results]
            
            # Aggregate common metrics
            metric_summary = {}
            for metric_name in ["accuracy", "latency_ms", "tokens_used", "user_rating"]:
                values = [m.get(metric_name) for m in all_metrics if metric_name in m]
                if values:
                    metric_summary[metric_name] = {
                        "mean": sum(values) / len(values),
                        "min": min(values),
                        "max": max(values),
                        "count": len(values),
                    }
            
            analysis[variant_name] = {
                "total_users": len(results),
                "metrics": metric_summary,
            }
        
        # Statistical significance (simple z-test approximation)
        if len(self.variants) == 2:
            variant_names = list(self.variants.keys())
            a_results = self.results[variant_names[0]]
            b_results = self.results[variant_names[1]]
            
            if a_results and b_results:
                a_scores = [r["metrics"].get("accuracy", 0) for r in a_results]
                b_scores = [r["metrics"].get("accuracy", 0) for r in b_results]
                
                if a_scores and b_scores:
                    a_mean = sum(a_scores) / len(a_scores)
                    b_mean = sum(b_scores) / len(b_scores)
                    
                    winner = variant_names[0] if a_mean > b_mean else variant_names[1]
                    improvement = abs(a_mean - b_mean) * 100
                    
                    analysis["winner"] = winner
                    analysis["improvement_pct"] = improvement
        
        analysis["test_name"] = self.test_name
        analysis["start_time"] = self.start_time
        analysis["total_participants"] = len(self.assignments)
        
        return analysis
    
    def get_winner(self) -> Optional[str]:
        """Get the winning variant"""
        analysis = self.analyze()
        return analysis.get("winner")
