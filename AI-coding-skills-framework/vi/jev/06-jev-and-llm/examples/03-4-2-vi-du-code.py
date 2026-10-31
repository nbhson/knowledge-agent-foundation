# Pydantic AI + TypeSafe integration (minh hoạ kiến trúc)
from pydantic_ai import Agent
# from pydantic_ai.models.typesafe import TypeSafeModel
# from pydantic_ai.models.fallback import FallbackModel

# --- Cấu hình kiến trúc ---
# primary   = TypeSafeModel('jev-1.13.0')      # Jev decide trước
# fallback  = FallbackModel('some-llm')          # LLM nhận cả bước khi Jev kẹt
# agent     = Agent(model=primary + fallback)    # (giả định) composition
#
# typesafe_tool_call_threshold = 0.6            # mặc định — TUNE từ labelled data


# --- Tool KHÔNG args: Jev pick và gọi ---
@agent.tool_plain
def refresh_dashboard() -> str:
    """Không tham số — Jev chọn tool này (hoặc tool khác) từ danh sách,
    nếu confidence ≥ 0.6 thì gọi thẳng, KHÔNG cần LLM sinh args."""
    return render_dashboard()


# --- Tool CÓ args: Jev không sinh args được ---
@agent.tool_plain
def search_docs(query: str, top_k: int = 5) -> list[str]:
    """Có args → Jev không generate được text args.
    Flow: ToolCallProposed → ModelAPIError → FallbackModel (LLM)
    LLM (fallback) đảm nhận CẢ BƯỚC: đọc context, sinh query, gọi tool."""
    return vector_search(query, top_k)


# --- Điều chỉnh threshold từ labelled data của bạn ---
# Cao hơn → ít handoff sang LLM hơn, nhưng đúng hơn KHI handoff xảy ra.
# agent/settings.typesafe_tool_call_threshold = 0.75   # sau khi tune
