def recursive_split(text, chunk_size=500, separators=["\n\n", "\n", ". ", " "]):
    if len(text) <= chunk_size: return [text]
    for sep in separators:
        if sep in text:
            return [p.strip() for p in text.split(sep) if p.strip()]
    return [text]
