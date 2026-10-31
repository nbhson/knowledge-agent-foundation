# ─── System Prompts ───

SYSTEM_PROMPT = PromptTemplate(
    name="system_prompt",
    template="""You are {role}, an expert in {domain}.

LANGUAGE: {language}
STYLE: {style}

RULES:
{rules}

{{#if examples}}
REFERENCE EXAMPLES:
{examples}
{{/if}}

{{#if constraints}}
CONSTRAINTS:
{constraints}
{{/if}}""",
    variables=["role", "domain", "language", "style", "rules", "examples", "constraints"],
    required_variables=["role", "domain", "language", "style", "rules"],
    version="2.0.0",
    description="System prompt template with conditional sections",
)

# ─── RAG Prompt ───

RAG_PROMPT = PromptTemplate(
    name="rag_prompt",
    template="""Based on the information below, answer the question.

CONTEXT:
{context}

QUESTION: {question}

REQUIREMENTS:
- Use only information from the context
- If information is insufficient, clearly state "Not enough information in the context"
- Cite specific sources when possible
{{#if output_format}}
- Output format: {output_format}
{{/if}}

ANSWER:""",
    variables=["context", "question", "output_format"],
    required_variables=["context", "question"],
    version="1.0.0",
    description="RAG prompt with source citation",
)

# ─── Few-shot Prompt ───

FEWSHOT_PROMPT = PromptTemplate(
    name="fewshot_prompt",
    template="""{system_message}

EXAMPLES:
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
