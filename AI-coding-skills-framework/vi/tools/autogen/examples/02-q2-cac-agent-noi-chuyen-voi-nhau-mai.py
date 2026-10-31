group_chat = GroupChat(
    agents=[planner, assistant, critic, executor],
    messages=[],
    max_round=20,
    speaker_selection_method="auto",
)
