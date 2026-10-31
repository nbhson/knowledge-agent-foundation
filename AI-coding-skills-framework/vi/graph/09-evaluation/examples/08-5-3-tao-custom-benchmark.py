# Tạo benchmark từ chính documents của bạn

def create_custom_benchmark(documents: List[str], num_questions: int = 20) -> List[Dict]:
    """
    Tự động tạo benchmark: dùng LLM sinh câu hỏi + đáp án từ documents.
    Cần human review sau đó!
    """
    questions = []
    for doc in documents[:num_questions]:
        prompt = f"""Từ tài liệu sau, tạo 1 câu hỏi và đáp án.

Tài liệu: {doc[:1000]}

Trả về JSON:
{{"question": "...", "answer": "...", "relevant_docs": ["..."], "type": "factoid/multi-hop/global"}}

Câu hỏi nên đa dạng: factoid, multi-hop, global.
"""
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": "gemma3:12b", "prompt": prompt, "stream": False, "format": "json"
        })
        import json
        try:
            q = json.loads(resp.json()["response"])
            q["source_doc"] = doc[:200]
            questions.append(q)
        except:
            continue
    return questions
