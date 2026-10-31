from sentence_transformers import CrossEncoder
import numpy as np

class Reranker:
    """Re-rank documents using a cross-encoder model"""

    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query, documents, top_k=5):
        """
        Re-rank documents based on query relevance

        Args:
            query: The search query
            documents: A list of document strings or dicts
            top_k: The number of results to return

        Returns:
            The reranked list with scores
        """
        # Create (query, document) pairs
        if isinstance(documents[0], dict):
            doc_texts = [d["document"] for d in documents]
        else:
            doc_texts = documents

        pairs = [(query, doc) for doc in doc_texts]

        # Score with the cross-encoder
        scores = self.model.predict(pairs)

        # Combine and sort
        results = []
        for i, (doc, score) in enumerate(zip(documents, scores)):
            if isinstance(doc, dict):
                result = {**doc, "rerank_score": float(score)}
            else:
                result = {"document": doc, "rerank_score": float(score)}
            results.append(result)

        results.sort(key=lambda x: x["rerank_score"], reverse=True)
        return results[:top_k]

    def rerank_with_feedback(self, query, documents, top_k=5,
                              user_feedback=None):
        """
        Re-rank with optional user feedback (learning from clicks)
        """
        results = self.rerank(query, documents, top_k=top_k * 2)

        if user_feedback:
            # Boost the documents the user found relevant
            for r in results:
                doc_text = r["document"]
                if doc_text in user_feedback.get("relevant", []):
                    r["rerank_score"] *= 1.5  # Boost
                elif doc_text in user_feedback.get("irrelevant", []):
                    r["rerank_score"] *= 0.5  # Penalize

        results.sort(key=lambda x: x["rerank_score"], reverse=True)
        return results[:top_k]
