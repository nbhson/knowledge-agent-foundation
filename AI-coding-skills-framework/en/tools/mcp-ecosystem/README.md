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

`harness/06-decide-tools-mcp` teaches you **which tool to use** — but the next question is *"how do I connect them into the harness?"*

Before MCP, every AI app had to write its own integration for each tool: one adapter for GitHub, one for the database, one for the file system... Repeated countless times, each one different.

> *"MCP is the USB-C of AI tools — one standard, every device."*

**MCP (Model Context Protocol)** — the open protocol released by Anthropic — standardizes how AI apps connect to external tools and data. Instead of writing N integrations, you write **one server**, and **every MCP-compatible client** (Cline, Claude, VS Code...) can use it.

### Why MCP Matters?

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Standardization** | One protocol (JSON-RPC) for every tool/dataset — no more scattered manual integrations |
| 2 | **Seamless scaling** | Adding a tool = adding an MCP server — the harness/06 registry easily registers new tools |
| 3 | **Already in the repo** | `MCP_SETUP.md` has the GitHub MCP server pre-configured — ready to use |
| 4 | **Harness/06 is the "brain"** | `harness/06` decides *which tool to use* — MCP is the *connection infrastructure* that executes that decision |

### Relationship to the Harness

```
┌──────────────────────────────────────────────────────────────┐
│  MCP ECOSYSTEM MAP VS HARNESS COMPONENTS                     │
│                                                              │
│  harness/06-decide-tools-mcp → decides which MCP to use      │
│  harness/06 tool registry   → register tools from MCP servers│
│  MCP_SETUP.md (repo root)    → GitHub MCP server config      │
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

## Overview

### What Is MCP?

**Model Context Protocol** — an open protocol that lets AI applications connect to external tools and data sources through a common standard:

| Concept | Role |
|---------|------|
| **MCP Server** | Provides tools + resources (e.g., the GitHub MCP server) |
| **MCP Client** | The consuming AI application (Cline, Claude Desktop, VS Code...) |
| **Tools** | Actions the server performs — the agent calls them like functions |
| **Resources** | Data the server exposes — context for the agent |

### GitHub MCP Server (from MCP_SETUP.md)

This repo already has the GitHub MCP server configured in `MCP_SETUP.md`:

```json
{
  "mcpServers": {
    "github.com/github/github-mcp-server": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**Capabilities**: manage repositories, issues & PRs, GitHub Actions, code security, projects, discussions, gists, notifications...

```text
Examples:
  "List my open pull requests"              → pull_request_read
  "Create an issue with title 'Bug: ...'"   → issue_write
  "Search Python repos about ML"            → search_repositories
```

### Quickly Adding Another MCP Server

```jsonc
// cline_mcp_settings.json — add a new server
{
  "mcpServers": {
    "github.com/github/github-mcp-server": { /* ... already there ... */ },
    "my-custom-tool": {
      "command": "npx",
      "args": ["-y", "@my-org/my-mcp-server"],
      "env": { "API_KEY": "${API_KEY}" }
    }
  }
}
```

## Learning Roadmap (Directory Structure)

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

| If you want to... | Read |
|-------------------|------|
| Decide which tool to use | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Configure the GitHub MCP server | [MCP_SETUP.md](../../../MCP_SETUP.md) |
| Tools registry & guardrails | [tools/guardrails](../guardrails/) |
| Vector DBs over MCP | [tools/vector-db](../vector-db/) |
| Build a harness with MCP tools | [tools/langchain](../langchain/) |

## Real-World Case Studies

### 1. GitHub MCP Inside a Harness Loop

```
Loop "issue-triage" (from loop/02-patterns):
  → MCP tool: list_issues        (read open issues)
  → MCP tool: issue_read         (read details)
  → LLM classifies severity/label
  → MCP tool: issue_write        (assign label, assignee)
  → MCP tool: add_issue_comment  (notify)
```

### 2. Registry Mixing Built-in + MCP

```python
registry.register(ToolDefinition(
    name="github_search_code",
    source="mcp:github",          # comes from an MCP server
    description="Search code in GitHub repos",
    parameters={"query": {"type": "string", "required": True}},
    category="search",
    requires_permission="standard",  # guardrails apply just like a normal tool
    rate_limit_per_minute=30,
))
```

## Reference Materials

- **MCP Protocol**: https://modelcontextprotocol.io
- **MCP Spec (GitHub)**: https://github.com/modelcontextprotocol
- **GitHub MCP Server**: https://github.com/github/github-mcp-server
- **Cline MCP Docs**: https://docs.cline.bot/features/mcp

### Links to Other Branches

- [MCP_SETUP.md](../../../MCP_SETUP.md) — GitHub MCP server configuration (repo root)
- [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) — Tool decision & registry
- [tools/guardrails](../guardrails/) — Safe tool calls from MCP
- [tools/vector-db](../vector-db/) — Connecting a vector DB as an MCP resource
- [tools/loop-cli](../loop-cli/) — Scaffolding loops that use MCP tools

---

> **"MCP turns tools from hardcoded integrations into pluggable capabilities."**

---

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — MCP Ecosystem*
