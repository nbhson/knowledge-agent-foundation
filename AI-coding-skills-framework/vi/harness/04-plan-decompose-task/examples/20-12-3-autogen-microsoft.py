from autogen import AssistantAgent, UserProxyAgent

planner = AssistantAgent(
    name="planner",
    llm_config={"model": "gpt-4"},
    system_message="""You are a planning specialist.
    Break down tasks into clear steps with dependencies.
    Always output JSON format."""
)

executor = AssistantAgent(
    name="executor",
    llm_config={"model": "gpt-4"},
    system_message="""You execute tasks based on the plan.
    Report completion status for each step."""
)

user = UserProxyAgent(
    name="user",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
)
