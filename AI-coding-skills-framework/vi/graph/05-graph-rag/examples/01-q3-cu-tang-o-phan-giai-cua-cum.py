comms = detect_communities(G, resolution=1.0)   # thử 0.5 / 1.0 / 2.0
for cid, members in comms.items():
    print(cid, len(members), members[:5])          # tên node đầu để đoán chủ đề
