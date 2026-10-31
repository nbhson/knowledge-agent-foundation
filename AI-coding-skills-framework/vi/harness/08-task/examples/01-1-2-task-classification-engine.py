from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
import re

class TaskCategory(Enum):
    GENERATION = "generation"
    MODIFICATION = "modification"
    ANALYSIS = "analysis"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    UNKNOWN = "unknown"

class TaskComplexity(Enum):
    TRIVIAL = 1     # 1 file, < 50 LOC
    SIMPLE = 2      # 1-2 files, < 200 LOC
    MODERATE = 3    # 3-5 files, 200-500 LOC
    COMPLEX = 4     # 5-15 files, 500-2000 LOC
    EPIC = 5        # 15+ files, 2000+ LOC


@dataclass
class Task:
    """Đại diện cho một coding task"""
    id: str
    title: str
    description: str
    category: TaskCategory = TaskCategory.UNKNOWN
    complexity: TaskComplexity = TaskComplexity.SIMPLE
    priority: int = 5                    # 1=highest, 10=lowest
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    estimated_tokens: int = 0
    files_involved: List[str] = field(default_factory=list)


class TaskClassifier:
    """
    Phân loại task tự động dựa trên keywords và patterns.
    
    Usage:
        classifier = TaskClassifier()
        task = classifier.classify(
            "Fix the authentication bug in login handler"
        )
        print(task.category)  # TaskCategory.MODIFICATION
        print(task.complexity)  # TaskComplexity.SIMPLE
    """
    
    PATTERNS = {
        TaskCategory.GENERATION: [
            r"tạo|create|generate|build|new|thêm|add",
            r"function|class|component|endpoint|api",
            r"from scratch|từ đầu|mới",
        ],
        TaskCategory.MODIFICATION: [
            r"sửa|fix|bug|error|broken",
            r"refactor|cải thiện|improve|optimize",
            r"thay đổi|change|update|migrate",
        ],
        TaskCategory.ANALYSIS: [
            r"kiểm tra|check|review|analyze|inspect",
            r"tìm|find|debug|trace|profile",
            r"security|audit|vulnerability",
        ],
        TaskCategory.DOCUMENTATION: [
            r"viết docs|write.*doc|readme|changelog",
            r"document|tài liệu|hướng dẫn|guide",
            r"comment|annotate",
        ],
        TaskCategory.TESTING: [
            r"test|viết test|write.*test|spec",
            r"mock|fixture|assert|coverage",
            r"integration|e2e|unit test",
        ],
    }
    
    COMPLEXITY_SIGNALS = {
        TaskComplexity.TRIVIAL: [
            r"1 dòng|one line|typo|formatting",
            r"rename|đổi tên|thay màu",
        ],
        TaskComplexity.SIMPLE: [
            r"fix.*bug|sửa lỗi đơn",
            r"thêm field|add field|add property",
            r"1 file|single file",
        ],
        TaskComplexity.MODERATE: [
            r"feature|tính năng|feature mới",
            r"refactor|cải trúc|restructure",
            r"multi.?file|nhiều file",
        ],
        TaskComplexity.COMPLEX: [
            r"module|system|hệ thống|architecture",
            r"migration|di chuyển|migrate",
            r"performance.*optimization|tối ưu lớn",
        ],
        TaskComplexity.EPIC: [
            r"redesign|thiết kế lại|rebuild",
            r"major.*overhaul|nâng cấp lớn",
            r"multiple.*module|nhiều module",
        ],
    }
    
    def classify(self, text: str) -> Task:
        text_lower = text.lower()
        
        # Classify category
        category_scores = {}
        for cat, patterns in self.PATTERNS.items():
            score = sum(
                1 for p in patterns 
                if re.search(p, text_lower)
            )
            category_scores[cat] = score
        
        category = max(category_scores, 
                      key=category_scores.get,
                      default=TaskCategory.UNKNOWN)
        if category_scores.get(category, 0) == 0:
            category = TaskCategory.UNKNOWN
        
        # Classify complexity
        complexity_scores = {}
        for comp, patterns in self.COMPLEXITY_SIGNALS.items():
            score = sum(
                1 for p in patterns 
                if re.search(p, text_lower)
            )
            complexity_scores[comp] = score
        
        complexity = max(complexity_scores,
                        key=complexity_scores.get,
                        default=TaskComplexity.SIMPLE)
        if complexity_scores.get(complexity, 0) == 0:
            complexity = TaskComplexity.SIMPLE
        
        return Task(
            id=f"task-{hash(text) % 10000:04d}",
            title=text[:100],
            description=text,
            category=category,
            complexity=complexity,
        )
