def chunk_for_extraction(text: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """Chia document thành chunks cho extraction — mỗi chunk trích riêng, rồi merge."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

# Extract từng chunk, rồi merge entities
def extract_from_document(doc_text: str) -> list:
    chunks = chunk_for_extraction(doc_text)
    all_entities = []
    for chunk in chunks:
        all_entities.extend(extract_entities(chunk, max_gleanings=1))
    return all_entities
