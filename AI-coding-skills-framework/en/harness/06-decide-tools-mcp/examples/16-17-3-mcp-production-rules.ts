const memo = new Map<string, { at: number; val: any }>();
export async function callMcp(url: string, token: string, tool: string, args: object, v = "2026-07-28") { // compat: "2025-06-18"; see 2026-07-28-migration.md
  const key = `${tool}:${JSON.stringify(args)}`; const m = memo.get(key);
  if (m && Date.now() - m.at < 60_000) return { ...m.val, memoHit: true };
  const r = await fetch(`${url}/tools/call`, { method: "POST", signal: AbortSignal.timeout(30_000),
    headers: { authorization: `Bearer ${token}`, "mcp-protocol-version": v, "content-type": "application/json" },
    body: JSON.stringify({ name: tool, arguments: args }) });
  if (r.status === 426) throw new Error("MCP version mismatch: refresh tools/list + capability cache");
  const j: any = await r.json(); let text = JSON.stringify(j.content ?? j).slice(0, 128_000);
  if (JSON.stringify(j).length > 128_000) text += "\n…[truncated: result cap 128k]";
  const out = { ok: !j.isError, text }; memo.set(key, { at: Date.now(), val: out }); return out;
}
