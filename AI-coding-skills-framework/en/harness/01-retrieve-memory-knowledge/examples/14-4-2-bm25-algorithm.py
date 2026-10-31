import math
from collections import Counter

class BM25:
    """
    The Okapi BM25 scoring function

    BM25(D, Q) = Σ IDF(qi) × (f(qi, D) × (k1 + 1)) /
                        (f(qi, D) + k1 × (1 - b + b × |D|/avgdl))

    Where:
    - IDF(qi): Inverse Document Frequency of term qi
    - f(qi, D): Term frequency of qi in document D
    - k1: Term saturation parameter (default 1.5)
    - b: Length normalization parameter (default 0.75)
    - |D|: Document length
    - avgdl: Average document length
    """

    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.documents = []
        self.doc_freqs = {}
        self.avgdl = 0
        self.n_docs = 0

    def fit(self, documents):
        """Build the index from documents"""
        self.documents = documents
        self.n_docs = len(documents)

        # Calculate document frequencies
        for doc in documents:
            terms = doc.lower().split()
            unique_terms = set(terms)
            for term in unique_terms:
                self.doc_freqs[term] = self.doc_freqs.get(term, 0) + 1

        # Average document length
        self.avgdl = sum(len(doc.split()) for doc in documents) / self.n_docs

    def _idf(self, term):
        """Inverse Document Frequency"""
        n_containing = self.doc_freqs.get(term, 0)
        return math.log((self.n_docs - n_containing + 0.5) / (n_containing + 0.5) + 1)

    def _score(self, document, query_terms):
        """BM25 score for a document"""
        terms = document.lower().split()
        doc_len = len(terms)
        term_freqs = Counter(terms)

        score = 0
        for term in query_terms:
            if term not in term_freqs:
                continue

            f = term_freqs[term]
            idf = self._idf(term)

            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)

            score += idf * numerator / denominator

        return score

    def search(self, query, top_k=10):
        """Search for the most relevant documents"""
        query_terms = query.lower().split()

        scores = []
        for i, doc in enumerate(self.documents):
            score = self._score(doc, query_terms)
            scores.append((i, score))

        scores.sort(key=lambda x: x[1], reverse=True)

        return [(self.documents[i], score) for i, score in scores[:top_k]]
