graph.add_conditional_edges(
    "agent", should_continue, {"tools": "tools", END: END}
)
graph.add_edge("tools", "agent")   # loop, gated by should_continue only
