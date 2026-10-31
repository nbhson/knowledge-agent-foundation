def chunk_for_extraction(text: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """Split a document into chunks for extraction — extract each chunk separately, then merge."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

# Extract from each chunk, then merge entities
def extract_from_document(doc_text: str) -> list:
    chunks = chunk_for_extraction(doc_text)
    all_entities = []
    for chunk in chunks:
        all_entities.extend(extract_entities(chunk, max_gleanings=1))
    return all_entities
