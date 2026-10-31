# when an agent writes
if current_version != version_the_agent_read:
    return "STALE — re-read and merge, do not overwrite"
write_file()
