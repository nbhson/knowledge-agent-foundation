from langgraph.graph import StateGraph, END

# Định nghĩa State Machine lập kế hoạch
def create_planning_graph():
    graph = StateGraph(dict)
    
    # Thêm các Node
    graph.add_node("analyze", analyze_task)
    graph.add_node("plan", create_plan)
    graph.add_node("validate", validate_plan)
    graph.add_node("execute", execute_step)
    graph.add_node("replan", replan_on_failure)
    
    # Thêm các Edge
    graph.add_edge("analyze", "plan")
    graph.add_edge("plan", "validate")
    graph.add_conditional_edges("validate", decide_next, {
        "pass": "execute",
        "fail": "replan",
        "done": END,
    })
    graph.add_edge("execute", "validate")
    graph.add_edge("replan", "validate")
    
    return graph.compile()
