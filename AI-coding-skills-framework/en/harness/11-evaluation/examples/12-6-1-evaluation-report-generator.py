from datetime import datetime
from typing import Dict, List

class EvaluationReporter:
    """
    Create evaluation reports — markdown, JSON, or dashboard.
    """
    
    def generate_markdown_report(self, 
                                  results: List[EvaluationResult],
                                  summary: Dict) -> str:
        """Create a Markdown report"""
        report = []
        report.append("# 📊 Evaluation Report")
        report.append(f"\n**Generated:** {datetime.now().isoformat()}")
        report.append(f"**Tasks Evaluated:** {len(results)}")
        
        # Summary
        report.append("\n## Summary\n")
        report.append("| Metric | Value |")
        report.append("|--------|-------|")
        report.append(f"| Total Tasks | {summary.get('total', 0)} |")
        report.append(f"| Success Rate | {summary.get('success_rate', 0):.1%} |")
        report.append(f"| Avg Quality Score | {summary.get('avg_quality', 0):.1f} |")
        report.append(f"| Total Tokens | {summary.get('total_tokens', 0):,} |")
        
        # Per-dimension scores
        report.append("\n## Dimension Scores\n")
        report.append("| Dimension | Avg Score | Status |")
        report.append("|-----------|-----------|--------|")
        
        for dim, score in summary.get("dimension_scores", {}).items():
            status = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"
            report.append(f"| {dim} | {score:.1f} | {status} |")
        
        # Top issues
        report.append("\n## Top Issues\n")
        for i, issue in enumerate(summary.get("top_issues", []), 1):
            report.append(f"{i}. {issue}")
        
        # Individual results
        report.append("\n## Task Results\n")
        for result in results:
            status = "✅" if result.total_score >= 70 else "❌"
            report.append(
                f"### {status} {result.task_id}\n"
            )
            report.append(f"**Score:** {result.total_score:.1f}/100\n")
            
            for dim, score in result.scores.items():
                bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))
                note = result.notes.get(dim, "")
                report.append(
                    f"- `{dim}`: {bar} {score:.0f}/100"
                    f"{f' — {note}' if note else ''}"
                )
            report.append("")
        
        return "\n".join(report)
    
    def generate_json_report(self,
                              results: List[EvaluationResult],
                              summary: Dict) -> Dict:
        """Create a JSON report"""
        return {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_tasks": len(results),
            },
            "summary": summary,
            "results": [
                {
                    "task_id": r.task_id,
                    "total_score": r.total_score,
                    "scores": r.scores,
                    "notes": r.notes,
                }
                for r in results
            ],
        }
    
    def generate_dashboard_data(self, 
                                 results: List[EvaluationResult]) -> Dict:
        """Generate data for the visual dashboard"""
        return {
            "timeline": self._build_timeline(results),
            "distribution": self._build_distribution(results),
            "heatmap": self._build_heatmap(results),
        }
    
    def _build_timeline(self, results: List) -> List:
        """Build timeline data for the chart"""
        return [
            {
                "date": r.timestamp,
                "score": r.total_score,
                "task": r.task_id,
            }
            for r in results
        ]
    
    def _build_distribution(self, results: List) -> Dict:
        """Build score distribution"""
        ranges = {
            "0-20": 0, "20-40": 0, "40-60": 0,
            "60-80": 0, "80-100": 0
        }
        
        for r in results:
            score = r.total_score
            if score < 20:
                ranges["0-20"] += 1
            elif score < 40:
                ranges["20-40"] += 1
            elif score < 60:
                ranges["40-60"] += 1
            elif score < 80:
                ranges["60-80"] += 1
            else:
                ranges["80-100"] += 1
        
        return ranges
    
    def _build_heatmap(self, results: List) -> List:
        """Build heatmap data (task x dimension)"""
        dimensions = set()
        for r in results:
            dimensions.update(r.scores.keys())
        
        heatmap = []
        for r in results:
            row = {"task": r.task_id}
            for dim in sorted(dimensions):
                row[dim] = r.scores.get(dim, 0)
            heatmap.append(row)
        
        return heatmap
