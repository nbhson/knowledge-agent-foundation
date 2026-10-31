def create_default_tools():
    """Create comprehensive default toolset"""
    registry = ToolRegistry()
    
    # ─── Search Tools ───
    registry.register(ToolDefinition(
        name="vector_search",
        description="Semantic search in the vector database",
        parameters={
            "query": {"type": "string", "description": "The query", "required": True},
            "top_k": {"type": "integer", "description": "Number of results to return", "default": 5},
            "collection": {"type": "string", "description": "Collection name"},
            "filters": {"type": "object", "description": "Metadata filters"},
        },
        category="search",
        tags=["semantic", "vector", "embedding"],
        examples=[
            {"query": "Health insurance for employees", "top_k": 3},
        ],
    ))
    
    registry.register(ToolDefinition(
        name="web_search",
        description="Search the internet",
        parameters={
            "query": {"type": "string", "description": "Search keyword", "required": True},
            "num_results": {"type": "integer", "default": 5},
            "region": {"type": "string", "default": "vn"},
        },
        category="search",
        tags=["internet", "realtime", "web"],
    ))
    
    registry.register(ToolDefinition(
        name="sql_query",
        description="Execute SQL query on the database",
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
        description="Safe mathematical calculation",
        parameters={
            "expression": {"type": "string", "description": "Math expression", "required": True},
        },
        category="computation",
        tags=["math", "arithmetic"],
    ))
    
    registry.register(ToolDefinition(
        name="execute_python",
        description="Execute Python code in a sandbox",
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
        description="Analyze data with pandas/numpy",
        parameters={
            "data": {"type": "string", "description": "Data path or CSV string", "required": True},
            "analysis_type": {"type": "string", "enum": ["summary", "correlation", "distribution", "trend"]},
            "columns": {"type": "array", "items": {"type": "string"}},
        },
        category="computation",
        tags=["analytics", "pandas", "statistics"],
    ))
    
    # ─── Code Tools ───
    registry.register(ToolDefinition(
        name="read_file",
        description="Read file content",
        parameters={
            "path": {"type": "string", "description": "File path", "required": True},
            "encoding": {"type": "string", "default": "utf-8"},
            "max_lines": {"type": "integer", "description": "Max lines to read"},
        },
        category="file",
        tags=["read", "file", "filesystem"],
    ))
    
    registry.register(ToolDefinition(
        name="write_file",
        description="Write content to a file",
        parameters={
            "path": {"type": "string", "description": "File path", "required": True},
            "content": {"type": "string", "description": "Content", "required": True},
            "mode": {"type": "string", "enum": ["overwrite", "append"], "default": "overwrite"},
        },
        category="file",
        requires_permission="elevated",
        tags=["write", "file", "filesystem"],
    ))
    
    registry.register(ToolDefinition(
        name="search_code",
        description="Search code in the codebase",
        parameters={
            "query": {"type": "string", "description": "Regex or text pattern", "required": True},
            "path": {"type": "string", "default": "."},
            "file_pattern": {"type": "string", "description": "glob pattern"},
        },
        category="code",
        tags=["code", "search", "regex"],
    ))
    
    registry.register(ToolDefinition(
        name="run_tests",
        description="Run the test suite",
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
        description="Query the knowledge graph",
        parameters={
            "entity": {"type": "string", "description": "Entity name", "required": True},
            "relation": {"type": "string", "description": "Relation type"},
            "max_hops": {"type": "integer", "default": 1},
        },
        category="knowledge",
        tags=["kg", "graph", "entity"],
    ))
    
    registry.register(ToolDefinition(
        name="lookup_definition",
        description="Look up a term definition",
        parameters={
            "term": {"type": "string", "description": "Term to look up", "required": True},
            "domain": {"type": "string", "description": "Domain"},
        },
        category="knowledge",
        tags=["definition", "glossary", "reference"],
    ))
    
    # ─── Memory Tools ───
    registry.register(ToolDefinition(
        name="recall_memory",
        description="Recall information from memory",
        parameters={
            "query": {"type": "string", "description": "The query", "required": True},
            "memory_type": {"type": "string", "enum": ["episodic", "semantic", "all"]},
            "limit": {"type": "integer", "default": 5},
        },
        category="memory",
        tags=["recall", "memory", "history"],
    ))
    
    registry.register(ToolDefinition(
        name="store_memory",
        description="Store information in memory",
        parameters={
            "content": {"type": "string", "description": "Content to store", "required": True},
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
        description="Send a notification to the user",
        parameters={
            "message": {"type": "string", "description": "Notification content", "required": True},
            "channel": {"type": "string", "enum": ["email", "slack", "in_app"], "default": "in_app"},
            "priority": {"type": "string", "enum": ["low", "normal", "high"], "default": "normal"},
        },
        category="communication",
        tags=["notify", "alert", "message"],
    ))
    
    # ─── Version Control Tools ───
    registry.register(ToolDefinition(
        name="git_status",
        description="View git repository status",
        parameters={
            "path": {"type": "string", "default": "."},
        },
        category="devops",
        tags=["git", "status", "vcs"],
    ))
    
    registry.register(ToolDefinition(
        name="git_diff",
        description="View the diff of git changes",
        parameters={
            "ref": {"type": "string", "description": "Branch/commit to diff against"},
            "path": {"type": "string"},
        },
        category="devops",
        tags=["git", "diff", "changes"],
    ))
    
    return registry
