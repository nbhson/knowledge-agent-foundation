def fixed_size_chunk(text, chunk_size=500, overlap=50):
    """
    Split by a fixed character count with overlap to avoid losing context.

    chunk_size: Number of characters per chunk
    overlap: Number of overlapping characters between consecutive chunks

    Example:
    chunk_size=10, overlap=2:
    "abcdefghij" → "abcdefghij"
    "klmnopqrst" → "ghijklmnop"
                    ^^ overlap ^^
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # Step back by the overlap amount

    return chunks

# Example
text = "Health insurance is a mandatory form of insurance. " * 10
chunks = fixed_size_chunk(text, chunk_size=100, overlap=20)
print(f"Number of chunks: {len(chunks)}")
