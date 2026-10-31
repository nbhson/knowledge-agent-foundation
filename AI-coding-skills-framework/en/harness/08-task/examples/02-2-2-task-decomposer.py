from typing import List, Dict, Optional
from dataclasses import dataclass, field

@dataclass
class SubTask:
    """Child sub-task in task decomposition"""
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
    Decompose a large task into sub-tasks that can be executed independently.
    
    Strategies:
    - feature-based: split by feature
    - layer-based: split by layer (UI, API, DB)
    - file-based: split by file
    - test-driven: write tests first, then code
    - vertical-slice: each slice = full-stack working increment
    - spike-then-execute: research first, then implement
    """
    
    def decompose(self, task: Task, strategy: str = "auto",
                  project_context: Dict = None) -> List[SubTask]:
        """Decompose a task into sub-tasks"""
        
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
        """Suggest a suitable strategy based on task characteristics"""
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
        """Split by feature — full workflow"""
        subtasks = []
        
        subtasks.append(SubTask(
            id=f"{task.id}-01",
            title="Analyze requirements",
            description=f"Read and understand the requirements: {task.description}",
            order=1,
            estimated_tokens=500,
            verification_criteria="Clear list of requirements",
        ))
        
        subtasks.append(SubTask(
            id=f"{task.id}-02",
            title="Read current code",
            description="Review related codebase to understand context",
            order=2,
            dependencies=[f"{task.id}-01"],
            estimated_tokens=1500,
            verification_criteria="Identified affected files and patterns",
        ))
        
        subtasks.append(SubTask(
            id=f"{task.id}-03",
            title="Plan changes",
            description="Identify files to change and the approach",
            order=3,
            dependencies=[f"{task.id}-02"],
            estimated_tokens=800,
            verification_criteria="Concrete plan with file list and approach",
        ))
        
        subtasks.append(SubTask(
            id=f"{task.id}-04",
            title="Implement code",
            description="Write code according to the plan",
            order=4,
            dependencies=[f"{task.id}-03"],
            estimated_tokens=task.estimated_tokens or 3000,
            verification_criteria="Code written, no syntax errors",
        ))
        
        subtasks.append(SubTask(
            id=f"{task.id}-05",
            title="Check & validate",
            description="Run tests, lint, review results",
            order=5,
            dependencies=[f"{task.id}-04"],
            estimated_tokens=1000,
            verification_criteria="Tests pass, lint clean, no regressions",
        ))
        
        return subtasks
    
    def _decompose_by_layer(self, task: Task) -> List[SubTask]:
        """Split by layer: DB → Service → API → UI"""
        return [
            SubTask(f"{task.id}-db", "Database layer",
                    "Change schema, queries, migrations", 1,
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
        """Split by file — each file is 1 sub-task"""
        subtasks = []
        for i, filepath in enumerate(task.files_involved, 1):
            subtasks.append(SubTask(
                id=f"{task.id}-f{i:02d}",
                title=f"Modify {filepath}",
                description=f"Modify file {filepath}",
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
            SubTask(f"{task.id}-test-design", "Design test cases",
                    "Write test cases based on requirements", 1,
                    estimated_tokens=1000,
                    verification_criteria="Test cases cover all scenarios"),
            SubTask(f"{task.id}-test-write", "Write tests",
                    "Write test code (will fail at first)", 2,
                    dependencies=[f"{task.id}-test-design"],
                    estimated_tokens=1500,
                    verification_criteria="Tests compile, run, and fail (RED)"),
            SubTask(f"{task.id}-impl", "Implement code",
                    "Write code to pass the tests", 3,
                    dependencies=[f"{task.id}-test-write"],
                    estimated_tokens=task.estimated_tokens or 2000,
                    verification_criteria="All tests pass (GREEN)"),
            SubTask(f"{task.id}-refactor", "Refactor",
                    "Improve code quality", 4,
                    dependencies=[f"{task.id}-impl"],
                    estimated_tokens=1000,
                    verification_criteria="Code clean, tests still pass"),
        ]
    
    def _decompose_vertical_slice(self, task: Task) -> List[SubTask]:
        """Vertical slice — each slice = full-stack working feature"""
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
        """Spike-then-execute — research before implementing"""
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
