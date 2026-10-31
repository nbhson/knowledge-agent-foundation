# MCP 2026-07-28: no more "remembering faces", now stateless

> Addendum to `README.md` §3 and §17.3.
> Latest spec: `2026-07-28` (final Jul-28-2026). Older ones you may meet: `2025-06-18`, `2025-11-25`.
> Source: https://modelcontextprotocol.io/specification/latest

## The short version

This section explains what changed in the MCP protocol (MCP = Model Context Protocol, the standard way an agent talks to external tool servers) and why it matters.

MCP used to work like a cafe that remembers regulars: the client said hello once
(`initialize` = a first handshake message that opens a conversation),
the server opened a session and remembered you via the `Mcp-Session-Id` header
(header = a small label sent along with every HTTP request). Every later request relied on that memory. Hard to scale: follow-up requests
had to land on the same server (sticky), and if that server died, the memory died too.

`2026-07-28` switches to "every order slip is complete": each request carries its own
version + client capabilities in `_meta` (capabilities = the list of features your client supports). Any server instance can handle any request —
no prior memory needed. Easier to scale horizontally (horizontal scaling = adding more identical servers behind a load balancer), easier behind a load balancer,
and the model reasons better over multi-step flows because state is visible
in the request instead of hidden on the server.

> **One-line summary:** MCP dropped server-side sessions — every request now carries its own identity and capabilities, so any server can answer any request.

## Before and after in one table

How to read it: the left column is how older MCP versions (up to `2025-11-25`) behaved, the right column is what `2026-07-28` does instead. Each row is one feature. For instance, row 1 says the `initialize` handshake is no longer needed at all.

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

Plain-language glosses: `tools/list` = the call that lists a server's available tools; SSE = Server-Sent Events, a one-way streaming connection; JSON-RPC = the request/response message format MCP uses; OpenTelemetry = the standard toolkit for tracing a request across services.

> **One-line summary:** Ten behaviors moved from "the server remembers" to "each request is self-contained" — the table maps each old habit to its replacement.

## How to talk to a server now

This section gives the two practical connection strategies — a probing one and a lazy one.

Fastest: ask `server/discover` first — every spec-compliant server MUST support it.
It answers in one pack: which versions I support, what I can do, who I am.
Then call with confidence.

Lazy way also works: just send the request; on version error read the
`UnsupportedProtocolVersionError` list and retry. Keep a fallback path for old
handshake-style servers (`2025-11-25`), and stop hardcoding `-32002` (hardcoding = writing the old error number directly into your code, where it silently goes stale).

> **One-line summary:** Either probe the server with `server/discover` first, or just send and retry on a version error — either way, never assume the server remembers you.

## Production rules, in plain words

This section lists the six rules a production MCP client must follow.

1. **Version per request, not per connection.** Cache `tools/list` per the
   `ttlMs/cacheScope` the server returns (fallback 5–15 min when absent).
   On `426` (the HTTP "update required" status), unknown tool, or version error, drop the cache immediately.
2. **Always send 3 headers:** `MCP-Protocol-Version`, `Mcp-Method`, `Mcp-Name`.
   Param-derived custom headers go under `x-mcp-header-*` (headers derived from parameters, so gateways can route without reading the body).
3. **Need memory across calls? Pass a ticket explicitly:** the server mints a handle
   and the client sends it back as an ordinary argument (SEP-2567 = the spec proposal defining this).
   Never rely on "the server remembers".
4. **Do auth properly:** OAuth as Resource Server + metadata, Resource Indicators
   (RFC 8707 — a spec that binds tokens to one specific server), validate `iss` (RFC 9207 — checks who issued the token). Rotate keys, redact `Bearer` in logs (`Bearer` = the secret token value in the `Authorization` header).
5. **Old limits stay:** `timeout 30s`, `result ≤128KB`, `args ≤32KB`,
   validate args before sending. For streaming, forward chunks as they arrive,
   enforce total cap + 10s idle timeout, stop on client cancel.
6. **Trace end to end:** carry `traceparent/tracestate/baggage` in `_meta`
   so gateways and backends join the same OpenTelemetry trace (trace = the linked chain of logs for one request across many services).

> **One-line summary:** Send version + routing headers on every call, cache per the server's TTL, pass state explicitly as a ticket, and trace everything.

## Patching the §17.3 client

This section shows what code changes the old sample client needs.

Old code POSTed to `${url}/tools/call` with `v = "2025-06-18"` (POST = send an HTTP request with a body).
Now POST straight to the MCP endpoint with `v = "2026-07-28"`,
the 3 new headers, and `_meta` in the JSON-RPC body:

> 📄 **Example code:** [`examples/01-patching-the-17-3-client.ts`](examples/01-patching-the-17-3-client.ts)

Keep a `"2025-06-18"` fallback branch for old servers.

> **One-line summary:** Point the client at the MCP endpoint with the new version, the 3 headers, and `_meta` — and keep one branch for old servers.

## Checklist before calling it done

This section is the go/no-go list; every box must be ticked before you ship.

- [ ] Probed `server/discover` or handle version-error retry
- [ ] Nothing left depending on `Mcp-Session-Id` / `initialize`
- [ ] `-32002` handler moved to `-32602`
- [ ] Tasks behind the extension gate, no longer called as core
- [ ] `_meta` trace flows through gateways

> **One-line summary:** Migration is done only when no session memory, no old error code, and no missing trace headers remain.
