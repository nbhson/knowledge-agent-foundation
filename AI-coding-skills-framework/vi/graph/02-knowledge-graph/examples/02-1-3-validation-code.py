from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class Ontology:
    node_types: Dict[str, Dict]
    edge_types: Dict[str, Dict]
    
    def validate_node(self, label: str, props: Dict) -> tuple[bool, str]:
        if label not in self.node_types:
            return False, f"Unknown node type: {label}"
        schema = self.node_types[label]
        for prop, rules in schema.get("properties", {}).items():
            if rules.get("required") and prop not in props:
                return False, f"Missing required property: {prop}"
            if prop in props and "enum" in rules:
                if props[prop] not in rules["enum"]:
                    return False, f"Invalid value for {prop}: {props[prop]}"
        return True, "OK"
    
    def validate_edge(self, edge_type: str, from_label: str, to_label: str) -> tuple[bool, str]:
        if edge_type not in self.edge_types:
            return False, f"Unknown edge type: {edge_type}"
        rule = self.edge_types[edge_type]
        if rule["from"] != from_label or rule["to"] != to_label:
            return False, f"Edge {edge_type} requires {rule['from']} -> {rule['to']}, got {from_label} -> {to_label}"
        if from_label == to_label and edge_type == "MANAGES":
            return False, "Cannot manage self"
        return True, "OK"

# Usage
ontology = Ontology(
    node_types={
        "Person": {"properties": {"name": {"required": True}, "role": {"enum": ["CTO", "Engineer"]}}},
        "Project": {"properties": {"name": {"required": True}}},
    },
    edge_types={
        "MANAGES": {"from": "Person", "to": "Person"},
        "WORKS_ON": {"from": "Person", "to": "Project"},
    }
)
print(ontology.validate_node("Person", {"name": "Alice", "role": "CTO"}))  # (True, OK)
print(ontology.validate_edge("MANAGES", "Person", "Person"))  # (True, OK)
print(ontology.validate_edge("MANAGES", "Project", "Person"))  # (False, ...)
