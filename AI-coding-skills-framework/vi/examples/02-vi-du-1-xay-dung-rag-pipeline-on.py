# Bước 1: Chunk documents
from pathlib import Path

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start = start + chunk_size - overlap
    return chunks

# Bước 2: Embed chunks với Ollama
import requests

def embed_text(text):
    response = requests.post("http://localhost:11434/api/embed", json={
        "model": "nomic-embed-text",
        "input": text
    })
    return response.json()["embeddings"][0]

# Bước 3: Tạo vector store đơn giản
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

# Bước 4: Generate câu trả lời
def generate_answer(query, context_docs):
    context = "\\n".join([f"- {doc}" for doc in context_docs])
    prompt = f"""Dựa vào thông tin sau, trả lời câu hỏi.

Thông tin:
{context}

Câu hỏi: {query}

Trả lời:"""
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3:12b",
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]
