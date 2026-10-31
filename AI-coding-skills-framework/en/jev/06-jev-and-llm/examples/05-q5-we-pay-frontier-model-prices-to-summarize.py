pick, info = route_model(task, agent_state)   # Jev difficulty question
if info["confidence"] < 0.70:                  # unsure → do not gamble cheap
    return "capable-model", info
return MODELS[pick], info                      # trivial→fast, hard→capable
