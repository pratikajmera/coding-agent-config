# Gemini Project Scaffolding Hook

A robust, idempotent Python script designed to serve as a scaffolding tool for the Gemini CLI. It automates the creation of a professional monorepo structure, initializes Git, sets up a Python virtual environment, and enforces strict engineering standards.

## Features

- **Standardized Monorepo Layout:** Backend (FastAPI), Frontend (Next.js 15), workers, migrations, and logging.
- **Automated Environment Setup:** Configures `.venv` with `ruff`, `pytest`, and `pip-tools`.
- **Instruction Enforcement:** Generates a comprehensive project-level `GEMINI.md` for AI agents.
- **Versioned Upgrades:** Safely migrates existing projects to newer scaffolding standards.

## Deployment Models

This tool can be used in two ways depending on your workflow preference.

### Model A: Manual Slash Command (Recommended for control)
Trigger the scaffolding only when you want it by adding a custom command to Gemini.

Edit `/root/.gemini/settings.json`:
```json
{
  "commands": [
    {
      "name": "init-full-stack-project",
      "type": "command",
      "command": "python3 /root/coding-agent-config/gemini_session_start.py --manual",
      "description": "Initialize or upgrade the current project"
    }
  ]
}
```
**Usage:** Type `/init-full-stack-project` inside Gemini.

---

### Model B: Automated SessionStart Hook
Automatically ensure every project is scaffolded or upgraded every time you start a Gemini session.

Edit `/root/.gemini/settings.json`:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "name": "project-scaffolding",
            "type": "command",
            "command": "python3 /root/coding-agent-config/gemini_session_start.py",
            "description": "Auto-scaffold at session start"
          }
        ]
      }
    ]
  }
}
```

## Installation

1. **Clone/Download:** Place `gemini_session_start.py` in `~/coding-agent-config/`.
2. **Make Executable:** `chmod +x ~/coding-agent-config/gemini_session_start.py`
3. **Configure Settings:** Apply one of the models above to your global `settings.json`.

## Tech Stack
Optimized for Next.js 15, FastAPI, PostgreSQL, Celery, and Redis.

## License
MIT
