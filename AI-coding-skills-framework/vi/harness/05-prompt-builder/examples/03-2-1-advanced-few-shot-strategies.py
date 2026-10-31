from typing import List, Dict, Tuple
import numpy as np

class FewShotBuilder:
    """
    Advanced few-shot example selection strategies:
    
    1. Random: Random selection (baseline)
    2. Similarity: Cosine similarity with embeddings
    3. Diversity: Maximal diversity (MMR)
    4. Class-balanced: Equal representation per class
    5. Progressive: Start simple, increase complexity
    """
    
    def __init__(self, examples: List[Dict], embedding_func=None):
        """
        examples: [{"input": ..., "output": ..., "class": ..., "difficulty": ...}]
        embedding_func: callable that returns embeddings
        """
        self.examples = examples
        self.embed = embedding_func
        self._embeddings_cache = {}
    
    def select(self, query: str, k: int = 3, strategy: str = "similarity") -> List[Dict]:
        """Select k examples using specified strategy"""
        
        strategies = {
            "random": self._select_random,
            "similarity": self._select_similarity,
            "diversity": self._select_diversity,
            "class_balanced": self._select_class_balanced,
            "progressive": self._select_progressive,
        }
        
        if strategy not in strategies:
            raise ValueError(f"Unknown strategy: {strategy}. Use: {list(strategies.keys())}")
        
        return strategies[strategy](query, k)
    
    def _select_random(self, query: str, k: int) -> List[Dict]:
        """Random selection (baseline)"""
        import random
        return random.sample(self.examples, min(k, len(self.examples)))
    
    def _select_similarity(self, query: str, k: int) -> List[Dict]:
        """Select most similar examples by embedding cosine similarity"""
        if not self.embed:
            return self._select_random(query, k)
        
        query_emb = self._get_embedding(query)
        
        scored = []
        for ex in self.examples:
            ex_emb = self._get_embedding(ex["input"])
            sim = self._cosine_similarity(query_emb, ex_emb)
            scored.append((sim, ex))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [ex for _, ex in scored[:k]]
    
    def _select_diversity(self, query: str, k: int) -> List[Dict]:
        """
        Maximal Marginal Relevance (MMR)
        Balances relevance and diversity to avoid redundant examples
        """
        if not self.embed:
            return self._select_random(query, k)
        
        query_emb = self._get_embedding(query)
        lambda_param = 0.7  # Balance: 1=relevance only, 0=diversity only
        
        selected = []
        remaining = list(range(len(self.examples)))
        
        for _ in range(min(k, len(self.examples))):
            best_idx = -1
            best_score = -float('inf')
            
            for idx in remaining:
                ex_emb = self._get_embedding(self.examples[idx]["input"])
                
                # Relevance to query
                relevance = self._cosine_similarity(query_emb, ex_emb)
                
                # Max similarity to already selected
                if selected:
                    max_sim = max(
                        self._cosine_similarity(
                            ex_emb, 
                            self._get_embedding(self.examples[s]["input"])
                        )
                        for s in selected
                    )
                else:
                    max_sim = 0
                
                # MMR score
                mmr = lambda_param * relevance - (1 - lambda_param) * max_sim
                
                if mmr > best_score:
                    best_score = mmr
                    best_idx = idx
            
            if best_idx >= 0:
                selected.append(best_idx)
                remaining.remove(best_idx)
        
        return [self.examples[i] for i in selected]
    
    def _select_class_balanced(self, query: str, k: int) -> List[Dict]:
        """Equal number of examples from each class"""
        from collections import defaultdict
        import random
        
        by_class = defaultdict(list)
        for ex in self.examples:
            cls = ex.get("class", "default")
            by_class[cls].append(ex)
        
        classes = list(by_class.keys())
        per_class = max(1, k // len(classes))
        
        selected = []
        for cls in classes:
            samples = random.sample(by_class[cls], min(per_class, len(by_class[cls])))
            selected.extend(samples)
        
        return selected[:k]
    
    def _select_progressive(self, query: str, k: int) -> List[Dict]:
        """Start with easy examples, progress to harder ones"""
        sorted_examples = sorted(
            self.examples, 
            key=lambda x: x.get("difficulty", 1)
        )
        
        # Select across difficulty levels
        n = len(sorted_examples)
        if n <= k:
            return sorted_examples
        
        step = max(1, n // k)
        selected = [sorted_examples[i] for i in range(0, n, step)][:k]
        return selected
    
    def format(self, examples: List[Dict], format_type: str = "standard") -> str:
        """Format examples for prompt"""
        
        formatters = {
            "standard": self._format_standard,
            "xml": self._format_xml,
            "json": self._format_json,
            "numbered": self._format_numbered,
        }
        
        return formatters.get(format_type, self._format_standard)(examples)
    
    def _format_standard(self, examples: List[Dict]) -> str:
        lines = []
        for i, ex in enumerate(examples):
            lines.append(f"Ví dụ {i+1}:")
            lines.append(f"Input: {ex['input']}")
            lines.append(f"Output: {ex['output']}")
            lines.append("")
        return "\n".join(lines)
    
    def _format_xml(self, examples: List[Dict]) -> str:
        lines = []
        for i, ex in enumerate(examples):
            lines.append(f"<example id=\"{i+1}\">")
            lines.append(f"  <input>{ex['input']}</input>")
            lines.append(f"  <output>{ex['output']}</output>")
            lines.append("</example>")
        return "\n".join(lines)
    
    def _format_json(self, examples: List[Dict]) -> str:
        simplified = [{"input": ex["input"], "output": ex["output"]} for ex in examples]
        return json.dumps(simplified, ensure_ascii=False, indent=2)
    
    def _format_numbered(self, examples: List[Dict]) -> str:
        lines = []
        for i, ex in enumerate(examples):
            lines.append(f"{i+1}. {ex['input']} → {ex['output']}")
        return "\n".join(lines)
    
    def _get_embedding(self, text: str):
        if text not in self._embeddings_cache:
            self._embeddings_cache[text] = self.embed(text)
        return self._embeddings_cache[text]
    
    def _cosine_similarity(self, a, b):
        a, b = np.array(a), np.array(b)
        norm_a, norm_b = np.linalg.norm(a), np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))
