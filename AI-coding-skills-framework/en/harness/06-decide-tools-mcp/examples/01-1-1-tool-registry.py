from typing import Any, Callable, Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import hashlib
import time

@dataclass
class ToolDefinition:
    """
    Production-grade tool definition with full metadata
    """
    name: str
    description: str
    parameters: Dict[str, Dict]  # {param_name: {"type": ..., "description": ...}}
    function: Callable = None
    category: str = "general"
    examples: List[Dict] = field(default_factory=list)
    
    # Harness metadata
    version: str = "1.0.0"
    author: str = "system"
    tags: List[str] = field(default_factory=list)
    requires_auth: bool = False
    requires_permission: str = "standard"  # standard, elevated, admin
    rate_limit_per_minute: int = 60
    timeout_seconds: int = 30
    max_retries: int = 3
    cost_per_call: float = 0.0  # Token cost estimate
    deprecation_date: Optional[str] = None
    replacement_tool: Optional[str] = None
    
    # Performance metrics
    avg_latency_ms: float = 0.0
    success_rate: float = 1.0
    total_calls: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "category": self.category,
            "version": self.version,
            "tags": self.tags,
            "requires_auth": self.requires_auth,
            "requires_permission": self.requires_permission,
            "rate_limit_per_minute": self.rate_limit_per_minute,
            "timeout_seconds": self.timeout_seconds,
            "avg_latency_ms": self.avg_latency_ms,
            "success_rate": self.success_rate,
            "total_calls": self.total_calls,
        }
    
    def is_deprecated(self) -> bool:
        if self.deprecation_date:
            return datetime.now().isoformat() > self.deprecation_date
        return False
    
    def update_metrics(self, latency_ms: float, success: bool):
        """Update running metrics"""
        self.total_calls += 1
        # Exponential moving average
        alpha = 0.1
        self.avg_latency_ms = alpha * latency_ms + (1 - alpha) * self.avg_latency_ms
        self.success_rate = alpha * (1.0 if success else 0.0) + (1 - alpha) * self.success_rate


class ToolRegistry:
    """
    Central registry for all available tools
    
    Supports: Registration, search, category filtering,
    versioning, deprecation, metrics tracking
    """
    
    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}
        self.categories: Dict[str, List[str]] = {}
        self.usage_log: List[Dict] = []
        self._aliases: Dict[str, str] = {}
    
    def register(self, tool: ToolDefinition):
        """Register a new tool"""
        if tool.name in self.tools:
            existing = self.tools[tool.name]
            if existing.version != tool.version:
                print(f"Warning: Updating tool '{tool.name}' from v{existing.version} to v{tool.version}")
        
        self.tools[tool.name] = tool
        if tool.category not in self.categories:
            self.categories[tool.category] = []
        if tool.name not in self.categories[tool.category]:
            self.categories[tool.category].append(tool.name)
    
    def unregister(self, name: str) -> bool:
        """Remove a tool from registry"""
        if name in self.tools:
            tool = self.tools.pop(name)
            if tool.category in self.categories:
                self.categories[tool.category] = [
                    n for n in self.categories[tool.category] if n != name
                ]
            return True
        return False
    
    def add_alias(self, alias: str, tool_name: str):
        """Add an alias for a tool"""
        self._aliases[alias] = tool_name
    
    def resolve_alias(self, name: str) -> str:
        """Resolve alias to actual tool name"""
        return self._aliases.get(name, name)
    
    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        resolved = self.resolve_alias(name)
        return self.tools.get(resolved)
    
    def list_tools(self, category=None, include_deprecated=False) -> List[ToolDefinition]:
        if category:
            names = self.categories.get(category, [])
            tools = [self.tools[n] for n in names if n in self.tools]
        else:
            tools = list(self.tools.values())
        
        if not include_deprecated:
            tools = [t for t in tools if not t.is_deprecated()]
        
        return tools
    
    def search(self, query: str, use_embedding: bool = False, embed_func=None) -> List[ToolDefinition]:
        """
        Search tools by keyword or semantic similarity
        """
        query_lower = query.lower()
        results = []
        
        for tool in self.tools.values():
            # Keyword matching
            name_match = query_lower in tool.name.lower()
            desc_match = query_lower in tool.description.lower()
            tag_match = any(query_lower in tag.lower() for tag in tool.tags)
            category_match = query_lower in tool.category.lower()
            
            if name_match or desc_match or tag_match or category_match:
                results.append(tool)
        
        # Semantic search if enabled
        if use_embedding and embed_func and not results:
            results = self._semantic_search(query, embed_func)
        
        # Sort by relevance (success rate * inverse latency)
        results.sort(
            key=lambda t: t.success_rate / max(t.avg_latency_ms, 1),
            reverse=True,
        )
        
        return results
    
    def _semantic_search(self, query: str, embed_func) -> List[ToolDefinition]:
        """Find tools by semantic similarity"""
        query_emb = embed_func(query)
        scored = []
        
        for tool in self.tools.values():
            tool_emb = embed_func(f"{tool.name}: {tool.description}")
            sim = self._cosine_sim(query_emb, tool_emb)
            if sim > 0.5:  # Threshold
                scored.append((sim, tool))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [tool for _, tool in scored[:5]]
    
    def _cosine_sim(self, a, b):
        import numpy as np
        a, b = np.array(a), np.array(b)
        norm_a, norm_b = np.linalg.norm(a), np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))
    
    def to_openai_format(self, include_deprecated=False) -> List[Dict]:
        """Export tools in OpenAI function calling format"""
        tools = self.list_tools(include_deprecated=include_deprecated)
        return [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": {
                        "type": "object",
                        "properties": t.parameters,
                        "required": [
                            k for k, v in t.parameters.items() 
                            if v.get("required", False)
                        ],
                    },
                }
            }
            for t in tools
        ]
    
    def to_mcp_format(self) -> List[Dict]:
        """Export tools in MCP format"""
        return [
            {
                "name": t.name,
                "description": t.description,
                "inputSchema": {
                    "type": "object",
                    "properties": t.parameters,
                },
            }
            for t in self.tools.values()
        ]
    
    def get_deprecated_tools(self) -> List[ToolDefinition]:
        """Get all deprecated tools"""
        return [t for t in self.tools.values() if t.is_deprecated()]
    
    def get_tool_stats(self) -> Dict:
        """Get aggregate stats for all tools"""
        tools = list(self.tools.values())
        total_calls = sum(t.total_calls for t in tools)
        avg_success = sum(t.success_rate for t in tools) / len(tools) if tools else 0
        
        return {
            "total_tools": len(tools),
            "total_categories": len(self.categories),
            "total_calls": total_calls,
            "avg_success_rate": avg_success,
            "deprecated": len([t for t in tools if t.is_deprecated()]),
            "by_category": {
                cat: len(names) for cat, names in self.categories.items()
            },
        }
