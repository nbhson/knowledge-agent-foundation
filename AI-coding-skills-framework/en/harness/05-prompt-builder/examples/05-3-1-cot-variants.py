class CoTPromptBuilder:
    """
    Chain-of-Thought prompt builder with multiple variants
    
    Variants:
    1. Standard CoT: "Let's think step by step"
    2. Zero-shot CoT: Add "Think carefully"
    3. Few-shot CoT: Show reasoning examples
    4. Self-consistency: Generate N paths, majority vote
    5. Tree-of-Thoughts: Explore multiple branches
    6. Graph-of-Thoughts: Non-linear reasoning
    """
    
    @staticmethod
    def standard(question: str) -> str:
        """Standard Chain-of-Thought"""
        return f"""Question: {question}

Let's think step by step:

Step 1: Analyze the problem
Step 2: Identify the necessary information
Step 3: Apply relevant knowledge
Step 4: Synthesize the results
...
Conclusion:"""
    
    @staticmethod
    def zero_shot(question: str) -> str:
        """Zero-shot CoT — no examples needed"""
        return f"""Question: {question}

Think carefully before answering. Explain the logic step by step.
Do not skip any step.

Answer:"""
    
    @staticmethod
    def few_shot(question: str, examples_text: str) -> str:
        """Few-shot CoT — show reasoning patterns"""
        return f"""Examples of how to think:

{examples_text}

Now, please think about the following question:

Question: {question}

Think step by step:"""
    
    @staticmethod
    def self_consistency(question: str, n_paths: int = 3) -> str:
        """
        Self-Consistency: Generate multiple reasoning paths,
        then take majority vote for final answer
        """
        paths = "\n\n".join(
            f"Approach {i+1}:\n... → Result: ..."
            for i in range(n_paths)
        )
        
        return f"""Question: {question}

Solve it in {n_paths} different ways:

{paths}

Compare the {n_paths} results above.
Final result (majority agreement):"""
    
    @staticmethod
    def tree_of_thoughts(question: str, n_branches: int = 3) -> str:
        """Tree of Thoughts — explore multiple branches"""
        branches = "\n\n".join(
            f"Branch {i+1}:\n  Thought: ...\n  Evaluation (1-10): ...\n  Result: ..."
            for i in range(n_branches)
        )
        
        return f"""Question: {question}

Explore {n_branches} different directions of thought:

{branches}

Evaluate the {n_branches} branches:
- Which branch has the best logic?
- Which branch has the most feasible result?

Choose the best branch and reach a conclusion:"""
    
    @staticmethod
    def structured_reasoning(question: str) -> str:
        """Structured reasoning with clear phases"""
        return f"""Question: {question}

=== PHASE 1: UNDERSTANDING ===
- What is the main problem?
- What information is already available?
- What information is missing?

=== PHASE 2: ANALYSIS ===
- What are the relevant factors?
- What are the relationships between the factors?
- What are the risks and opportunities?

=== PHASE 3: REASONING ===
- Apply logic/knowledge
- Consider multiple perspectives
- Evaluate alternatives

=== PHASE 4: CONCLUSION ===
- Main conclusion
- Confidence level (1-10)
- Limitations of the conclusion"""
