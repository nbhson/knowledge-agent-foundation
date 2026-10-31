import asyncio
from typing import Any

import httpx

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {"Authorization": "Bearer <KEY>", "Content-Type": "application/json"}
MODEL = "jev-1.13.0"

TAGS = ["bug", "feature_request", "question", "docs", "spam"]


async def classify_one(client: httpx.AsyncClient, record: dict) -> dict:
    """MAP: một record → một label + probability."""
    resp = await client.post(
        API,
        headers=HEADERS,
        json={
            "model": MODEL,
            "state": record["text"],            # state nhỏ, liên quan
            "questions": {
                "tag": {"type": "choice", "options": TAGS},
            },
        },
        timeout=5,
    )
    resp.raise_for_status()
    data = resp.json()
    ans = data["answers"]["tag"]
    return {
        "id": record["id"],
        "tag": ans["selected"],
        "p": ans.get("probabilities", {}).get(ans["selected"], 0.0),
        "confidence": ans.get("confidence", 0.0),
        "request_id": data.get("request_id"),
    }


async def classify_dataset(records: list[dict], batch: int = 50) -> list[dict]:
    """MAP song song từng batch, trả về labels đã phân loại."""
    results: list[dict] = []
    async with httpx.AsyncClient() as client:
        for i in range(0, len(records), batch):
            chunk = records[i : i + batch]
            # Async song song trong chunk — mỗi decide vẫn ~70-500ms
            results.extend(await asyncio.gather(
                *[classify_one(client, r) for r in chunk]
            ))
    return results


def reduce(results: list[dict]) -> dict:
    """REDUCE: gộp kết quả + tách bucket confidence."""
    auto, review = [], []
    for r in results:
        (auto if r["confidence"] >= 0.8 else review).append(r)
    return {
        "auto_tagged": auto,
        "needs_review": review,
        "coverage": len(auto) / max(len(results), 1),
    }


# dataset = load_records()
# summary = reduce(asyncio.run(classify_dataset(dataset)))
