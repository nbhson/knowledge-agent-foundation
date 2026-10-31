# ─── System Prompts ───

SYSTEM_PROMPT = PromptTemplate(
    name="system_prompt",
    template="""Bạn là {role}, chuyên gia về {domain}.

NGÔN NGỮ: {language}
PHONG CÁCH: {style}

QUY TẮC:
{rules}

{{#if examples}}
VÍ DỤ THAM KHẢO:
{examples}
{{/if}}

{{#if constraints}}
HẠN CHẾ:
{constraints}
{{/if}}""",
    variables=["role", "domain", "language", "style", "rules", "examples", "constraints"],
    required_variables=["role", "domain", "language", "style", "rules"],
    version="2.0.0",
    description="System prompt template với conditional sections",
)

# ─── RAG Prompt ───

RAG_PROMPT = PromptTemplate(
    name="rag_prompt",
    template="""Dựa trên thông tin sau, hãy trả lời câu hỏi.

CONTEXT:
{context}

CÂU HỎI: {question}

YÊU CẦU:
- Chỉ dùng thông tin từ context
- Nếu không đủ thông tin, nói rõ "Không đủ thông tin từ context"
- Trích dẫn nguồn cụ thể khi có thể
{{#if output_format}}
- Output format: {output_format}
{{/if}}

TRẢ LỜI:""",
    variables=["context", "question", "output_format"],
    required_variables=["context", "question"],
    version="1.0.0",
    description="RAG prompt với source citation",
)

# ─── Few-shot Prompt ───

FEWSHOT_PROMPT = PromptTemplate(
    name="fewshot_prompt",
    template="""{system_message}

VÍ DỤ:
{examples}

TASK:
{input}

OUTPUT:""",
    variables=["system_message", "examples", "input"],
    required_variables=["system_message", "examples", "input"],
    version="1.0.0",
    description="Few-shot prompt template",
)

# ─── Code Generation Prompt ───

CODEGEN_PROMPT = PromptTemplate(
    name="codegen_prompt",
    template="""You are an expert {language} developer.

Task: {task}

{{#if context}}
Context:
{context}
{{/if}}

{{#if existing_code}}
Current code to modify:
```{language}
{existing_code}
