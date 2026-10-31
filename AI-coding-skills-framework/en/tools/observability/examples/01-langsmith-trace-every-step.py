from langsmith import Client
from langchain_openai import ChatOpenAI

# Auto-traces every LLM call when using LangChain
llm = ChatOpenAI(model="gpt-4", callbacks=[tracing_callback])

# See it in the LangSmith UI:
#   - Chain steps: retrieve → build → agent → tools
#   - Token usage per call
#   - Latency per node
#   - User feedback/reviews
