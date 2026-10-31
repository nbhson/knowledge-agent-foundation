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
