// Before: v = "2025-06-18", POST `${url}/tools/call`
// After: stateless 2026-07-28
export async function callMcp(url: string, token: string, tool: string, args: object, v = "2026-07-28") {
  const r = await fetch(url, { method: "POST", signal: AbortSignal.timeout(30_000),
    headers: {
      authorization: `Bearer ${token}`,
      "content-type": "application/json",
      "MCP-Protocol-Version": v,
      "Mcp-Method": "tools/call",
      "Mcp-Name": tool,
    },
    body: JSON.stringify({ jsonrpc: "2.0", id: crypto.randomUUID(), method: "tools/call",
      params: { name: tool, arguments: args },
      _meta: { "io.modelcontextprotocol/protocolVersion": v, "io.modelcontextprotocol/clientCapabilities": {} } }) });
  if (r.status === 426) throw new Error("MCP version mismatch: call server/discover then retry");
  const j: any = await r.json();
  if (j.error?.code === "UnsupportedProtocolVersionError") throw new Error(`Unsupported protocol: ${JSON.stringify(j.error.data?.supported ?? [])}`);
  return j;
}
