const key = `${tool}:${JSON.stringify(args)}`;
const hit = memo.get(key);
if (hit && Date.now() - hit.at < 60_000) return { ...hit.val, memoHit: true };
// after the call:
if (JSON.stringify(j).length > 128_000) text += "\n…[truncated: result cap 128k]";
