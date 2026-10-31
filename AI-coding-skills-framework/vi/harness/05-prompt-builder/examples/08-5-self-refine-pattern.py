class SelfRefinePrompt:
    """
    Self-Refine: LLM critiques and improves its own output
    
    Pattern: Generate → Critique → Refine → Repeat until quality threshold
    
    Based on paper: "Self-Refine: Iterative Refinement with Self-Feedback"
    (Madaan et al., 2023)
    """
    
    def __init__(self, llm_func=None, max_iterations: int = 3):
        self.llm = llm_func
        self.max_iterations = max_iterations
    
    def generate(self, task: str) -> str:
        """Initial generation"""
        prompt = f"""Task: {task}

Generate a high-quality response.
Output:"""
        
        if self.llm:
            return self.llm(prompt)
        return f"Response for: {task}"
    
    def critique(self, task: str, output: str) -> Dict:
        """Self-critique the output"""
        prompt = f"""Task: {task}
Output: {output}

Critically evaluate this output:
1. Quality (1-10): 
2. Issues: [list specific problems]
3. Suggestions: [list improvements]
4. Overall: good/improve_needed

Output JSON:"""
        
        if self.llm:
            response = self.llm(prompt)
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                pass
        
        return {"score": 5, "issues": [], "suggestions": [], "overall": "improve_needed"}
    
    def refine(self, task: str, output: str, critique: Dict) -> str:
        """Refine based on critique"""
        issues = "\n".join(f"- {i}" for i in critique.get("issues", []))
        suggestions = "\n".join(f"- {s}" for s in critique.get("suggestions", []))
        
        prompt = f"""Task: {task}

Previous output:
{output}

Issues found:
{issues}

Suggestions:
{suggestions}

Please improve the output addressing all issues and incorporating suggestions.
Improved output:"""
        
        if self.llm:
            return self.llm(prompt)
        
        return output
    
    def run(self, task: str, quality_threshold: int = 8) -> Dict:
        """Full self-refine loop"""
        output = self.generate(task)
        history = [{"iteration": 0, "output": output}]
        
        for i in range(self.max_iterations):
            critique = self.critique(task, output)
            score = critique.get("score", 0)
            
            history.append({
                "iteration": i + 1,
                "critique": critique,
                "score": score,
            })
            
            if score >= quality_threshold:
                break
            
            output = self.refine(task, output, critique)
            history.append({"iteration": i + 1, "output": output})
        
        return {
            "final_output": output,
            "iterations": i + 1,
            "final_score": critique.get("score", 0),
            "history": history,
        }
