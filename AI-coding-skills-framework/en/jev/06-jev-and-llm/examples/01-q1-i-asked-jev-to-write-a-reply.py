if task_needs_text(task):                 # "draft", "summarize", "explain"
    return call_llm(task)                 # only the LLM produces language
verdict = jev.ask(state, questions=q)     # typed, 70-500 ms
return code_acts(verdict)                 # code executes, never Jev
