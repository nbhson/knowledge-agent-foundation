import requests

OLLAMA_URL = "http://localhost:11434"

EXTRACTION_PROMPT = """Extract entities from the text below.
Only extract these types: Person, Project, Document, Organization.

Text:
{text}

Already extracted (to avoid duplicates):
{already_extracted}

Return a JSON list:
[{{"name": "...", "type": "Person", "description": "..."}}]

If there are no new entities, return []
"""

def extract_entities(text: str, model: str = "gemma3:12b", max_gleanings: int = 2) -> list:
    """Gleaning loop: extract in multiple rounds to increase coverage."""
    all_entities = []
    already = set()
    
    for glean_round in range(max_gleanings + 1):
        prompt = EXTRACTION_PROMPT.format(
            text=text,
            already_extracted=", ".join(already) if already else "none yet"
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
        
        # Filter out duplicates
        added = 0
        for ent in new_entities:
            key = ent["name"].lower().strip()
            if key not in already:
                already.add(key)
                all_entities.append(ent)
                added += 1
        
        print(f"Gleaning round {glean_round}: +{added} entities")
        if added == 0:
            break  # Nothing new left
    
    return all_entities

# Usage
text = """
The Phoenix project was approved by Nguyen Van A. Contract C-2024 belongs to the Phoenix project.
Nguyen Van A reports to Tran Thi B, the company's CTO. Tran Thi B manages the AI team.
"""
entities = extract_entities(text)
print(entities)
# [{"name": "Nguyen Van A", "type": "Person", ...}, {"name": "Phoenix", "type": "Project", ...}, ...]
