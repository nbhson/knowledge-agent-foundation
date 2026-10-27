# Agent Foundation — AI Coding Skills Framework

Repo tổng hợp **kiến thức nền tảng về AI Agent** và **bộ cấu hình agent thực chiến** để triển khai AI agent vào dự án thật. Repo gồm 3 phần độc lập nhưng liên kết logic với nhau:

| # | Thành phần | Vai trò |
|---|------------|---------|
| 1 | [`AI-coding-skills-framework/`](AI-coding-skills-framework/) | **Giáo trình lý thuyết** — 15 module về AI Agent (Retrieve Memory, Context, Workflow, Multi-Agent, Evaluation…), viết song song EN + VI |
| 2 | [`instruction/`](instruction/) | **Cấu hình triển khai** — workspace config cho AI agent (Copilot, Cline, Cursor, Gemini): workflows, skills, rules, knowledge, hooks |
| 3 | [`ollama/`](ollama/) | **AI local** — hướng dẫn chạy model local (embedding, chat) trên Mac / Windows bằng Ollama |

> **Framework (phần 1)** trả lời câu hỏi *"tại sao và làm thế nào"* — **instruction (phần 2)** là files mà agent đọc trực tiếp khi coding — **ollama (phần 3)** là nền tảng chạy model/embedding cục bộ.

---

## 📖 Mục lục

- [1. AI-coding-skills-framework — Giáo trình lý thuyết](#1-ai-coding-skills-framework--giáo-trình-lý-thuyết)
- [2. instruction — Cấu hình agent workspace](#2-instruction--cấu-hình-agent-workspace)
- [3. ollama — AI local](#3-ollama--ai-local)
- [Cập nhật 2026-07+](#-cập-nhật-2026-07)
- [Ghi chú về `.github-migration/`](#ghi-chú-về-github-migration)

---

## 1. `AI-coding-skills-framework/` — Giáo trình lý thuyết

Tài liệu học tập về kiến trúc AI Agent, viết song song 2 ngôn ngữ (`en/` và `vi/`), cấu trúc giống hệt nhau:

```
AI-coding-skills-framework/
├── en/                              ← bản tiếng Anh
├── vi/                              ← bản tiếng Việt
│   (mỗi ngôn ngữ gồm)
│   ├── AI_AGENT_FRAMEWORK.md        ← giáo trình chính: 15 modules
│   ├── AGENT_SYSTEM_ARCHITECTURE.md ← 8-layer kiến trúc agent + build checklist
│   ├── HARNESS_ENGINEERING.md       ← Harness engineering
│   ├── GRAPH_ENGINEERING.md         ← Graph / knowledge engineering
│   ├── FAQ.md
│   ├── graph/    (7 submodule)      ← Graph & knowledge engineering
│   ├── harness/  (7 submodule)      ← Agent harness
│   ├── jev/      (7 submodule)      ← Jev & System One Models (decision layer)
│   ├── loop/     (7 submodule)      ← Loop / orchestration
│   └── tools/                       ← Tools & ecosystems (langchain, crewai, autogen,
│                                       mcp-ecosystem, vector-db, guardrails, rtk,
│                                       evaluation, observability, loop-cli)
└──
```

- **Đối tượng:** developers muốn hiểu nguyên lý — mỗi module có `README.md` riêng, học tuần tự 01 → 07.
- **Ngôn ngữ:** nội dung EN/VI song song, cùng cấu trúc thư mục.

---

## 2. `instruction/` — Cấu hình agent triển khai thực tế

Bộ files mà AI agent (GitHub Copilot, Cline, Cursor, Gemini CLI…) đọc trực tiếp khi làm việc với dự án. Copy thư mục này vào bất kỳ repo nào cần agent hỗ trợ, sau đó customize `knowledge/`, `rules/`, `workflows/`.

```
instruction/
├── MCP_SETUP.md                     ← Hướng dẫn setup MCP server (GitHub MCP...)
├── .agents/                         ← Config cho general agents (Cline, Gemini...)
│   ├── AGENTS.md                    ← Orchestration workflow chính (chuẩn AGENTS.md)
│   ├── GEMINI.md                    ← Config riêng cho Gemini
│   ├── copilot-instructions.md      ← Instructions cho Copilot
│   ├── agents/                      ← Agent definitions (*.agent.md)
│   ├── hooks/                       ← 5 lifecycle hooks (phase-1 → phase-5)
│   ├── knowledge/                   ← Kiến thức dự án (bắt buộc load)
│   ├── rules/                       ← Quy tắc coding (angular, scss, coding-style...)
│   ├── scripts/                     ← Script hỗ trợ
│   ├── skills/                      ← Kỹ năng chuyên sâu (SKILL.md)
│   ├── templates/                   ← Templates cho reports & tickets
│   ├── workflows/                   ← bug-fix, feature-delivery, refactor,
│   │                                  code-review, jira-review
│   ├── report-templates/ + reports/ ← Báo cáo *.ctx.md (context memory)
│   └── ISSUE_TEMPLATE/, workflows/  ← Cấu hình GitHub
├── .github/                         ← Config cho GitHub Copilot
│   ├── copilot-instructions.md      ← Entry point của Copilot
│   ├── agents/ + instructions/      ← Agent & instruction definitions
│   ├── phases/                      ← 5 phase definitions + DIAGRAM.md
│   ├── hooks/                       ← Hooks dạng script (phase-guard.sh, check-refs.sh,
│   │                                  pre-commit, verify-report-hash.sh...)
│   ├── prompts/                     ← Prompt files cho Copilot
│   ├── knowledge/ + skills/         ← Knowledge base + skills cho Copilot
│   └── reports/                     ← Output reports
└── .github-migration/               ← ⚠️ Bản migration (xem ghi chú bên dưới)
```

**Flow hoạt động:** Request → Classify → Load Workflow → Load Knowledge → Apply Rules → Plan & Approval → Implement → Validate → Report + PR.

Chi tiết đầy đủ từng thành phần: xem [`instruction/.agents/README.md`](instruction/.agents/README.md).

---

## 3. `ollama/` — AI local

Hướng dẫn chạy model & embedding cục bộ bằng Ollama — dùng cho local RAG / vector search (tham chiếu từ `AI-coding-skills-framework/*/tools/vector-db/`):

| File | Nội dung |
|------|----------|
| [`MODEL.md`](ollama/MODEL.md) | Danh sách model gợi ý (chat + embedding, vd `nomic-embed-text`) |
| [`local-ai-setup-for-mac.md`](ollama/local-ai-setup-for-mac.md) | Setup AI local trên macOS |
| [`local-ai-setup-for-window.md`](ollama/local-ai-setup-for-window.md) | Setup AI local trên Windows |

---

## 🔄 Cập nhật 2026-07

Repo được cập nhật theo chuẩn agent mới nhất (07/2026 trở đi):

- **MCP spec 2026-07-28** — MCP (Model Context Protocol) là chuẩn kết nối tool/data cho agent; cấu hình tham khảo trong [`instruction/MCP_SETUP.md`](instruction/MCP_SETUP.md) (GitHub MCP remote server) và module Tools/MCP trong framework.
- **`AGENTS.md`** — file hướng dẫn agent theo chuẩn mở [agents.md](https://agents.md), đặt tại [`instruction/.agents/AGENTS.md`](instruction/.agents/AGENTS.md): orchestration 5-phase, workflow routing, strict compliance & memory artifacts (`*.ctx.md`).
- **Hooks mới** — lifecycle hooks 5 phase (Understanding → Planning → Execution → Validation/PR → Report):
  - `instruction/.agents/hooks/` — hooks dạng markdown (`phase-1-understanding.hook.md` → `phase-5-report-generation.hook.md`) + `session.json`.
  - `instruction/.github/hooks/` — hooks dạng script thực thi: `phase-guard.sh` / `.ps1`, `phase-gates.json`, `check-refs.sh`, `pre-commit`, `verify-report-hash.sh`, `report-lifecycle.sh`, `sync-routing.sh`.
  - `instruction/.github/phases/` — định nghĩa 5 phase kèm diagram.

---

## ⚠️ Ghi chú về `.github-migration/`

[`instruction/.github-migration/`](instruction/.github-migration/) là **bản copy trong quá trình migration** cấu hình từ layout cũ sang layout mới (`.github/` + `.agents/`). Nội dung hiện đã được phản ánh ở hai thư mục đích, nên thư mục này **có thể xóa sau khi xác nhận migration hoàn tất**. Không tham chiếu trực tiếp vào nó từ cấu hình mới.

---

## 🔗 Liên kết nhanh

| Resource | Path |
|----------|------|
| Giáo trình framework (EN / VI) | `AI-coding-skills-framework/en/AI_AGENT_FRAMEWORK.md` · `AI-coding-skills-framework/vi/AI_AGENT_FRAMEWORK.md` |
| Kiến trúc hệ thống agent (8 layer) | `AI-coding-skills-framework/en/AGENT_SYSTEM_ARCHITECTURE.md` · `AI-coding-skills-framework/vi/AGENT_SYSTEM_ARCHITECTURE.md` |
| Orchestration workflow | `instruction/.agents/AGENTS.md` |
| GitHub Copilot config | `instruction/.github/copilot-instructions.md` |
| MCP Server setup | `instruction/MCP_SETUP.md` |
| Model local (Ollama) | `ollama/MODEL.md` |
