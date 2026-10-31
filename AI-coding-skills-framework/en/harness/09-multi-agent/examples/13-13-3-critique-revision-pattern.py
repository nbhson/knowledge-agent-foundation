class CritiqueRevisionLoop:
    """
    Critique-Revision pattern — one agent writes, one agent gives
    feedback, repeated until a quality threshold is met.
    
    Iterative improvement loop:
    1. Writer generates code
    2. Critic reviews code
    3. Writer revises based on feedback
    4. Repeat until quality threshold met or max iterations
    
    Use when:
    - Code quality matters more than speed
    - Multiple perspectives are needed
    - Complex tasks need refinement
    """
    
    def __init__(self, max_iterations: int = 3,
                 quality_threshold: float = 0.8):
        self.max_iterations = max_iterations
        self.quality_threshold = quality_threshold
        self.history: List[Dict] = []
    
    def iterate(self, task: str, 
                writer_func: Callable,
                critic_func: Callable,
                quality_func: Callable) -> Dict:
        """
        Run the critique-revision loop.
        
        writer_func: function(task, feedback) -> code
        critic_func: function(code, task) -> feedback
        quality_func: function(code, task) -> float (0-1)
        """
        best_code = ""
        best_score = 0.0
        all_iterations = []
        
        feedback = ""  # No feedback for first iteration
        
        for i in range(self.max_iterations):
            # WRITE
            code = writer_func(task, feedback)
            
            # CRITIQUE
            critique = critic_func(code, task)
            
            # EVALUATE
            score = quality_func(code, task)
            
            iteration_data = {
                "iteration": i + 1,
                "code_preview": code[:200],
                "critique": critique[:200],
                "score": score,
            }
            all_iterations.append(iteration_data)
            self.history.append(iteration_data)
            
            # Track best
            if score > best_score:
                best_score = score
                best_code = code
            
            # Check threshold
            if score >= self.quality_threshold:
                return {
                    "status": "threshold_met",
                    "iterations": i + 1,
                    "final_code": code,
                    "final_score": score,
                    "all_iterations": all_iterations,
                }
            
            # Build feedback for next iteration
            feedback = f"Previous score: {score:.2f}. Critique: {critique}"
        
        return {
            "status": "max_iterations",
            "iterations": self.max_iterations,
            "final_code": best_code,
            "final_score": best_score,
            "all_iterations": all_iterations,
        }
