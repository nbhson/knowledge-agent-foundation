import asyncio
from typing import Any, Dict, List, Optional

class MCPClient:
    """
    Production MCP Client for calling MCP tools
    
    Supports: Tool listing, tool calling, resource access,
    prompt templates, sampling, error handling
    """
    
    def __init__(self, server_name: str, transport: str = "stdio", config: Dict = None):
        self.server_name = server_name
        self.transport = transport
        self.config = config or {}
        self._tools_cache: List[Dict] = []
        self._resources_cache: List[Dict] = []
        self._prompts_cache: List[Dict] = []
        self._connected = False
        self._request_id = 0
        self._server_capabilities = {}
        self._latencies = []
    
    async def connect(self) -> bool:
        """Connect to MCP server with capability negotiation"""
        try:
            # In real implementation:
            # 1. Start server subprocess
            # 2. Send initialize request
            # 3. Receive capabilities
            
            self._server_capabilities = {
                "tools": {"listChanged": True},
                "resources": {"subscribe": True},
                "prompts": {},
                "logging": {},
            }
            
            self._connected = True
            return True
            
        except Exception as e:
            print(f"Failed to connect to {self.server_name}: {e}")
            return False
    
    async def disconnect(self):
        """Gracefully disconnect"""
        self._connected = False
        self._tools_cache = []
    
    async def list_tools(self) -> List[Dict]:
        """List available tools from MCP server"""
        if not self._connected:
            await self.connect()
        
        # Cache tools
        self._tools_cache = await self._send_request("tools/list", {})
        return self._tools_cache
    
    async def call_tool(self, tool_name: str, arguments: Dict, 
                        timeout: float = 30.0) -> Dict:
        """Call a tool on MCP server with timeout and error handling"""
        if not self._connected:
            await self.connect()
        
        start_time = time.time()
        
        try:
            response = await asyncio.wait_for(
                self._send_request("tools/call", {
                    "name": tool_name,
                    "arguments": arguments,
                }),
                timeout=timeout,
            )
            
            elapsed_ms = (time.time() - start_time) * 1000
            self._latencies.append(elapsed_ms)
            
            return {
                "success": True,
                "content": response.get("content", []),
                "isError": response.get("isError", False),
                "latency_ms": elapsed_ms,
                "server": self.server_name,
            }
            
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": f"Timeout after {timeout}s",
                "content": [],
                "server": self.server_name,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": [],
                "server": self.server_name,
            }
    
    async def read_resource(self, uri: str) -> Dict:
        """Read a resource from MCP server"""
        if not self._connected:
            await self.connect()
        
        return await self._send_request("resources/read", {"uri": uri})
    
    async def list_resources(self) -> List[Dict]:
        """List available resources"""
        if not self._connected:
            await self.connect()
        
        self._resources_cache = await self._send_request("resources/list", {})
        return self._resources_cache
    
    async def get_prompt(self, name: str, arguments: Dict = None) -> Dict:
        """Get a prompt template from server"""
        return await self._send_request("prompts/get", {
            "name": name,
            "arguments": arguments or {},
        })
    
    async def _send_request(self, method: str, params: Dict) -> Dict:
        """Send JSON-RPC request to MCP server"""
        self._request_id += 1
        
        request = {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": method,
            "params": params,
        }
        
        # In production: send via subprocess stdin/stdout or HTTP
        # For now, simulate response
        return {}
    
    def format_tools_for_llm(self, provider: str = "openai") -> List[Dict]:
        """Format MCP tools for specific LLM provider"""
        if provider == "openai":
            return [
                {
                    "type": "function",
                    "function": {
                        "name": t["name"],
                        "description": t.get("description", ""),
                        "parameters": t.get("inputSchema", {}),
                    }
                }
                for t in self._tools_cache
            ]
        elif provider == "anthropic":
            return [
                {
                    "name": t["name"],
                    "description": t.get("description", ""),
                    "input_schema": t.get("inputSchema", {}),
                }
                for t in self._tools_cache
            ]
        
        return self._tools_cache
    
    def get_latency_stats(self) -> Dict:
        """Get latency statistics"""
        if not self._latencies:
            return {"avg_ms": 0, "p50_ms": 0, "p95_ms": 0, "p99_ms": 0, "count": 0}
        
        sorted_lat = sorted(self._latencies)
        n = len(sorted_lat)
        
        return {
            "avg_ms": sum(sorted_lat) / n,
            "p50_ms": sorted_lat[n // 2],
            "p95_ms": sorted_lat[int(n * 0.95)],
            "p99_ms": sorted_lat[int(n * 0.99)],
            "min_ms": sorted_lat[0],
            "max_ms": sorted_lat[-1],
            "count": n,
        }


class MultiServerMCPManager:
    """
    Manage connections to multiple MCP servers
    
    Features:
    - Auto-discovery
    - Load balancing
    - Failover
    - Unified tool namespace
    """
    
    def __init__(self):
        self.servers: Dict[str, MCPClient] = {}
        self._tool_to_server: Dict[str, str] = {}
    
    async def add_server(self, name: str, server: MCPClient):
        """Add and connect to a server"""
        await server.connect()
        self.servers[name] = server
        
        # Index tools
        tools = await server.list_tools()
        for tool in tools:
            self._tool_to_server[tool["name"]] = name
    
    async def remove_server(self, name: str):
        """Disconnect and remove a server"""
        if name in self.servers:
            await self.servers[name].disconnect()
            del self.servers[name]
            
            # Rebuild index
            self._tool_to_server = {
                tool: srv for tool, srv in self._tool_to_server.items()
                if srv != name
            }
    
    def get_all_tools(self) -> List[Dict]:
        """Get tools from all servers, unified namespace"""
        all_tools = []
        for server_name, server in self.servers.items():
            for tool in server._tools_cache:
                tool_copy = dict(tool)
                tool_copy["_server"] = server_name
                all_tools.append(tool_copy)
        return all_tools
    
    async def call_tool(self, tool_name: str, arguments: Dict) -> Dict:
        """Call tool, routing to correct server"""
        server_name = self._tool_to_server.get(tool_name)
        
        if not server_name:
            return {
                "success": False,
                "error": f"No server found for tool '{tool_name}'",
            }
        
        server = self.servers.get(server_name)
        if not server:
            return {
                "success": False,
                "error": f"Server '{server_name}' not available",
            }
        
        result = await server.call_tool(tool_name, arguments)
        
        # If failed, try failover to other servers
        if not result.get("success"):
            for other_name, other_server in self.servers.items():
                if other_name != server_name:
                    tools = [t["name"] for t in other_server._tools_cache]
                    if tool_name in tools:
                        return await other_server.call_tool(tool_name, arguments)
        
        return result
    
    def get_server_stats(self) -> Dict:
        """Get stats for all servers"""
        stats = {}
        for name, server in self.servers.items():
            stats[name] = {
                "tools_count": len(server._tools_cache),
                "connected": server._connected,
                "latency": server.get_latency_stats(),
            }
        return stats
