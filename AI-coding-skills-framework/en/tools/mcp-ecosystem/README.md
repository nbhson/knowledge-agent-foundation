# 🔌 MCP Ecosystem — The Protocol Connecting AI ↔ Tools

> ## 📑 Table of Contents
>
> - [The Opening Story](#the-opening-story)
> - [Why MCP Matters?](#why-mcp-matters)
> - [Relationship to the Harness](#relationship-to-the-harness)
> - [Overview](#overview)
> - [Learning Roadmap (Directory Structure)](#learning-roadmap-directory-structure)
> - [Real-World Case Studies](#real-world-case-studies)
> - [Reference Materials](#reference-materials)

---

### The Opening Story

This section explains why MCP exists, using a pain you have probably felt: wiring one AI app to one tool at a time.

`harness/06-decide-tools-mcp` (the module that teaches **which tool to pick**) answers one half of the problem — but the next question is *"how do I plug it into my harness?"*

Before MCP, every AI app had to build its own link for each tool: one connector for GitHub, one for the database, one for files... The same work was repeated again and again, each time a little different.

> *"MCP is the USB-C of AI tools — one standard, every device."*

**MCP (Model Context Protocol)** — the open standard from Anthropic (think "USB-C port", but for AI ↔ tools) — sets one common way for AI apps to reach outside tools and data. Instead of writing many one-off links, you write **one server**, and **every MCP-friendly client** (Cline, Claude, VS Code... — the apps that call those tools) can use it.

> **One-line summary:** MCP replaces "one hand-made cable per tool per app" with a single standard plug everyone shares.

### Why MCP Matters?

This table gives the four concrete reasons MCP pays off in this repo. How to read it: column # is just the row number; **Reason** names the benefit; **Explanation** says in plain words what that benefit means. For instance, row 1 means "one shared language (JSON-RPC) instead of many private ones".

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Standardization** | One shared protocol (JSON-RPC — a simple "send a request, get a response" message format) for all tools and data — no more scattered hand-made links |
| 2 | **Seamless scaling** | A new tool is just a new MCP server — the harness/06 list can add it easily |
| 3 | **Already in the repo** | `MCP_SETUP.md` already sets up the GitHub MCP server — ready to try |
| 4 | **Harness/06 is the "brain"** | `harness/06` picks *which tool to use* — MCP is the *wiring* that runs that choice |

> **One-line summary:** One protocol means new tools plug in cheaply, and this repo already has a working example to copy.

### Relationship to the Harness

This section shows where MCP sits inside the repo's own pieces — read the two boxes as "who decides" and "who executes".

```
┌──────────────────────────────────────────────────────────────┐
│  MCP ECOSYSTEM MAP VS HARNESS COMPONENTS                     │
│                                                              │
│  harness/06-decide-tools-mcp → decides which MCP to use      │
│  harness/06 tool registry   → register tools from MCP servers│
│  MCP_SETUP.md (instruction/)    → GitHub MCP server config      │
│  mcp-ecosystem/ (here)       → protocol overview + build     │
└──────────────────────────────────────────────────────────────┘
```

```
Harness Tool Pipeline (harness/06):
  User Query → Intent → Tool Selector → pick from the registry
      ↓
  Registry holds tools from 2 sources:
    ├─ Built-in tools   (file I/O, execute, search...)
    └─ MCP servers      (GitHub MCP, vector-db MCP, custom MCP...)
      → Tool Executor → Result Processor
```

In plain words: the **registry** is a contact list of available tools; the **selector** picks one from that list; the **executor** actually calls it. MCP servers simply add more entries to that contact list.

> **One-line summary:** harness/06 decides *which* tool to use; MCP is the standard wiring that lets the choice actually run.

## Overview

### What Is MCP?

This subsection defines the four words you will see everywhere in MCP docs. How to read the table: **Concept** is the term, **Role** is what it does — for instance, the *MCP Server* is the "shop" offering tools, and the *MCP Client* is the "customer" calling them.

**Model Context Protocol** — an open standard that lets AI apps reach outside tools and data in the same way:

| Concept | Role |
|---------|------|
| **MCP Server** | Offers tools + resources (for example, the GitHub MCP server) |
| **MCP Client** | The AI app that uses them (Cline, Claude Desktop, VS Code...) |
| **Tools** | Actions the server can run — the agent calls them like functions |
| **Resources** | Data the server shares — background info for the agent |

> **One-line summary:** A server *offers* actions and data; a client (your AI app) *calls* them — all over one shared protocol.

### GitHub MCP Server (from MCP_SETUP.md)

This subsection points at a server you can try today, already configured in this repo.

This repo already sets up the GitHub MCP server in `MCP_SETUP.md`:

> 📄 **Example code:** [`examples/01-github-mcp-server-from-mcp-setup-md.json`](examples/01-github-mcp-server-from-mcp-setup-md.json)

**Capabilities**: manage repos, issues and PRs, GitHub Actions, code security, projects, discussions, gists, notifications... (in short: almost anything you can do on github.com, the agent can do through this server).

```text
Examples:
  "List my open pull requests"              → pull_request_read
  "Create an issue with title 'Bug: ...'"   → issue_write
  "Search Python repos about ML"            → search_repositories
```

> **One-line summary:** The GitHub MCP server is already wired up here — say what you want in plain English and it maps to a tool call.

### Quickly Adding Another MCP Server

This subsection links to a ready-made config snippet for plugging in one more server.

> 📄 **Example code:** [`examples/02-quickly-adding-another-mcp-server.json`](examples/02-quickly-adding-another-mcp-server.json)

> **One-line summary:** Adding a tool = adding one config entry, not writing a new integration.

## Learning Roadmap (Directory Structure)

This section maps the folder layout to a study order, so you know what to read next.

```
mcp-ecosystem/
├── README.md            ← YOU ARE HERE — overview + roadmap
├── 01-concepts/         ← (TODO) Protocol, server/client, tools/resources, JSON-RPC
├── 02-setup/            ← (TODO) Configuring more MCP servers, auth, scopes
├── 03-patterns/         ← (TODO) Tool registry + MCP adapter, mixing built-in/MCP
├── 04-savings/          ← (TODO) Less integration code, shareable tools
└── 05-troubleshooting/  ← (TODO) Auth failures, server timeout, tool name conflicts
```

### Recommended Roadmap

The five steps below go from "use what exists" to "build your own" — do them in order.

```
Step 1: Read harness/06-decide-tools-mcp — understand the tool registry & decisions
   ↓
Step 2: Read MCP_SETUP.md — try the existing GitHub MCP server
   ↓
Step 3: Understand the protocol concepts (server, client, tools, resources)
   ↓
Step 4: Configure another MCP server for vector-db / a custom tool (02-setup)
   ↓
Step 5: Build your own MCP server for an internal tool (03-patterns)
```

How to read this table: the left column is a goal you might have; the right column is the doc that serves it. For instance, "Decide which tool to use" is covered by the harness/06 module.

| If you want to... | Read |
|-------------------|------|
| Decide which tool to use | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Configure the GitHub MCP server | [MCP_SETUP.md](../../../../instruction/MCP_SETUP.md) |
| Tools registry & guardrails | [tools/guardrails](../guardrails/) |
| Vector DBs over MCP | [tools/vector-db](../vector-db/) |
| Build a harness with MCP tools | [tools/langchain](../langchain/) |

> **One-line summary:** Start by *using* the pre-configured GitHub server; only study the protocol deeply when you build your own server.

## Real-World Case Studies

### 1. GitHub MCP Inside a Harness Loop

This case shows MCP tools working inside a repeating loop — here, automatically sorting incoming issues.

```
Loop "issue-triage" (from loop/02-patterns):
  → MCP tool: list_issues        (read open issues)
  → MCP tool: issue_read         (read details)
  → LLM classifies severity/label
  → MCP tool: issue_write        (assign label, assignee)
  → MCP tool: add_issue_comment  (notify)
```

> **One-line summary:** A triage loop reads issues, classifies them, and writes labels back — all through MCP tools.

### 2. Registry Mixing Built-in + MCP

This case shows built-in tools and MCP tools living side by side in one registry, so guardrails treat them the same.

> 📄 **Example code:** [`examples/03-2-registry-mixing-built-in-mcp.py`](examples/03-2-registry-mixing-built-in-mcp.py)

> **One-line summary:** MCP tools join the same registry as built-in tools — one list, one set of rules.

## Reference Materials

This section collects the official links, plus pointers to related docs in this repo.

- **MCP Protocol**: https://modelcontextprotocol.io
- **MCP Spec (GitHub)**: https://github.com/modelcontextprotocol
- **GitHub MCP Server**: https://github.com/github/github-mcp-server
- **Cline MCP Docs**: https://docs.cline.bot/features/mcp

### Links to Other Branches

- [MCP_SETUP.md](../../../../instruction/MCP_SETUP.md) — GitHub MCP server configuration (instruction/)
- [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) — Tool decision & registry
- [tools/guardrails](../guardrails/) — Safe tool calls from MCP
- [tools/vector-db](../vector-db/) — Connecting a vector DB as an MCP resource
- [tools/loop-cli](../loop-cli/) — Scaffolding loops that use MCP tools

> **One-line summary:** The official MCP docs plus this repo's related modules — everything you need to go deeper.

---

> **"MCP turns tools from hardcoded integrations into pluggable capabilities."**

---

## ⚠️ Update 10/2026: MCP Spec 2026-07-28

This section lists what changed in the newest MCP specification, so old guides do not mislead you. "Transport" here just means *how messages travel* between client and server.

Latest MCP spec (2026-07-28) has major changes:

- **Streamable HTTP replaces SSE:** HTTP+SSE (2024-11-05) deprecated. Streamable HTTP is now the standard transport — stateless, request/response over HTTP POST. (SSE = Server-Sent Events, the old one-way streaming channel.)
- **Stateless (handshake removed):** No more `initialize`/`notifications/initialized` handshake. Servers no longer maintain sessions. (Stateless = the server forgets you between requests, like a vending machine.)
- **Protocol version header required:** Every HTTP request must include `MCP-Protocol-Version: 2026-07-28`.
- **Elicitation:** Clients can embed user input requests inside tool calls — i.e., the agent can pause and ask the human a question mid-task.
- **Sampling:** Servers can request the client to generate an LLM response (server-side sampling) — the server borrows the client's model.
- **Registry spec:** MCP server discovery via a centralized registry — one public catalog instead of hunting for server URLs.

Ref: https://modelcontextprotocol.io/specification/2026-07-28/

> **One-line summary:** The 2026 spec makes MCP simpler and stateless — plain HTTP POST, no handshake, a required version header, plus new elicitation/sampling/registry features.

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — MCP Ecosystem*
