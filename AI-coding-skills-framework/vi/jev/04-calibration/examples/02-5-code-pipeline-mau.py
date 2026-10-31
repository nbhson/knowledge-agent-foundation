import requests
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

API = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-1.13.0"  # alias: jev-latest
HEADERS = {"Authorization": "Bearer <YOUR_KEY>", "Content-Type": "application/json"}


class Band(Enum):
    HIGH = "high"        # auto-act
    MEDIUM = "medium"    # confirm / more context
    LOW = "low"          # escalate to human / LLM


@dataclass
class Decision:
    question: str
    selected: Any
    probabilities: Dict[str, float]
    confidence: float
    band: Band
    request_id: Optional[str]
    model_version: str


def noul_confidence(p_yes: float) -> float:
    """Noul confidence = margin từ 0.5."""
    return abs(p_yes - 0.5) * 2


def classify_band(confidence: float, high_t: float, low_t: float) -> Band:
    if confidence >= high_t:
        return Band.HIGH
    if confidence >= low_t:
        return Band.MEDIUM
    return Band.LOW


def ask_jev(state: str, questions: dict) -> dict:
    resp = requests.post(
        API,
        headers=HEADERS,
        json={"model": MODEL, "state": state, "questions": questions},
        timeout=5,
    )
    resp.raise_for_status()
    return resp.json()


def decide_with_bands(
    state: str,
    questions: dict,
    thresholds: Dict[str, tuple] = None,
) -> list[Decision]:
    """
    thresholds: {question_name: (low_t, high_t)} — per-question.
    Mặc định: low=0.5, high=0.8 (guidance, tune từ labelled data).
    """
    thresholds = thresholds or {}
    payload = ask_jev(state, questions)
    request_id = payload.get("request_id")
    decisions = []

    for name, ans in payload.get("answers", {}).items():
        low_t, high_t = thresholds.get(name, (0.5, 0.8))

        if ans.get("type") == "noul" or "p_yes" in ans:
            # Noul: confidence = |p - 0.5| * 2
            p_yes = ans.get("p_yes", ans.get("probability_yes", 0.5))
            selected = p_yes >= 0.5
            confidence = noul_confidence(p_yes)
            probs = {"yes": p_yes, "no": 1 - p_yes}
        else:
            # Choice / Score
            probs = ans.get("probabilities", {})
            selected = ans.get("selected")
            confidence = ans.get("confidence", 0.0)

        band = classify_band(confidence, high_t, low_t)
        decisions.append(Decision(
            question=name,
            selected=selected,
            probabilities=probs,
            confidence=confidence,
            band=band,
            request_id=request_id,
            model_version=MODEL,
        ))
    return decisions


def act(state: str, questions: dict) -> None:
    for d in decide_with_bands(state, questions):
        if d.band is Band.HIGH:
            auto_act(d.selected)                 # code tự hành động
        elif d.band is Band.MEDIUM:
            confirm_with_user(d)                 # hiện cho user xác nhận
        else:
            escalate_to_human_or_llm(d)          # route sang người / LLM


# --- Ví dụ: routing ticket ---
questions = {
    "queue": {
        "type": "choice",
        "options": ["billing", "tech_support", "sales", "churn_risk"],
    },
    "priority": {
        "type": "score",
        "levels": ["p0", "p1", "p2", "p3"],
    },
}
# act(ticket_text, questions)
