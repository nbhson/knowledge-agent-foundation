RELATION_PROMPT = """Given a list of entities and a text, extract relations.

Entities:
{entities}

Text:
{text}

Valid relation types:
- MANAGES: Person -> Person
- APPROVES: Person -> Document
- WORKS_ON: Person -> Project
- BELONGS_TO: Document -> Project
- REPORTS_TO: Person -> Person

Return JSON:
[{{"source": "Nguyen Van A", "target": "Contract C-2024", "type": "APPROVES", "confidence": 0.9, "evidence": "..."}}]
"""

def extract_relations(text: str, entities: list, model: str = "gemma3:12b") -> list:
    ent_str = "\n".join(f"- {e['name']} ({e['type']})" for e in entities)
    prompt = RELATION_PROMPT.format(entities=ent_str, text=text)
    
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    })
    import json as js
    try:
        return js.loads(resp.json()["response"])
    except:
        return []

# Usage
relations = extract_relations(text, entities)
print(relations)
# [{"source": "Nguyen Van A", "target": "Contract C-2024", "type": "APPROVES", "confidence": 0.9}, ...]
