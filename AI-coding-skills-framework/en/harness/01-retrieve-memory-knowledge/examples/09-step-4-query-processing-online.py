"""
Step 4: Process the query before searching

Techniques:
- Query Expansion: Create multiple variations
- HyDE: Create a hypothetical answer before searching
- Query Rewriting: Rewrite the query to be clearer
"""

class QueryProcessor:
    def __init__(self, llm_func):
        self.llm = llm_func

    def expand_query(self, query):
        """
        Create multiple variations of the query to increase recall

        Input: "How much is the health insurance contribution?"
        Output: [
            "health insurance contribution rate",
            "how much is the health insurance fee",
            "health insurance contribution percentage"
        ]
        """
        prompt = f"""Create 3 different questions based on the following question to search for information:

Original question: {query}

Write 3 questions (one per line):"""

        response = self.llm(prompt)
        variations = [q.strip() for q in response.split('\n') if q.strip()]
        return [query] + variations

    def hyde_query(self, query):
        """
        HyDE (Hypothetical Document Embeddings):
        Create a hypothetical answer, then use it to search

        Idea: The hypothetical answer will be closer to the real answer
        in the embedding space
        """
        prompt = f"""Write a short paragraph answering the following question:

Question: {query}

Short answer:"""

        hypothetical_answer = self.llm(prompt)
        return hypothetical_answer

    def classify_query(self, query):
        """
        Classify the query to choose the appropriate search strategy

        Simple: only needs 1 source
        Complex: needs multiple sources
        Aggregation: needs calculation/data combining
        """
        prompt = f"""Classify the following question:

Question: {query}

Type (simple/complex/aggregation):"""

        response = self.llm(prompt).strip().lower()
        return response if response in ["simple", "complex", "aggregation"] else "simple"
