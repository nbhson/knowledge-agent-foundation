CLAIM_PROMPT = """Trích xuất các khẳng định (claims) từ văn bản.
Mỗi claim = 1 sự thật đáng lưu, kèm header (chủ đề) đơn giản.

Văn bản:
{text}

Trả về JSON list, mỗi phần tử:
{{"subject": "...", "predicate": "...", "object": "...", "description": "..."}}
Nếu không có claim, trả về []
"""

def extract_claims(text: str, model: str = "gemma3:12b") -> list:
    # (triển khai tương tự extract_entities — gọi LLM, parse JSON)
    ...
    return claims

# Mỗi claim được GẮN với chunk gốc → truy vết được về tài liệu
def attach_claims(chunks: list[dict]) -> list[dict]:
    for chunk in chunks:
        claims = extract_claims(chunk["text"])
        for c in claims:
            c["source_chunk_id"] = chunk["id"]   # ← evidence provenance
    return ...
