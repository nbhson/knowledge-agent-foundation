"""
Bước 2: Tạo embeddings cho tất cả chunks

Sử dụng: nomic-embed-text (Ollama) hoặc sentence-transformers
"""

import requests
import numpy as np

OLLAMA_URL = "http://localhost:11434"

class Embedder:
    def __init__(self, model="nomic-embed-text"):
        self.model = model
        self.cache = {}  # Simple cache
    
    def embed(self, text):
        """Embed single text"""
        if text in self.cache:
            return self.cache[text]
        
        response = requests.post(f"{OLLAMA_URL}/api/embed", json={
            "model": self.model,
            "input": text
        })
        
        embedding = response.json()["embeddings"][0]
        self.cache[text] = embedding
        return embedding
    
    def embed_batch(self, texts, batch_size=32):
        """Embed nhiều texts (Ollama supports batch)"""
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = requests.post(f"{OLLAMA_URL}/api/embed", json={
                "model": self.model,
                "input": batch
            })
            embeddings = response.json()["embeddings"]
            all_embeddings.extend(embeddings)
        
        return all_embeddings
    
    def embed_query(self, query):
        """Embed query (thêm prefix để phân biệt với documents)"""
        return self.embed(f"query: {query}")


# Usage
embedder = Embedder(model="nomic-embed-text")

# Embed chunks
chunks = ["BHYT là gì?", "Quy định BHYT 2024", ...]
embeddings = embedder.embed_batch(chunks)
