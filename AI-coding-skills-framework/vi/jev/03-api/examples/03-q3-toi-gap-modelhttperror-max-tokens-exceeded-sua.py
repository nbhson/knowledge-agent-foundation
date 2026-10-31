core = f"{ticket['subject']}\n{ticket['body'][:1500]}"   # cắt trước khi gửi
resp = client.ask(model="jev-1.13.0", state=core, questions=questions)
