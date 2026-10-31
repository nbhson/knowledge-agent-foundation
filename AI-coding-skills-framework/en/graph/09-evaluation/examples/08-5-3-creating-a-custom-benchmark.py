# Create a benchmark from your own documents

def create_custom_benchmark(documents: List[str], num_questions: int = 20) -> List[Dict]:
    """
    Automatically create a benchmark: use an LLM to generate questions + answers from the documents.
    Requires human review afterwards!
    """
    questions = []
    for doc in documents[:num_questions]:
        prompt = f"""From the document below, create 1 question and its answer.

Document: {doc[:1000]}

Return JSON:
{{"question": "...", "answer": "...", "relevant_docs": ["..."], "type": "factoid/multi-hop/global"}}

Questions should be diverse: factoid, multi-hop, global.
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
