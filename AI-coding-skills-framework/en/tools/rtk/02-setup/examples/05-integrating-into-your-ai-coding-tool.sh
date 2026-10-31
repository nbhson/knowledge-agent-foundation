# Hook-based (transparent rewrite — recommended)
rtk init -g                     # Claude Code / GitHub Copilot (default)
rtk init -g --gemini            # Gemini CLI
rtk init -g --codex             # Codex (OpenAI)
rtk init -g --agent cursor      # Cursor
rtk init -g --agent windsurf    # Windsurf
rtk init -g --opencode          # OpenCode
rtk init -g --agent pi          # Pi
rtk init -g --agent droid       # Factory Droid

# Plugin / Rule-based (project-scoped)
rtk init --agent cline          # Cline / Roo Code  ← uses .clinerules
rtk init --agent kilocode       # Kilo Code
rtk init --agent antigravity    # Google Antigravity
rtk init --agent kimi           # Kimi AI
rtk init --agent hermes         # Hermes
