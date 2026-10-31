resp = requests.post("http://localhost:11434/api/generate",
    json={"model":"gemma3:12b","prompt":prompt,"format":"json"})
result["hallucination_rate"] = 1.0 - result.get("faithfulness", 0)
# claims: [{"claim":"Phoenix ngân sách 700 triệu","supported":false}, ...]
