from autogen import GroupChat, GroupChatManager

agents = [planner, assistant, critic, executor]
group_chat = GroupChat(
    agents=agents,
    messages=[],
    max_round=20,
    speaker_selection_method="auto"  # hoặc "round_robin", "vote"
)
manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)
