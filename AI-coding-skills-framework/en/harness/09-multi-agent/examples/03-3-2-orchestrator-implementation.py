from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

class OrchestrationMode(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"
    NEGOTIATION = "negotiation"
    EVENT_DRIVEN = "event_driven"


class AgentOrchestrator:
    """
    Central orchestrator manages agent lifecycle, routing,
    and coordination.
    
    Modes:
    - sequential: Agents execute one after another
    - parallel: Independent agents run simultaneously
    - hierarchical: Manager delegates to workers
    - negotiation: Agents discuss to reach consensus
    """
    
    def __init__(self, mode: OrchestrationMode = OrchestrationMode.SEQUENTIAL):
        self.mode = mode
        self.agents: Dict[str, Any] = {}
        self.router = MessageRouter()
        self.execution_log: List[Dict] = []
        self.max_retries = 2
        self.token_budget = 100000
        self.tokens_used = 0
    
    def register_agent(self, agent_id: str, role: AgentRole,
                       agent_instance: Any = None):
        """Register an agent with the orchestrator"""
        self.agents[agent_id] = {
            "role": role,
            "instance": agent_instance,
            "status": "idle",
            "tasks_completed": 0,
            "errors": 0,
            "avg_tokens": 0,
        }
        self.router.register_agent(agent_id)
    
    def execute_pipeline(self, tasks: List[Dict[str, Any]]) -> Dict:
        """
        Execute tasks through the agent pipeline.
        
        Each task: {
            "id": str,
            "type": str,          # maps to AgentRole
            "input": Dict,
            "depends_on": [str],  # task IDs
        }
        """
        results = {}
        executed = set()
        
        # Topological sort based on dependencies
        execution_order = self._resolve_execution_order(tasks)
        
        for task in execution_order:
            task_id = task["id"]
            
            # Check dependencies
            deps_met = all(
                dep in executed 
                for dep in task.get("depends_on", [])
            )
            if not deps_met:
                results[task_id] = {
                    "status": "skipped",
                    "reason": "Dependencies not met"
                }
                continue
            
            # Route to appropriate agent
            agent_id = self._route_task(task)
            if not agent_id:
                results[task_id] = {
                    "status": "failed",
                    "reason": "No available agent for task type"
                }
                continue
            
            # Execute with retry
            result = self._execute_with_retry(
                agent_id, task, 
                context=results
            )
            results[task_id] = result
            executed.add(task_id)
            
            # Track token usage
            self.tokens_used += result.get("tokens_used", 0)
            if self.tokens_used > self.token_budget:
                break
        
        return {
            "results": results,
            "tokens_used": self.tokens_used,
            "tasks_completed": len(executed),
            "execution_log": self.execution_log,
        }
    
    def _route_task(self, task: Dict) -> Optional[str]:
        """Route task to best available agent"""
        task_type = task.get("type", "")
        
        # Map task type to agent role
        role_map = {
            "plan": AgentRole.PLANNER,
            "architect": AgentRole.ARCHITECT,
            "code": AgentRole.CODER,
            "review": AgentRole.CODE_REVIEWER,
            "test": AgentRole.TESTER,
            "debug": AgentRole.DEBUGGER,
            "deploy": AgentRole.DEVOPS,
            "docs": AgentRole.DOC_WRITER,
            "refactor": AgentRole.REFACTORER,
            "security": AgentRole.SECURITY_AUDITOR,
        }
        
        target_role = role_map.get(task_type)
        if not target_role:
            return None
        
        # Find available agent with matching role
        for agent_id, info in self.agents.items():
            if (info["role"] == target_role 
                and info["status"] == "idle"):
                return agent_id
        
        return None
    
    def _execute_with_retry(self, agent_id: str, task: Dict,
                            context: Dict = None) -> Dict:
        """Execute a task with retry logic"""
        agent = self.agents[agent_id]
        agent["status"] = "busy"
        
        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                # Simulate agent execution
                result = {
                    "status": "success",
                    "output": f"Task {task['id']} completed by {agent_id}",
                    "tokens_used": task.get("estimated_tokens", 1000),
                    "attempt": attempt + 1,
                }
                
                agent["tasks_completed"] += 1
                agent["status"] = "idle"
                
                self.execution_log.append({
                    "task_id": task["id"],
                    "agent_id": agent_id,
                    "attempt": attempt + 1,
                    "status": "success",
                })
                
                return result
                
            except Exception as e:
                last_error = str(e)
                agent["errors"] += 1
                
                self.execution_log.append({
                    "task_id": task["id"],
                    "agent_id": agent_id,
                    "attempt": attempt + 1,
                    "status": "error",
                    "error": last_error,
                })
        
        agent["status"] = "idle"
        return {
            "status": "failed",
            "error": last_error,
            "attempts": self.max_retries + 1,
        }
    
    def _resolve_execution_order(self, tasks: List[Dict]) -> List[Dict]:
        """Topological sort tasks by dependencies"""
        task_map = {t["id"]: t for t in tasks}
        in_degree = {t["id"]: 0 for t in tasks}
        
        for task in tasks:
            for dep in task.get("depends_on", []):
                if dep in in_degree:
                    in_degree[task["id"]] += 1
        
        from collections import deque
        queue = deque([t for t, d in in_degree.items() if d == 0])
        order = []
        
        while queue:
            task_id = queue.popleft()
            order.append(task_map[task_id])
            
            for task in tasks:
                if task_id in task.get("depends_on", []):
                    in_degree[task["id"]] -= 1
                    if in_degree[task["id"]] == 0:
                        queue.append(task_id)
        
        return order
    
    def get_status_report(self) -> str:
        """Report the orchestrator's status"""
        lines = [
            "=== Orchestrator Status ===",
            f"Mode: {self.mode.value}",
            f"Tokens used: {self.tokens_used:,} / {self.token_budget:,}",
            f"Agents: {len(self.agents)}",
            "",
            "Agent Status:",
        ]
        for aid, info in self.agents.items():
            lines.append(
                f"  {aid}: {info['role'].value} "
                f"[{info['status']}] "
                f"tasks={info['tasks_completed']} "
                f"errors={info['errors']}"
            )
        
        return "\n".join(lines)
