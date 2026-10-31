def gate(conversation, tool_name, tool_args, p_threshold=0.6, conf_threshold=0.5):
    ans = decide(state=f"{conversation}\nTool: {tool_name}\nArgs: {tool_args}",
                 questions={"authorized": {"type": "noul"}})
    p, conf = ans["p"], abs(ans["p"] - 0.5) * 2
    if p >= p_threshold and conf >= conf_threshold:
        return True                       # cho qua
    request_human_approval(tool_name, tool_args, p, conf)   # chặn + hỏi người
    return False
