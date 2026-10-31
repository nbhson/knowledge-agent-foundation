questions = {f"classify_{i}": {"type": "choice", "choices": OPTIONS}
             for i in range(len(items))}
resp = client.ask(model="jev-1.13.0", state=items, questions=questions)
