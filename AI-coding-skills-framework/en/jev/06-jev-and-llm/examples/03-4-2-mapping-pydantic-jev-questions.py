# Pydantic AI: TypeSafeModel (Jev) + FallbackModel (LLM)
# pip install pydantic-ai typesafe  (names illustrative)

from enum import Enum
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.typesafe import TypeSafeModel
from pydantic_ai.models.fallback import FallbackModel


class Action(str, Enum):
    """Which workflow step should run next?"""
    REFETCH = Field(description="Re-fetch the missing data")
    RETRY = Field(description="Retry the failed operation")
    ESCALATE = Field(description="Escalate to a human")


# Jev path: output_type → questions; docstring → framing
jev_model = TypeSafeModel(
    'jev-latest',
    # default typesafe_tool_call_threshold=0.6 — retune from YOUR labels
)

# LLM path: handles steps Jev cannot (anything proposing arg-taking tools)
llm_model = FallbackModel('gpt-class-model', 'claude-class-model')

agent = Agent(FallbackModel(jev_model, llm_model))


@agent.tool_plain          # NO-ARG tool → called directly on Jev's pick
def escalate() -> str:
    return create_escalation_ticket()


@agent.tool                 # tool WITH args → ToolCallProposed (ModelAPIError)
def retry(operation_id: str, reason: str) -> str:
    return retry_operation(operation_id, reason)


# Flow in practice:
# 1. Jev evaluates questions in parallel; if the pick maps to a no-arg tool
#    above threshold → tool runs immediately (fast, typed, cheap).
# 2. If the step needs an arg-taking tool → ToolCallProposed ModelAPIError
#    → FallbackModel (LLM) takes over THE WHOLE STEP — it decides and writes args.
# 3. Never drop the fallback: Jev can be confidently wrong in-schema (see 04/07).
