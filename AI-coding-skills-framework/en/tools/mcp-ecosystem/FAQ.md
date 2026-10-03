# ❓ FAQ — MCP Ecosystem (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. Why do I need MCP at all — can't I just write an adapter for GitHub myself? [→ What Is MCP?]

**What you see**

You have one tool to connect: GitHub. You write a small adapter, it works, and you move on. Two months later the tool needs a second system, then a third. Every adapter looks different, each one is a private module only your app can import, and the same "list my open pull requests" logic exists in three files. You are maintaining integrations, not building a harness.

**Why**

Because MCP (Model Context Protocol, the open protocol released by Anthropic) turns **one private integration into one reusable server**. Write the server once, and every MCP-compatible client — Cline, Claude, VS Code — can use it. The README's phrase is literal: "MCP is the USB-C of AI tools — one standard, every device." Before MCP, each AI app wrote its own adapter for each tool; that work never stopped, it just moved.

| Concept | Role |
|---|---|
| **MCP Server** | provides tools and resources |
| **MCP Client** | the consuming app (Cline, Claude Desktop, VS Code) |
| **Tools** | actions the agent calls like functions |
| **Resources** | data the server exposes as context |

**What to do**

1. Write an MCP server when a tool will be used by more than one client, or by more than one app you own.
2. Skip MCP for a one-off tool with one consumer — a plain function is less machinery.
3. Keep the decision logic where it belongs: `harness/06-decide-tools-mcp` decides **which** tool to use; MCP is the connection layer that executes that decision.
4. Register MCP tools in the same registry as built-in tools so guardrails and rate limits apply unchanged.

**Verify**

Take your existing GitHub adapter and expose it as an MCP server. If two clients can both call "list my open pull requests" with no code changes in either client, the abstraction earned its place.

---

## Q2. How do I add a second MCP server without breaking the one I already have? [→ Quickly Adding Another MCP Server]

**What you see**

You copy the GitHub MCP server block into your settings and it works. You add a second entry and suddenly GitHub stops responding. You paste your new block with a trailing comma issue, or you overwrite `mcpServers` instead of adding to it, and now the whole config is one server you cannot restore.

**Why**

Because the settings file holds **one `mcpServers` object containing many servers**, and they are siblings. Adding a tool is not a new file and not a new top-level key — it is a new entry inside the same object. Two shapes are common in the wild: `"type": "http"` with a `url` (the GitHub server uses `https://api.githubcopilot.com/mcp/`), and `"command": "npx"` with `args` for a locally launched server. Mixing them in one object is fine; splitting the object is not.

**What to do**

1. Back up the settings file before every edit. It is the cheapest possible rollback.
2. Add your entry **inside** the existing `mcpServers` object, keeping the previous entries byte for byte.
3. Put secrets in the environment block, not the file: `"env": { "API_KEY": "${API_KEY}" }`.
4. Set `"disabled": false` deliberately and keep `"autoApprove": []` empty until you have seen what the server does.
5. Restart the client after each single addition, so you know which entry broke it.

```jsonc
{
  "mcpServers": {
    "github.com/github/github-mcp-server": { "type": "http", "url": "https://api.githubcopilot.com/mcp/" },
    "my-custom-tool": { "command": "npx", "args": ["-y", "@my-org/my-mcp-server"],
                        "env": { "API_KEY": "${API_KEY}" } }
  }
}
```

**Verify**

Restart the client and list available tools. The GitHub tools must still be present — a tool count that dropped means you replaced the object instead of extending it.

---

## Q3. Two servers expose a tool with the same name — which one does the agent call? [→ 2. Registry Mixing Built-in + MCP]

**What you see**

Your registry has `github_search_code` from the GitHub MCP server and a built-in `search_code` tool. Later a second MCP server ships a `search_code` too. The agent picks the wrong one, writes to a repository it should not have touched, and the log does not tell you which of the three it called — all three names look similar.

**Why**

Because the registry entry carries a **name, a source, and a permission** — and the name alone is not unique once sources multiply. The documented entry has `source="mcp:github"` to record where a tool came from, plus `requires_permission` and `rate_limit_per_minute`. Without a naming convention, two servers can publish the same tool name, and tool selection becomes a coin flip for the model.

**What to do**

1. Namespace every MCP tool by server: `github_search_code`, not `search_code`. Namespacing is your problem to solve; the protocol does not do it for you.
2. Record `source` on every registered tool so a log line always answers "which server was this".
3. Copy the guardrail fields from the sample — `category`, `requires_permission`, `rate_limit_per_minute` — so an MCP tool is no different from a built-in one.
4. Detect duplicates at registration time and fail loudly rather than letting the second entry win silently.
5. Keep `autoApprove` empty for write-capable tools; MCP servers can include actions you did not write.

**Verify**

Register two tools with the same bare name and confirm the loader rejects the duplicate. Then run one tool call and check the log contains the full namespaced name and its source.

---

## Q4. The agent wrote an issue label to the wrong repository — what should I have set up first? [→ Real-World Case Studies]

**What you see**

The issue-triage loop does exactly what the README describes: `list_issues` → `issue_read` → the model classifies severity → `issue_write` (assign label, assignee) → `add_issue_comment`. It runs in seconds and feels safe. Then you point it at a client repository and it labels sixty issues at once, because nothing constrained which repository, how many, or how fast.

**Why**

Because every step in the loop was individually permitted. `harness/06` decided correctly — issue triage needs `list_issues` then `issue_write` — and the MCP server executed faithfully. What was missing is the **blast radius**: scope (which repository), volume (how many writes), and rate (how fast). The registry entry carries `rate_limit_per_minute=30` for exactly this reason, and `requires_permission` says which guardrails apply.

**What to do**

1. Pin the target explicitly in the task and in the tool arguments — never let "the current repo" be inferred.
2. Set `rate_limit_per_minute` on every write tool and let the registry enforce it.
3. Use a dry-run mode first: read tools only, produce the labels, write nothing. Compare against what you would have done by hand.
4. Put the write tools behind an approval gate rather than in `autoApprove`.
5. Write a loop that stops after N writes and reports, so one bad run cannot become sixty changes.

**Verify**

Run triage in dry-run on 10 issues and read every proposed label yourself. If even one is wrong, fix the classification prompt before enabling writes — not after.

---

## Q5. Do I need to learn the whole protocol to use one server? [→ Recommended Roadmap]

**What you see**

You want to try the GitHub MCP server. The documentation describes JSON-RPC, server and client roles, tools and resources, and it looks like a protocol to master before you can do anything. You postpone the whole thing, keep writing private adapters, and the duplication grows.

**Why**

Because the roadmap deliberately separates "use a server" from "understand the protocol". Step 2 of the README is to read `MCP_SETUP.md` and try the GitHub server that is already configured — no protocol knowledge required. Understanding server, client, tools, and resources is step 3, and writing your own server is step 5. The protocol is one JSON-RPC standard for every tool and dataset; that is why learning it once pays off across every server you ever meet.

**What to do**

1. Do step 2 first: open `MCP_SETUP.md`, start the client, and run one read call ("List my open pull requests" → `pull_request_read`).
2. Do step 3 next, and only the parts you will meet: what a server offers, what a client asks for.
3. Add one more server from step 4 (vector database or a custom tool) before building anything.
4. Read `harness/06-decide-tools-mcp` first if you have not — the decision layer is what your servers will plug into.
5. Build your own server only when you have a tool that no existing server covers.

**Verify**

Get `pull_request_read` to return your open pull requests without writing a line of integration code. If that works, the protocol is doing its job and you have nothing left to learn before day-to-day use.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*