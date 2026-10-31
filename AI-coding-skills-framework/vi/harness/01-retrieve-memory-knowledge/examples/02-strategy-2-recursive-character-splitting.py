def recursive_split(text, chunk_size=500, overlap=50,
                    separators=["\n\n", "\n", ". ", " "]):
    """
    Chia theo cấu trúc văn bản, ưu tiên separator quan trọng nhất.
    
    Thứ tự ưu tiên:
    1. "\n\n" (đoạn văn)
    2. "\n" (dòng mới)
    3. ". " (câu)
    4. " " (từ)
    
    → Tôn trọng cấu trúc văn bản tự nhiên
    """
    if len(text) <= chunk_size:
        return [text]
    
    for sep in separators:
        if sep not in text:
            continue
        
        parts = text.split(sep)
        chunks = []
        current = ""
        
        for part in parts:
            candidate = current + sep + part if current else part
            if len(candidate) <= chunk_size:
                current = candidate
            else:
                if current:
                    chunks.append(current.strip())
                current = part
        
        if current:
            chunks.append(current.strip())
        
        # Nếu chia được thành nhiều chunks, trả về
        if len(chunks) > 1:
            return chunks
    
    return [text]

# Example
text = """Điều 1: Bảo hiểm y tế là hình thức bảo hiểm bắt buộc.

Điều 2: Mức đóng bảo hiểm y tế là 4.5% mức lương cơ sở.

Điều 3: Người tham gia được hưởng quyền lợi theo quy định.

Điều 4: Thẻ bảo hiểm y tế có hiệu lực trong 5 năm."""

chunks = recursive_split(text, chunk_size=80)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk[:60]}...")
