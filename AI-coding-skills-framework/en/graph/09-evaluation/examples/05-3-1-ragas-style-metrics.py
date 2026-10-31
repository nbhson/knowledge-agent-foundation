import requests

OLLAMA_URL = "http://localhost:11434"

FAITHFULNESS_PROMPT = """Evaluate whether the answer is faithful to the context.

Context:
{context}

Answer:
{answer}

Task: Split the answer into claims (individual facts),
and assess whether each claim is supported by the context.

Return JSON:
{{"claims": [{{"claim": "...", "supported": true/false, "reason": "..."}}],
  "faithfulness": 0.0-1.0}}

faithfulness = number of supported claims / total claims
"""

def evaluate_faithfulness(context: str, answer: str, model: str = "gemma3:12b") -> Dict:
    prompt = FAITHFULNESS_PROMPT.format(context=context, answer=answer)
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": model, "prompt": prompt, "stream": False, "format": "json"
    })
    import json
    try:
        result = json.loads(resp.json()["response"])
        # Compute the hallucination rate
        result["hallucination_rate"] = 1.0 - result.get("faithfulness", 0)
        return result
    except:
        return {"faithfulness": 0.0, "hallucination_rate": 1.0, "claims": []}

# Usage
context = "The Phoenix project has a budget of 500 million, approved by Nguyen Van A. The AI team has 10 people."
answer_good = "Phoenix's budget is 500 million, approved by Nguyen Van A."
answer_bad = "Phoenix's budget is 700 million, approved by Tran Thi B. The AI team has 15 people."

print(evaluate_faithfulness(context, answer_good))
# {"faithfulness": 1.0, "hallucination_rate": 0.0, ...}

print(evaluate_faithfulness(context, answer_bad))
# {"faithfulness": 0.0, "hallucination_rate": 1.0, "claims": [
#   {"claim": "Phoenix's budget is 700 million", "supported": false},
#   {"claim": "Tran Thi B approved Phoenix", "supported": false},
# ]}

# Graph-specific: citation accuracy
def evaluate_citation_accuracy(answer: str, cited_paths: List[List[str]], 
                                graph: "nx.Graph") -> Dict:
    """Check that citations (paths) exist in the graph."""
    valid = 0
    for path in cited_paths:
        # Check whether the path exists in the graph
        is_valid = True
        for i in range(len(path) - 1):
            if not graph.has_edge(path[i], path[i+1]):
                is_valid = False
                break
        if is_valid:
            valid += 1
    
    return {
        "total_citations": len(cited_paths),
        "valid_citations": valid,
        "citation_accuracy": valid / len(cited_paths) if cited_paths else 0,
    }
