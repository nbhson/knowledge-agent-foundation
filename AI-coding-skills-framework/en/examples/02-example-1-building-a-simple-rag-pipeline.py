# Step 1: Chunk documents
from pathlib import Path

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start = start + chunk_size - overlap
    return chunks

# Step 2: Embed chunks with Ollama
import requests

def embed_text(text):
    response = requests.post("http://localhost:11434/api/embed", json={
        "model": "nomic-embed-text",
        "input": text
    })
    return response.json()["embeddings"][0]

# Step 3: Create a simple vector store
import numpy as np

class SimpleVectorStore:
    def __init__(self):
        self.vectors = []
        self.documents = []
    
    def add(self, doc, vector):
        self.documents.append(doc)
        self.vectors.append(vector)
    
    def search(self, query_vec, top_k=3):
        scores = []
        q = np.array(query_vec)
        for i, v in enumerate(self.vectors):
            score = np.dot(q, np.array(v)) / (np.linalg.norm(q) * np.linalg.norm(np.array(v)))
            scores.append((i, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return [(self.documents[i], s) for i, s in scores[:top_k]]

# Step 4: Generate the answer
def generate_answer(query, context_docs):
    context = "\\n".join([f"- {doc}" for doc in context_docs])
    prompt = f"""Based on the information below, answer the question.

Information:
{context}

Question: {query}

Answer:"""
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3:12b",
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]
