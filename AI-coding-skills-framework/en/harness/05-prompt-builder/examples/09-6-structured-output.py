class StructuredOutputBuilder:
    """
    Control LLM output format with schemas
    
    Supports: JSON, XML, Markdown, CSV, custom formats
    """
    
    JSON_SCHEMA_PROMPT = """Answer as valid JSON following the schema:

Schema:
{schema}

IMPORTANT:
- Output JSON only, no other text
- Do not use markdown code blocks
- Schema must match 100%"""
    
    XML_OUTPUT_PROMPT = """Answer in XML format:

Format:
<{root_tag}>
  <field1>value1</field1>
  <field2>value2</field2>
</{root_tag}>"""
    
    @staticmethod
    def json_output(schema_description: str, examples: List[Dict] = None) -> str:
        """Generate JSON output prompt"""
        examples_text = ""
        if examples:
            examples_text = "\nExample:\n" + json.dumps(examples[0], ensure_ascii=False, indent=2)
        
        return f"""Answer in JSON:

Schema:
{schema_description}
{examples_text}

IMPORTANT: Output pure JSON only, no markdown or extra text."""
    
    @staticmethod
    def markdown_output() -> str:
        """Generate Markdown output prompt"""
        return """Answer in structured Markdown:
# Main heading
### Sub-heading
- Main point
- Detail

**Bold** for important keywords.
`Code` for identifiers."""
    
    @staticmethod
    def table_output(columns: List[str]) -> str:
        """Generate table output prompt"""
        cols = " | ".join(columns)
        sep = " | ".join(["---"] * len(columns))
        return f"""Answer in a Markdown table:

| {cols} |
| {sep} |
"""
    
    @staticmethod
    def with_validation(prompt: str, schema: Dict) -> str:
        """Add validation rules to any prompt"""
        validation_rules = []
        
        if schema.get("type") == "json":
            validation_rules.append("Output must be valid JSON")
        if schema.get("max_length"):
            validation_rules.append(f"Output at most {schema['max_length']} characters")
        if schema.get("required_fields"):
            validation_rules.append(f"Required fields: {', '.join(schema['required_fields'])}")
        if schema.get("enum_fields"):
            for field, values in schema["enum_fields"].items():
                validation_rules.append(f"Field '{field}' must be one of: {values}")
        
        rules_text = "\n".join(f"- {r}" for r in validation_rules)
        
        return f"""{prompt}

VALIDATION RULES:
{rules_text}"""
    
    @staticmethod
    def pydantic_schema(model_class) -> str:
        """Generate prompt from Pydantic model"""
        schema = model_class.model_json_schema()
        return json.dumps(schema, indent=2)
