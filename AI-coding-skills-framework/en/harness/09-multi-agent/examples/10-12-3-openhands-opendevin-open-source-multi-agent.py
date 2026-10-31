# OpenHands architecture pattern — simplified implementation
# Based on open-source OpenHands (formerly OpenDevin) architecture

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field

@dataclass
class AgentConfig:
    """Configuration for one agent in a multi-agent system"""
    name: str
    model: str
    system_prompt: str
    tools: List[str]
    max_iterations: int = 20
    max_tokens: int = 100000
    temperature: float = 0.0


class OpenHandsStyleOrchestrator:
    """
    Multi-agent orchestrator in the OpenHands/Devin style.
    
    Key patterns:
    - Central brain (LLM) decides actions
    - Sandbox environment for safe execution
    - Iterative read→act→observe cycle
    - Conversation memory across iterations
    - Automatic retry on failure
    """
    
    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.sandbox_state: Dict = {
            "files": {},
            "env_vars": {},
            "processes": [],
        }
        self.tool_registry: Dict[str, Callable] = {}
        self.metrics = {
            "total_tokens": 0,
            "total_actions": 0,
            "files_modified": set(),
            "errors": 0,
        }
    
    def register_tool(self, name: str, func: Callable):
        """Register a tool for the agent to use"""
        self.tool_registry[name] = func
    
    def run_agent_loop(self, task: str, config: AgentConfig,
                       llm_func: Callable) -> Dict:
        """
        Main agent loop — core execution cycle:
        1. LLM observes state
        2. LLM decides action
        3. System executes action
        4. System observes result
        5. Repeat until done or max iterations
        """
        self.conversation_history.append({
            "role": "user",
            "content": task,
        })
        
        for iteration in range(config.max_iterations):
            # 1. Build context for LLM
            context = self._build_context(config)
            
            # 2. Get LLM action
            action = llm_func(context)
            self.metrics["total_actions"] += 1
            
            # 3. Parse action
            parsed = self._parse_action(action)
            
            # 4. Execute action
            if parsed["type"] == "finish":
                return {
                    "status": "completed",
                    "iterations": iteration + 1,
                    "metrics": self.metrics,
                    "result": parsed.get("output", ""),
                }
            
            if parsed["type"] == "error":
                self.metrics["errors"] += 1
                if self.metrics["errors"] > 3:
                    return {
                        "status": "failed",
                        "reason": "Too many errors",
                        "iterations": iteration + 1,
                        "metrics": self.metrics,
                    }
                continue
            
            # Execute tool
            result = self._execute_tool(parsed)
            
            # 5. Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": action,
            })
            self.conversation_history.append({
                "role": "environment",
                "content": f"Tool result: {result}",
            })
        
        return {
            "status": "max_iterations",
            "iterations": config.max_iterations,
            "metrics": self.metrics,
        }
    
    def _build_context(self, config: AgentConfig) -> str:
        """Build context for the LLM call"""
        parts = [config.system_prompt]
        
        # Add sandbox state summary
        parts.append(f"\nSandbox state: {len(self.sandbox_state['files'])} files")
        
        # Add conversation history (limited)
        recent = self.conversation_history[-20:]  # Last 20 messages
        for msg in recent:
            parts.append(f"{msg['role']}: {msg['content'][:500]}")
        
        # Add available tools
        parts.append(f"\nAvailable tools: {list(self.tool_registry.keys())}")
        
        return "\n".join(parts)
    
    def _parse_action(self, action: str) -> Dict:
        """Parse LLM action output"""
        if "FINISH" in action.upper():
            return {"type": "finish", "output": action}
        elif "ERROR" in action.upper():
            return {"type": "error", "message": action}
        else:
            return {"type": "tool_use", "tool": "default", "args": action}
    
    def _execute_tool(self, parsed: Dict) -> str:
        """Execute tool call"""
        tool_name = parsed.get("tool", "default")
        if tool_name in self.tool_registry:
            try:
                result = self.tool_registry[tool_name](parsed.get("args", ""))
                return str(result)[:2000]  # Limit output size
            except Exception as e:
                return f"Tool error: {str(e)}"
        return f"Unknown tool: {tool_name}"
