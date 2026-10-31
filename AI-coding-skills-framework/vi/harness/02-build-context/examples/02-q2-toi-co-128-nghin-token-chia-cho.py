budget = ContextBudget(total_tokens=128000, reserve_output=4000)
budget.adjust_for_query_type("retrieval")   # retrieved_context 70%
budget.fit_text_to_budget(text, "retrieved_context")  # cắt kèm [...truncated...]
budget.report()   # in ra: retrieved_context 84,700 token (70%)
