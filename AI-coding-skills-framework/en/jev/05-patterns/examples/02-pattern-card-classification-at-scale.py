import asyncio
import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"
CONCURRENCY = 32
LABEL_THRESHOLD = 0.75

async def classify_one(client: httpx.AsyncClient, record: dict) -> dict:
    r = await client.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "jev-latest",
            "state": record,
            "questions": {
                "category": {
                    "type": "choice",
                    "options": ["news", "opinion", "research", "spam"],
                }
            },
        },
        timeout=10.0,
    )
    r.raise_for_status()
    cat = r.json()["results"]["category"]
    p = cat["probabilities"].get(cat["selected"], 0.0)
    return {
        "id": record.get("id"),
        "label": cat["selected"],
        "label_p": p,
        # below threshold → send to LLM or human; don't silently accept
        "needs_review": p < LABEL_THRESHOLD,
    }

async def classify_all(records: list[dict]) -> list[dict]:
    sem = asyncio.Semaphore(CONCURRENCY)
    async with httpx.AsyncClient() as client:
        async def bound(rec):
            async with sem:
                return await classify_one(client, rec)
        return await asyncio.gather(*(bound(r) for r in records))
