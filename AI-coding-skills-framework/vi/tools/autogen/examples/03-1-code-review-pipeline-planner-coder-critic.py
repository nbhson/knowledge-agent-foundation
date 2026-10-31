planner  = AssistantAgent(name="planner",  system_message="Tạo kế hoạch chi tiết")
coder    = AssistantAgent(name="coder",    system_message="Viết code theo plan")
critic   = AssistantAgent(name="critic",   system_message="Review lỗi logic & an toàn")

group_chat = GroupChat(agents=[planner, coder, critic], max_round=15)
manager = GroupChatManager(groupchat=group_chat)

# Harness khởi động hội đồng
result = manager.run(task="Implement login API with rate limiting")
