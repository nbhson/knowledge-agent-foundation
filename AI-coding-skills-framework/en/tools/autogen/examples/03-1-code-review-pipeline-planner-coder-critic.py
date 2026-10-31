planner  = AssistantAgent(name="planner",  system_message="Create a detailed plan")
coder    = AssistantAgent(name="coder",    system_message="Write code following the plan")
critic   = AssistantAgent(name="critic",   system_message="Review logic & safety errors")

group_chat = GroupChat(agents=[planner, coder, critic], max_round=15)
manager = GroupChatManager(groupchat=group_chat)

# The harness starts the council
result = manager.run(task="Implement login API with rate limiting")
