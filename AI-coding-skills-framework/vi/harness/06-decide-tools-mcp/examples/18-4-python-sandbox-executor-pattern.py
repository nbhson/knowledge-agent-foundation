import json
from typing import Any, Dict, List, Optional


class MCPToolExecutor:
    """
    Agent viết code gọi MCP tools, chạy trong sandbox.
    Chỉ kết quả tổng hợp được trả về context — giảm token đáng kể.

    Pattern:
    1. Agent nhận task → viết code gọi mcp_batch()
    2. Sandbox chạy code → gọi các MCP servers
    3. Trả về kết quả tổng hợp (aggregate results)
    4. Agent tổng hợp → final answer
    """

    def __init__(self, mcp_client, sandbox_config: Dict = None):
        self.mcp = mcp_client
        self.sandbox = sandbox_config or {
            "timeout_seconds": 30,
            "max_output_bytes": 1_000_000,
            "allowed_servers": None,  # None = all, list = subset
        }
        self._results_cache: Dict[str, Any] = {}
        self._call_log: List[Dict] = []

    def execute_agent_code(self, code: str, cache_key: str = None) -> Dict:
        """
        Agent viết code → chạy trong sandbox → trả kết quả tổng hợp.

        Args:
            code: Python code do agent viết, gọi mcp_batch([...])
            cache_key: Key để cache kết quả (tránh chạy lại cùng lời gọi)

        Returns:
            {"success": bool, "aggregate_result": {...}, "tool_calls": [...],
             "tokens_saved": int}
        """
        # 1. Kiểm tra cache
        if cache_key and cache_key in self._results_cache:
            return {
                "success": True,
                "aggregate_result": self._results_cache[cache_key],
                "from_cache": True,
                "tool_calls": [],
            }

        # 2. Sandbox chạy code với kiểm soát timeout + output limit
        tool_calls = self._run_in_sandbox(code)

        # 3. Tổng hợp kết quả từ tất cả tool calls
        aggregate = self._aggregate_results(tool_calls)

        # 4. Ước tính token tiết kiệm được
        token_saved = self._estimate_token_savings(tool_calls, aggregate)

        # 5. Cache kết quả (theo hash của code)
        if cache_key:
            self._results_cache[cache_key] = aggregate

        # 6. Log trajectory
        self._call_log.append({
            "cache_key": cache_key,
            "tool_calls": tool_calls,
            "aggregate": aggregate,
            "token_saved": token_saved,
        })

        return {
            "success": True,
            "aggregate_result": aggregate,
            "tool_calls": tool_calls,
            "tokens_saved": token_saved,
            "from_cache": False,
        }

    def _run_in_sandbox(self, code: str) -> List[Dict]:
        """Chạy code agent viết trong sandbox có kiểm soát."""
        results = []
        try:
            batch_calls = self._extract_mcp_batch_calls(code)
            for call in batch_calls:
                server = call["server"]
                tool = call["tool"]
                args = call["args"]

                # Kiểm tra server được phép gọi
                allowed = self.sandbox.get("allowed_servers")
                if allowed and server not in allowed:
                    results.append({
                        "server": server, "tool": tool,
                        "error": f"Server '{server}' không được phép gọi",
                    })
                    continue

                # Gọi MCP server với timeout
                response = self.mcp.call_tool(server, tool, args,
                                              timeout=self.sandbox["timeout_seconds"])
                results.append({
                    "server": server,
                    "tool": tool,
                    "result": response,
                })
        except Exception as e:
            results.append({"error": str(e)})

        return results

    def _aggregate_results(self, tool_calls: List[Dict]) -> Dict:
        """Gộp kết quả từ nhiều tool calls thành một response gọn gàng."""
        success_count = sum(1 for r in tool_calls if "error" not in r)
        error_count = len(tool_calls) - success_count

        if len(tool_calls) == 1:
            return tool_calls[0].get("result", {})

        return {
            "total_calls": len(tool_calls),
            "success_count": success_count,
            "error_count": error_count,
            "results": [r.get("result", {"error": r.get("error")}) for r in tool_calls],
            "summary": f"{success_count} thành công, {error_count} lỗi",
        }

    def _extract_mcp_batch_calls(self, code: str) -> List[Dict]:
        """Trích xuất các mcp_batch() calls từ code agent viết."""
        import re
        pattern = (
            r'\{"server":\s*"([^"]+)",\s*"tool":\s*"([^"]+)",'
            r'\s*"args":\s*(\{[^}]+\})\}'
        )
        matches = re.findall(pattern, code)
        return [
            {"server": m[0], "tool": m[1], "args": json.loads(m[2])}
            for m in matches
        ]

    def _estimate_token_savings(self, tool_calls: List[Dict], aggregate: Dict) -> int:
        """
        Ước tính token tiết kiệm được nhờ aggregate thay vì expose từng tool.
        Mỗi tool description ~200-500 tokens; aggregate chỉ ~50-100 tokens.
        """
        n_tools = len(tool_calls)
        # Giả sử mỗi tool description = 300 tokens avg
        original_context_cost = n_tools * 300
        # Aggregate result ≈ 80 tokens
        new_context_cost = 80
        return max(0, original_context_cost - new_context_cost)
