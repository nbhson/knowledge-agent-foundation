RELATION_PROMPT = """Cho danh sách entities và văn bản, trích xuất quan hệ.

Entities:
{entities}

Văn bản:
{text}

Các loại quan hệ hợp lệ:
- MANAGES: Person -> Person
- APPROVES: Person -> Document
- WORKS_ON: Person -> Project
- BELONGS_TO: Document -> Project
- REPORTS_TO: Person -> Person

Trả về JSON:
[{{"source": "Nguyễn Văn A", "target": "Hợp đồng C-2024", "type": "APPROVES", "confidence": 0.9, "evidence": "..."}}]
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
# [{"source": "Nguyễn Văn A", "target": "Hợp đồng C-2024", "type": "APPROVES", "confidence": 0.9}, ...]
