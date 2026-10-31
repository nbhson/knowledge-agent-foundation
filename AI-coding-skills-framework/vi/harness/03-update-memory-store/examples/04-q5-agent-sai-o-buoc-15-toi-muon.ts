this.events.set(newSessionId, forkedEvents);   // tiền tố đăng ký trước
this.append({ sessionId: newSessionId, kind: "checkpoint",
              payload: { forkedFrom: { sessionId: src, atSeq: n - 1, by: "human:ui" } } });
