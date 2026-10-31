class MultiAgentDebugger:
    """Debug utilities cho multi-agent systems"""
    
    def __init__(self, orchestrator: AgentOrchestrator):
        self.orchestrator = orchestrator
        self.trace_log: List[Dict] = []
    
    def trace_message_flow(self) -> str:
        """Trace toàn bộ message flow giữa agents"""
        messages = self.orchestrator.router.message_log
        
        lines = ["=== Message Flow Trace ==="]
        for msg in messages:
            direction = "→" if msg.message_type in [
                MessageType.TASK_ASSIGN, MessageType.REQUEST_INFO
            ] else "←"
            lines.append(
                f"  {msg.from_agent} {direction} {msg.to_agent} "
                f"[{msg.message_type.value}] "
                f"at {msg.timestamp}"
            )
        
        return "\n".join(lines)
    
    def inspect_agent_state(self, agent_id: str) -> str:
        """Kiểm tra state của 1 agent"""
        agent = self.orchestrator.agents.get(agent_id, {})
        memory = self.orchestrator.router.peek(agent_id)
        
        lines = [
            f"=== Agent: {agent_id} ===",
            f"Role: {agent.get('role', 'unknown')}",
            f"Status: {agent.get('status', 'unknown')}",
            f"Tasks completed: {agent.get('tasks_completed', 0)}",
            f"Errors: {agent.get('errors', 0)}",
            f"Pending messages: {len(memory)}",
        ]
        
        return "\n".join(lines)
    
    def generate_timeline(self) -> str:
        """Tạo execution timeline"""
        log = self.orchestrator.execution_log
        
        lines = ["=== Execution Timeline ==="]
        for entry in log:
            status_icon = "✓" if entry["status"] == "success" else "✗"
            lines.append(
                f"  [{entry.get('attempt', 1)}] {status_icon} "
                f"{entry['task_id']} → {entry['agent_id']}"
            )
        
        return "\n".join(lines)
