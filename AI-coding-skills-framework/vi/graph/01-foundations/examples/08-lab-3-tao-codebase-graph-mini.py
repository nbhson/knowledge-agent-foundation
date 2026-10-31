# Graph cho codebase: File → Function → Calls
G_code = nx.DiGraph()
G_code.add_node("main.py", type="File")
G_code.add_node("handlePayment", type="Function", file="main.py")
G_code.add_node("validateCard", type="Function", file="utils.py")
G_code.add_edges_from([
    ("main.py", "handlePayment", {"type": "DEFINES"}),
    ("handlePayment", "validateCard", {"type": "CALLS"}),
])

# Truy vấn: hàm nào gọi validateCard?
callers = list(G_code.predecessors("validateCard"))
print(f"Callers of validateCard: {callers}")
