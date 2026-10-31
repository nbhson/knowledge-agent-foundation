# Pseudocode — Think-on-Graph
def Think_on_Graph(question: str, graph):
    entities = find_entities(question, graph)          # Bước 1: tìm nodes liên quan
    best_reasoning_path = None
    
    for _ in range(max_depth):                         # BFS style
        neighbors = get_neighbors(entities, graph)     # Lấy các neighbors tiềm năng
        reasoning_paths = llm(f"""
            Câu hỏi: {question}
            Đang ở: {entities}
            Các bước tiếp theo có thể thực hiện: {neighbors}
            Chọn 1 hướng đi hợp lý nhất.""")
        # LLM tự quyết định: đây là LLM làm planner
        entities = advance(reasoning_paths)            # Di chuyển đến nodes tiếp
        if is_answer(entities): 
            return llm(f"Tóm tắt: {reasoning_path}")  # LLM tổng hợp từ bằng chứng
    
    return "Không tìm được"
