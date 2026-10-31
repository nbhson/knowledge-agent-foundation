class IntentClassifier:
    """
    Multi-strategy intent classification:
    1. Rule-based (fast, no LLM needed)
    2. Embedding-based (moderate accuracy)
    3. LLM-based (highest accuracy, most expensive)
    
    Auto-selects strategy based on confidence threshold
    """
    
    INTENT_RULES = {
        "search": {
            "keywords": ["find", "search", "lookup", "google"],
            "tools": ["vector_search", "web_search", "query_knowledge_graph"],
            "priority": 1,
        },
        "calculate": {
            "keywords": ["calculate", "compute", "math", "how much", "percent", "sum", "average"],
            "tools": ["calculator", "execute_python", "data_analysis"],
            "priority": 2,
        },
        "code": {
            "keywords": ["code", "write code", "program", "function", "script", "implement", "refactor"],
            "tools": ["execute_python", "write_file", "search_code"],
            "priority": 1,
        },
        "read": {
            "keywords": ["read", "open", "show", "display", "cat"],
            "tools": ["read_file", "git_status"],
            "priority": 2,
        },
        "write": {
            "keywords": ["write", "save", "create file"],
            "tools": ["write_file", "store_memory"],
            "priority": 2,
        },
        "remember": {
            "keywords": ["remember", "note", "don't forget"],
            "tools": ["store_memory"],
            "priority": 3,
        },
        "recall": {
            "keywords": ["recall", "earlier", "mentioned", "history", "previous"],
            "tools": ["recall_memory"],
            "priority": 3,
        },
        "knowledge": {
            "keywords": ["what do you know", "knowledge", "facts", "information about", "define", "what is"],
            "tools": ["query_knowledge_graph", "vector_search", "lookup_definition"],
            "priority": 2,
        },
        "test": {
            "keywords": ["test", "run test", "verify", "validate", "check"],
            "tools": ["run_tests"],
            "priority": 2,
        },
        "git": {
            "keywords": ["git", "commit", "branch", "diff", "merge", "push", "pull"],
            "tools": ["git_status", "git_diff"],
            "priority": 2,
        },
    }
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
        self.classification_history = []
    
    def classify_rule_based(self, query: str) -> Dict:
        """Fast rule-based classification"""
        query_lower = query.lower()
        scores = {}
        
        for intent, config in self.INTENT_RULES.items():
            score = sum(1 for kw in config["keywords"] if kw in query_lower)
            # Boost by priority
            if score > 0:
                score = score * (4 - config.get("priority", 2))
                scores[intent] = score
        
        if not scores:
            return {"intent": "chat", "tools": [], "confidence": 0.5, "method": "rule"}
        
        best_intent = max(scores, key=scores.get)
        confidence = min(scores[best_intent] / 5, 1.0)
        
        return {
            "intent": best_intent,
            "tools": self.INTENT_RULES[best_intent]["tools"],
            "confidence": confidence,
            "method": "rule",
            "all_scores": scores,
        }
    
    def classify_llm_based(self, query: str) -> Dict:
        """LLM-based classification (more accurate, more expensive)"""
        intents_desc = "\n".join([
            f"- {intent}: keywords={config['keywords'][:3]}..., tools={config['tools']}"
            for intent, config in self.INTENT_RULES.items()
        ])
        
        prompt = f"""Analyze the user's intent and pick the most suitable tool.

User query: "{query}"

Possible intents:
{intents_desc}

Output JSON:
{{
  "intent": "...",
  "tools": ["tool1", "tool2"],
  "confidence": 0.0-1.0,
  "reasoning": "Why this intent was chosen",
  "parameters_hint": {{"param": "suggested value"}}
}}"""
        
        response = self.llm(prompt)
        try:
            result = json.loads(response)
            result["method"] = "llm"
            return result
        except json.JSONDecodeError:
            return self.classify_rule_based(query)  # Fallback
    
    def classify(self, query: str, strategy: str = "auto") -> Dict:
        """
        Classify with auto-strategy selection
        
        Strategies:
        - "auto": Rule first, LLM if confidence < threshold
        - "rule": Rule-based only
        - "llm": LLM-based only
        - "ensemble": Combine both
        """
        
        if strategy == "rule" or strategy == "auto":
            rule_result = self.classify_rule_based(query)
            
            if strategy == "rule":
                return rule_result
            
            # Auto: use LLM if rule confidence is low
            if rule_result["confidence"] >= 0.7:
                return rule_result
            
            if self.llm:
                llm_result = self.classify_llm_based(query)
                
                # Take the higher confidence result
                if llm_result.get("confidence", 0) > rule_result["confidence"]:
                    return llm_result
            
            return rule_result
        
        elif strategy == "llm":
            if self.llm:
                return self.classify_llm_based(query)
            return self.classify_rule_based(query)
        
        elif strategy == "ensemble":
            rule_result = self.classify_rule_based(query)
            llm_result = None
            
            if self.llm:
                llm_result = self.classify_llm_based(query)
            
            if llm_result and rule_result["intent"] == llm_result.get("intent"):
                # Agreement → high confidence
                return {
                    "intent": rule_result["intent"],
                    "tools": rule_result["tools"],
                    "confidence": 0.95,
                    "method": "ensemble",
                }
            elif llm_result:
                # Disagreement → use LLM
                llm_result["method"] = "ensemble_override"
                return llm_result
            
            return rule_result
        
        return self.classify_rule_based(query)
    
    def classify_multi_intent(self, query: str) -> List[Dict]:
        """
        Detect multiple intents in a single query
        E.g., "Find the README file and run tests" → [read, test]
        """
        # Split by conjunction words
        import re
        parts = re.split(r'\s+(and|;|then|after that)\s+', query)
        
        intents = []
        for part in parts:
            part = part.strip()
            if part.lower() in ['and', ';', 'then', 'after that']:
                continue
            if len(part) > 3:  # Skip very short parts
                intent = self.classify(part)
                intents.append(intent)
        
        return intents if intents else [self.classify(query)]
