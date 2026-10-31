# Agent action loop — like loop/ but inside a graph
while True:
    action = agent.invoke(state)       # harness/04 plan
    if action.type == "finish": break  # answer the user
    result = execute_tool(action)      # harness/06 execute
    state = update_memory(result)      # harness/03 update
