# python 03-update-memory-store/lab_writeback.py

writer = MemoryWriter()

# 1. Store episodic memory
event_id = writer.write_episodic(
    "learning",
    "User learned about health insurance deduction rates",
    metadata={"topic": "health insurance", "importance": "medium"}
)

# 2. Store facts
writer.write_fact("health insurance", "contribution rate", "4.5% of base salary", confidence=0.95)
writer.write_fact("health insurance", "card validity", "5 years", confidence=0.99)
writer.write_fact("Ollama", "runs", "gemma3:12b", confidence=1.0)

# 3. Update user profile
writer.write_user_profile("user_1", {
    "name": "John Doe",
    "occupation": "developer",
    "interests": ["AI", "health insurance"]
})

# 4. Check stats
print(writer.get_stats())
# {'episodic_count': 1, 'entity_count': 3, 'event_count': 4}
