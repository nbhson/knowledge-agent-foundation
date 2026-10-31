class PromptBuilder:
    """Advanced prompt building techniques for RAG"""
    
    def __init__(self, system_prompt=None):
        self.system_prompt = system_prompt or "You are a smart AI assistant."
    
    def build_with_instructions(self, query, context_docs, 
                                  custom_instructions=None):
        """
        Prompt with custom instructions
        
        Techniques:
        - Explicit constraints
        - Step-by-step instructions
        - Output format specification
        """
        instructions = custom_instructions or """
Rules:
1. Use only information from the provided context
2. Always cite sources [1], [2]...
3. If information is insufficient, say so clearly
4. Answer briefly and clearly
"""
        
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            score = doc.get("score", 0)
            text = doc["content"] if isinstance(doc, dict) else doc
            context_parts.append(f"[{i}] {text}")
        
        context = "\n".join(context_parts)
        
        return f"""{self.system_prompt}

{instructions}

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""
    
    def build_with_reasoning(self, query, context_docs):
        """
        Prompt that asks the model to "think" before answering

        Helps reduce hallucination and improve accuracy
        """
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            text = doc["content"] if isinstance(doc, dict) else doc
            context_parts.append(f"[{i}] {text}")
        
        context = "\n".join(context_parts)
        
        return f"""You are an analytical assistant.

INFORMATION:
{context}

QUESTION: {query}

FOLLOW THESE STEPS:
1. [ANALYZE] Identify which information in the context is relevant
2. [EVALUATE] Assess the completeness of the information
3. [SYNTHESIZE] Synthesize the relevant information
4. [ANSWER] Answer the question clearly

BEGIN:"""
    
    def build_with_format(self, query, context_docs, 
                           output_format="markdown"):
        """
        Prompt with a specific output format

        output_format: "markdown", "json", "table", "list"
        """
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            text = doc["content"] if isinstance(doc, dict) else doc
            context_parts.append(f"[{i}] {text}")
        
        context = "\n".join(context_parts)
        
        format_instructions = {
            "markdown": "Answer in Markdown format with headers and bullet points.",
            "json": 'Answer in JSON format: {"answer": "...", "sources": [...], "confidence": 0.0-1.0}',
            "table": "Answer in a Markdown table.",
            "list": "Answer as a numbered list.",
        }
        
        return f"""{self.system_prompt}

CONTEXT:
{context}

QUESTION: {query}

OUTPUT FORMAT: {format_instructions.get(output_format, "Natural text.")}

ANSWER:"""
    
    def build_with_guardrails(self, query, context_docs):
        """
        Prompt with guardrails to prevent hallucination

        Techniques:
        - Explicit "don't make up" instruction
        - Confidence scoring
        - Source verification
        """
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            text = doc["content"] if isinstance(doc, dict) else doc
            context_parts.append(f"[{i}] {text}")
        
        context = "\n".join(context_parts)
        
        return f"""You are a precise assistant. FOLLOW STRICTLY:

⚠️ SAFETY RULES:
- NEVER fabricate information
- Do not infer beyond the context
- If the context is insufficient → Say "Not enough information available"
- Every claim MUST cite a source [n]

CONTEXT:
{context}

QUESTION: {query}

EVALUATE BEFORE ANSWERING:
1. Does the context contain information that answers the question?
2. If YES → Answer + cite sources
3. If NO → Say clearly "No information from reference sources yet"

ANSWER:"""


# Usage
builder = PromptBuilder()

prompt = builder.build_with_guardrails(
    query="How much is the health insurance contribution?",
    context_docs=[
        {"content": "The health insurance contribution level is 4.5% of base salary", "score": 0.95},
        {"content": "Insurance cards are valid for 5 years", "score": 0.7},
    ]
)
