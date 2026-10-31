from typing import List, Dict, Optional
from dataclasses import dataclass, field

@dataclass
class SubTask:
    """Sub-task con trong task decomposition"""
    id: str
    title: str
    description: str
    order: int
    parallel: bool = False
    estimated_tokens: int = 0
    dependencies: List[str] = field(default_factory=list)
    files_to_modify: List[str] = field(default_factory=list)
    verification_criteria: str = ""


class TaskDecomposer:
    """
    Phân rã task lớn thành các sub-task có thể thực hiện riêng.
    
    Strategies:
    - feature-based: Chia theo tính năng
    - layer-based: Chia theo layer (UI, API, DB)
    - file-based: Chia theo file
    - test-driven: Viết test trước, rồi code
    - vertical-slice: Mỗi slice = full stack working increment
    - spike-then-execute: Research trước, rồi implement
    """
    
    def decompose(self, task: Task, strategy: str = "auto",
                  project_context: Dict = None) -> List[SubTask]:
        """Phân rã task thành sub-tasks"""
        
        if strategy == "auto":
            strategy = self._suggest_strategy(task, project_context)
        
        if strategy == "feature":
            return self._decompose_by_feature(task)
        elif strategy == "layer":
            return self._decompose_by_layer(task)
        elif strategy == "file":
            return self._decompose_by_file(task)
        elif strategy == "tdd":
            return self._decompose_tdd(task)
        elif strategy == "vertical_slice":
            return self._decompose_vertical_slice(task)
        elif strategy == "spike":
            return self._decompose_spike(task)
        else:
            return self._decompose_by_feature(task)
    
    def _suggest_strategy(self, task: Task, 
                          context: Dict = None) -> str:
        """Gợi ý strategy phù hợp dựa trên task characteristics"""
        context = context or {}
        
        # Trivial tasks - don't decompose
        if task.complexity.value <= 1:
            return "simple"
        
        # Test-related tasks
        if "test" in task.description.lower():
            return "tdd"
        
        # Generation tasks - feature-based
        if task.category == TaskCategory.GENERATION:
            if len(task.files_involved) > 3:
                return "vertical_slice"
            return "feature"
        
        # Modification tasks - file-based or layer-based
        if task.category == TaskCategory.MODIFICATION:
            if len(task.files_involved) > 5:
                return "layer"
            return "file"
        
        # Complex/uncertain tasks - spike first
        if task.complexity.value >= 4:
            if context.get("uncertain_approach", False):
                return "spike"
            return "layer"
        
        return "feature"
    
    def _decompose_by_feature(self, task: Task) -> List[SubTask]:
        """Chia theo tính năng — full workflow"""
        subtasks = []
        
        subtasks.append(SubTask(
            id=f"{task.id}-01",
            title="Phân tích yêu cầu",
            description=f"Đọc và hiểu yêu cầu: {task.description}",
            order=1,
            estimated_tokens=500,
            verification_criteria="Có danh sách requirements rõ ràng",
        ))
        
        subtasks.append(SubTask(
            id=f"{task.id}-02",
            title="Đọc code hiện tại",
            description="Xem codebase liên quan để hiểu context",
            order=2,
            dependencies=[f"{task.id}-01"],
            estimated_tokens=1500,
            verification_criteria="Đã identify affected files và patterns",
        ))
        
        subtasks.append(SubTask(
            id=f"{task.id}-03",
            title="Lên kế hoạch thay đổi",
            description="Xác định files cần sửa và cách tiếp cận",
            order=3,
            dependencies=[f"{task.id}-02"],
            estimated_tokens=800,
            verification_criteria="Có plan cụ thể với file list và approach",
        ))
        
        subtasks.append(SubTask(
            id=f"{task.id}-04",
            title="Triển khai code",
            description="Viết code theo kế hoạch",
            order=4,
            dependencies=[f"{task.id}-03"],
            estimated_tokens=task.estimated_tokens or 3000,
            verification_criteria="Code đã viết xong, không có syntax errors",
        ))
        
        subtasks.append(SubTask(
            id=f"{task.id}-05",
            title="Kiểm tra & validate",
            description="Chạy test, lint, review kết quả",
            order=5,
            dependencies=[f"{task.id}-04"],
            estimated_tokens=1000,
            verification_criteria="Tests pass, lint clean, no regressions",
        ))
        
        return subtasks
    
    def _decompose_by_layer(self, task: Task) -> List[SubTask]:
        """Chia theo layer: DB → Service → API → UI"""
        return [
            SubTask(f"{task.id}-db", "Database layer",
                    "Thay đổi schema, queries, migrations", 1,
                    estimated_tokens=1500,
                    verification_criteria="Schema updated, migrations run"),
            SubTask(f"{task.id}-svc", "Service layer",
                    "Business logic, validation", 2,
                    dependencies=[f"{task.id}-db"],
                    estimated_tokens=2000,
                    verification_criteria="Service logic complete, unit tests pass"),
            SubTask(f"{task.id}-api", "API layer",
                    "Endpoints, request/response, error handling", 3,
                    dependencies=[f"{task.id}-svc"],
                    estimated_tokens=1500,
                    verification_criteria="API endpoints working, OpenAPI spec updated"),
            SubTask(f"{task.id}-ui", "UI layer",
                    "Frontend components, forms, display", 4,
                    dependencies=[f"{task.id}-api"],
                    estimated_tokens=2000,
                    verification_criteria="UI renders correctly, forms submit"),
            SubTask(f"{task.id}-test", "Integration tests",
                    "End-to-end flow tests", 5,
                    dependencies=[f"{task.id}-ui"],
                    estimated_tokens=1500,
                    verification_criteria="All integration tests pass"),
        ]
    
    def _decompose_by_file(self, task: Task) -> List[SubTask]:
        """Chia theo file — mỗi file là 1 sub-task"""
        subtasks = []
        for i, filepath in enumerate(task.files_involved, 1):
            subtasks.append(SubTask(
                id=f"{task.id}-f{i:02d}",
                title=f"Modify {filepath}",
                description=f"Thay đổi file {filepath}",
                order=i,
                files_to_modify=[filepath],
                parallel=True,
                estimated_tokens=1000,
                verification_criteria=f"File {filepath} updated correctly",
            ))
        return subtasks
    
    def _decompose_tdd(self, task: Task) -> List[SubTask]:
        """Test-Driven Development decomposition"""
        return [
            SubTask(f"{task.id}-test-design", "Thiết kế test cases",
                    "Viết test cases dựa trên requirements", 1,
                    estimated_tokens=1000,
                    verification_criteria="Test cases cover all scenarios"),
            SubTask(f"{task.id}-test-write", "Viết tests",
                    "Viết test code (sẽ fail lúc đầu)", 2,
                    dependencies=[f"{task.id}-test-design"],
                    estimated_tokens=1500,
                    verification_criteria="Tests compile, run, and fail (RED)"),
            SubTask(f"{task.id}-impl", "Triển khai code",
                    "Viết code để pass tests", 3,
                    dependencies=[f"{task.id}-test-write"],
                    estimated_tokens=task.estimated_tokens or 2000,
                    verification_criteria="All tests pass (GREEN)"),
            SubTask(f"{task.id}-refactor", "Refactor",
                    "Cải thiện code quality", 4,
                    dependencies=[f"{task.id}-impl"],
                    estimated_tokens=1000,
                    verification_criteria="Code clean, tests still pass"),
        ]
    
    def _decompose_vertical_slice(self, task: Task) -> List[SubTask]:
        """Vertical slice — mỗi slice = full stack working feature"""
        return [
            SubTask(f"{task.id}-slice-core", "Core slice",
                    "Implement core logic + minimal API", 1,
                    estimated_tokens=3000,
                    verification_criteria="Core flow works end-to-end"),
            SubTask(f"{task.id}-slice-data", "Data slice",
                    "Database + repository layer", 2,
                    dependencies=[f"{task.id}-slice-core"],
                    estimated_tokens=2000,
                    verification_criteria="Data persistence working"),
            SubTask(f"{task.id}-slice-api", "API slice",
                    "Full API with validation + error handling", 3,
                    dependencies=[f"{task.id}-slice-data"],
                    estimated_tokens=2000,
                    verification_criteria="All API endpoints functional"),
            SubTask(f"{task.id}-slice-ui", "UI slice",
                    "Frontend integration", 4,
                    dependencies=[f"{task.id}-slice-api"],
                    estimated_tokens=2500,
                    verification_criteria="UI fully functional"),
            SubTask(f"{task.id}-slice-test", "Test slice",
                    "Integration + E2E tests", 5,
                    dependencies=[f"{task.id}-slice-ui"],
                    estimated_tokens=2000,
                    verification_criteria="Full test coverage"),
        ]
    
    def _decompose_spike(self, task: Task) -> List[SubTask]:
        """Spike-then-execute — research trước khi implement"""
        return [
            SubTask(f"{task.id}-spike", "Spike: Research & Decide",
                    "Timebox 1-2h research, compare approaches", 1,
                    estimated_tokens=3000,
                    verification_criteria="Chosen approach documented with rationale"),
            SubTask(f"{task.id}-poc", "Proof of Concept",
                    "Minimal implementation to validate approach", 2,
                    dependencies=[f"{task.id}-spike"],
                    estimated_tokens=2000,
                    verification_criteria="POC works, approach validated"),
            SubTask(f"{task.id}-impl", "Full Implementation",
                    "Implement complete solution", 3,
                    dependencies=[f"{task.id}-poc"],
                    estimated_tokens=task.estimated_tokens or 4000,
                    verification_criteria="Feature complete"),
            SubTask(f"{task.id}-validate", "Validation",
                    "Test, review, verify", 4,
                    dependencies=[f"{task.id}-impl"],
                    estimated_tokens=1500,
                    verification_criteria="All tests pass, code reviewed"),
        ]
