import sys
import subprocess
import json
import traceback
import shutil
from pathlib import Path

def log(message):
    """Logs to stderr for Gemini CLI hook compatibility."""
    print(message, file=sys.stderr, flush=True)

class GitManager:
    def __init__(self, root: Path):
        self.root = root

    def ensure_init(self):
        if not (self.root / ".git").is_dir():
            log("Initializing git repository...")
            subprocess.run(["git", "init"], cwd=self.root, check=True, stdout=sys.stderr)
        else:
            log("Git repository already initialized.")

class StructureManager:
    FOLDERS = {
        "backend/app": "FastAPI application logic.",
        "backend/workers": "Celery worker definitions.",
        "backend/alembic": "Alembic migrations.",
        "frontend": "Next.js application.",
        "scripts": "Operational and utility scripts.",
        "systemd": "Systemd unit files for deployment.",
        "tests": "Pytest and other test suites.",
        "docs": "Project documentation.",
        "delete": "Destination for soft-deleted files.",
        "logs": "Application and system logs.",
        "gemini-logs": "Gemini session logs.",
        "gemini-inputs": "Gemini-specific user inputs."
    }

    def __init__(self, root: Path):
        self.root = root

    def ensure_structure(self):
        log("Ensuring directory structure...")
        for path_str, desc in self.FOLDERS.items():
            dir_path = self.root / path_str
            dir_path.mkdir(parents=True, exist_ok=True)
            readme = dir_path / "README.md"
            if not readme.exists():
                readme.write_text(f"# {path_str}\n\n{desc}\n")

class BoilerplateManager:
    GEMINI_MD_CONTENT = """# Project Operating Rules

## Technical Stack
- **Frontend:** Next.js 15 (App Router), TypeScript (strict), Tailwind, Shadcn/ui, Zustand, Recharts.
- **Backend:** FastAPI + Pydantic, SQLAlchemy (Core for raw, ORM for CRUD), Uvicorn.
- **Database:** PostgreSQL (Schema changes via Alembic only).
- **Jobs:** Celery + Redis + Celery Beat.
- **Auth:** API key stub (local/personal).

## Data Flow Mandates (NO SHORTCUTS)
- **Backend:** router → service → model → DB.
- **Frontend:** page → store → API client → backend.
- **BFF:** Next.js API routes are proxy-only — no business logic.
- **API Client:** Generated from OpenAPI spec — never hand-written.

## Environment & Ports
- Services run as systemd units on Ubuntu.
- Next.js (3000) → FastAPI (8000) via `next.config` rewrites.
- Postgres (5432), Redis (6379).

## Coding Standards
- **Python:** Type hints on all signatures. No untyped dicts as returns. Use `.venv/bin/python`.
- **TypeScript:** Strict mode — no `any`, no unchecked casts. Functional components only.
- **General:** ES modules only. Explicit async error handling. Structured logging (no `print`/`console.log` in production).
- **Git:** Conventional commits. Branch per task — never commit to `main`.

## Boundaries & Workflow
- **Safety:** Soft-deletes only (move to `delete/` folder or `delete_` prefix).
- **Planning:** Tasks >30m require a written plan (scope, files, risks) before coding.
- **Execution:** Scaffold structure before writing implementation.

## Documentation & Logging
- Keep `README.md` current with architecture and setup.
- **Session Log:** After every significant interaction/decision, append a timestamped entry to `gemini-logs/session.log`.
"""

    def __init__(self, root: Path):
        self.root = root

    def ensure_boilerplate(self):
        log("Ensuring technical stack boilerplate...")
        self._backend_app()
        self._backend_workers()
        self._root_configs()
        self.write_gemini_md()

    def _backend_app(self):
        app_dir = self.root / "backend" / "app"
        main_py = app_dir / "main.py"
        if not main_py.exists():
            content = 'from fastapi import FastAPI\n\napp = FastAPI(title="Project API")\n\n@app.get("/")\nasync def root():\n    return {"message": "API is online"}\n'
            main_py.write_text(content)
        
        reqs = self.root / "backend" / "requirements.in"
        if not reqs.exists():
            reqs.write_text("fastapi\nuvicorn\npydantic\nsqlalchemy\nalembic\npsycopg2-binary\n")

    def _backend_workers(self):
        worker_dir = self.root / "backend" / "workers"
        celery_py = worker_dir / "celery_app.py"
        if not celery_py.exists():
            content = 'from celery import Celery\n\napp = Celery("project_workers", broker="redis://localhost:6379/0")\n\n@app.task\ndef example_task():\n    return "Task executed"\n'
            celery_py.write_text(content)

    def _root_configs(self):
        files = {
            ".gitignore": "node_modules/\n__pycache__/\n.venv/\n.env\n*.log\n.project_meta.json\n",
            "README.md": "# Project Title\n\n## Stack\n- Next.js 15, FastAPI, PostgreSQL, Celery, Redis\n",
            "Makefile": "install:\n\t.venv/bin/pip install -r backend/requirements.in\n\ndev-backend:\n\t.venv/bin/uvicorn backend.app.main:app --reload\n",
            ".env.example": "DATABASE_URL=postgres://root:pass@localhost:5432/db\nREDIS_URL=redis://localhost:6379/0\n"
        }
        for name, content in files.items():
            f = self.root / name
            if not f.exists():
                f.write_text(content)

    def write_gemini_md(self):
        gemini_md = self.root / "GEMINI.md"
        if not gemini_md.exists():
            gemini_md.write_text(self.GEMINI_MD_CONTENT)

class EnvironmentManager:
    def __init__(self, root: Path):
        self.root = root

    def ensure_venv(self):
        venv_path = self.root / ".venv"
        if not venv_path.exists():
            log("Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True, stdout=sys.stderr)
        
        if sys.platform == "win32":
            pip_path = venv_path / "Scripts" / "pip.exe"
        else:
            pip_path = venv_path / "bin" / "pip"
        
        log("Ensuring essential packages (ruff, pytest, pip-tools)...")
        subprocess.run([str(pip_path), "install", "--upgrade", "pip", "ruff", "pytest", "pip-tools"], check=True, stdout=sys.stderr)

class UpgradeManager:
    CURRENT_VERSION = 2
    
    def __init__(self, root: Path):
        self.root = root
        self.meta_file = root / ".project_meta.json"

    def get_version(self):
        if not self.meta_file.exists():
            return 0
        try:
            return json.loads(self.meta_file.read_text()).get("scaffold_version", 0)
        except:
            return 0

    def run_upgrades(self):
        old_version = self.get_version()
        if old_version >= self.CURRENT_VERSION:
            return

        log(f"Upgrading project from v{old_version} to v{self.CURRENT_VERSION}...")
        
        if old_version < 2:
            self._upgrade_to_v2()

        # Update metadata
        self.meta_file.write_text(json.dumps({"scaffold_version": self.CURRENT_VERSION}, indent=2))
        log("Upgrade complete.")

    def _upgrade_to_v2(self):
        # Version 2 adds gemini-logs and expands GEMINI.md
        log("- Expanding GEMINI.md (backing up existing as .old)")
        gemini_md = self.root / "GEMINI.md"
        if gemini_md.exists():
            shutil.copy(gemini_md, gemini_md.with_suffix(".md.old"))
            gemini_md.unlink()
        
        bm = BoilerplateManager(self.root)
        bm.write_gemini_md()
        
        log("- Adding gemini-logs and backend/alembic directories")
        # StructureManager is already idempotent, so just running it handles new folders

def main():
    try:
        root = Path.cwd()
        log(f"Project path: {root}")
        
        # 1. Basics
        GitManager(root).ensure_init()
        StructureManager(root).ensure_structure()
        
        # 2. Run Upgrades if needed
        UpgradeManager(root).run_upgrades()
        
        # 3. Ensure everything else is present
        BoilerplateManager(root).ensure_boilerplate()
        EnvironmentManager(root).ensure_venv()
        
        print(json.dumps({"status": "success", "message": "Project is up to date"}))
    except Exception as e:
        log("\n" + "="*40)
        log("ERROR DETECTED")
        log(traceback.format_exc())
        log("="*40)
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
