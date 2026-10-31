group_chat = GroupChat(
    agents=[planner, coder, critic],
    messages=[],
    max_round=12,
    speaker_selection_method="round_robin",
)
