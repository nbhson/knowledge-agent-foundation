def compressHistory(self):
    if self.messages.length > 20:
        old = self.messages.slice(0, -10)
        return self.summarize(old)   # Goal | Decisions | Open | Repro | Next
    return "\n".join(f"{m.role}: {m.content}" for m in self.messages)
