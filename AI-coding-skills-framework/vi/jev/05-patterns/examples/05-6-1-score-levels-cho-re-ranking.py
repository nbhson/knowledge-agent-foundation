import requests
from typing import List

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {"Authorization": "Bearer <KEY>", "Content-Type": "application/json"}

RELEVANCE_LEVELS = ["irrelevant", "weak", "relevant", "strong"]


def score_candidate(query: str, passage: str) -> dict:
    state = f"User query:\n{query}\n\nCandidate passage:\n{passage}"
    resp = requests.post(
        API,
        headers=HEADERS,
        json={
            "model": "jev-1.13.0",
            "state": state,
            "questions": {
                "relevance": {"type": "score", "levels": RELEVANCE_LEVELS},
            },
        },
        timeout=5,
    )
    resp.raise_for_status()
    ans = resp.json()["answers"]["relevance"]
    return {
        # probability-weighted score — có thể nằm giữa 2 level
        "score": ans.get("score", ans.get("selected")),
        "confidence": ans.get("confidence", 0.0),
        "probabilities": ans.get("probabilities", {}),
    }


def rerank(query: str, passages: List[str], min_score: float = 1.5) -> List[dict]:
    scored = []
    for p in passages:                          # production: async/map-reduce
        r = score_candidate(query, p)
        r["passage"] = p
        scored.append(r)
    # Sort desc theo weighted score
    scored.sort(key=lambda r: r["score"], reverse=True)
    # Filter: dưới min_score → loại khỏi top-K
    return [r for r in scored if r["score"] >= min_score]


# VD RAG: shortlist = rerank(query, retriever.top20(query), min_score=2.0)
# → lấy 3 passage cao nhất để LLM viết câu trả lời
