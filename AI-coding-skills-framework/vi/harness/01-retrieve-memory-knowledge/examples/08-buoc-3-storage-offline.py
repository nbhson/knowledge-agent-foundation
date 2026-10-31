"""
Bước 3: Lưu vào Vector Database

Options: FAISS, ChromaDB, Qdrant, hoặc đơn giản là numpy array
"""

# Option A: Simple numpy storage (nhỏ, đơn giản)
class SimpleVectorStore:
    def __init__(self):
        self.vectors = []
        self.documents = []
        self.metadata = []
    
    def add(self, document, vector, metadata=None):
        self.documents.append(document)
        self.vectors.append(vector)
        self.metadata.append(metadata or {})
    
    def search(self, query_vector, top_k=5):
        """Search using cosine similarity"""
        query = np.array(query_vector)
        scores = []
        
        for i, vec in enumerate(self.vectors):
            v = np.array(vec)
            score = np.dot(query, v) / (np.linalg.norm(query) * np.linalg.norm(v))
            scores.append((i, score))
        
        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for idx, score in scores[:top_k]:
            results.append({
                "document": self.documents[idx],
                "score": score,
                "metadata": self.metadata[idx],
            })
        
        return results
    
    def save(self, path):
        """Save to disk"""
        import pickle
        with open(path, 'wb') as f:
            pickle.dump({
                "vectors": self.vectors,
                "documents": self.documents,
                "metadata": self.metadata,
            }, f)
    
    @classmethod
    def load(cls, path):
        """Load from disk"""
        import pickle
        store = cls()
        with open(path, 'rb') as f:
            data = pickle.load(f)
            store.vectors = data["vectors"]
            store.documents = data["documents"]
            store.metadata = data["metadata"]
        return store


# Option B: ChromaDB (persistent, feature-rich)
import chromadb

class ChromaVectorStore:
    def __init__(self, collection_name="documents"):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add(self, documents, embeddings=None, metadatas=None, ids=None):
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids or [f"doc_{i}" for i in range(len(documents))],
        )
    
    def search(self, query_embedding, top_k=5):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results
