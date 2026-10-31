def recursive_split(text, chunk_size=500, overlap=50,
                    separators=["\n\n", "\n", ". ", " "]):
    """
    Split by text structure, prioritizing the most important separator.

    Priority order:
    1. "\n\n" (paragraph)
    2. "\n" (new line)
    3. ". " (sentence)
    4. " " (word)

    → Respects the natural structure of the text
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

        # If it was split into multiple chunks, return them
        if len(chunks) > 1:
            return chunks

    return [text]

# Example
text = """Article 1: Health insurance is a mandatory form of insurance.

Article 2: The health insurance contribution rate is 4.5% of the base salary.

Article 3: Participants are entitled to benefits as prescribed by law.

Article 4: The health insurance card is valid for 5 years."""

chunks = recursive_split(text, chunk_size=80)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk[:60]}...")
