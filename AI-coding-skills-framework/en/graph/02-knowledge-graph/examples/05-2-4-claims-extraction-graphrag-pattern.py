CLAIM_PROMPT = """Extract assertions (claims) from the text.
Each claim = one fact worth keeping, with a simple header (topic).

Text:
{text}

Return a JSON list, each element:
{{"subject": "...", "predicate": "...", "object": "...", "description": "..."}}
If there are no claims, return []
"""

def extract_claims(text: str, model: str = "gemma3:12b") -> list:
    # (implementation similar to extract_entities — call the LLM, parse JSON)
    ...
    return claims

# Each claim is LINKED to its source chunk → traceable back to the document
def attach_claims(chunks: list[dict]) -> list[dict]:
    for chunk in chunks:
        claims = extract_claims(chunk["text"])
        for c in claims:
            c["source_chunk_id"] = chunk["id"]   # ← evidence provenance
    return ...
