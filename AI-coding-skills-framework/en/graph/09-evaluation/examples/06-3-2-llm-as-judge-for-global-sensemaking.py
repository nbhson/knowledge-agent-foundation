JUDGE_PROMPT = """Compare two answers to the same question. Evaluate on 4 criteria:

Question: {question}

Answer A: {answer_a}
Answer B: {answer_b}

Evaluate (0-10 scale for each criterion):
1. Comprehensiveness: does it cover the aspects fully?
2. Diversity: does it offer diverse perspectives?
3. Empowerment: does it help the reader understand and act?
4. Directness: does it answer the question directly?

Return JSON:
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
