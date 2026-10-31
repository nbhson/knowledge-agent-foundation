class TreeOfThoughts:
    """
    Tree of Thoughts: Explore multiple reasoning paths
    
    Better than linear chain-of-thought for complex problems
    Based on paper: "Tree of Thoughts" (Yao et al., 2023)
    
    Key insight: Not all reasoning paths are equal.
    ToT explores multiple branches and evaluates which path is most promising.
    """
    
    def __init__(self, llm_func=None, branching_factor=3, max_depth=3):
        self.llm = llm_func
        self.branching_factor = branching_factor
        self.max_depth = max_depth
    
    def generate_thoughts(self, state, n=None):
        """Generate multiple candidate thoughts"""
        n = n or self.branching_factor
        
        prompt = f"""Từ trạng thái hiện tại, hãy nghĩ ra {n} hướng giải quyết khác nhau.

Trạng thái: {state}

Hướng 1: 
Hướng 2: 
Hướng 3: """
        
        if self.llm:
            response = self.llm(prompt)
            thoughts = [t.strip() for t in response.split('\n') 
                       if t.strip().startswith("Hướng")]
            return thoughts[:n]
        
        return [f"Thought {i+1}" for i in range(n)]
    
    def evaluate_thought(self, state, thought):
        """Evaluate how promising a thought is"""
        prompt = f"""Đánh giá hướng giải quyết này (1-10):

Trạng thái: {state}
Hướng: {thought}

Tiêu chí:
- Tính khả thi (0-3)
- Tốc độ giải quyết (0-3)
- Chất lượng kết quả (0-4)

Điểm số (1-10):"""
        
        if self.llm:
            response = self.llm(prompt)
            try:
                score = int(''.join(c for c in response if c.isdigit())[:2])
                return min(max(score, 1), 10)
            except (ValueError, IndexError):
                pass
        
        return 5  # Điểm mặc định
    
    def solve(self, problem):
        """
        Tree search: explore best paths
        
        Uses BFS with pruning to avoid exponential explosion
        """
        root_state = {"problem": problem, "path": [], "score": 0}
        
        frontier = [root_state]
        best_solution = None
        best_score = -1
        
        for depth in range(self.max_depth):
            next_frontier = []
            
            for state in frontier:
                thoughts = self.generate_thoughts(
                    f"{state['problem']} | Path: {' → '.join(state['path'])}"
                )
                
                for thought in thoughts:
                    score = self.evaluate_thought(state['problem'], thought)
                    
                    new_state = {
                        "problem": state["problem"],
                        "path": state["path"] + [thought],
                        "score": state["score"] + score,
                    }
                    
                    if new_state["score"] > best_score:
                        best_score = new_state["score"]
                        best_solution = new_state
                    
                    next_frontier.append(new_state)
            
            # Cắt tỉa: chỉ giữ lại top-k đường dẫn tốt nhất
            frontier = sorted(next_frontier, key=lambda x: x["score"], reverse=True)
            frontier = frontier[:self.branching_factor]
        
        return {
            "solution": best_solution["path"] if best_solution else [],
            "total_score": best_score,
            "paths_explored": self.branching_factor ** self.max_depth,
        }
