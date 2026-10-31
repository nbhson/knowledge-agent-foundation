def fixed_size_chunk(text, chunk_size=500, overlap=50):
    """
    Chia theo số ký tự cố định với overlap để tránh mất context.
    
    chunk_size: Số ký tự mỗi chunk
    overlap: Số ký tự chồng lấp giữa các chunk liên tiếp
    
    Ví dụ:
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
        start = end - overlap  # Lùi lại overlap ký tự
    
    return chunks

# Example
text = "Bảo hiểm y tế là hình thức bảo hiểm bắt buộc. " * 10
chunks = fixed_size_chunk(text, chunk_size=100, overlap=20)
print(f"Số chunks: {len(chunks)}")
