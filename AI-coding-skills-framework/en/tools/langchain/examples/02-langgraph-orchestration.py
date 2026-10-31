from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

graph = StateGraph(State)
graph.add_node("retrieve", retrieve_memory)   # harness/01
graph.add_node("build", build_context)        # harness/02
graph.add_node("agent", call_model)           # harness/05 + 06
graph.add_node("tools", ToolNode(tools))      # harness/06

graph.add_edge("retrieve", "build")
graph.add_edge("build", "agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")              # loop — like loop/
