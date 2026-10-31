MODEL = "jev-1.13.0"   # ghim phiên bản, không dùng alias trong production
resp = client.ask(model=MODEL, state=core, questions=questions)
