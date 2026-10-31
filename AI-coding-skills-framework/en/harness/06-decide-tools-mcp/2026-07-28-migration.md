# MCP 2026-07-28: no more "remembering faces", now stateless

> Addendum to `README.md` §3 and §17.3.
> Latest spec: `2026-07-28` (final Jul-28-2026). Older ones you may meet: `2025-06-18`, `2025-11-25`.
> Source: https://modelcontextprotocol.io/specification/latest

## The short version

MCP used to work like a cafe that remembers regulars: the client said hello once
(`initialize`), the server opened a session and remembered you via the `Mcp-Session-Id`
header. Every later request relied on that memory. Hard to scale: follow-up requests
had to land on the same server (sticky), and if that server died, the memory died too.

`2026-07-28` switches to "every order slip is complete": each request carries its own
version + client capabilities in `_meta`. Any server instance can handle any request —
no prior memory needed. Easier to scale horizontally, easier behind a load balancer,
and the model reasons better over multi-step flows because state is visible
in the request instead of hidden on the server.

## Before and after in one table

| Before (stateful, up to `2025-11-25`) | Now (`2026-07-28`, stateless) |
|---|---|
| `initialize` handshake before anything | Gone. Each request declares itself, just do it |
| Server remembers you via `Mcp-Session-Id`, needs sticky | Gone. Requests are independent, any server works |
| `tools/list` differs per connection | Responses state `ttlMs` (how long to cache) + `cacheScope` (safe to share?) — just follow that |
| No routing headers | POST must include `Mcp-Method` + `Mcp-Name`. Header/body mismatch = rejected, so gateways can route without opening the body |
| SSE resume via `Last-Event-ID` | Removed from Streamable HTTP |
| Tasks in core | Moved to extension `io.modelcontextprotocol/tasks`, opt in when needed |
| Free-form `result` | Must say `resultType: "complete"` (done) or `"input_required"` (needs another round). Old servers without the field mean `"complete"` |
| "Resource not found" was `-32002` | Now `-32602 (Invalid Params)` per JSON-RPC. Old code hardcoding `-32002` will miss |
| No trace convention | Standard W3C keys in `_meta`: `traceparent`, `tracestate`, `baggage` — plugs into OpenTelemetry |
| Version negotiated once at hello | Negotiated per request: `_meta["io.modelcontextprotocol/protocolVersion"]` + `MCP-Protocol-Version` header. Wrong version gets `UnsupportedProtocolVersionError` with the list the server supports |

## How to talk to a server now

Fastest: ask `server/discover` first — every spec-compliant server MUST support it.
It answers in one pack: which versions I support, what I can do, who I am.
Then call with confidence.

Lazy way also works: just send the request; on version error read the
`UnsupportedProtocolVersionError` list and retry. Keep a fallback path for old
handshake-style servers (`2025-11-25`), and stop hardcoding `-32002`.

## Production rules, in plain words

1. **Version per request, not per connection.** Cache `tools/list` per the
   `ttlMs/cacheScope` the server returns (fallback 5–15 min when absent).
   On `426`, unknown tool, or version error, drop the cache immediately.
2. **Always send 3 headers:** `MCP-Protocol-Version`, `Mcp-Method`, `Mcp-Name`.
   Param-derived custom headers go under `x-mcp-header-*`.
3. **Need memory across calls? Pass a ticket explicitly:** the server mints a handle
   and the client sends it back as an ordinary argument (SEP-2567).
   Never rely on "the server remembers".
4. **Do auth properly:** OAuth as Resource Server + metadata, Resource Indicators
   (RFC 8707), validate `iss` (RFC 9207). Rotate keys, redact `Bearer` in logs.
5. **Old limits stay:** `timeout 30s`, `result ≤128KB`, `args ≤32KB`,
   validate args before sending. For streaming, forward chunks as they arrive,
   enforce total cap + 10s idle timeout, stop on client cancel.
6. **Trace end to end:** carry `traceparent/tracestate/baggage` in `_meta`
   so gateways and backends join the same OpenTelemetry trace.

## Patching the §17.3 client

Old code POSTed to `${url}/tools/call` with `v = "2025-06-18"`.
Now POST straight to the MCP endpoint with `v = "2026-07-28"`,
the 3 new headers, and `_meta` in the JSON-RPC body:

> 📄 **Example code:** [`examples/01-patching-the-17-3-client.ts`](examples/01-patching-the-17-3-client.ts)

Keep a `"2025-06-18"` fallback branch for old servers.

## Checklist before calling it done

- [ ] Probed `server/discover` or handle version-error retry
- [ ] Nothing left depending on `Mcp-Session-Id` / `initialize`
- [ ] `-32002` handler moved to `-32602`
- [ ] Tasks behind the extension gate, no longer called as core
- [ ] `_meta` trace flows through gateways
