import ast
import math
from dataclasses import dataclass, field
from typing import Dict, List
from pathlib import Path

@dataclass
class CodeQualityReport:
    """Code quality report"""
    file_path: str
    lines_of_code: int = 0
    cyclomatic_complexity: float = 0.0
    maintainability_index: float = 0.0
    duplication_ratio: float = 0.0
    naming_score: float = 0.0
    documentation_score: float = 0.0
    overall_score: float = 0.0


class CodeQualityAnalyzer:
    """
    Analyze code quality — compute metrics automatically.
    
    Metrics:
    - Lines of Code (LOC)
    - Cyclomatic Complexity
    - Maintainability Index
    - Code Duplication
    - Naming Conventions
    - Documentation Coverage
    """
    
    def analyze(self, code: str, file_path: str = "") -> CodeQualityReport:
        report = CodeQualityReport(file_path=file_path)
        
        lines = code.strip().split("\n")
        report.lines_of_code = len(lines)
        report.cyclomatic_complexity = self._calc_complexity(code)
        report.maintainability_index = self._calc_maintainability(
            code, report.cyclomatic_complexity, report.lines_of_code
        )
        report.naming_score = self._calc_naming_score(code)
        report.documentation_score = self._calc_doc_score(code)
        
        # Overall score (weighted average)
        scores = [
            report.maintainability_index * 0.3,
            report.naming_score * 0.25,
            report.documentation_score * 0.25,
            max(0, 100 - report.cyclomatic_complexity * 10) * 0.2,
        ]
        report.overall_score = sum(scores)
        
        return report
    
    def _calc_complexity(self, code: str) -> float:
        """Compute cyclomatic complexity"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return 10.0  # High complexity for unparseable code
        
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For,
                                ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def _calc_maintainability(self, code: str, 
                               complexity: float, loc: int) -> float:
        """Compute maintainability index (0-100)"""
        if loc == 0:
            return 100.0
        
        # Simplified MI formula
        mi = 171 - 5.2 * math.log(max(loc, 1)) - 0.23 * complexity - 16.2 * math.log(max(loc, 1))
        return max(0, min(100, mi))
    
    def _calc_naming_score(self, code: str) -> float:
        """Evaluate naming conventions"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return 0.0
        
        good_names = 0
        total_names = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                total_names += 1
                if (node.name.islower() and 
                    "_" in node.name or 
                    node.name.startswith("_")):
                    good_names += 1
            elif isinstance(node, ast.ClassDef):
                total_names += 1
                if node.name[0].isupper():
                    good_names += 1
        
        return (good_names / total_names * 100) if total_names else 100.0
    
    def _calc_doc_score(self, code: str) -> float:
        """Evaluate documentation coverage"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return 0.0
        
        documented = 0
        total = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                total += 1
                if (ast.get_docstring(node)):
                    documented += 1
        
        return (documented / total * 100) if total else 100.0
