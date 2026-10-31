JUDGE_PROMPT = """So sánh 2 câu trả lời cho cùng câu hỏi. Đánh giá theo 4 tiêu chí:

Câu hỏi: {question}

Câu trả lời A: {answer_a}
Câu trả lời B: {answer_b}

Đánh giá (thang 0-10 cho mỗi tiêu chí):
1. Comprehensiveness: bao quát đầy đủ khía cạnh?
2. Diversity: đa dạng góc nhìn?
3. Empowerment: giúp người đọc hiểu và hành động?
4. Directness: trả lời trực tiếp câu hỏi?

Trả về JSON:
{{"comprehensiveness": {{"A": 7, "B": 8, "winner": "B"}},
  "diversity": {{"A": 6, "B": 9, "winner": "B"}},
  ...,
  "overall_winner": "B"}}
"""

def llm_judge(question: str, answer_a: str, answer_b: str, model: str = "gemma3:12b") -> Dict:
    prompt = JUDGE_PROMPT.format(question=question, answer_a=answer_a, answer_b=answer_b)
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": model, "prompt": prompt, "stream": False, "format": "json"
    })
    import json
    try:
        return json.loads(resp.json()["response"])
    except:
        return {"overall_winner": "unknown"}
