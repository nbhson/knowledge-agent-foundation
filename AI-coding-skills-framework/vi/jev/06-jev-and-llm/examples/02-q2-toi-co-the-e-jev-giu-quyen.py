def gateway(context, tool, p_threshold=0.6):
    ans = decide(state=f"Context:\n{context}\nTool: {tool['name']}\nArgs: {tool.get('args', {})}",
                 questions={"authorized": {"type": "noul"}})
    p, conf = ans["p"], abs(ans["p"] - 0.5) * 2
    if p >= p_threshold and conf >= 0.5:
        return True, {"p": p, "conf": conf}     # cho chạy
    approval_request(tool, {"p": p, "conf": conf})   # lớp phân quyền thật
    return False, {"p": p, "conf": conf}
