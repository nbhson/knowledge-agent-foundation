# MAF new (2025+)
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

agent = OpenAIChatClient(model_id="gpt-4o").create_agent(
    name="assistant",
    instructions="You are a helpful assistant",
)
result = await agent.run("Hello!")
