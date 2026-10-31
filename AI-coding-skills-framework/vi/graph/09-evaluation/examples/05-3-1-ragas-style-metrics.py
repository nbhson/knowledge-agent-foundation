import requests

OLLAMA_URL = "http://localhost:11434"

FAITHFULNESS_PROMPT = """Đánh giá xem câu trả lời có trung thành với context không.

Context:
{context}

Câu trả lời:
{answer}

Nhiệm vụ: Tách câu trả lời thành các claims (từng sự thật riêng lẻ), 
và đánh giá mỗi claim có được hỗ trợ bởi context không.

Trả về JSON:
{{"claims": [{{"claim": "...", "supported": true/false, "reason": "..."}}],
  "faithfulness": 0.0-1.0}}

faithfulness = số claims supported / tổng claims
"""

def evaluate_faithfulness(context: str, answer: str, model: str = "gemma3:12b") -> Dict:
    prompt = FAITHFULNESS_PROMPT.format(context=context, answer=answer)
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": model, "prompt": prompt, "stream": False, "format": "json"
    })
    import json
    try:
        result = json.loads(resp.json()["response"])
        # Tính hallucination rate
        result["hallucination_rate"] = 1.0 - result.get("faithfulness", 0)
        return result
    except:
        return {"faithfulness": 0.0, "hallucination_rate": 1.0, "claims": []}

# Usage
context = "Dự án Phoenix ngân sách 500 triệu, do Nguyễn Văn A phê duyệt. Team AI có 10 người."
answer_good = "Phoenix ngân sách 500 triệu, do Nguyễn Văn A duyệt."
answer_bad = "Phoenix ngân sách 700 triệu, do Trần Thị B duyệt. Team AI có 15 người."

print(evaluate_faithfulness(context, answer_good))
# {"faithfulness": 1.0, "hallucination_rate": 0.0, ...}

print(evaluate_faithfulness(context, answer_bad))
# {"faithfulness": 0.0, "hallucination_rate": 1.0, "claims": [
#   {"claim": "Phoenix ngân sách 700 triệu", "supported": false},
#   {"claim": "Trần Thị B duyệt Phoenix", "supported": false},
# ]}

# Graph-specific: citation accuracy
def evaluate_citation_accuracy(answer: str, cited_paths: List[List[str]], 
                                graph: "nx.Graph") -> Dict:
    """Kiểm tra citations (paths) có tồn tại trong graph không."""
    valid = 0
    for path in cited_paths:
        # Kiểm tra path có tồn tại trong graph không
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
