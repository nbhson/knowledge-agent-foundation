from langsmith import Client
from langchain_openai import ChatOpenAI

# Auto-trace mọi LLM call khi dùng LangChain
llm = ChatOpenAI(model="gpt-4", callbacks=[tracing_callback])

# Xem trong LangSmith UI:
#   - Chain steps: retrieve → build → agent → tools
#   - Token usage mỗi call
#   - Latency từng node
#   - Feedback/review của user
