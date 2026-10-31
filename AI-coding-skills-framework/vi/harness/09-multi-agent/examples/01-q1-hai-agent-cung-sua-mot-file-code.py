# trước khi spawn
if file_đã_có_chủ:
    xếp_hàng_cho_chạy_sau   # không spawn song song
    return
gán_chủ(file, agent_id)
spawn(agent_id)
