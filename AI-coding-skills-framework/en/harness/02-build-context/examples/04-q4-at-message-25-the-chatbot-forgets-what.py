mgr = MultiTurnContextManager(max_turns=50, summary_threshold=20)
mgr.add_turn("user", "health insurance contribution?")
mgr.add_turn("assistant", "4.5% employee share")
mgr.add_turn("user", "and the validity period?")
prompt = mgr.build_context(max_tokens=4000)  # facts + summary + last 10
