# LangSmith integration for prompt tracking
from langsmith import Client

class LangSmithPromptManager:
    def __init__(self, api_key: str):
        self.client = Client(api_key=api_key)
    
    def log_prompt(self, name: str, template: str, metrics: Dict):
        """Log prompt version to LangSmith"""
        self.client.create_prompt(
            name=name,
            template=template,
            metadata=metrics,
        )
    
    def get_prompt(self, name: str) -> Dict:
        """Get latest prompt version"""
        return self.client.get_prompt(name)
    
    def compare_prompts(self, prompt_a: str, prompt_b: str, dataset: List[Dict]):
        """Compare two prompts on same dataset"""
        results_a = []
        results_b = []
        
        for item in dataset:
            result_a = self.client.run(prompt_a, input=item)
            result_b = self.client.run(prompt_b, input=item)
            results_a.append(result_a)
            results_b.append(result_b)
        
        return {
            "prompt_a_avg": sum(r.get("score", 0) for r in results_a) / len(results_a),
            "prompt_b_avg": sum(r.get("score", 0) for r in results_b) / len(results_b),
        }
