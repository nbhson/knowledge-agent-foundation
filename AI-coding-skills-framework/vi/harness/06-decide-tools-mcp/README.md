# 🔧 VI. Decide Tools / MCP Calls

> ## 📑 Mục Lục
>
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Tool Selection Patterns](#1-tool-selection-patterns)
>   - [1.1 Tool Registry](#11-tool-registry)
>   - [1.2 Example Tools — Extended Set](#12-example-tools-extended-set)
> - [2. Intent Classification](#2-intent-classification)
>   - [2.1 Multi-Strategy Intent Classifier](#21-multi-strategy-intent-classifier)
> - [3. MCP Protocol](#3-mcp-protocol)
>   - [3.1 MCP Architecture Deep Dive](#31-mcp-architecture-deep-dive)
>   - [3.2 MCP Client Implementation](#32-mcp-client-implementation)
> - [4. Tool Executor](#4-tool-executor)
> - [5. Function Calling](#5-function-calling)
> - [6. Tool Decision Pipeline](#6-tool-decision-pipeline)
> - [7. Tool Composition](#7-tool-composition)
> - [8. Permission System](#8-permission-system)
> - [9. Rate Limiting](#9-rate-limiting)
> - [10. Harness Integration](#10-harness-integration)
>   - [10.1 TypeScript Interfaces](#101-typescript-interfaces)
> - [11. Case Studies](#11-case-studies)
>   - [11.1. SWE-agent — Tool-Use for Software Engineering](#111-swe-agent-tool-use-for-software-engineering)
>   - [11.2. Claude Code — Hierarchical Tool Access](#112-claude-code-hierarchical-tool-access)
>   - [11.3. Cursor IDE — Context-Aware Tool Selection](#113-cursor-ide-context-aware-tool-selection)
> - [12. Design Principles](#12-design-principles)
>   - [12.1 SOLID Cho Tools](#121-solid-cho-tools)
> - [13. Best Practices](#13-best-practices)
>   - [13.1 DO ✅](#131-do)
>   - [13.2 DON'T ❌](#132-dont)
> - [14. Testing](#14-testing)
> - [15. Advanced Patterns](#15-advanced-patterns)
>   - [15.1 Tool Learning](#151-tool-learning)
> - [16. Tương Lai](#16-tương-lai)
>   - [16.1 Xu Hướng 2026-2028](#161-xu-hướng-2026-2028)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)
>   - [Papers & Research](#papers-research)
>   - [Frameworks & Tools](#frameworks-tools)
>
---

### Câu Chuyện Mở Đầu

Hãy tưởng tượng bạn ghé vào một **tiệm sửa xe** đầy ắp đồ nghề: cờ lê, tua vít, máy khoan, máy hàn... Bác thợ lâu năm liếc qua là biết ngay phải cầm món nào. Còn anh học việc mới vào nghề thì lóng ngóng — có khi lại mang **máy khoan ra vặn con ốc nhỏ**, tệ hơn là **vác búa gõ vào lốc máy**.

**Agent AI mà thiếu khả năng chọn tool khôn ngoan thì cũng y hệt như vậy.**

Mô hình ngôn ngữ thì "biết" gọi tool đấy, nhưng khi trong tay có tới **50+ tools**, chỉ cần chọn nhầm một cái hay truyền sai tham số là đủ rắc rối: tốn token vô ích, nhận về kết quả sai bét, hoặc tệ nhất là gây ra **hậu quả khó cứu vãn** — như xóa nhầm file quan trọng, gửi nhầm email, hay châm ngòi cho một hành động không thể quay lại.

**Cách gỡ rối**: dựng một quy trình chọn tool rõ ràng từng bước — **nghe xem user thật sự muốn gì → chọn tool hợp nhất → kiểm tra tham số cho kỹ → chạy thử → ngó lại kết quả xem ổn không**.

### Tại Sao Tool Decision Quan Trọng?

> *"Có 50 cái tool trong tay mà chọn sai thì cũng như có cả hộp búa nhưng lại mang búa ra đập kính."*

#### 3 Bằng Chứng Khoa Học

| # | Nghiên Cứu | Phát Hiện Quan Trọng |
|---|-----------|----------------------|
| 1 | **Anthropic MCP Research (2025)** | Agent sử dụng structured tool selection giảm **60% failed tool calls** so với unstructured approach |
| 2 | **LangChain Benchmark (2025)** | Tool selection accuracy tăng từ **65% lên 92%** khi sử dụng intent classification trước tool routing |
| 3 | **Princeton SWE-agent (2024)** | Giới hạn 50 search results + tool validation tăng **64% success rate** |

#### Triết lý cốt lõi:

```
Tool Selection = Intent Classification → Tool Matching → Parameter Validation → Execution → Result Validation
```

**Nói cho dễ nhớ**: chọn tool cũng như bác sĩ kê đơn — phải bắt đúng bệnh (intent), bốc đúng thuốc (tool), dặn đúng liều (parameters), rồi còn hẹn tái khám xem thuốc có hợp không (result validation).

**Nếu làm ẩu bước này**: gọi nhầm tool là mất tiền token, nhận kết quả trật lất, thậm chí rước họa (xóa nhầm file, gửi nhầm mail...).

## Tổng Quan

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Tool Decision là lúc agent quyết định "giờ dùng món nào, xài ra sao" — từ đọc đề bài, lựa tool, gọi API cho tới xử lý kết quả trả về.
>
> **Hình dung vui:** Module này là đôi "tay chân" của agent: mọi kế hoạch hay ho trong đầu (planning) muốn thành việc thật đều phải qua đây, giống cánh tay robot nghe lệnh từ bộ não (LLM) nhưng luôn có dây an toàn đi kèm.
>
> **Sao phải quan tâm:** Chọn đúng người, đúng việc, đúng cách thì xong việc; chọn ẩu là hỏng việc.

Nói ngắn gọn, agent lúc nào cũng quanh quẩn với hai câu hỏi: **việc này nên dùng tool nào?** và **gọi nó thế nào cho đúng?** Toàn bộ quá trình gói trong một vòng: đọc task → chọn tool → gọi API → xử gọn kết quả.

Trong Harness Engineering, Tool Decision chính là **"đôi tay"** biến kế hoạch trên giấy thành hành động thật. Tool nào muốn chạy cũng phải đi qua cổng kiểm soát, kiểm tra hợp lệ và ghi log đầy đủ.

```
┌──────────────────────────────────────────────────────────────────┐
│                 DECIDE TOOLS / MCP CALLS                          │
│                                                                  │
│  User Query                                                      │
│       │                                                          │
│       ▼                                                          │
│  ┌────────────────┐                                             │
│  │  INTENT        │  Phân tích ý định user                     │
│  │  CLASSIFIER    │  "search" / "calculate" / "code" / ...     │
│  └───────┬────────┘                                             │
│          ▼                                                       │
│  ┌────────────────┐                                             │
│  │  TOOL          │  Chọn tool phù hợp từ danh sách            │
│  │  SELECTOR      │  "vector_search" / "calculator" / ...      │
│  └───────┬────────┘                                             │
│          ▼                                                       │
│  ┌────────────────┐                                             │
│  │  PARAMETER     │  Trích xuất & validate parameters           │
│  │  EXTRACTOR     │  query="BHYT", top_k=5, ...                │
│  └───────┬────────┘                                             │
│          ▼                                                       │
│  ┌────────────────┐                                             │
│  │  GUARDRAILS    │  Validate permission, safety, rate limit    │
│  │  CHECK         │                                             │
│  └───────┬────────┘                                             │
│          ▼                                                       │
│  ┌────────────────┐                                             │
│  │  TOOL          │  Gọi tool (function call / MCP)             │
│  │  EXECUTOR      │  Handle errors, timeout, retry              │
│  └───────┬────────┘                                             │
│          ▼                                                       │
│  ┌────────────────┐                                             │
│  │  RESULT        │  Parse kết quả → Format → Trả lời          │
│  │  PROCESSOR     │                                             │
│  └────────────────┘                                             │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  HARNESS INTEGRATION                                       │  │
│  │  Memory ←→ Guardrails ←→ Feedback ←→ Permissions          │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Nội Dung

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Tool Selection Patterns](#1-tool-selection-patterns) | Registry, search, categories |
| 2 | [Intent Classification](#2-intent-classification) | Rule-based & LLM-based |
| 3 | [MCP Protocol](#3-mcp-protocol) | Model Context Protocol chi tiết |
| 4 | [Tool Executor](#4-tool-executor) | Error handling, retries, logging |
| 5 | [Function Calling](#5-function-calling) | OpenAI style + parallel calls |
| 6 | [Tool Decision Pipeline](#6-tool-decision-pipeline) | End-to-end pipeline |
| 7 | [Tool Composition](#7-tool-composition) | Chain & parallel tool calls |
| 8 | [Permission System](#8-permission-system) | RBAC cho tools |
| 9 | [Rate Limiting](#9-rate-limiting) | Token/usage quotas |
| 10 | [Harness Integration](#10-harness-integration) | TypeScript interfaces |
| 11 | [Case Studies](#11-case-studies) | SWE-agent, Claude Code, Cursor |
| 12 | [Design Principles](#12-design-principles) | SOLID cho tools |
| 13 | [Best Practices](#13-best-practices) | DO/DON'T chi tiết |
| 14 | [Testing](#14-testing) | Unit & integration tests |
| 15 | [Advanced Patterns](#15-advanced-patterns) | Tool learning, dynamic tools |
| 16 | [Tương Lai](#16-tương-lai) | Xu hướng 2026-2028 |

---

## 1. Tool Selection Patterns

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Tool Selection Patterns là mấy "chiêu" chọn tool của agent khi đứng trước cả một kho tool (registry, tìm kiếm, phân loại theo nhóm) — gặp việc nào thì rút món nào cho hợp.
>
> **Hình dung vui:** Như bác thợ sửa xe đứng trước tủ đồ nghề đầy ắp: người lành nghề chẳng cần đọc hướng dẫn từng cây cờ lê mà liếc con ốc là biết phải cầm cây nào.
>
> **Sao phải quan tâm:** Chọn trúng ngay từ đầu thì đỡ tốn token, tránh gây chuyện ngoài ý muốn và tăng khả năng làm xong việc.

### 1.1 Tool Registry

Mục này là cuốn "danh bạ" của cả nhà tool. `ToolDefinition` là tờ lý lịch của từng tool (tên gì, làm được gì, cần tham số nào, cần quyền gì, giới hạn gọi, timeout, chi phí...); còn `ToolRegistry` là bác quản thủ thư viện lo việc đăng ký, tìm kiếm, lọc theo nhóm, đánh dấu tool hết hạn và theo dõi xem tool nào chạy ngon, tool nào hay hỏng. Đọc thì cứ xem tờ lý lịch `ToolDefinition` trước, rồi ngó các hàm của `ToolRegistry` để biết "bác thủ thư" làm được những gì.

*Hình dung vui:* Như tủ thuốc dán nhãn cẩn thận — mỗi lọ ghi rõ công dụng (description), liều dùng (parameters), hạn dùng (deprecation date); còn registry là người giữ tủ, hỏi lọ nào là chỉ đúng ngăn đó.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
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
```

</details>

### 1.2 Example Tools — Extended Set

Mục này bày sẵn cho bạn một bộ tool "mở tủ là xài". Hàm `create_default_tools()` lần lượt đăng ký từng `ToolDefinition` vào `ToolRegistry` kèm tên, mô tả, tham số, nhóm và thẻ gợi nhớ. Để ý mấy tool nhạy cảm như `sql_query`, `execute_python`, `write_file` bị dán nhãn `requires_permission="elevated"` — tức là muốn chạy phải có quyền cao hơn mới được. Bộ tool này sẽ được xài chung cho các phần sau (phân loại ý định, chạy tool, viết test).

*Hình dung vui:* Như bộ hộp đồ nghề đóng sẵn cho người mới: khỏi phải đi chợ mua lẻ từng món, mở nắp ra là đủ đồ chơi cho hầu hết việc thường ngày.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
def create_default_tools():
    """Create comprehensive default toolset"""
    registry = ToolRegistry()
    
    # ─── Search Tools ───
    registry.register(ToolDefinition(
        name="vector_search",
        description="Tìm kiếm ngữ nghĩa trong cơ sở dữ liệu vector",
        parameters={
            "query": {"type": "string", "description": "Câu truy vấn", "required": True},
            "top_k": {"type": "integer", "description": "Số kết quả trả về", "default": 5},
            "collection": {"type": "string", "description": "Tên collection"},
            "filters": {"type": "object", "description": "Metadata filters"},
        },
        category="search",
        tags=["semantic", "vector", "embedding"],
        examples=[
            {"query": "BHYT cho người lao động", "top_k": 3},
        ],
    ))
    
    registry.register(ToolDefinition(
        name="web_search",
        description="Tìm kiếm trên internet",
        parameters={
            "query": {"type": "string", "description": "Từ khóa tìm kiếm", "required": True},
            "num_results": {"type": "integer", "default": 5},
            "region": {"type": "string", "default": "vn"},
        },
        category="search",
        tags=["internet", "realtime", "web"],
    ))
    
    registry.register(ToolDefinition(
        name="sql_query",
        description="Thực thi SQL query trên database",
        parameters={
            "query": {"type": "string", "description": "SQL query", "required": True},
            "database": {"type": "string", "default": "main"},
            "readonly": {"type": "boolean", "default": True},
        },
        category="search",
        requires_permission="elevated",
        tags=["database", "sql", "structured"],
    ))
    
    # ─── Computation Tools ───
    registry.register(ToolDefinition(
        name="calculator",
        description="Tính toán toán học an toàn",
        parameters={
            "expression": {"type": "string", "description": "Biểu thức toán học", "required": True},
        },
        category="computation",
        tags=["math", "arithmetic"],
    ))
    
    registry.register(ToolDefinition(
        name="execute_python",
        description="Thực thi code Python trong sandbox",
        parameters={
            "code": {"type": "string", "description": "Python code", "required": True},
            "timeout": {"type": "integer", "default": 30},
        },
        category="computation",
        requires_permission="elevated",
        tags=["python", "code", "sandbox"],
    ))
    
    registry.register(ToolDefinition(
        name="data_analysis",
        description="Phân tích dữ liệu với pandas/numpy",
        parameters={
            "data": {"type": "string", "description": "Data path hoặc CSV string", "required": True},
            "analysis_type": {"type": "string", "enum": ["summary", "correlation", "distribution", "trend"]},
            "columns": {"type": "array", "items": {"type": "string"}},
        },
        category="computation",
        tags=["analytics", "pandas", "statistics"],
    ))
    
    # ─── Code Tools ───
    registry.register(ToolDefinition(
        name="read_file",
        description="Đọc nội dung file",
        parameters={
            "path": {"type": "string", "description": "Đường dẫn file", "required": True},
            "encoding": {"type": "string", "default": "utf-8"},
            "max_lines": {"type": "integer", "description": "Max lines to read"},
        },
        category="file",
        tags=["read", "file", "filesystem"],
    ))
    
    registry.register(ToolDefinition(
        name="write_file",
        description="Ghi nội dung vào file",
        parameters={
            "path": {"type": "string", "description": "Đường dẫn file", "required": True},
            "content": {"type": "string", "description": "Nội dung", "required": True},
            "mode": {"type": "string", "enum": ["overwrite", "append"], "default": "overwrite"},
        },
        category="file",
        requires_permission="elevated",
        tags=["write", "file", "filesystem"],
    ))
    
    registry.register(ToolDefinition(
        name="search_code",
        description="Tìm kiếm code trong codebase",
        parameters={
            "query": {"type": "string", "description": "Regex hoặc text pattern", "required": True},
            "path": {"type": "string", "default": "."},
            "file_pattern": {"type": "string", "description": "glob pattern"},
        },
        category="code",
        tags=["code", "search", "regex"],
    ))
    
    registry.register(ToolDefinition(
        name="run_tests",
        description="Chạy test suite",
        parameters={
            "test_path": {"type": "string", "description": "Path to test file/directory"},
            "framework": {"type": "string", "enum": ["pytest", "unittest", "jest", "vitest"]},
            "verbose": {"type": "boolean", "default": True},
        },
        category="code",
        tags=["testing", "ci", "quality"],
    ))
    
    # ─── Knowledge Tools ───
    registry.register(ToolDefinition(
        name="query_knowledge_graph",
        description="Truy vấn knowledge graph",
        parameters={
            "entity": {"type": "string", "description": "Tên entity", "required": True},
            "relation": {"type": "string", "description": "Loại relation"},
            "max_hops": {"type": "integer", "default": 1},
        },
        category="knowledge",
        tags=["kg", "graph", "entity"],
    ))
    
    registry.register(ToolDefinition(
        name="lookup_definition",
        description="Tra cứu định nghĩa thuật ngữ",
        parameters={
            "term": {"type": "string", "description": "Thuật ngữ cần tra cứu", "required": True},
            "domain": {"type": "string", "description": "Lĩnh vực"},
        },
        category="knowledge",
        tags=["definition", "glossary", "reference"],
    ))
    
    # ─── Memory Tools ───
    registry.register(ToolDefinition(
        name="recall_memory",
        description="Nhớ lại thông tin từ memory",
        parameters={
            "query": {"type": "string", "description": "Câu truy vấn", "required": True},
            "memory_type": {"type": "string", "enum": ["episodic", "semantic", "all"]},
            "limit": {"type": "integer", "default": 5},
        },
        category="memory",
        tags=["recall", "memory", "history"],
    ))
    
    registry.register(ToolDefinition(
        name="store_memory",
        description="Lưu thông tin vào memory",
        parameters={
            "content": {"type": "string", "description": "Nội dung cần lưu", "required": True},
            "memory_type": {"type": "string", "enum": ["episodic", "semantic"]},
            "importance": {"type": "string", "enum": ["low", "medium", "high"]},
            "tags": {"type": "array", "items": {"type": "string"}},
        },
        category="memory",
        tags=["store", "memory", "persistence"],
    ))
    
    # ─── Communication Tools ───
    registry.register(ToolDefinition(
        name="send_notification",
        description="Gửi thông báo cho user",
        parameters={
            "message": {"type": "string", "description": "Nội dung thông báo", "required": True},
            "channel": {"type": "string", "enum": ["email", "slack", "in_app"], "default": "in_app"},
            "priority": {"type": "string", "enum": ["low", "normal", "high"], "default": "normal"},
        },
        category="communication",
        tags=["notify", "alert", "message"],
    ))
    
    # ─── Version Control Tools ───
    registry.register(ToolDefinition(
        name="git_status",
        description="Xem trạng thái git repository",
        parameters={
            "path": {"type": "string", "default": "."},
        },
        category="devops",
        tags=["git", "status", "vcs"],
    ))
    
    registry.register(ToolDefinition(
        name="git_diff",
        description="Xem diff của git changes",
        parameters={
            "ref": {"type": "string", "description": "Branch/commit to diff against"},
            "path": {"type": "string"},
        },
        category="devops",
        tags=["git", "diff", "changes"],
    ))
    
    return registry
```

</details>

---

## 2. Intent Classification

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Intent Classification là bước "đoán ý" user: chỉ cần nghe câu hỏi là biết họ muốn tìm kiếm, tính toán, viết code hay lưu ghi nhớ... rồi dẫn tới đúng nhóm tool. Thường kết hợp hai kiểu: rule-based (soi từ khóa, nhanh mà rẻ) với embedding/LLM-based (hiểu sâu hơn, tốn kém hơn) để vừa nhanh vừa trúng.
>
> **Hình dung vui:** Như chị lễ tân khách sạn nghe khách mở miệng một câu là đoán được họ cần đặt phòng, gọi xe hay hỏi giờ ăn sáng, rồi chuyển máy đúng bộ phận.
>
> **Sao phải quan tâm:** Đoán sai ý là gọi sai tool, vừa đốt token vừa trả lời lạc đề; đoán trúng là đặt nền móng cho mọi bước sau.

### 2.1 Multi-Strategy Intent Classifier

Mục này là bộ máy đoán ý ba tầng, đọc hiểu để xài lại. Tầng 1 là soi từ khóa (rule-based): thấy chữ "tìm", "tính", "đọc" là khoanh vùng ngay. Tầng 2 là nhờ LLM đọc kỹ rồi phán. Tầng 3 là chế độ auto: nếu rule đã chắc ăn (confidence từ 0.7 trở lên) thì tin luôn, còn lấn cấn mới gọi LLM cho chắc. Hàm `classify_multi_intent()` còn tách được câu dài nhiều ý, ví dụ "Đọc file và chạy test" thì tách thành hai ý [read, test].

*Hình dung vui:* Như quầy lễ tân có sẵn sổ kịch bản (rule) để trả lời nhanh mấy câu quen thuộc; chỉ khi gặp câu khoai mới nhấc máy gọi quản lý (LLM) xuống xử lý.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class IntentClassifier:
    """
    Multi-strategy intent classification:
    1. Rule-based (fast, no LLM needed)
    2. Embedding-based (moderate accuracy)
    3. LLM-based (highest accuracy, most expensive)
    
    Auto-selects strategy based on confidence threshold
    """
    
    INTENT_RULES = {
        "search": {
            "keywords": ["tìm", "search", "kiếm", "tra cứu", "google", "lookup", "find"],
            "tools": ["vector_search", "web_search", "query_knowledge_graph"],
            "priority": 1,
        },
        "calculate": {
            "keywords": ["tính", "calculate", "math", "bao nhiêu", "phần trăm", "sum", "average"],
            "tools": ["calculator", "execute_python", "data_analysis"],
            "priority": 2,
        },
        "code": {
            "keywords": ["code", "viết code", "program", "function", "script", "implement", "refactor"],
            "tools": ["execute_python", "write_file", "search_code"],
            "priority": 1,
        },
        "read": {
            "keywords": ["đọc", "read", "xem", "open", "file", "show", "display", "cat"],
            "tools": ["read_file", "git_status"],
            "priority": 2,
        },
        "write": {
            "keywords": ["ghi", "write", "lưu", "save", "tạo file", "create", "update"],
            "tools": ["write_file", "store_memory"],
            "priority": 2,
        },
        "remember": {
            "keywords": ["nhớ", "remember", "lưu ý", "ghi nhớ", "don't forget"],
            "tools": ["store_memory"],
            "priority": 3,
        },
        "recall": {
            "keywords": ["nhắc lại", "recall", "trước đó", "đã nói", "history", "previous"],
            "tools": ["recall_memory"],
            "priority": 3,
        },
        "knowledge": {
            "keywords": ["biết gì", "knowledge", "facts", "thông tin về", "define", "what is"],
            "tools": ["query_knowledge_graph", "vector_search", "lookup_definition"],
            "priority": 2,
        },
        "test": {
            "keywords": ["test", "chạy test", "verify", "validate", "check"],
            "tools": ["run_tests"],
            "priority": 2,
        },
        "git": {
            "keywords": ["git", "commit", "branch", "diff", "merge", "push", "pull"],
            "tools": ["git_status", "git_diff"],
            "priority": 2,
        },
    }
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
        self.classification_history = []
    
    def classify_rule_based(self, query: str) -> Dict:
        """Fast rule-based classification"""
        query_lower = query.lower()
        scores = {}
        
        for intent, config in self.INTENT_RULES.items():
            score = sum(1 for kw in config["keywords"] if kw in query_lower)
            # Boost by priority
            if score > 0:
                score = score * (4 - config.get("priority", 2))
                scores[intent] = score
        
        if not scores:
            return {"intent": "chat", "tools": [], "confidence": 0.5, "method": "rule"}
        
        best_intent = max(scores, key=scores.get)
        confidence = min(scores[best_intent] / 5, 1.0)
        
        return {
            "intent": best_intent,
            "tools": self.INTENT_RULES[best_intent]["tools"],
            "confidence": confidence,
            "method": "rule",
            "all_scores": scores,
        }
    
    def classify_llm_based(self, query: str) -> Dict:
        """LLM-based classification (more accurate, more expensive)"""
        intents_desc = "\n".join([
            f"- {intent}: keywords={config['keywords'][:3]}..., tools={config['tools']}"
            for intent, config in self.INTENT_RULES.items()
        ])
        
        prompt = f"""Phân tích ý định của user và chọn tool phù hợp nhất.

User query: "{query}"

Các intent có thể:
{intents_desc}

Output JSON:
{{
  "intent": "...",
  "tools": ["tool1", "tool2"],
  "confidence": 0.0-1.0,
  "reasoning": "Tại sao chọn intent này",
  "parameters_hint": {{"param": "suggested value"}}
}}"""
        
        response = self.llm(prompt)
        try:
            result = json.loads(response)
            result["method"] = "llm"
            return result
        except json.JSONDecodeError:
            return self.classify_rule_based(query)  # Fallback
    
    def classify(self, query: str, strategy: str = "auto") -> Dict:
        """
        Classify with auto-strategy selection
        
        Strategies:
        - "auto": Rule first, LLM if confidence < threshold
        - "rule": Rule-based only
        - "llm": LLM-based only
        - "ensemble": Combine both
        """
        
        if strategy == "rule" or strategy == "auto":
            rule_result = self.classify_rule_based(query)
            
            if strategy == "rule":
                return rule_result
            
            # Auto: use LLM if rule confidence is low
            if rule_result["confidence"] >= 0.7:
                return rule_result
            
            if self.llm:
                llm_result = self.classify_llm_based(query)
                
                # Take the higher confidence result
                if llm_result.get("confidence", 0) > rule_result["confidence"]:
                    return llm_result
            
            return rule_result
        
        elif strategy == "llm":
            if self.llm:
                return self.classify_llm_based(query)
            return self.classify_rule_based(query)
        
        elif strategy == "ensemble":
            rule_result = self.classify_rule_based(query)
            llm_result = None
            
            if self.llm:
                llm_result = self.classify_llm_based(query)
            
            if llm_result and rule_result["intent"] == llm_result.get("intent"):
                # Agreement → high confidence
                return {
                    "intent": rule_result["intent"],
                    "tools": rule_result["tools"],
                    "confidence": 0.95,
                    "method": "ensemble",
                }
            elif llm_result:
                # Disagreement → use LLM
                llm_result["method"] = "ensemble_override"
                return llm_result
            
            return rule_result
        
        return self.classify_rule_based(query)
    
    def classify_multi_intent(self, query: str) -> List[Dict]:
        """
        Detect multiple intents in a single query
        E.g., "Tìm file README và chạy test" → [read, test]
        """
        # Split by conjunction words
        import re
        parts = re.split(r'\s+(và|and|;|rồi|then|after that)\s+', query)
        
        intents = []
        for part in parts:
            part = part.strip()
            if part.lower() in ['và', 'and', ';', 'rồi', 'then', 'after that']:
                continue
            if len(part) > 3:  # Skip very short parts
                intent = self.classify(part)
                intents.append(intent)
        
        return intents if intents else [self.classify(query)]
```

</details>

---

## 3. MCP Protocol

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** MCP Protocol (Model Context Protocol) là "ngôn ngữ chung" dựa trên JSON-RPC 2.0 để bất kỳ LLM nào cũng bắt chuyện được với tool bên ngoài: muốn biết có gì thì hỏi (tools/list), muốn xài thì gọi (tools/call), kèm theo resources và prompts — một chuẩn xài chung cho mọi nhà.
>
> **Hình dung vui:** Như cổng sạc USB-C: ngày xưa mỗi hãng một kiểu cáp riêng, giờ một chuẩn cắm được hết. MCP là "chuẩn cắm chung" để AI gắn tool của bất kỳ ai mà khỏi viết code riêng cho từng loại.
>
> **Sao phải quan tâm:** Không có chuẩn chung thì cứ mỗi cặp LLM-tool lại phải viết một cầu nối riêng; có chuẩn rồi thì hệ sinh thái tool lớn nhanh gấp bội.

### 3.1 MCP Architecture Deep Dive

Đọc sơ đồ này ra sao? Có ba tầng rõ ràng. Tầng trên là HOST (nơi LLM chạy: Claude Desktop, app GPT, agent nhà trồng...); tầng dưới là các SERVERS (GitHub, Database, File, Web Search, Slack...) chuyên cung cấp tool. Ở giữa là đường dây JSON-RPC qua stdio/SSE/HTTP — như một tổng đài điện thoại chuẩn. Luồng chạy rất đời thường: LLM hỏi server "bên bạn có món gì hay" (tools/list), rồi gọi đúng món mình cần (tools/call). Dải cuối sơ đồ liệt kê hết các tính năng: thống nhất khả năng hỗ trợ (capabilities negotiation), đọc resource, dùng prompt mẫu, sampling và ghi log.

*Hình dung vui:* Như tổng đài điều xe: hãng xe (host) gọi theo đúng quy chuẩn tổng đài (protocol) tới các bác tài (servers), ai rảnh thì nhận cuốc — khỏi cần quen riêng từng bác tài.

```
┌──────────────────────────────────────────────────────────────────┐
│                  MCP (MODEL CONTEXT PROTOCOL)                     │
│                                                                  │
│  MCP là giao thức chuẩn để LLM giao tiếp với tools bên ngoài  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    HOST (Client)                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │   │
│  │  │ Claude   │  │ GPT-4    │  │ Custom   │              │   │
│  │  │ Desktop  │  │ App      │  │ Agent    │              │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘              │   │
│  │       └──────────────┼──────────────┘                    │   │
│  │                      ▼                                    │   │
│  │              MCP Client SDK                              │   │
│  └──────────────────────┬───────────────────────────────────┘   │
│                         │ JSON-RPC 2.0                           │
│                         │ (stdio/SSE/HTTP)                       │
│  ┌──────────────────────┴───────────────────────────────────┐   │
│  │                    SERVERS                                │   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │  GitHub     │  │  Database   │  │  File       │     │   │
│  │  │  Server     │  │  Server     │  │  Server     │     │   │
│  │  │  ─────────  │  │  ─────────  │  │  ─────────  │     │   │
│  │  │  - search   │  │  - query    │  │  - read     │     │   │
│  │  │  - create   │  │  - insert   │  │  - write    │     │   │
│  │  │  - update   │  │  - update   │  │  - delete   │     │   │
│  │  │  - delete   │  │  - schema   │  │  - list     │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │  Web Search │  │  Slack      │  │  Custom     │     │   │
│  │  │  Server     │  │  Server     │  │  API Server │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Protocol Features:                                              │
│  ├── Capabilities negotiation                                   │
│  ├── Tool discovery (tools/list)                                │
│  ├── Tool execution (tools/call)                                │
│  ├── Resource access (resources/read)                           │
│  ├── Prompt templates (prompts/list, prompts/get)              │
│  ├── Sampling (sampling/createMessage)                          │
│  └── Logging (logging/setLevel)                                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 3.2 MCP Client Implementation

Mục này tặng bạn một client MCP đầy đủ để mang về xài ngay: `connect()` bắt tay với server và thống nhất khả năng hỗ trợ, `list_tools()` lấy danh sách tool về cache, `call_tool()` gọi tool có timeout và xử lý lỗi đàng hoàng, `read_resource()` đọc resource. Hàm `format_tools_for_llm()` biến tool MCP thành đúng "khẩu vị" từng nhà (OpenAI kiểu `type: function`, Anthropic kiểu khác). Lớp `MultiServerMCPManager` ở cuối lo quản nhiều server cùng lúc: gom tool về một mối, server này sập thì tự chuyển sang server khác. Nhớ bốn chữ để sống sót trong production: cache, timeout, định tuyến và dự phòng (fallback).

*Hình dung vui:* Như cô tổng đài viên dày dạn: thuộc lòng số máy nào giải quyết được việc gì; số này bận thì bấm ngay sang số dự phòng (failover).

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
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
```

</details>

---

## 4. Tool Executor

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Tool Executor là "người trực bếp" chuyên bấm nút chạy tool cho an toàn: kiểm tra tham số, soát quyền và giới hạn lượt gọi, chạy có hẹn giờ (timeout), hỏng thì thử lại theo kiểu backoff, và ghi log từng lần gọi — nằm giữa khâu chọn tool và kết quả trả về.
>
> **Hình dung vui:** Như anh bồi bàn kỹ tính: trước khi đưa order xuống bếp phải ngó lại — món này quán có bán không (tool tồn tại), còn nguyên liệu không (parameters), bếp có nhận không (permission, rate limit) — rồi mới đưa phiếu và đứng canh tới khi món ra lò (timeout, retry).
>
> **Sao phải quan tâm:** Đa số pha "toang" của agent đều từ tool gọi hỏng; executor là chỗ gom hết mớ rắc rối đó về một mối để xử lý gọn, dễ soi, không làm sập cả bữa ăn.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import time
from typing import Any, Dict, Optional, Callable
from datetime import datetime

class ToolExecutor:
    """
    Execute tools with comprehensive error handling:
    - Parameter validation
    - Retry with exponential backoff
    - Timeout handling
    - Rate limiting
    - Permission checking
    - Cost tracking
    - Execution logging
    """
    
    def __init__(self, registry: ToolRegistry, 
                 permission_checker=None,
                 rate_limiter=None):
        self.registry = registry
        self.permission_checker = permission_checker
        self.rate_limiter = rate_limiter
        self.execution_log: List[Dict] = []
        self._call_counts: Dict[str, int] = {}
    
    def execute(self, tool_name: str, parameters: Dict, 
                user_id: str = None,
                timeout: float = None) -> Dict:
        """
        Execute a tool with full guardrails
        """
        start_time = time.time()
        
        # 1. Resolve tool
        tool = self.registry.get_tool(tool_name)
        if not tool:
            return self._error_result(tool_name, "Tool not found", start_time)
        
        # 2. Check deprecation
        if tool.is_deprecated():
            replacement = tool.replacement_tool or "unknown"
            return self._error_result(
                tool_name, 
                f"Tool deprecated. Use '{replacement}' instead.",
                start_time,
            )
        
        # 3. Validate parameters
        validation = self._validate_params(tool, parameters)
        if not validation["valid"]:
            return self._error_result(
                tool_name,
                f"Invalid parameters: {validation['errors']}",
                start_time,
            )
        
        # 4. Check permissions
        if self.permission_checker and user_id:
            perm_check = self.permission_checker(user_id, tool.requires_permission)
            if not perm_check.get("allowed"):
                return self._error_result(
                    tool_name,
                    f"Permission denied: {perm_check.get('reason', 'insufficient permissions')}",
                    start_time,
                )
        
        # 5. Check rate limit
        if self.rate_limiter:
            rate_check = self.rate_limiter(tool_name)
            if not rate_check.get("allowed"):
                return self._error_result(
                    tool_name,
                    f"Rate limit exceeded: {rate_check.get('retry_after', 60)}s",
                    start_time,
                )
        
        # 6. Execute with retries
        max_retries = tool.max_retries
        effective_timeout = timeout or tool.timeout_seconds
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Set timeout per-attempt
                if tool.function:
                    result = tool.function(**parameters)
                else:
                    result = f"Tool '{tool_name}' has no function implementation"
                
                elapsed_ms = (time.time() - start_time) * 1000
                
                # Update metrics
                tool.update_metrics(elapsed_ms, success=True)
                
                # Log success
                log_entry = {
                    "tool": tool_name,
                    "params": parameters,
                    "success": True,
                    "attempt": attempt + 1,
                    "elapsed_ms": round(elapsed_ms, 2),
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat(),
                }
                self.execution_log.append(log_entry)
                self._call_counts[tool_name] = self._call_counts.get(tool_name, 0) + 1
                
                return {
                    "success": True,
                    "result": result,
                    "attempts": attempt + 1,
                    "elapsed_ms": elapsed_ms,
                    "tool": tool_name,
                    "cost": tool.cost_per_call,
                }
                
            except TimeoutError:
                last_error = f"Timeout after {effective_timeout}s"
            except Exception as e:
                last_error = str(e)
            
            # Exponential backoff before retry
            if attempt < max_retries - 1:
                backoff = 0.5 * (2 ** attempt)
                time.sleep(min(backoff, 5.0))
        
        # All retries failed
        tool.update_metrics(
            (time.time() - start_time) * 1000, 
            success=False,
        )
        
        return self._error_result(
            tool_name,
            f"Failed after {max_retries} attempts: {last_error}",
            start_time,
        )
    
    def execute_batch(self, calls: List[Dict], parallel: bool = False) -> List[Dict]:
        """
        Execute multiple tool calls
        
        calls: [{"tool": "name", "params": {...}, "user_id": "..."}]
        parallel: If True, execute without waiting (simulated)
        """
        results = []
        
        for call in calls:
            result = self.execute(
                call["tool"],
                call.get("params", {}),
                user_id=call.get("user_id"),
            )
            results.append({
                "tool": call["tool"],
                **result,
            })
        
        return results
    
    def execute_chain(self, steps: List[Dict]) -> Dict:
        """
        Execute tools in chain, passing results as inputs
        
        steps: [
            {"tool": "search", "params": {"query": "..."}, "output_key": "search_result"},
            {"tool": "analyze", "params": {"data": "$search_result"}, "output_key": "analysis"},
        ]
        """
        results = {}
        
        for i, step in enumerate(steps):
            # Substitute variables
            params = {}
            for key, value in step.get("params", {}).items():
                if isinstance(value, str) and value.startswith("$"):
                    var_name = value[1:]
                    params[key] = results.get(var_name, value)
                else:
                    params[key] = value
            
            result = self.execute(step["tool"], params)
            
            if not result["success"]:
                return {
                    "success": False,
                    "error": f"Chain failed at step {i+1}: {result.get('error')}",
                    "completed_steps": i,
                    "results": results,
                }
            
            # Store result with output key
            output_key = step.get("output_key", f"step_{i+1}")
            results[output_key] = result["result"]
        
        return {
            "success": True,
            "results": results,
            "steps_completed": len(steps),
        }
    
    def _validate_params(self, tool: ToolDefinition, params: Dict) -> Dict:
        """Validate parameters against tool definition"""
        errors = []
        warnings = []
        
        # Check required params
        for param_name, param_def in tool.parameters.items():
            if param_def.get("required", False) and param_name not in params:
                errors.append(f"Missing required param: {param_name}")
        
        # Check types (basic)
        for param_name, value in params.items():
            if param_name in tool.parameters:
                expected_type = tool.parameters[param_name].get("type")
                if expected_type == "string" and not isinstance(value, str):
                    warnings.append(f"Param '{param_name}' expected string, got {type(value).__name__}")
                elif expected_type == "integer" and not isinstance(value, int):
                    warnings.append(f"Param '{param_name}' expected integer, got {type(value).__name__}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }
    
    def _error_result(self, tool_name: str, error: str, start_time: float) -> Dict:
        """Create error result and log it"""
        elapsed_ms = (time.time() - start_time) * 1000
        
        self.execution_log.append({
            "tool": tool_name,
            "success": False,
            "error": error,
            "elapsed_ms": round(elapsed_ms, 2),
            "timestamp": datetime.now().isoformat(),
        })
        
        return {
            "success": False,
            "error": error,
            "result": None,
            "elapsed_ms": elapsed_ms,
            "tool": tool_name,
        }
    
    def get_stats(self) -> Dict:
        """Get comprehensive execution statistics"""
        total = len(self.execution_log)
        successful = sum(1 for log in self.execution_log if log["success"])
        failed = total - successful
        
        tool_counts = {}
        tool_errors = {}
        total_cost = 0.0
        
        for log in self.execution_log:
            tool = log.get("tool", "unknown")
            tool_counts[tool] = tool_counts.get(tool, 0) + 1
            
            if not log["success"]:
                tool_errors[tool] = tool_errors.get(tool, 0) + 1
        
        # Calculate total cost
        for tool_name, count in self._call_counts.items():
            tool = self.registry.get_tool(tool_name)
            if tool:
                total_cost += tool.cost_per_call * count
        
        return {
            "total_calls": total,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total if total > 0 else 0,
            "tool_usage": tool_counts,
            "tool_errors": tool_errors,
            "total_cost": total_cost,
            "avg_latency_ms": (
                sum(log.get("elapsed_ms", 0) for log in self.execution_log) / total
                if total > 0 else 0
            ),
        }
```

</details>

---

## 5. Function Calling

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Function Calling là cách để LLM không chỉ "nói suông" mà còn biết "ra toa" hẳn hoi theo mẫu có sẵn — ví dụ gọi `calculator` kèm `{"expression": "2+3"}` — lại còn gọi nhiều tool một lượt (parallel calls) cho nhanh, đỡ phải chờ từng cái.
>
> **Hình dung vui:** Như bác sĩ kê toa thay vì kể chuyện: model "viết toa" (tool call kèm JSON) để dược sĩ (executor) bốc đúng thuốc đúng liều, thay vì để bệnh nhân tự về nhà sắc thuốc.
>
> **Sao phải quan tâm:** Đây là tiếng nói chung giữa LLM và code — nền tảng của mọi agent hiện đại, cũng là cách LLM "thò tay" ra thế giới bên ngoài.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class FunctionCallingAgent:
    """
    Agent using OpenAI-style function calling
    
    Supports: Multi-turn tool calls, parallel calls, forced tool use,
    chained tool calls, automatic retry on malformed calls
    """
    
    def __init__(self, llm_func, tool_registry):
        self.llm = llm_func
        self.registry = tool_registry
        self.executor = ToolExecutor(tool_registry)
        self.conversation_history = []
    
    def run(self, user_message: str, max_rounds: int = 10, 
            auto_retry: bool = True) -> Dict:
        """
        Execute agent loop with function calling
        """
        messages = self.conversation_history + [
            {"role": "user", "content": user_message}
        ]
        tools = self.registry.to_openai_format()
        
        total_tool_calls = 0
        tool_usage = {}
        
        for round_num in range(max_rounds):
            # Call LLM
            response = self._call_llm(messages, tools)
            
            # Check for tool calls
            if not response.get("tool_calls"):
                final_answer = response.get("content", "")
                self.conversation_history = messages + [
                    {"role": "assistant", "content": final_answer}
                ]
                return {
                    "answer": final_answer,
                    "rounds": round_num + 1,
                    "total_tool_calls": total_tool_calls,
                    "tool_usage": tool_usage,
                }
            
            # Add assistant message with tool calls
            messages.append({
                "role": "assistant",
                "content": response.get("content"),
                "tool_calls": response["tool_calls"],
            })
            
            # Execute each tool call
            for tc in response["tool_calls"]:
                func_name = tc["function"]["name"]
                total_tool_calls += 1
                tool_usage[func_name] = tool_usage.get(func_name, 0) + 1
                
                try:
                    func_args = json.loads(tc["function"]["arguments"])
                except json.JSONDecodeError as e:
                    if auto_retry:
                        # Ask LLM to fix malformed arguments
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tc["id"],
                            "content": json.dumps({
                                "error": f"Invalid JSON arguments: {e}",
                                "hint": "Please provide valid JSON arguments",
                            }),
                        })
                        continue
                    func_args = {}
                
                # Execute tool
                result = self.executor.execute(func_name, func_args)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": json.dumps(result, ensure_ascii=False, default=str),
                })
        
        return {
            "answer": "Max rounds reached without final answer",
            "rounds": max_rounds,
            "total_tool_calls": total_tool_calls,
            "tool_usage": tool_usage,
        }
    
    def forced_tool_call(self, user_message: str, tool_name: str) -> Dict:
        """
        Force LLM to use a specific tool
        Useful when intent is clear from pre-classification
        """
        tool = self.registry.get_tool(tool_name)
        if not tool:
            return {"error": f"Tool '{tool_name}' not found"}
        
        messages = [{"role": "user", "content": user_message}]
        tools = self.registry.to_openai_format()
        
        # Force specific tool
        response = self._call_llm(
            messages, 
            tools,
            tool_choice={"type": "function", "function": {"name": tool_name}}
        )
        
        if response.get("tool_calls"):
            tc = response["tool_calls"][0]
            try:
                func_args = json.loads(tc["function"]["arguments"])
            except json.JSONDecodeError:
                func_args = {}
            
            result = self.executor.execute(tool_name, func_args)
            
            return {
                "tool": tool_name,
                "args": func_args,
                "result": result,
            }
        
        return {"error": "LLM did not call the forced tool"}
    
    def parallel_tool_calls(self, user_message: str) -> Dict:
        """
        Enable parallel tool calling
        LLM can call multiple tools simultaneously
        """
        messages = [{"role": "user", "content": user_message}]
        tools = self.registry.to_openai_format()
        
        response = self._call_llm(messages, tools)
        
        if response.get("tool_calls"):
            # Execute all in parallel (simulated with batch)
            calls = []
            for tc in response["tool_calls"]:
                try:
                    func_args = json.loads(tc["function"]["arguments"])
                except json.JSONDecodeError:
                    func_args = {}
                calls.append({
                    "tool": tc["function"]["name"],
                    "params": func_args,
                })
            
            results = self.executor.execute_batch(calls)
            
            return {
                "parallel_results": results,
                "tools_called": len(results),
                "all_success": all(r["success"] for r in results),
            }
        
        return {"answer": response.get("content", "")}
    
    def _call_llm(self, messages, tools, tool_choice=None):
        """Call LLM with function calling support"""
        if self.llm:
            kwargs = {"messages": messages, "tools": tools}
            if tool_choice:
                kwargs["tool_choice"] = tool_choice
            return self.llm(**kwargs)
        return {"content": "No LLM configured"}
```

</details>

---

## 6. Tool Decision Pipeline

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Tool Decision Pipeline là đường ống khép kín từ lúc nghe câu hỏi → đoán ý → lựa tool → nắn tham số cho chuẩn → chạy thử → soi lại kết quả, bước nào cũng có người gác cổng và sổ ghi chép.
>
> **Hình dung vui:** Như dây chuyền trong xưởng: đầu vào phân loại nguyên liệu (intent classification), giữa chuyền chọn máy và nạp liệu (tool matching + parameters), cuối chuyền kiểm hàng trước khi đóng thùng (result validation).
>
> **Sao phải quan tâm:** Gom hết chuyện chọn tool vào một ống duy nhất thì muốn gắn thêm chốt an toàn cũng dễ, muốn tìm chỗ hỏng cũng nhanh, muốn mở rộng cũng không sợ bung các chỗ khác.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class ToolDecisionPipeline:
    """
    Complete pipeline: Query → Intent → Tool Selection → Execution → Response
    
    Features:
    - Multi-strategy classification
    - Parameter extraction
    - Guardrails integration
    - Fallback handling
    - Performance tracking
    """
    
    def __init__(self, registry: ToolRegistry, llm_func=None):
        self.registry = registry
        self.classifier = IntentClassifier(llm_func)
        self.executor = ToolExecutor(registry)
        self.llm = llm_func
    
    def process(self, query: str, user_id: str = None, 
                context: Dict = None) -> Dict:
        """Full pipeline"""
        
        # Step 1: Classify intent
        intent = self.classifier.classify(query)
        
        selected_tools = intent.get("tools", [])
        
        if not selected_tools:
            return {
                "tool_used": None,
                "result": "No tool needed — direct response",
                "intent": intent,
                "pipeline_steps": ["classify"],
            }
        
        # Step 2: Try each potential tool
        for tool_name in selected_tools:
            tool = self.registry.get_tool(tool_name)
            if not tool:
                continue
            
            # Step 3: Extract parameters
            params = self._extract_params(query, tool, context)
            
            # Step 4: Execute
            result = self.executor.execute(
                tool_name, params, user_id=user_id
            )
            
            if result["success"]:
                return {
                    "tool_used": tool_name,
                    "result": result["result"],
                    "intent": intent,
                    "params": params,
                    "pipeline_steps": ["classify", "select", "extract", "execute"],
                    "elapsed_ms": result.get("elapsed_ms"),
                }
        
        return {
            "tool_used": None,
            "result": "No tool could process this query",
            "intent": intent,
            "pipeline_steps": ["classify", "select", "execute_failed"],
        }
    
    def process_multi(self, query: str) -> Dict:
        """
        Process query that may require multiple tools
        """
        # Detect multi-intent
        intents = self.classifier.classify_multi_intent(query)
        
        results = []
        for intent in intents:
            for tool_name in intent.get("tools", []):
                tool = self.registry.get_tool(tool_name)
                if not tool:
                    continue
                
                params = self._extract_params(query, tool)
                result = self.executor.execute(tool_name, params)
                
                if result["success"]:
                    results.append({
                        "tool": tool_name,
                        "result": result["result"],
                        "params": params,
                    })
                    break  # Move to next intent
        
        return {
            "tools_used": [r["tool"] for r in results],
            "results": results,
            "total_intents": len(intents),
            "total_success": len(results),
        }
    
    def _extract_params(self, query: str, tool: ToolDefinition, 
                        context: Dict = None) -> Dict:
        """Extract tool parameters from query"""
        if self.llm:
            params_desc = json.dumps(tool.parameters, indent=2, ensure_ascii=False)
            context_text = json.dumps(context, indent=2, ensure_ascii=False) if context else "None"
            
            prompt = f"""Trích xuất parameters cho tool từ query.

Query: "{query}"
Context: {context_text}
Tool: {tool.name}
Description: {tool.description}
Parameters schema: {params_desc}

Output JSON (chỉ parameters, đúng types):"""
            
            response = self.llm(prompt)
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                pass
        
        # Fallback: put query as first string param
        first_param = list(tool.parameters.keys())[0] if tool.parameters else None
        if first_param:
            return {first_param: query}
        return {}
```

</details>

---

## 7. Tool Composition

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Tool Composition là nghệ thuật xâu nhiều tool lại với nhau — nối đuôi (chain), chạy song song (parallel), rẽ nhánh theo điều kiện (conditional) hay tỏa ra rồi gom lại (fan-out/fan-in) — để xử những việc khó mà một tool đơn lẻ làm không xuể.
>
> **Hình dung vui:** Như nấu một mâm cơm: nhiều đồ nghề bếp (thái, luộc, xào) phải chạy đúng thứ tự, có món làm song song (vừa luộc rau vừa nấu canh), có lúc lại rẽ nhánh tùy xem nếm thử mặn nhạt ra sao.
>
> **Sao phải quan tâm:** Việc đời thực hiếm khi xong bằng một tool; biết ghép tool thành quy trình là bước từ "chạy vặt từng món" lên "đứng bếp cả mâm".

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class ToolComposer:
    """
    Compose multiple tools into workflows
    
    Patterns:
    - Chain: A → B → C (sequential)
    - Parallel: A + B + C (simultaneous)
    - Conditional: if A > threshold then B else C
    - Pipeline: A → fan-out → B, C, D → fan-in → E
    """
    
    def __init__(self, executor: ToolExecutor):
        self.executor = executor
    
    def chain(self, steps: List[Dict], shared_context: Dict = None) -> Dict:
        """
        Execute tools in chain
        Each tool's output becomes next tool's input
        """
        context = shared_context or {}
        
        for i, step in enumerate(steps):
            tool_name = step["tool"]
            input_mapping = step.get("input_mapping", {})
            
            # Map inputs from context
            params = {}
            for param_name, source_key in input_mapping.items():
                params[param_name] = context.get(source_key, source_key)
            
            # Merge with static params
            params.update(step.get("params", {}))
            
            result = self.executor.execute(tool_name, params)
            
            if not result["success"]:
                return {
                    "success": False,
                    "error": f"Chain broke at step {i+1} ({tool_name}): {result.get('error')}",
                    "partial_results": context,
                }
            
            # Store result in context
            output_key = step.get("output_key", f"step_{i+1}_result")
            context[output_key] = result["result"]
        
        return {"success": True, "results": context}
    
    def parallel(self, tasks: List[Dict]) -> Dict:
        """
        Execute tools in parallel
        All tools run simultaneously, results collected
        """
        results = self.executor.execute_batch(tasks)
        
        return {
            "success": all(r["success"] for r in results),
            "results": results,
            "total": len(results),
            "succeeded": sum(1 for r in results if r["success"]),
            "failed": sum(1 for r in results if not r["success"]),
        }
    
    def conditional(self, condition_tool: str, condition_params: Dict,
                    condition_check: Callable,
                    true_branch: List[Dict], 
                    false_branch: List[Dict] = None) -> Dict:
        """
        Execute tool conditionally
        
        1. Execute condition_tool
        2. Check result with condition_check function
        3. Execute true_branch or false_branch
        """
        # Execute condition
        condition_result = self.executor.execute(condition_tool, condition_params)
        
        if not condition_result["success"]:
            return {"success": False, "error": "Condition tool failed"}
        
        # Evaluate condition
        branch = true_branch if condition_check(condition_result["result"]) else (false_branch or [])
        
        # Execute branch
        if branch:
            return self.chain(branch, {"condition_result": condition_result["result"]})
        
        return {"success": True, "results": {"condition_result": condition_result["result"]}}
    
    def pipeline(self, stages: List[Dict]) -> Dict:
        """
        Fan-out / Fan-in pipeline
        
        Stage format:
        {
            "name": "stage_name",
            "tools": [{"tool": "name", "params": {...}}],
            "aggregator": "merge" | "first" | "all"
        }
        """
        results = {}
        
        for stage in stages:
            stage_name = stage["name"]
            tools = stage["tools"]
            aggregator = stage.get("aggregator", "merge")
            
            # Fan-out: execute all tools
            stage_results = self.executor.execute_batch(tools)
            
            # Fan-in: aggregate results
            if aggregator == "merge":
                results[stage_name] = [
                    r["result"] for r in stage_results if r["success"]
                ]
            elif aggregator == "first":
                for r in stage_results:
                    if r["success"]:
                        results[stage_name] = r["result"]
                        break
            elif aggregator == "all":
                results[stage_name] = all(r["success"] for r in stage_results)
        
        return {"success": True, "results": results}
```

</details>

---

## 8. Permission System

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Permission System là bộ phận "gác cổng" theo vai vế (RBAC): ai được đụng vào tool nào, theo vai (guest/user/power_user/admin) và theo mức (public/standard/elevated/admin), lần nào cho qua hay chặn lại cũng ghi sổ (audit log).
>
> **Hình dung vui:** Như thẻ ra vào công ty: khách chỉ loanh quanh được ở sảnh, nhân viên vào được văn phòng, còn phòng máy chủ thì chỉ quản lý mới có vân tay — mà mỗi lần quẹt thẻ đều để lại dấu vết.
>
> **Sao phải quan tâm:** Mấy tool như `write_file` hay `execute_python` mà xài bừa là gây chuyện khó cứu; phân quyền là hàng rào chắn mấy pha "táy máy" ngoài ý muốn của agent.

> 🔑 **Điểm cần nhớ về Policy / Permission:** đây là **ngã ba quyết định policy & permission** — vai trò (role) dẫn tới mức quyền → cho qua hay chặn lại + ghi audit. Muốn xem thi hành thật thì ghé `12-sandbox-execution` (§6 ma trận policy), muốn xem người duyệt thì ghé `15-approval-gates`, còn kiểm tra ngay trước giờ chạy thì nằm ở `tools/guardrails`.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class ToolPermissionChecker:
    """
    Role-Based Access Control (RBAC) for tools
    
    Permission levels:
    - public: Anyone can use
    - standard: Authenticated users
    - elevated: Users with elevated privileges
    - admin: System admin only
    """
    
    ROLE_PERMISSIONS = {
        "guest": ["public"],
        "user": ["public", "standard"],
        "power_user": ["public", "standard", "elevated"],
        "admin": ["public", "standard", "elevated", "admin"],
    }
    
    def __init__(self):
        self.user_roles: Dict[str, str] = {}
        self.custom_permissions: Dict[str, List[str]] = {}
        self.audit_log: List[Dict] = []
    
    def set_user_role(self, user_id: str, role: str):
        """Set role for a user"""
        if role not in self.ROLE_PERMISSIONS:
            raise ValueError(f"Invalid role: {role}. Valid: {list(self.ROLE_PERMISSIONS.keys())}")
        self.user_roles[user_id] = role
    
    def grant_permission(self, user_id: str, permission: str):
        """Grant additional permission to user"""
        if user_id not in self.custom_permissions:
            self.custom_permissions[user_id] = []
        if permission not in self.custom_permissions[user_id]:
            self.custom_permissions[user_id].append(permission)
    
    def check(self, user_id: str, required_permission: str) -> Dict:
        """Check if user has required permission"""
        role = self.user_roles.get(user_id, "guest")
        role_perms = self.ROLE_PERMISSIONS.get(role, ["public"])
        custom_perms = self.custom_permissions.get(user_id, [])
        
        all_perms = set(role_perms + custom_perms)
        allowed = required_permission in all_perms
        
        # Log audit trail
        self.audit_log.append({
            "user_id": user_id,
            "required_permission": required_permission,
            "user_role": role,
            "allowed": allowed,
            "timestamp": datetime.now().isoformat(),
        })
        
        if allowed:
            return {"allowed": True}
        else:
            return {
                "allowed": False,
                "reason": f"Role '{role}' does not have '{required_permission}' permission",
                "required": required_permission,
                "current_permissions": list(all_perms),
            }
```

</details>

---

## 9. Rate Limiting

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Rate Limiting là cái "van tiết lưu" giới hạn số lần gọi tool trong một khoảng thời gian (ví dụ tối đa 60 lần/phút), với đủ kiểu van như fixed window, sliding window hay token bucket — để giữ ngân sách token, chặn phá hoại và giữ hệ thống khỏi quá tải.
>
> **Hình dung vui:** Như van giảm áp của bình nước: nước vẫn chảy đều nhưng không bao giờ xối xả — một vòi không thể hút cạn cả bể (abuse) và đường ống cũng khỏi lo bị vỡ (overload).
>
> **Sao phải quan tâm:** Agent mà loop cả trăm lần gọi tool trong một phút thì rate limit chính là phao cứu sinh cho ví tiền và sức khỏe hệ thống.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class RateLimiter:
    """
    Rate limiting for tool calls
    
    Strategies:
    - Fixed window: X calls per minute
    - Sliding window: X calls in last 60 seconds
    - Token bucket: Burst + sustained rate
    """
    
    def __init__(self, strategy: str = "sliding_window"):
        self.strategy = strategy
        self._call_records: Dict[str, List[float]] = {}
        self._burst_limits: Dict[str, int] = {}
        self._token_buckets: Dict[str, Dict] = {}
    
    def set_limit(self, tool_name: str, max_calls: int, window_seconds: int = 60):
        """Set rate limit for a tool"""
        self._burst_limits[tool_name] = max_calls
    
    def check(self, tool_name: str) -> Dict:
        """Check if call is allowed"""
        now = time.time()
        
        if tool_name not in self._call_records:
            self._call_records[tool_name] = []
        
        records = self._call_records[tool_name]
        limit = self._burst_limits.get(tool_name, 60)
        window = 60  # 1 minute
        
        if self.strategy == "sliding_window":
            # Remove old records
            records = [t for t in records if now - t < window]
            self._call_records[tool_name] = records
            
            if len(records) >= limit:
                oldest = records[0]
                retry_after = window - (now - oldest)
                return {
                    "allowed": False,
                    "retry_after": round(retry_after, 1),
                    "current_rate": len(records),
                    "limit": limit,
                }
            
            records.append(now)
            return {
                "allowed": True,
                "current_rate": len(records),
                "limit": limit,
                "remaining": limit - len(records),
            }
        
        return {"allowed": True}
    
    def get_usage(self) -> Dict:
        """Get current usage for all tools"""
        usage = {}
        for tool_name, records in self._call_records.items():
            now = time.time()
            recent = [t for t in records if now - t < 60]
            usage[tool_name] = {
                "calls_last_minute": len(recent),
                "limit": self._burst_limits.get(tool_name, 60),
            }
        return usage
```

</details>

---

## 10. Harness Integration

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Harness Integration là chấu cắm nối module chọn tool với cả nhà Harness — Memory, Guardrails, Feedback, Permissions — qua mấy bản interface TypeScript xài chung.
>
> **Hình dung vui:** Như đầu nối chuẩn của máy hút bụi đa năng: dù là bàn chải, đầu hút hay ống mềm, cứ đúng cỡ là cắm vào chạy được — interface TypeScript chính là cái cỡ chuẩn để các module gắn vào nhau.
>
> **Sao phải quan tâm:** Module hay mấy mà cắm không vừa harness thì cũng để ngắm; có interface chung thì cắm nhanh, test riêng từng món cũng dễ, món này đổi cũng không làm bung món kia.

### 10.1 TypeScript Interfaces

Mục này là tờ "hợp đồng mẫu" bằng TypeScript, ghi rõ một hệ thống chọn tool muốn chơi với harness thì phải có mặt mũi ra sao: đăng ký/lấy/liệt kê/tìm tool, `classifyIntent`, `executeTool`/`executeChain`/`executeParallel`, thêm `checkPermission`/`checkRateLimit` và `getStats`. Đọc thì cứ xem `interface` là điều khoản bắt buộc, còn class `HarnessToolDecisionSystem` là một bản làm mẫu cho thấy một lần gọi tool ngoài đời chạy qua các cửa nào: soát quyền → soát lượt gọi → bấm chạy → ghi sổ đo đạc. Sau này bạn viết module riêng, chỉ cần đúng hợp đồng là harness nhận ngay.

*Hình dung vui:* Như hợp đồng thuê văn phòng: interface là điều khoản chung ai cũng phải theo, class là cách từng bên tự trang trí văn phòng của mình.

<details>
<summary><b>10.1 TypeScript Interfaces (Click to expand/collapse)</b></summary>

```typescript
// Tool Decision System — Full Harness Integration
interface ToolDecisionSystem {
  // Tool management
  registerTool: (tool: ToolDefinition) => void;
  getTool: (name: string) => ToolDefinition | null;
  listTools: (category?: string) => ToolDefinition[];
  searchTools: (query: string) => ToolDefinition[];
  
  // Classification
  classifyIntent: (query: string) => IntentResult;
  
  // Execution
  executeTool: (name: string, params: Record<string, any>, userId?: string) => ToolResult;
  executeChain: (steps: ToolChainStep[]) => ChainResult;
  executeParallel: (calls: ToolCall[]) => ParallelResult;
  
  // Guardrails
  checkPermission: (userId: string, permission: string) => boolean;
  checkRateLimit: (toolName: string) => boolean;
  
  // Metrics
  getStats: () => ToolStats;
}

interface ToolDefinition {
  name: string;
  description: string;
  parameters: Record<string, ParameterDef>;
  category: string;
  version: string;
  requiresAuth: boolean;
  requiresPermission: string;
  rateLimitPerMinute: number;
  timeoutSeconds: number;
  maxRetries: number;
  costPerCall: number;
}

interface ToolResult {
  success: boolean;
  result?: any;
  error?: string;
  attempts: number;
  elapsedMs: number;
  cost: number;
}

interface IntentResult {
  intent: string;
  tools: string[];
  confidence: number;
  method: string;
}

// Complete Harness Tool Decision System
class HarnessToolDecisionSystem implements ToolDecisionSystem {
  private registry: ToolRegistry;
  private classifier: IntentClassifier;
  private executor: ToolExecutor;
  private permissionChecker: ToolPermissionChecker;
  private rateLimiter: RateLimiter;
  private metricsCollector: MetricsCollector;
  
  constructor(config: HarnessConfig) {
    this.registry = new ToolRegistry();
    this.classifier = new IntentClassifier(config.llm);
    this.executor = new ToolExecutor(this.registry);
    this.permissionChecker = new ToolPermissionChecker();
    this.rateLimiter = new RateLimiter();
    this.metricsCollector = config.metrics;
  }
  
  async executeTool(name: string, params: Record<string, any>, userId?: string): Promise<ToolResult> {
    // 1. Check permission
    const tool = this.registry.getTool(name);
    if (tool && userId) {
      const permCheck = this.permissionChecker.check(userId, tool.requiresPermission);
      if (!permCheck.allowed) {
        return { success: false, error: permCheck.reason, attempts: 0, elapsedMs: 0, cost: 0 };
      }
    }
    
    // 2. Check rate limit
    const rateCheck = this.rateLimiter.check(name);
    if (!rateCheck.allowed) {
      return { success: false, error: `Rate limited. Retry after ${rateCheck.retryAfter}s`, attempts: 0, elapsedMs: 0, cost: 0 };
    }
    
    // 3. Execute with tracking
    const result = this.executor.execute(name, params, userId);
    
    // 4. Report metrics
    this.metricsCollector.track('tool_executed', {
      tool: name,
      success: result.success,
      latency_ms: result.elapsed_ms,
    });
    
    return result;
  }
  
  // ... other interface implementations
}
```

</details>

---

## 11. Case Studies

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Case Studies là mấy câu chuyện người thật việc thật: mổ xẻ xem các sản phẩm AI xịn (SWE-agent, Claude Code, Cursor IDE, DeepSeek Harness) đang xài tool ra sao, để mình học lỏm chiêu hay về áp dụng.
>
> **Hình dung vui:** Như đọc chuyện nghề của đầu bếp nổi tiếng: không phải để bê nguyên công thức về, mà để ngấm cái nguyên tắc (thứ tự, an toàn, hợp ngữ cảnh) rồi tự nêm nếm cho vừa bếp nhà mình.
>
> **Sao phải quan tâm:** Mấy sản phẩm này đã trả học phí bằng tiền thật và người dùng thật để tối ưu; học họ thì mình khỏi phải phát minh lại cái bánh xe méo.

### 11.1. SWE-agent — Tool-Use for Software Engineering

**Chiêu dùng tool**: ít mà chất, tool nào cũng mô tả rõ ràng dễ hiểu.

```
Tools: read_file, search_code, edit_file, run_command

Key insight: "Read before edit" — SWE-agent always reads files first
to understand context before making changes.
```

**Kết quả**: tỉ lệ thành công 20.5% trên SWE-bench (+64% so với cách làm cũ)

### 11.2. Claude Code — Hierarchical Tool Access

**Chiêu dùng tool**: phân quyền theo tầng, tool ghép được với nhau.

```
Layer 1 (always available): read_file, search_code
Layer 2 (standard): write_file, run_tests
Layer 3 (elevated): execute_command, delete_file
Layer 4 (admin): push_code, deploy
```

### 11.3. Cursor IDE — Context-Aware Tool Selection

**Chiêu dùng tool**: nhìn ngữ cảnh trong editor mà chọn tool (đang mở file gì, đang bôi đen đoạn nào...).

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
// Cursor dynamically selects tools based on:
// 1. Current file type
// 2. Selected code
// 3. Editor mode (insert vs replace)
// 4. Git status

const toolsForContext = {
  python: ["execute_python", "lint", "format"],
  typescript: ["run_tests", "type_check", "lint"],
  markdown: ["spell_check", "format"],
};
```

</details>

---

### 11.4. DeepSeek Harness — Code Mode SDK (`@deepseek-ai/dsh`)

**Bối cảnh**: DeepSeek Harness có một chế độ chạy gọi là **Code Mode** — sinh ra để xử nhanh gọn mấy task code chỉ cần chạy một lượt. Bạn dùng SDK `@deepseek-ai/dsh` để chạy code trong sandbox `vm` của Node.js, gom nhiều thao tác tool thành từng mẻ (batch) nên **nhẹ hơn hẳn 70-90% cả thời gian chờ lẫn tiền token** so với kiểu agent hỏi-đáp nhiều vòng.

<details>
<summary><b>TypeScript Architecture (Click to expand/collapse)</b></summary>

```typescript
/**
 * DeepSeek Harness - Code Mode SDK
 * 
 * Core philosophy: "Batch everything, execute once"
 * Single-turn script execution instead of multi-turn agent loop.
 * 
 * Package: @deepseek-ai/dsh
 * Runtime: Node.js vm sandbox (isolated, no network)
 */

// ═══════════════════════════════════════════════
// 1. CODE MODE SDK INTERFACE
// ═══════════════════════════════════════════════

interface CodeModeConfig {
  /** Maximum execution time in milliseconds */
  timeoutMs: number;
  
  /** Allow network access (default: false for isolation) */
  allowNetwork: boolean;
  
  /** Allowed built-in modules */
  allowedModules: string[];
  
  /** Custom globals injected into sandbox */
  globals: Record<string, any>;
  
  /** Tool batching configuration */
  batching: {
    /** Batch multiple tool calls into single execution */
    enabled: boolean;
    /** Max tools per batch */
    maxBatchSize: number;
    /** Max wait time for batching (ms) */
    maxWaitMs: number;
  };
  
  /** Memory limit (MB) */
  memoryLimitMb: number;
}

interface ToolBatch {
  calls: ToolCall[];
  sessionId: string;
  timestamp: number;
}

interface ToolCall {
  id: string;
  name: string;
  args: Record<string, any>;
  /** For batched execution: resolve all at once */
  resolve: (result: any) => void;
  reject: (error: Error) => void;
}

// ═══════════════════════════════════════════════
// 2. SANDBOX EXECUTOR (vm-based isolation)
// ═══════════════════════════════════════════════

class CodeModeSandbox {
  private vm: import('vm').Context;
  private config: CodeModeConfig;
  private toolRegistry: Map<string, ToolFunction>;
  private batchQueue: ToolCall[] = [];
  private batchTimer: NodeJS.Timeout | null = null;
  
  constructor(config: Partial<CodeModeConfig> = {}) {
    this.config = {
      timeoutMs: 30000,
      allowNetwork: false,
      allowedModules: ['fs', 'path', 'crypto', 'util'],
      globals: {},
      batching: { enabled: true, maxBatchSize: 10, maxWaitMs: 50 },
      memoryLimitMb: 128,
      ...config
    };
    
    this.toolRegistry = new Map();
    this.setupSandbox();
  }
  
  private setupSandbox(): void {
    // Create isolated vm context
    const sandboxGlobals = {
      console: this.createSafeConsole(),
      setTimeout,
      clearTimeout,
      setInterval,
      clearInterval,
      ...this.config.globals
    };
    
    // Add allowed modules
    for (const mod of this.config.allowedModules) {
      try {
        sandboxGlobals[mod] = require(mod);
      } catch {
        // Module not available
      }
    }
    
    // Inject tool caller
    sandboxGlobals.callTool = this.createToolCaller();
    sandboxGlobals.batchTools = this.createBatchCaller();
    
    this.vm = import('vm').createContext(sandboxGlobals);
  }
  
  private createSafeConsole() {
    return {
      log: (...args: any[]) => { /* captured */ },
      error: (...args: any[]) => { /* captured */ },
      warn: (...args: any[]) => { /* captured */ },
    };
  }
  
  private createToolCaller() {
    return async (name: string, args: Record<string, any>) => {
      const tool = this.toolRegistry.get(name);
      if (!tool) throw new Error(`Tool not found: ${name}`);
      return await tool(args);
    };
  }
  
  private createBatchCaller() {
    return (calls: Array<{name: string, args: Record<string, any>}>) => {
      return this.executeBatch(calls);
    };
  }
  
  registerTool(name: string, fn: ToolFunction): void {
    this.toolRegistry.set(name, fn);
  }
  
  // ═══════════════════════════════════════════════
  // 3. BATCHED EXECUTION (Core optimization)
  // ═══════════════════════════════════════════════
  
  async executeScript(script: string): Promise<ExecutionResult> {
    const startTime = Date.now();
    const scriptId = `script_${startTime}_${Math.random().toString(36).slice(2)}`;
    
    // Wrap script with error handling and result capture
    const wrappedScript = `
      (async () => {
        try {
          const result = await (async () => {
            ${script}
          })();
          return { success: true, result, scriptId: "${scriptId}" };
        } catch (error) {
          return { success: false, error: error.message, stack: error.stack, scriptId: "${scriptId}" };
        }
      })()
    `;
    
    try {
      const result = await import('vm').runInContext(wrappedScript, this.vm, {
        timeout: this.config.timeoutMs,
        displayErrors: true
      });
      
      // Flush any pending batch
      await this.flushBatch();
      
      return {
        success: result.success,
        result: result.success ? result.result : undefined,
        error: result.success ? undefined : result.error,
        durationMs: Date.now() - startTime,
        scriptId
      };
      
    } catch (error: any) {
      return {
        success: false,
        error: error.message,
        durationMs: Date.now() - startTime,
        scriptId
      };
    }
  }
  
  private async executeBatch(calls: Array<{name: string, args: any}>): Promise<any[]> {
    if (!this.config.batching.enabled) {
      // Sequential fallback
      return Promise.all(calls.map(c => this.callTool(c.name, c.args)));
    }
    
    // Queue for batching
    const promises = calls.map(call => new Promise((resolve, reject) => {
      this.batchQueue.push({
        id: uuid(),
        name: call.name,
        args: call.args,
        resolve,
        reject
      });
    }));
    
    // Schedule flush
    if (this.batchTimer) clearTimeout(this.batchTimer);
    this.batchTimer = setTimeout(() => this.flushBatch(), this.config.batching.maxWaitMs);
    
    // Flush immediately if batch full
    if (this.batchQueue.length >= this.config.batching.maxBatchSize) {
      await this.flushBatch();
    }
    
    return Promise.all(promises);
  }
  
  private async flushBatch(): Promise<void> {
    if (this.batchQueue.length === 0) return;
    
    const batch = this.batchQueue.splice(0, this.config.batching.maxBatchSize);
    if (this.batchTimer) {
      clearTimeout(this.batchTimer);
      this.batchTimer = null;
    }
    
    // Execute all tools in parallel
    const results = await Promise.allSettled(
      batch.map(async call => {
        const tool = this.toolRegistry.get(call.name);
        if (!tool) throw new Error(`Tool not found: ${call.name}`);
        return await tool(call.args);
      })
    );
    
    // Resolve/reject promises
    for (let i = 0; i < batch.length; i++) {
      const call = batch[i];
      const result = results[i];
      if (result.status === 'fulfilled') {
        call.resolve(result.value);
      } else {
        call.reject(result.reason);
      }
    }
  }
  
  async callTool(name: string, args: Record<string, any>): Promise<any> {
    const tool = this.toolRegistry.get(name);
    if (!tool) throw new Error(`Tool not found: ${name}`);
    return await tool(args);
  }
}

// ═══════════════════════════════════════════════
// 4. HIGH-LEVEL SDK API (@deepseek-ai/dsh)
// ═══════════════════════════════════════════════

class DeepSeekHarnessSDK {
  private sandbox: CodeModeSandbox;
  private sessionId: string;
  
  constructor(config?: Partial<CodeModeConfig>) {
    this.sandbox = new CodeModeSandbox(config);
    this.sessionId = `session_${Date.now()}_${Math.random().toString(36).slice(2)}`;
    this.registerDefaultTools();
  }
  
  private registerDefaultTools(): void {
    // File operations
    this.sandbox.registerTool('read_file', async ({path, encoding = 'utf-8'}) => {
      return await fs.promises.readFile(path, encoding);
    });
    
    this.sandbox.registerTool('write_file', async ({path, content, mode = 'overwrite'}) => {
      if (mode === 'append') {
        await fs.promises.appendFile(path, content);
      } else {
        await fs.promises.writeFile(path, content);
      }
      return { success: true, path };
    });
    
    this.sandbox.registerTool('list_files', async ({path = '.', recursive = false}) => {
      const files = await glob('**/*', { cwd: path, nodir: !recursive });
      return files;
    });
    
    // Code execution
    this.sandbox.registerTool('execute_command', async ({command, cwd, timeout = 30000}) => {
      const { execFile } = require('child_process');
      return new Promise((resolve, reject) => {
        const proc = execFile(command, { cwd, timeout }, (err, stdout, stderr) => {
          if (err) reject(err);
          else resolve({ stdout, stderr, code: 0 });
        });
      });
    });
    
    // Search
    this.sandbox.registerTool('search_code', async ({query, path = '.', filePattern}) => {
      // Use ripgrep or similar
      const results = await ripgrep(query, { path, filePattern });
      return results;
    });
    
    // LLM call (for code generation within script)
    this.sandbox.registerTool('llm_complete', async ({prompt, model = 'deepseek-coder'}) => {
      const response = await callLLM(prompt, model);
      return response;
    });
  }
  
  /**
   * Main entry point: Execute a coding task in single turn
   * 
   * Example:
   * ```typescript
   * const sdk = new DeepSeekHarnessSDK();
   * const result = await sdk.execute(`
   *   const files = await list_files({path: './src'});
   *   const content = await read_file({path: files[0]});
   *   const fixed = await llm_complete({prompt: \`Fix bugs in: \${content}\`});
   *   await write_file({path: files[0], content: fixed});
   * `);
   * ```
   */
  async execute(script: string): Promise<ExecutionResult> {
    return await this.sandbox.executeScript(script);
  }
  
  /**
   * Execute with pre-defined tools (for structured tasks)
   */
  async executeWithTools(
    script: string, 
    tools: Record<string, ToolFunction>
  ): Promise<ExecutionResult> {
    for (const [name, fn] of Object.entries(tools)) {
      this.sandbox.registerTool(name, fn);
    }
    return await this.execute(script);
  }
  
  /**
   * Get session metrics
   */
  getMetrics(): SessionMetrics {
    return {
      sessionId: this.sessionId,
      toolsRegistered: this.sandbox.toolRegistry.size,
      // ... more metrics
    };
  }
}

// ═══════════════════════════════════════════════
// 5. USAGE EXAMPLES
// ═══════════════════════════════════════════════

/**
 * Example 1: Refactor a TypeScript file
 */
async function exampleRefactor() {
  const sdk = new DeepSeekHarnessSDK({
    timeoutMs: 60000,
    allowedModules: ['fs', 'path', 'typescript'],
    batching: { enabled: true, maxBatchSize: 20, maxWaitMs: 100 }
  });
  
  const result = await sdk.execute(`
    // 1. Find all TS files
    const files = await list_files({path: './src', recursive: true});
    const tsFiles = files.filter(f => f.endsWith('.ts'));
    
    // 2. Read all files in parallel (BATCHED!)
    const contents = await batchTools(
      tsFiles.map(f => ({name: 'read_file', args: {path: f}}))
    );
    
    // 3. Analyze with LLM (single call)
    const analysis = await llm_complete({
      prompt: \`Analyze these files for code smells:\n\${contents.map((c,i) => \`// \${tsFiles[i]}\n\${c}\`).join('\n\n')}\`
    });
    
    // 4. Apply fixes (batched writes)
    const fixes = JSON.parse(analysis);
    await batchTools(
      fixes.map(f => ({name: 'write_file', args: {path: f.path, content: f.fixedCode}}))
    );
    
    return { fixed: fixes.length, files: tsFiles.length };
  `);
  
  console.log(result); // { success: true, result: { fixed: 5, files: 12 }, durationMs: 2340 }
}

/**
 * Example 2: Run tests and fix failures
 */
async function exampleTestFix() {
  const sdk = new DeepSeekHarnessSDK();
  
  const result = await sdk.execute(`
    // Run tests
    const testResult = await execute_command({
      command: 'npm test',
      cwd: '.'
    });
    
    if (testResult.code !== 0) {
      // Parse failures
      const failures = parseTestFailures(testResult.stdout);
      
      // For each failure, read file and fix
      for (const fail of failures) {
        const content = await read_file({path: fail.file});
        const fixed = await llm_complete({
          prompt: \`Fix this test failure:\nFile: \${fail.file}\nError: \${fail.error}\nCode:\n\${content}\`
        });
        await write_file({path: fail.file, content: fixed});
      }
      
      // Re-run tests
      const retry = await execute_command({command: 'npm test'});
      return { fixed: failures.length, passed: retry.code === 0 };
    }
    
    return { fixed: 0, passed: true };
  `);
  
  return result;
}

/**
 * Example 3: Code generation from spec
 */
async function exampleCodeGen() {
  const sdk = new DeepSeekHarnessSDK({
    globals: { SPEC: loadSpec('./spec.yaml') }
  });
  
  return await sdk.execute(`
    // Generate API routes from OpenAPI spec
    const routes = generateRoutes(SPEC);
    
    // Write all files in one batch
    await batchTools(
      routes.map(r => ({name: 'write_file', args: r}))
    );
    
    // Run linter
    await execute_command({command: 'npm run lint'});
    
    return { generated: routes.length };
  `);
}

interface ToolFunction {
  (args: Record<string, any>): Promise<any>;
}

interface ExecutionResult {
  success: boolean;
  result?: any;
  error?: string;
  durationMs: number;
  scriptId: string;
}

interface SessionMetrics {
  sessionId: string;
  toolsRegistered: number;
  totalExecutions: number;
  totalDurationMs: number;
  avgDurationMs: number;
  batchedCalls: number;
  estimatedTokenSavings: number;
}

function uuid(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}
```

</details>

**Mấy điểm ăn tiền**:

1. ✅ **Chạy một lượt là xong** — Cả task gói trong 1 script, khỏi vòng lặp LLM nhiều lượt
2. ✅ **Gom mẻ mà chạy** — `batchTools([...])` dồn nhiều tool calls vào 1 lần chạy, **đỡ chờ 70-90% thời gian**
3. ✅ **Nhốt trong sandbox VM** — Node.js `vm` context, không mạng, không thò tay ra ngoài chỗ cho phép
4. ✅ **Chạy lại y hệt** — Cùng script + cùng input là ra cùng output. Debug, test, CI/CD đều khỏe
5. ✅ **Đỡ tốn token** — Khỏi gửi kết quả tool về cho LLM tính bước tiếp. LLM chỉ cần gọi 1 lần (có khi 0 lần nếu code thuần)
6. ✅ **Song song mặc định** — `batchTools` cho mọi tool chạy cùng lúc tự động

**Code Mode so với kiểu thường**:

| Aspect | Standard Mode | Code Mode (`@deepseek-ai/dsh`) |
|--------|---------------|-------------------------------|
| **Turns** | Multi-turn (5-20+) | Single-turn (1) |
| **Latency** | High (sequential LLM calls) | Low (batched, parallel) |
| **Token Cost** | High (full context each turn) | **70-90% less** |
| **Tools** | All tools | `bash`, `editor`, `llm_complete` only |
| **Isolation** | Process-level | VM sandbox (stronger) |
| **Determinism** | Non-deterministic | Deterministic (script-based) |
| **Use Case** | Open-ended tasks | Well-defined coding tasks |

**Đọc thêm code thật ở đâu**: xem chi tiết implementation trong [`code-mode-sdk.md`](code-mode-sdk.md)

---

## 12. Design Principles

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Design Principles là bộ "luật làng" về kiến trúc phần mềm — ở đây là mang nguyên lý SOLID vào áp cho hệ thống quản lý và điều phối tools.
>
> **Hình dung vui:** Như quy hoạch khu phố trước khi cấp phép xây nhà: không cần biết từng căn sẽ sơn màu gì, nhưng móng, đường, điện nước ai cũng theo một chuẩn thì phố mới không thành mớ bòng bong.
>
> **Sao phải quan tâm:** Nhà tool nay nở mai thêm món mới liên tục; làm theo SOLID thì thêm món mới mà không làm sập món cũ.

### 12.1 SOLID Cho Tools

**1. Single Responsibility — Mỗi tool một nghề**
- Mỗi tool chỉ nhận một việc rõ ràng
- Đừng nhét cả tìm kiếm + ghi file vào chung một tool

**2. Open/Closed — Dễ thêm, khó vỡ**
- Thoải mái đăng ký tool mới (register)
- Hạn chế đụng chạm tool đang chạy ổn

**3. Liskov Substitution — Hàng nào cũng vừa khay**
- Tool nào cũng nói chung một interface
- Đổi tool này bằng tool khác mà chỗ cắm vẫn vừa

**4. Interface Segregation — Ai lo việc nấy**
- Tờ khai tool (definition) để riêng với người chạy tool (execution)
- Người gác cổng quyền (permission checker) để riêng với người chạy (executor)

**5. Dependency Inversion — Nhờ vào hợp đồng, đừng bám vào ruột**
- Tool nào cũng dựa vào abstraction `ToolRegistry`
- Đừng hardcode ruột gan từng tool vào code

---

## 13. Best Practices

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Best Practices là cuốn "bí kíp" rút ra từ bao pha toát mồ hôi: việc nên làm (DO), việc nên tránh (DON'T) và mẹo tối ưu khi dựng hệ thống chọn tool.
>
> **Hình dung vui:** Như bảng nội quy an toàn trong xưởng: ghi rõ thao tác chuẩn (DO) và việc cấm tiệt (DON'T) để người mới vào không phải trả giá bằng đồ hỏng.
>
> **Sao phải quan tâm:** Đa số pha hỏng của hệ tool đều là lỗi hoàn toàn tránh được; đọc trước bảng này là hưởng ké bài học xương máu của người đi trước.

### 13.1 DO ✅

- **Kiểm tra tham số trước khi chạy**: chặn lỗi từ trong trứng
- **Thử lại theo kiểu backoff (càng lúc chờ càng lâu)**: đừng nện liên tục vào service đang ốm
- **Ghi log mọi lần gọi tool**: sau này debug hay tối ưu đều cần
- **Đặt timeout**: đừng để một cuộc gọi treo cả hệ thống
- **Soát quyền trước**: an toàn là trên hết
- **Theo dõi chi phí mỗi lần gọi**: giữ hầu bao cho chặt
- **Viết mô tả tool cho rõ ràng**: LLM cũng như người mới — mô tả ú ớ là làm sai
- **Xài song song cả rule-based lẫn LLM-based**: vừa nhanh vừa chắc
- **Cache danh sách tool**: đừng lần nào cũng đi hỏi lại từ đầu
- **Có tool dự phòng**: món chính hỏng thì còn món thay thế

### 13.2 DON'T ❌

- **Đừng bỏ qua kiểm tra tham số**: tham số bậy là sập ngay
- **Đừng coi thường rate limit**: bị khóa API là chuyện có thật
- **Đừng ghi cứng đường dẫn tool trong code**: cứ đi qua registry
- **Đừng quên xử lý lỗi**: tool nào cũng có ngày dở chứng
- **Đừng viết mô tả tool chung chung**: LLM không đoán mò giùm bạn đâu
- **Đừng cho thử lại vô hạn**: đặt trần số lần retry
- **Đừng chạy tool nguy hiểm mà không xin phép**: lúc nào cũng phải kiểm tra quyền
- **Đừng lờ tool đã deprecated**: dắt user sang tool mới cho nhẹ nhàng

---

## 14. Testing

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Testing là khâu "tổng duyệt": viết unit test soi từng món (chọn tool, đoán ý, chạy tool, phân quyền, giới hạn lượt gọi) rồi viết integration test cho cả pipeline chạy liền một mạch.
>
> **Hình dung vui:** Như buổi tổng duyệt trước đêm diễn: từng diễn viên thoại riêng (unit test), rồi cả đoàn chạy liền vở (integration test) để bắt lỗi trước khi mở màn trước khán giả (production).
>
> **Sao phải quan tâm:** Tool gọi hỏng ngoài production là lỗi đắt nhất; bắt được lúc còn trên bàn test thì tiền sửa gần như bằng không.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import unittest

class TestToolRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = create_default_tools()
    
    def test_register_and_get(self):
        tool = self.registry.get_tool("calculator")
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "calculator")
    
    def test_search(self):
        results = self.registry.search("tìm")
        self.assertGreater(len(results), 0)
    
    def test_category_filter(self):
        tools = self.registry.list_tools(category="search")
        for tool in tools:
            self.assertEqual(tool.category, "search")
    
    def test_deprecation(self):
        tool = self.registry.get_tool("calculator")
        self.assertFalse(tool.is_deprecated())

class TestIntentClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = IntentClassifier()
    
    def test_search_intent(self):
        result = self.classifier.classify("Tìm thông tin về BHYT")
        self.assertEqual(result["intent"], "search")
        self.assertGreater(len(result["tools"]), 0)
    
    def test_calculate_intent(self):
        result = self.classifier.classify("Tính 15% của 5000000")
        self.assertEqual(result["intent"], "calculate")
    
    def test_chat_fallback(self):
        result = self.classifier.classify("Xin chào!")
        self.assertEqual(result["intent"], "chat")
    
    def test_multi_intent(self):
        intents = self.classifier.classify_multi_intent("Đọc file và chạy test")
        self.assertGreaterEqual(len(intents), 2)

class TestToolExecutor(unittest.TestCase):
    def setUp(self):
        self.registry = create_default_tools()
        self.executor = ToolExecutor(self.registry)
    
    def test_successful_execution(self):
        result = self.executor.execute("calculator", {"expression": "2+3"})
        self.assertTrue(result["success"])
    
    def test_missing_tool(self):
        result = self.executor.execute("nonexistent", {})
        self.assertFalse(result["success"])
        self.assertIn("not found", result["error"])
    
    def test_missing_required_param(self):
        result = self.executor.execute("vector_search", {})
        self.assertFalse(result["success"])
        self.assertIn("Invalid parameters", result["error"])
    
    def test_stats(self):
        self.executor.execute("calculator", {"expression": "1+1"})
        self.executor.execute("calculator", {"expression": "2+2"})
        stats = self.executor.get_stats()
        self.assertEqual(stats["total_calls"], 2)
        self.assertEqual(stats["successful"], 2)

class TestPermissionSystem(unittest.TestCase):
    def setUp(self):
        self.checker = ToolPermissionChecker()
        self.checker.set_user_role("user1", "user")
        self.checker.set_user_role("admin1", "admin")
    
    def test_standard_permission(self):
        result = self.checker.check("user1", "standard")
        self.assertTrue(result["allowed"])
    
    def test_elevated_denied(self):
        result = self.checker.check("user1", "elevated")
        self.assertFalse(result["allowed"])
    
    def test_admin_has_all(self):
        result = self.checker.check("admin1", "admin")
        self.assertTrue(result["allowed"])
    
    def test_custom_grant(self):
        self.checker.grant_permission("user1", "elevated")
        result = self.checker.check("user1", "elevated")
        self.assertTrue(result["allowed"])

class TestRateLimiter(unittest.TestCase):
    def setUp(self):
        self.limiter = RateLimiter(strategy="sliding_window")
        self.limiter.set_limit("api_call", max_calls=3, window_seconds=60)
    
    def test_within_limit(self):
        for _ in range(3):
            result = self.limiter.check("api_call")
            self.assertTrue(result["allowed"])
    
    def test_exceeds_limit(self):
        for _ in range(3):
            self.limiter.check("api_call")
        result = self.limiter.check("api_call")
        self.assertFalse(result["allowed"])
        self.assertIn("retry_after", result)

class TestToolComposer(unittest.TestCase):
    def setUp(self):
        self.registry = create_default_tools()
        self.executor = ToolExecutor(self.registry)
        self.composer = ToolComposer(self.executor)
    
    def test_chain(self):
        steps = [
            {"tool": "calculator", "params": {"expression": "2+3"}, "output_key": "result"},
        ]
        result = self.composer.chain(steps)
        self.assertTrue(result["success"])

if __name__ == "__main__":
    unittest.main()
```

</details>

---

## 15. Advanced Patterns

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Advanced Patterns là mấy chiêu nâng cao như Tool Learning — để agent tự học cách xài tool mới ngay trong lúc chạy — cùng kiểu đăng ký tool động (dynamic registration).
>
> **Hình dung vui:** Như bạn nhân viên bán hàng mới: tuần đầu việc gì cũng phải giở sổ hướng dẫn, vài tháng sau tự biết món nào bán chạy, khâu nào dễ mất khách — càng làm càng thuộc bài mà chẳng cần ai sửa code giùm.
>
> **Sao phải quan tâm:** Hệ thống chạy càng lâu càng tự khôn ra — trúng nhiều hơn, chờ ít hơn, mà khỏi cần người canh chỉnh tay.

### 15.1 Tool Learning

Mục này chạy được trò gì? `ToolLearner` cặm cụi ghi sổ mỗi lần agent gọi tool: việc thuộc loại nào, xài tool nào, thành hay bại, chờ bao lâu (hàm `record`). Tới lúc cần chọn tool, hàm `recommend()` xếp hạng ứng viên theo tỉ lệ thành công rồi trừ điểm mấy anh chậm chạp; tool nào chưa từng xài thì cho điểm giữa giữa 0.5. Chiêu đơn giản mà là nền móng để agent tự khôn lên: rút kinh nghiệm từ sổ cũ thay vì chờ người sửa code.

*Hình dung vui:* Như app gọi xe nhớ mặt bác tài nào hay đón đúng giờ, chạy êm — lần sau ưu tiên gán xe của bác đó cho bạn.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class ToolLearner:
    """
    Agent learns which tools work best for which tasks
    
    Based on execution history, learns:
    - Tool preference per task type
    - Parameter patterns
    - Failure modes
    """
    
    def __init__(self):
        self.history: List[Dict] = []
        self.tool_scores: Dict[str, Dict] = {}
    
    def record(self, task_type: str, tool_name: str, 
               params: Dict, success: bool, latency_ms: float):
        """Record a tool usage"""
        self.history.append({
            "task_type": task_type,
            "tool": tool_name,
            "params": params,
            "success": success,
            "latency_ms": latency_ms,
            "timestamp": datetime.now().isoformat(),
        })
        
        # Update scores
        key = f"{task_type}:{tool_name}"
        if key not in self.tool_scores:
            self.tool_scores[key] = {"success_count": 0, "total_count": 0, "avg_latency": 0}
        
        score = self.tool_scores[key]
        score["total_count"] += 1
        if success:
            score["success_count"] += 1
        score["avg_latency"] = (
            0.1 * latency_ms + 0.9 * score["avg_latency"]
        )
    
    def recommend(self, task_type: str, available_tools: List[str]) -> List[str]:
        """Recommend tools for a task type based on history"""
        scored = []
        
        for tool in available_tools:
            key = f"{task_type}:{tool}"
            score = self.tool_scores.get(key, {"success_count": 0, "total_count": 0})
            
            if score["total_count"] > 0:
                success_rate = score["success_count"] / score["total_count"]
                # Penalize high latency
                latency_penalty = min(score["avg_latency"] / 1000, 1)
                final_score = success_rate * (1 - latency_penalty)
            else:
                final_score = 0.5  # Unknown = medium score
            
            scored.append((final_score, tool))
        
        scored.sort(reverse=True)
        return [tool for _, tool in scored]
```

</details>

---

## 16. Tương Lai

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Tương Lai là mục ngó trước mấy con sóng lớn của làng tool decision và MCP giai đoạn 2026-2028: chuẩn hóa giao thức, agent tự mò ra tool mới và tự gói wrapper, rồi chia sẻ tool giữa nhiều agent.
>
> **Hình dung vui:** Như coi dự báo thời tiết trước chuyến đi xa: không ai dám chắc 100%, nhưng ngó trước thì soạn hành lý (kiến trúc) mới đúng hướng.
>
> **Sao phải quan tâm:** Cách đặt móng hôm nay quyết định hai ba năm nữa bạn ung dung lướt sóng hay phải đập đi xây lại từ đầu.

### 16.1 Xu Hướng 2026-2028

**1. Tự mò ra tool (Auto Tool Discovery)**
- Agent tự lần ra tool từ các MCP servers
- Tự gói wrapper cho tool lạ chưa gặp bao giờ
- Ghép tool theo nghĩa (semantic matching)

**2. AI tự ghép tool (Tool Composition AI)**
- Agent tự xâu tool thành quy trình
- Học chuỗi tool ngon từ lịch sử chạy thật
- Pipeline tự tối ưu dần

**3. Tool xài chéo mọi nơi (Cross-Platform Tools)**
- Tool mang từ agent này sang agent khác vẫn chạy
- Chợ tool theo chuẩn chung
- Một interface xài cho mọi nhà

**4. Đoán trước để dọn sẵn (Predictive Tool Use)**
- Đoán trước sẽ cần tool nào
- Hâm nóng kết nối từ sớm
- Lấy sẵn dữ liệu chờ đó

**5. Tool an toàn hơn (Tool Security)**
- Chạy tool kiểu zero-trust (không tin ai sẵn)
- Nhốt tool trong sandbox
- Việc nào cũng để lại vết audit

## 17. Củng Cố Production: MCP, Ranh Giới Thực Thi, Memoization

> **Ghi chú sở hữu.** Mục này phụ trách phần **tầng tool** sở hữu: MCP client, các khai báo
> năng lực mà một tool phải công bố, và memoization. **Chính sách cách ly** (tier, 5 control
> bắt buộc, runner đã harden) do [`12-sandbox-execution`](../12-sandbox-execution/README.md) sở hữu;
> **phán quyết của con người** (risk tier, payload cổng, timeout-deny) do
> [`15-approval-gates`](../15-approval-gates/README.md) sở hữu. Cả hai là module cross-cutting
> bao quanh mọi tool call. Module này khai báo *tool cần gì*; 12 và 15 quyết định *tool có được không*.

### 17.1 Định nghĩa

| Thuật ngữ | Định nghĩa | Chủ sở hữu |
|------|------------|-------|
| Sandbox | Tool/code không tin cậy chạy trong Docker/microVM/gVisor với allowlist FS, mặc định không net, timeout+kill, không chứa secret env | → `12-sandbox-execution` |
| MCP client production | Auth (OAuth/xoay key), ghim `protocolVersion` + cache capability có TTL, `tools/list` ETag, giới hạn kích thước kết quả + cắt ngắn | module này |
| Cổng op nguy hiểm | Ghi/chạy/mạng/publish cần bản ghi approval tường minh (ai, cái gì, diff, hết hạn) | → `15-approval-gates` |
| Memoization | `(tool, args_hash)` giống nhau trong TTL trả kết quả cache; streaming nhả chunk một phần có trần | module này |

### 17.2 Ranh Giới Thực Thi — Phần Module Này Sở Hữu

Tool registry là nơi một tool *công bố* bán kính ảnh hưởng của nó; `12-sandbox-execution` là
nơi bản công bố đó được *cưỡng chế*. Việc của module này là giữ cho bản công bố đó trung thực:

1. **Mọi tool phải công bố năng lực, không chỉ tham số.** Cùng với `path`/`query`, một tool
   khai báo `net: ["api.example.com"]`, `allowWrite: ["src/**"]`, `secrets: ["EXAMPLE_API_KEY"]`
   và `irreversible: boolean`. Tool không khai báo gì sẽ nhận profile từ chối mặc định.
2. **Bản khai báo được version và có thể review.** Đổi `irreversible: false → true` là một
   diff có ý nghĩa bảo mật và phải qua cùng quy trình review với code; các tier cổng trong
   `15-approval-gates` được định khoá theo chính các field này.
3. **Executor từ chối mở rộng quyền.** Nếu runtime của tool yêu cầu nhiều hơn điều nó đã khai
   báo (ghi ngoài `allowWrite`, egress ra host không có trong `net`), harness chặn lời gọi và
   phát `tool_result` với `error: "capability-escalation"` — không cho qua trong im lặng.
4. **Rate limit và timeout cũng là phần khai báo của tool** (`rate_limit_per_minute`,
   `timeout_seconds` trong `ToolDefinition` ở trên), và deadline sandbox ở `12` phải
   `≥` timeout của tool để deadline ngoài không bao giờ nổ trước deadline trong.

Bộ quy tắc đầy đủ — tier cách ly, allowlist filesystem, network deny-by-default,
deadline + process-group kill, trần output, giữ secret, ma trận policy theo role,
và runner đã harden với image ghim theo digest — nằm ở
[`12-sandbox-execution`](../12-sandbox-execution/README.md). Hãy đọc module đó trước khi
viết bất kỳ dòng code nào spawn subprocess.

### 17.3 Quy Tắc MCP Trong Production

> **Oct-2026:** spec stateless `2026-07-28` là bản mới nhất rồi nhé.
> Cách chuyển chi tiết từng bước xem ở [`2026-07-28-migration.md`](./2026-07-28-migration.md).
> Kiểu chào hỏi `initialize` và `Mcp-Session-Id` cũ bỏ hẳn.

1. Ghim `protocolVersion` **theo từng request** (`_meta` + header `MCP-Protocol-Version`, mặc định `"2026-07-28"`, giữ shim tương thích `"2025-06-18"`); cache `tools/list` theo `ttlMs/cacheScope` (fallback 5–15 phút); gặp `426`/tool lạ/`UnsupportedProtocolVersionError` thì vô hiệu ngay.
2. Auth: OAuth2 bearer có refresh + scope tối thiểu; xoay key; không bao giờ log token (redact `Bearer`).
3. Trần: `timeout 30s`, `kết quả ≤128KB`, `args ≤32KB`, validate args theo schema trước khi gửi.
4. Streaming: chuyển tiếp chunk `content` khi tới, áp trần tổng + idle timeout (10s); hủy khi client cancel.

<details>
<summary>TypeScript Code — Gọi MCP + Memoization (Click to expand/collapse)</summary>

```typescript
const memo = new Map<string, { at: number; val: any }>();
export async function callMcp(url: string, token: string, tool: string, args: object, v = "2026-07-28") { // tương thích: "2025-06-18"; xem 2026-07-28-migration.md
  const key = `${tool}:${JSON.stringify(args)}`; const m = memo.get(key);
  if (m && Date.now() - m.at < 60_000) return { ...m.val, memoHit: true };
  const r = await fetch(`${url}/tools/call`, { method: "POST", signal: AbortSignal.timeout(30_000),
    headers: { authorization: `Bearer ${token}`, "mcp-protocol-version": v, "content-type": "application/json" },
    body: JSON.stringify({ name: tool, arguments: args }) });
  if (r.status === 426) throw new Error("MCP version mismatch: refresh tools/list + capability cache");
  const j: any = await r.json(); let text = JSON.stringify(j.content ?? j).slice(0, 128_000);
  if (JSON.stringify(j).length > 128_000) text += "\n…[truncated: result cap 128k]";
  const out = { ok: !j.isError, text }; memo.set(key, { at: Date.now(), val: out }); return out;
}
```

> Runner subprocess có sandbox từng nằm ở đây đã chuyển sang
> [`12-sandbox-execution` §4.2](../12-sandbox-execution/README.md), nơi ghim image theo digest,
> chặn path traversal qua `realpath`, ép idle timeout, và redact secret khỏi output.
> Đừng đưa lại runner gắn tag `:latest` vào đây.

</details>

### 17.4 UX Approval Cho Op Nguy Hiểm

Taxonomy tier, payload cổng bắt buộc có bằng chứng, timeout-deny (fail closed), và audit
trail `approval_request` / `approval_verdict` đều do
[`15-approval-gates`](../15-approval-gates/README.md) sở hữu. Phần thuộc về đây là
**UX đồng ý phía tool**, vì tool definition chính là nơi người duyệt biết mình đang duyệt cái gì:

- **Hiển thị từ bản khai báo, không phải từ args thô.** Cổng hiện `command`, `cwd`, các file
  chạm tới, egress mạng, và cờ `irreversible` — tất cả đến từ năng lực tool đã khai báo (§17.2),
  không phải từ việc phân tích lại `args` tại thời điểm duyệt.
- **Tool không khai báo năng lực gì sẽ hiện thành bán kính ảnh hưởng không xác định**, điều này
  ép lên tier cao nhất. Không bao giờ để một tool có vẻ an toàn hơn thực tế.
- **Một click cho `write/exec`, gõ xác nhận cho `publish/delete/auth-change`** — nhưng cửa sổ
  hết hạn và luật hai-người đến từ `15`, không từ đây.
- **Tool MCP nhận nhãn server** trong prompt đồng ý. Duyệt một lời gọi tới MCP server từ xa
  là quyết định tin cậy khác hẳn việc duyệt một subprocess cục bộ.

### 17.5 Checklist

- [ ] Mọi tool có khai báo `net` / `allowWrite` / `secrets` / `irreversible`? Không khai báo = từ chối mặc định?
- [ ] Control sandbox đã đối chiếu với `12-sandbox-execution` (tắt net, allowlist FS, timeout+SIGKILL, trần output, không secret env, image ghim digest)?
- [ ] MCP: ghim version, cache giới hạn có TTL + vô hiệu, auth xoay vòng, trần kích thước/timeout?
- [ ] Op nguy hiểm qua cổng với xem trước diff + bản ghi approval hết hạn, theo `15-approval-gates`?
- [ ] Memo cuộc gọi giống nhau theo hash args chuẩn có TTL; streaming có trần?

---

## Tài Liệu Tham Khảo

### Papers & Research

1. **Toolformer: Language Models Can Teach Themselves to Use Tools**
   - Schick et al., 2023
   - https://arxiv.org/abs/2302.04761

2. **Gorilla: Large Language Model Connected with Massive APIs**
   - Patil et al., 2023
   - https://arxiv.org/abs/2305.15334

3. **API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs**
   - Li et al., 2023
   - https://arxiv.org/abs/2304.08354

4. **NexusRaven: Function Calling for LLMs**
   - Nexusflow, 2023
   - https://arxiv.org/abs/2312.15933

### Frameworks & Tools

1. **MCP (Model Context Protocol)** - https://modelcontextprotocol.io
2. **OpenAI Function Calling** - https://platform.openai.com/docs
3. **Anthropic Tool Use** - https://docs.anthropic.com
4. **LangChain Tools** - https://langchain.com
5. **Semantic Kernel** - https://learn.microsoft.com/semantic-kernel

---

*Tài liệu: VI. Decide Tools / MCP Calls — HARNESS ENGINEERING EDITION*
*Ngày cập nhật: 16/10/2026 (stateless 2026-07-28: xem 2026-07-28-migration.md)*
*Ngày cập nhật: 10/2026 — MCP Ecosystem & Code Execution Pattern*

---

## Cập nhật 10/2026 — MCP Ecosystem & Code Execution Pattern

> **📌 Tóm tắt**
>
> Tháng 10/2026, hệ sinh thái MCP đã phát triển vượt bậc: spec `2026-07-28` hoàn thiện, hàng loạt AI clients hỗ trợ (Claude, ChatGPT, VS Code, Cursor, MCPJam...), và quan trọng nhất — mô hình **code execution với MCP** (Anthropic 11/2025) giúp agent viết code gọi MCP tools thay vì expose hàng chục tools riêng lẻ, giảm token và latency đáng kể.

### 1. MCP Ecosystem 2026 — "USB-C cho AI"

**MCP** (Model Context Protocol) ngày càng trở thành chuẩn kết nối tool cho AI agents. Spec `2026-07-28` hoàn thiện nhiều tính năng mới:

| Thành phần | Mô tả |
|---|---|
| **Spec** | `2026-07-28` — định nghĩa đầy đủ tools, resources, prompts, sampling |
| **MCP Apps** | Các ứng dụng chạy trong AI clients (Cursor, VS Code, Claude Desktop...) |
| **Hỗ trợ rộng** | Claude, ChatGPT, VS Code, Cursor, MCPJam, nhiều nhà khác |
| **Mô tả gốc** | MCP = "USB-C cho AI" — kết nối unified thay vì mỗi nhà một kiểu |

> **Phân biệt MCP vs A2A:** Hai giao thức bổ sung nhau:
> - **MCP** (Model Context Protocol): Agent → Tool (gọi tool/services)
> - **A2A** (Agent-to-Agent): Agent → Agent (giao tiếp giữa các agents với nhau)
>
> A2A đã được tích hợp vào [Agentic AI Foundation 08/2026](https://github.com/agentprotocol/A2A) — Layer 4. MCP và A2A cùng tồn tại, phục vụ hai nhu cầu khác nhau.

### 2. Code Execution Pattern với MCP (Anthropic 11/2025)

**Bài toán cũ:** Khi agent kết nối nhiều MCP servers (mỗi server có 5-10 tools), tổng cộng có thể lên tới 50-100 tools. Mỗi tool description phải nằm trong context của mỗi LLM call → tốn **token + latency**.

**Giải pháp — Agent viết code gọi MCP tools:**

```
┌─────────────────────────────────────────────────────────────┐
│              CODE EXECUTION WITH MCP                        │
│                                                             │
│  Agent viết code:                                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ # Agent viết code để gọi tool                       │   │
│  │ results = await mcp_batch([                          │   │
│  │   {"server": "filesystem", "tool": "read",           │   │
│  │    "args": {"path": "/data/a.txt"}},                │   │
│  │   {"server": "web", "tool": "search",                │   │
│  │    "args": {"query": "bug fixes"}},                 │   │
│  │   {"server": "db", "tool": "query",                 │   │
│  │    "args": {"sql": "SELECT * FROM logs"}},          │   │
│  │ ])                                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│       │                                                    │
│       ▼                                                    │
│  Sandbox executor chạy code → gọi MCP servers              │
│       │                                                    │
│       ▼                                                    │
│  Chỉ TRẢ VỀ KẾT QUẢ TỔNG HỢP cho context                  │
│       (giảm token đáng kể so với expose 50+ tools)         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**So sánh hai cách tiếp cận:**

| Tiêu chí | Expose mỗi tool riêng lẻ | Code execution pattern |
|---|---|---|
| Số tools trong context | 50-100 tool descriptions | 1 tool `mcp_batch_execute` |
| Token cost | Cao (mỗi tool × mỗi call) | Thấp (chỉ kết quả aggregate) |
| Latency | Tăng theo số tools | Tương đương 1 tool call |
| Phù hợp | < 20 tools | Nhiều MCP servers, nhiều tools |
| Code complexity | Thấp | Trung bình (cần sandbox executor) |

### 3. Tool Design — Action Centered Intelligence (ACI)

Tool descriptions cần viết như **docstring cho junior developer** — rõ ràng, đầy đủ, không mơ hồ:

```python
# ❌ BAD: Description mơ hồ
{
    "name": "get_data",
    "description": "Lấy dữ liệu từ hệ thống",
}

# ✅ GOOD: Description như docstring dev
{
    "name": "get_employee_records",
    "description": """
    Trả về danh sách nhân viên theo filter.
    Args:
        department (str): Tên phòng ban (VD: "IT", "HR")
        status (str): Trạng thái ("active"|"all", default="active")
        limit (int): Số bản ghi tối đa (1-100, default=50)
    Returns:
        List[dict]: Danh sách nhân viên với fields: id, name, department, email
    Raises:
        ValueError: department không hợp lệ
        PermissionError: Không có quyền truy cập phòng ban này
    """,
}
```

**4 nguyên tắc ACI Tool Design:**

1. **Descriptions = docstring cho junior dev** — mô tả rõ input/output/error, không viết tắt
2. **Format gần text tự nhiên** — tool name dùng underscores, mô tả dạng câu
3. **Poka-yoke params** — dùng absolute paths, enums thay vì free-form strings, defaults rõ ràng
4. **Test tool với inputs thật** — đừng chỉ viết mô tả; phải chạy thử, nhất là edge cases

**Tránh bloated toolset:** 10 tool chất lượng tốt hơn 50 tool "cũng được".

### 4. Python — Sandbox Executor Pattern

```python
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
```

### 5. Cross-links

- [AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md)
- [agent-skills-spec.md](../05-prompt-builder/agent-skills-spec.md) — Agent Skills Open Standard (agentskills.io)

*Tác giả: AI Knowledge Repository*