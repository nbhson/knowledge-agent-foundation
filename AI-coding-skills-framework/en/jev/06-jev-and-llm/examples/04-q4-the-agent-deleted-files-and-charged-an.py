p_yes = jev_noul(state, "does the user authorize this?")   # typed yes/no
if p_yes >= 0.80:
    execute(tool, args)
else:
    return {"allow": False, "next": "request_approval"}
