def attach_claims(chunks):
    for chunk in chunks:
        for c in extract_claims(chunk["text"]):
            c["source_chunk_id"] = chunk["id"]   # provenance, set once
    return chunks
