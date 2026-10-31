# before spawning
if file_has_owner:
    queue_for_next_run     # no parallel spawn
    return
assign_owner(file, agent_id)
spawn(agent_id)
