# Gemini Project Scaffolding Hook

A robust, idempotent Python script designed to serve as a `SessionStart` hook for the Gemini CLI. This tool automates the creation of a professional monorepo structure, initializes Git, sets up a Python virtual environment, and enforces strict engineering standards via a project-level `GEMINI.md`.

## Features

- **Standardized Monorepo Layout:** Automatically creates folders for `backend`, `frontend`, `systemd`, `tests`, `docs`, and specialized logging directories.
- **Automated Environment Setup:** Creates a `.venv`, upgrades `pip`, and installs essential development tools (`ruff`, `pytest`, `pip-tools`).
- **Idempotent Git Initialization:** Ensures the project is a Git repository without overwriting existing `.git` configurations.
- **Standard Root Files:** Generates `.gitignore`, `Makefile`, `.env.example`, and `README.md` if missing.
- **Instruction Enforcement:** Generates a comprehensive `GEMINI.md` file that guides the AI agent on project-specific stack rules, data flow mandates, and coding standards.
- **Versioned Upgrades:** Includes a migration system (`.project_meta.json`) to safely upgrade existing projects to newer scaffolding standards.

## Project Structure Generated

```text
.
├── backend/
│   ├── app/            # FastAPI logic
│   ├── workers/        # Celery workers
│   └── alembic/        # DB migrations
├── frontend/           # Next.js 15 App
├── systemd/            # Linux unit files
├── scripts/            # Operational utilities
├── tests/              # Pytest suite
├── docs/               # Documentation
├── delete/             # Soft-deleted files
├── logs/               # App logs
├── gemini-logs/        # AI Session logs
├── gemini-inputs/      # AI User inputs
├── .venv/              # Python virtual environment
├── GEMINI.md           # AI operating rules
└── Makefile            # Task automation
```

## Installation & Usage

### 1. Deploy the Script
Place the `gemini_session_start.py` script in a persistent location (e.g., `~/coding-agent-config/`).

```bash
mkdir -p ~/coding-agent-config
cp gemini_session_start.py ~/coding-agent-config/
chmod +x ~/coding-agent-config/gemini_session_start.py
```

### 2. Configure Gemini CLI Hook
Add the script to your global Gemini CLI settings to ensure it runs every time you start a session in a new or existing project.

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
            "description": "Runs the project scaffolding script at session start"
          }
        ]
      }
    ]
  }
}
```

### 3. Usage
Simply navigate to any directory and start Gemini:

```bash
mkdir my-new-project && cd my-new-project
gemini
```

The script will automatically detect if the project needs scaffolding or an upgrade and execute the necessary steps before the first prompt.

## Tech Stack Defaults
The generated scaffold is optimized for:
- **Frontend:** Next.js 15 (App Router), TypeScript, Tailwind.
- **Backend:** FastAPI, Pydantic, SQLAlchemy.
- **Database:** PostgreSQL + Alembic.
- **Background Jobs:** Celery + Redis.

## Contributing
This project is designed for internal developer productivity. Feel free to fork and modify the `StructureManager` or `BoilerplateManager` classes to suit your specific tech stack.

## License
MIT
