class StructuredOutputBuilder:
    """
    Control LLM output format with schemas
    
    Supports: JSON, XML, Markdown, CSV, custom formats
    """
    
    JSON_SCHEMA_PROMPT = """Trả lời dưới dạng JSON hợp lệ theo schema:

Schema:
{schema}

QUAN TRỌNG:
- Chỉ output JSON, không thêm text khác
- Không dùng markdown code blocks
- Schema phải đúng 100%"""
    
    XML_OUTPUT_PROMPT = """Trả lời dưới dạng XML:

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
            examples_text = "\nVí dụ:\n" + json.dumps(examples[0], ensure_ascii=False, indent=2)
        
        return f"""Trả lời dưới dạng JSON:

Schema:
{schema_description}
{examples_text}

QUAN TRỌNG: Chỉ output JSON thuần túy, không có markdown hay text thừa."""
    
    @staticmethod
    def markdown_output() -> str:
        """Generate Markdown output prompt"""
        return """Trả lời có cấu trúc bằng Markdown:
# Tiêu đề chính
### Tiêu đề con
- Điểm chính
- Chi tiết

**Bold** cho từ khóa quan trọng.
`Code` cho identifiers."""
    
    @staticmethod
    def table_output(columns: List[str]) -> str:
        """Generate table output prompt"""
        cols = " | ".join(columns)
        sep = " | ".join(["---"] * len(columns))
        return f"""Trả lời dưới dạng bảng Markdown:

| {cols} |
| {sep} |
"""
    
    @staticmethod
    def with_validation(prompt: str, schema: Dict) -> str:
        """Add validation rules to any prompt"""
        validation_rules = []
        
        if schema.get("type") == "json":
            validation_rules.append("Output phải là JSON hợp lệ")
        if schema.get("max_length"):
            validation_rules.append(f"Output tối đa {schema['max_length']} ký tự")
        if schema.get("required_fields"):
            validation_rules.append(f"Các field bắt buộc: {', '.join(schema['required_fields'])}")
        if schema.get("enum_fields"):
            for field, values in schema["enum_fields"].items():
                validation_rules.append(f"Field '{field}' phải là một trong: {values}")
        
        rules_text = "\n".join(f"- {r}" for r in validation_rules)
        
        return f"""{prompt}

VALIDATION RULES:
{rules_text}"""
    
    @staticmethod
    def pydantic_schema(model_class) -> str:
        """Generate prompt from Pydantic model"""
        schema = model_class.model_json_schema()
        return json.dumps(schema, indent=2)
