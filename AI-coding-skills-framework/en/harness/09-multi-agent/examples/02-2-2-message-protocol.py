from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
import uuid

class MessageType(Enum):
    TASK_ASSIGN = "task_assign"
    TASK_COMPLETE = "task_complete"
    TASK_FAILED = "task_failed"
    REQUEST_INFO = "request_info"
    PROVIDE_INFO = "provide_info"
    FEEDBACK = "feedback"
    HEARTBEAT = "heartbeat"
    ESCALATE = "escalate"


@dataclass
class AgentMessage:
    """Standard message format for inter-agent communication"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    from_agent: str = ""
    to_agent: str = ""
    message_type: MessageType = MessageType.TASK_ASSIGN
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    reply_to: Optional[str] = None
    priority: int = 5       # 1=highest
    ttl_seconds: int = 300   # Time to live
    
    def to_prompt_context(self) -> str:
        """Convert message to readable prompt context"""
        lines = [
            f"From: {self.from_agent}",
            f"Type: {self.message_type.value}",
            f"Time: {self.timestamp}",
            "---",
        ]
        for key, value in self.payload.items():
            lines.append(f"{key}: {value}")
        return "\n".join(lines)


class MessageRouter:
    """
    Routes messages between agents — manages message queues
    and delivery.
    """
    
    def __init__(self):
        self.queues: Dict[str, List[AgentMessage]] = {}
        self.message_log: List[AgentMessage] = []
        self.handlers: Dict[str, Callable] = {}
    
    def register_agent(self, agent_id: str, 
                       handler: Callable = None):
        """Register an agent with the message router"""
        self.queues[agent_id] = []
        if handler:
            self.handlers[agent_id] = handler
    
    def send(self, message: AgentMessage) -> bool:
        """Send a message to an agent"""
        if message.to_agent not in self.queues:
            return False
        
        self.queues[message.to_agent].append(message)
        self.message_log.append(message)
        
        # Auto-deliver if handler registered
        if message.to_agent in self.handlers:
            handler = self.handlers[message.to_agent]
            handler(message)
        
        return True
    
    def receive(self, agent_id: str) -> List[AgentMessage]:
        """Receive messages for an agent"""
        messages = self.queues.get(agent_id, [])
        self.queues[agent_id] = []
        return messages
    
    def peek(self, agent_id: str) -> List[AgentMessage]:
        """View messages without removing them"""
        return self.queues.get(agent_id, [])
    
    def broadcast(self, sender: str, message_type: MessageType,
                  payload: Dict[str, Any]):
        """Send a message to all agents"""
        for agent_id in self.queues:
            if agent_id != sender:
                msg = AgentMessage(
                    from_agent=sender,
                    to_agent=agent_id,
                    message_type=message_type,
                    payload=payload,
                )
                self.send(msg)
    
    def get_metrics(self) -> Dict[str, int]:
        """Metrics about message activity"""
        return {
            "total_sent": len(self.message_log),
            "by_type": {
                mt.value: sum(
                    1 for m in self.message_log 
                    if m.message_type == mt
                )
                for mt in MessageType
            },
            "pending": {
                aid: len(q) for aid, q in self.queues.items()
            },
        }
