from dataclasses import dataclass
from typing import Any, Dict, Literal

import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"  # alias for jev-1.13.0

# Per-question thresholds — tune from YOUR labelled data, not defaults
HIGH_THRESHOLD = 0.85
LOW_THRESHOLD = 0.60

Decision = Literal["auto_act", "confirm", "escalate"]


@dataclass
class GatedDecision:
    answer: str
    probabilities: Dict[str, float]
    confidence: float
    band: Decision
    request_id: str | None


def decide(state: Any, questions: Dict[str, Any]) -> GatedDecision:
    """One Jev call → read the distribution → pick a band."""
    resp = httpx.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": MODEL, "state": state, "questions": questions},
        timeout=5.0,
    )
    resp.raise_for_status()
    body = resp.json()
    request_id = resp.headers.get("x-request-id")

    # Choice question: selected option + full distribution + confidence
    result = body["results"]["route_ticket"]
    answer = result["selected"]
    probabilities = result["probabilities"]
    confidence = result["confidence"]

    # Confidence = distribution concentration (NOT P(correct)).
    # For calibration you ALSO compare the winner's probability to labels.
    winner_p = probabilities.get(answer, 0.0)

    if confidence >= HIGH_THRESHOLD and winner_p >= HIGH_THRESHOLD:
        band: Decision = "auto_act"
    elif confidence >= LOW_THRESHOLD:
        band = "confirm"       # clear-ish signal — human glance or more context
    else:
        band = "escalate"      # flat distribution — human / another system / LLM

    return GatedDecision(answer, probabilities, confidence, band, request_id)


def handle_ticket(ticket: Dict[str, str]) -> str:
    """Act / confirm / escalate — the three-band policy in action."""
    d = decide(
        state=ticket,  # keep state SMALL and relevant — see 07 State Hygiene
        questions={
            "route_ticket": {
                "type": "choice",
                "options": ["billing", "infra", "product", "data"],
            },
            "priority": {
                "type": "score",
                "levels": ["p0", "p1", "p2", "p3"],
            },
        },
    )

    # Never log the state (PII) — log the decision metadata only
    audit = {
        "request_id": d.request_id,
        "question": "route_ticket",
        "selected": d.answer,
        "probabilities": d.probabilities,
        "confidence": d.confidence,
        "threshold_high": HIGH_THRESHOLD,
        "threshold_low": LOW_THRESHOLD,
        "model_version": MODEL,
        "band": d.band,
    }

    if d.band == "auto_act":
        return route_to_queue(d.answer)            # code acts
    if d.band == "confirm":
        return request_human_confirmation(d.answer)  # medium band
    return escalate_with_context(audit)              # low band
