from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime
import json

@dataclass
class EvalResult:
    run_id: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    graph_quality: Dict = field(default_factory=dict)
    retrieval_metrics: Dict = field(default_factory=dict)
    generation_metrics: Dict = field(default_factory=dict)
    kg_completion_metrics: Dict = field(default_factory=dict)
    overall_score: float = 0.0

class GraphEvaluationFramework:
    """
    A comprehensive evaluation framework for Graph Engineering.
    
    Runs: Graph Quality → Retrieval → Generation → KG Completion
    Output: JSON + Markdown report
    """
    
    def __init__(self, graph, model_name: str = "gemma3:12b"):
        self.graph = graph
        self.model_name = model_name
        self.results: List[EvalResult] = []
    
    def evaluate_graph_quality(self, ontology=None) -> Dict:
        print("  📊 Evaluating graph quality...")
        metrics = evaluate_graph_quality(self.graph, ontology)
        print(f"    Nodes: {metrics['nodes']}, Edges: {metrics['edges']}, "
              f"Connectivity: {metrics['connectivity']:.0%}, Isolated: {metrics['isolated_rate']:.0%}")
        return metrics
    
    def evaluate_retrieval(self, queries: List[Dict],
                           retrieval_fn) -> Dict:
        """
        retrieval_fn: (query: str) -> List[str] (retrieved doc_ids)
        """
        print(f"  🔍 Evaluating retrieval on {len(queries)} queries...")
        precisions, recalls, mrrs = [], [], []
        for q in queries:
            retrieved = retrieval_fn(q["query"])
            relevant = q["relevant"]
            precisions.append(precision_at_k(retrieved, relevant, 5))
            recalls.append(recall_at_k(retrieved, relevant, 5))
            mrrs.append(mrr(retrieved, relevant))
        
        import numpy as np
        return {
            "P@5": round(float(np.mean(precisions)), 3),
            "R@5": round(float(np.mean(recalls)), 3),
            "MRR": round(float(np.mean(mrrs)), 3),
            "num_queries": len(queries),
        }
    
    def evaluate_generation(self, qa_pairs: List[Dict],
                            generation_fn) -> Dict:
        """
        generation_fn: (query: str, context: str) -> str (answer)
        qa_pairs: [{"query": "...", "context": "...", "expected": "..."}, ...]
        """
        print(f"  💬 Evaluating generation on {len(qa_pairs)} QA pairs...")
        faithfulness_scores = []
        for qa in qa_pairs:
            answer = generation_fn(qa["query"], qa["context"])
            result = evaluate_faithfulness(qa["context"], answer, self.model_name)
            faithfulness_scores.append(result.get("faithfulness", 0))
        
        import numpy as np
        avg_faith = float(np.mean(faithfulness_scores)) if faithfulness_scores else 0
        return {
            "faithfulness": round(avg_faith, 3),
            "hallucination_rate": round(1 - avg_faith, 3),
            "num_qa": len(qa_pairs),
        }
    
    def run_full_evaluation(
        self, queries: List[Dict] = None,
        qa_pairs: List[Dict] = None,
        retrieval_fn=None, generation_fn=None,
        ontology=None,
    ) -> EvalResult:
        import uuid
        result = EvalResult(run_id=str(uuid.uuid4())[:8])
        
        print(f"\n{'='*60}")
        print(f"  Evaluation Run: {result.run_id}")
        print(f"{'='*60}")
        
        # 1. Graph quality
        result.graph_quality = self.evaluate_graph_quality(ontology)
        
        # 2. Retrieval
        if queries and retrieval_fn:
            result.retrieval_metrics = self.evaluate_retrieval(queries, retrieval_fn)
            print(f"    P@5: {result.retrieval_metrics['P@5']}, "
                  f"R@5: {result.retrieval_metrics['R@5']}, "
                  f"MRR: {result.retrieval_metrics['MRR']}")
        
        # 3. Generation
        if qa_pairs and generation_fn:
            result.generation_metrics = self.evaluate_generation(qa_pairs, generation_fn)
            print(f"    Faithfulness: {result.generation_metrics['faithfulness']}, "
                  f"Hallucination: {result.generation_metrics['hallucination_rate']}")
        
        # Overall score (weighted)
        gq = 1 - result.graph_quality.get("isolated_rate", 0) - result.graph_quality.get("invalid_rate", 0)
        rm = result.retrieval_metrics.get("MRR", 0)
        gm = result.generation_metrics.get("faithfulness", 0)
        # If some metrics are missing, only compute from what's available
        scores = [s for s in [gq, rm, gm] if s > 0]
        result.overall_score = round(sum(scores) / len(scores), 3) if scores else round(gq, 3)
        
        print(f"\n  ⭐ Overall Score: {result.overall_score:.3f}")
        self.results.append(result)
        return result
    
    def generate_report(self, result: EvalResult, format: str = "markdown") -> str:
        if format == "json":
            return json.dumps(result.__dict__, indent=2, ensure_ascii=False)
        
        # Markdown
        report = f"""# Graph Evaluation Report — {result.run_id}

> Generated: {result.timestamp} | Model: {self.model_name}

## Graph Quality

| Metric | Value |
|--------|-------|
| Nodes | {result.graph_quality.get('nodes', '-')} |
| Edges | {result.graph_quality.get('edges', '-')} |
| Connectivity | {result.graph_quality.get('connectivity', '-')} |
| Isolated Rate | {result.graph_quality.get('isolated_rate', '-')} |
| Invalid Edge Rate | {result.graph_quality.get('invalid_rate', '-')} |

## Retrieval

| Metric | Value |
|--------|-------|
| P@5 | {result.retrieval_metrics.get('P@5', '-')} |
| R@5 | {result.retrieval_metrics.get('R@5', '-')} |
| MRR | {result.retrieval_metrics.get('MRR', '-')} |

## Generation

| Metric | Value |
|--------|-------|
| Faithfulness | {result.generation_metrics.get('faithfulness', '-')} |
| Hallucination Rate | {result.generation_metrics.get('hallucination_rate', '-')} |

## Overall Score: {result.overall_score:.3f} / 1.0
"""
        return report

# Usage
import networkx as nx
G = nx.karate_club_graph()
G = nx.relabel_nodes(G, {n: f"n{n}" for n in G.nodes()})
for n in G.nodes():
    G.nodes[n]["type"] = "Person"

framework = GraphEvaluationFramework(G)
result = framework.run_full_evaluation()
print(framework.generate_report(result))
