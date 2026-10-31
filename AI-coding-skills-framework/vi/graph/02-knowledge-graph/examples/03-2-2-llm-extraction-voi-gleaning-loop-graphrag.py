import requests

OLLAMA_URL = "http://localhost:11434"

EXTRACTION_PROMPT = """Trích xuất entities từ văn bản sau.
Chỉ trích các loại: Person, Project, Document, Organization.

Văn bản:
{text}

Đã trích trước đó (để tránh trùng):
{already_extracted}

Trả về JSON list:
[{{"name": "...", "type": "Person", "description": "..."}}]

Nếu không còn entity mới, trả về []
"""

def extract_entities(text: str, model: str = "gemma3:12b", max_gleanings: int = 2) -> list:
    """Gleaning loop: trích nhiều vòng để tăng coverage."""
    all_entities = []
    already = set()
    
    for glean_round in range(max_gleanings + 1):
        prompt = EXTRACTION_PROMPT.format(
            text=text,
            already_extracted=", ".join(already) if already else "chưa có"
        )
        
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        })
        import json as js
        try:
            new_entities = js.loads(resp.json()["response"])
        except:
            new_entities = []
        
        # Lọc trùng
        added = 0
        for ent in new_entities:
            key = ent["name"].lower().strip()
            if key not in already:
                already.add(key)
                all_entities.append(ent)
                added += 1
        
        print(f"Gleaning round {glean_round}: +{added} entities")
        if added == 0:
            break  # Không còn gì mới
    
    return all_entities

# Usage
text = """
Dự án Phoenix do Nguyễn Văn A phê duyệt. Hợp đồng C-2024 thuộc dự án Phoenix.
Nguyễn Văn A báo cáo cho Trần Thị B, CTO của công ty. Trần Thị B quản lý team AI.
"""
entities = extract_entities(text)
print(entities)
# [{"name": "Nguyễn Văn A", "type": "Person", ...}, {"name": "Phoenix", "type": "Project", ...}, ...]
