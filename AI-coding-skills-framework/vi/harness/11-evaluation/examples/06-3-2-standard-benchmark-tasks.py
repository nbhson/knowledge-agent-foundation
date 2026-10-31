BENCHMARK_TASKS = {
    # === TRIVIAL (Difficulty: 1/5) ===
    "hello_world": {
        "id": "basic-001",
        "description": "Create a hello world function",
        "difficulty": "trivial",
        "expected": "Hello, World!",
    },
    
    "string_reverse": {
        "id": "basic-002",
        "description": "Reverse a string without built-in",
        "difficulty": "trivial",
        "validator": lambda out: out("hello") == "olleh",
    },
    
    # === EASY (Difficulty: 2/5) ===
    "fibonacci": {
        "id": "algo-001",
        "description": "Implement fibonacci with memoization",
        "difficulty": "easy",
        "validator": lambda out: out(10) == 55,
    },
    
    "binary_search": {
        "id": "algo-002",
        "description": "Implement binary search",
        "difficulty": "easy",
        "validator": lambda out: out([1,2,3,4,5], 3) == 2,
    },
    
    # === MODERATE (Difficulty: 3/5) ===
    "api_endpoint": {
        "id": "web-001",
        "description": "Create a REST API endpoint for CRUD",
        "difficulty": "moderate",
        "validator": lambda out: True,
    },
    
    "bug_fix": {
        "id": "debug-001",
        "description": "Fix off-by-one error in loop",
        "difficulty": "easy",
        "validator": lambda out: True,
    },
    
    # === COMPLEX (Difficulty: 4/5) ===
    "refactor_class": {
        "id": "refactor-001",
        "description": "Refactor God class into smaller classes",
        "difficulty": "complex",
        "validator": lambda out: True,
    },
    
    "write_tests": {
        "id": "test-001",
        "description": "Write comprehensive unit tests",
        "difficulty": "moderate",
        "validator": lambda out: True,
    },
    
    # === HARD (Difficulty: 5/5) ===
    "security_audit": {
        "id": "security-001",
        "description": "Find and fix SQL injection vulnerabilities",
        "difficulty": "moderate",
        "validator": lambda out: True,
    },
    
    "multi_file_refactor": {
        "id": "complex-001",
        "description": "Refactor across 5+ files with dependency updates",
        "difficulty": "hard",
        "validator": lambda out: True,
    },
}
