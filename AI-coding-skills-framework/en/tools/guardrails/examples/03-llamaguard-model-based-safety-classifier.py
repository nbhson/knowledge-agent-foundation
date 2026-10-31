# LlamaGuard is a specialized LLM — it only classifies:
#   UNSAFE: violence, illegal, PII, ...
#   SAFE:   normal

# Prompt: "<prompt>USER: {user_input or model_output}</prompt>"
# Output: "safe" or "unsafe" with the violation type
