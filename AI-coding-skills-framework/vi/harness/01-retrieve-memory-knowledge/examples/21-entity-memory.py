class EntityMemory:
    """
    Theo dõi entities (người, nơi, sự kiện) được nhắc đến
    
    ✅ Structured information
    ✅ Persistent across sessions
    ❌ Cần NER (Named Entity Recognition)
    """
    
    def __init__(self):
        self.entities = {}  # entity_name -> {attributes}
    
    def extract_and_update(self, text, llm_func):
        """Extract entities from text and update memory"""
        prompt = f"""Extract entities from this text:
Text: {text}

Format as JSON:
{{
  "entities": [
    {{"name": "...", "type": "person/org/location/...", "attributes": {{"key": "value"}}}},
  ]
}}"""
        
        response = llm_func(prompt)
        
        # Parse and update
        import json
        try:
            data = json.loads(response)
            for entity in data.get("entities", []):
                name = entity["name"]
                if name not in self.entities:
                    self.entities[name] = {
                        "type": entity.get("type", "unknown"),
                        "attributes": {},
                    }
                self.entities[name]["attributes"].update(
                    entity.get("attributes", {})
                )
        except json.JSONDecodeError:
            pass
    
    def recall(self, entity_name):
        """Recall information about an entity"""
        return self.entities.get(entity_name, None)
    
    def get_context_string(self):
        """Get all entities as context string"""
        lines = []
        for name, data in self.entities.items():
            attrs = ", ".join(
                f"{k}={v}" for k, v in data["attributes"].items()
            )
            lines.append(f"- {name} ({data['type']}): {attrs}")
        return "\n".join(lines)
