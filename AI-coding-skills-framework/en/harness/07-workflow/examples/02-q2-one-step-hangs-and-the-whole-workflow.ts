const deadlineAt = Date.now() + deadlineMs;            // once per run
const remain = deadlineAt - Date.now() - 500;
if (remain <= 0) throw new Error("deadline exceeded");
const out = await gate(() => s.run({ signal: AbortSignal.timeout(remain) }));
