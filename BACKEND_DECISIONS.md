# Backend Architecture Decisions

## BEDR-001: Monorepo Organization with `MockPrep_BE` Directory
- **Date:** 2026-11-05
- **Status:** Accepted
- **Context:** The application consists of a Next.js 16 frontend and a Python FastAPI backend. We need a clear repository layout that allows independent package management while keeping all code in one version-controlled workspace.
- **Decision:** Place the backend in a dedicated subfolder `MockPrep_BE/` at repository root. Root contains Next.js frontend code; `MockPrep_BE/` contains Python project files (`pyproject.toml`, virtual environment, backend source code, migrations, tests).
- **Alternatives Considered:**
  - Separate Git repository (adds coordination overhead for PRs, issues, and documentation in early development).
  - Merging backend into Next.js Route Handlers (rejected because Python is essential for the planned AI simulation, code analysis, and sandbox execution pipelines).
- **Consequences:** Easy navigation, single Git history, clean boundary between Node.js and Python ecosystems.

## BEDR-002: Package and Environment Management via `uv`
- **Date:** 2026-11-05
- **Status:** Accepted
- **Context:** Python package management historically involved disparate tools (`pip`, `virtualenv`, `poetry`, `pipenv`), often with slow resolution times and lockfile inconsistencies across platforms.
- **Decision:** Use `uv` (from Astral) as the unified package and virtual environment manager.
- **Alternatives Considered:**
  - Standard `pip` + `venv` (requires manual `requirements.txt` generation and lacks deterministic universal lockfiles).
  - `poetry` (slower dependency resolution, heavier runtime footprint).
- **Consequences:** Extremely fast installs, deterministic cross-platform `uv.lock`, seamless `uv run` command execution without manual virtualenv activation script issues.

## BEDR-003: FastAPI with Pydantic v2 and Async Architecture
- **Date:** 2026-11-05
- **Status:** Accepted
- **Context:** Need an asynchronous, type-safe Python API layer with first-class OpenAPI documentation and minimal boilerplate.
- **Decision:** Adopt FastAPI with Pydantic v2 for data validation and request/response serialization.
- **Alternatives Considered:**
  - Django / Django REST Framework (heavier monolithic battery, synchronous legacy defaults).
  - Flask (lacks native async, automatic validation, and modern OpenAPI schema generation).
- **Consequences:** High concurrency, automatic interactive Swagger UI documentation at `/docs`, compile-time/runtime type validation matching TypeScript developer mental models.
