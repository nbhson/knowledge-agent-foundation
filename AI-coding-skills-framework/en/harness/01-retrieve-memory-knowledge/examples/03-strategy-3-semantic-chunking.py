import numpy as np

def semantic_chunking(text, embedding_func, threshold=0.5,
                      min_chunk_sentences=2):
    """
    Split based on semantic change between sentences.

    If two consecutive sentences have similarity < threshold → split them

    threshold:
    - High (0.8): small chunks, more of them
    - Low (0.3): large chunks, fewer of them
    """
    sentences = text.split('. ')
    if len(sentences) <= min_chunk_sentences:
        return [text]

    # Embed each sentence
    embeddings = [embedding_func(s) for s in sentences]

    # Compute similarity between consecutive sentences
    chunks = []
    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):
        # Cosine similarity
        sim = cosine_similarity(embeddings[i-1], embeddings[i])

        if sim < threshold:
            # Meaning changes → split the chunk
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
