import numpy as np

def semantic_chunking(text, embedding_func, threshold=0.5, 
                      min_chunk_sentences=2):
    """
    Chia dựa trên sự thay đổi ngữ nghĩa giữa các câu.
    
    Nếu 2 câu liên tiếp có similarity < threshold → tách ra
    
    threshold:
    - Cao (0.8):_chunks nhỏ, nhiều chunks hơn
    - Thấp (0.3): chunks lớn, ít chunks hơn
    """
    sentences = text.split('. ')
    if len(sentences) <= min_chunk_sentences:
        return [text]
    
    # Embed từng câu
    embeddings = [embedding_func(s) for s in sentences]
    
    # Tính similarity giữa các câu liên tiếp
    chunks = []
    current_chunk = [sentences[0]]
    
    for i in range(1, len(sentences)):
        # Cosine similarity
        sim = cosine_similarity(embeddings[i-1], embeddings[i])
        
        if sim < threshold:
            # Ngữ nghĩa thay đổi → tách chunk
            chunks.append('. '.join(current_chunk) + '.')
            current_chunk = [sentences[i]]
        else:
            current_chunk.append(sentences[i])
    
    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')
    
    return chunks

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
