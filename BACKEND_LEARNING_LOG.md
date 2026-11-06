# Backend Learning Log

## Phase 0: Repository Audit & Backend Learning Setup (2026-11-05)

### 1. Environment Audit Results
- **Operating System:** Windows 11.
- **Python Runtime:** Python 3.13.12 verified via `python --version`.
- **Package Manager:** `uv` 0.10.8 verified via `uv --version`.
- **Repository Structure:** Monorepo approach. Frontend lives at repository root (`/src`, Next.js 16); backend lives in `/MockPrep_BE`.
- **Git & Ignores:** Configured dedicated `MockPrep_BE/.gitignore` and updated root `.gitignore` to ignore `.venv/`, `__pycache__/`, `.pytest_cache/`, and `.ruff_cache/`.

### 2. Core Concepts Taught & Understood
- **Python's Role in the Backend:** Serves as the computational, authoritative engine for data persistence, cryptographic token verification, AI orchestration, and code evaluation.
- **What FastAPI is:** A high-performance Python web framework designed around standard Python type hints, automatic Pydantic request/response validation, and auto-generated interactive OpenAPI documentation (Swagger UI).
- **Backend Server vs. Frontend:** The Next.js frontend runs in user browsers and edge rendering nodes, handling UI state and presentation. The FastAPI backend is the trusted server that securely connects to the database, checks Clerk JWT signatures, guards secrets, and controls assessment state machines.
- **HTTP Request & Response Flow:** Clients issue requests with an HTTP verb (`GET`, `POST`, `PUT`, `DELETE`), headers (e.g. `Authorization: Bearer <token>`), and optional JSON bodies. The backend processes the request, validates data, queries the database, and returns a status code (e.g. `200 OK`, `201 Created`, `401 Unauthorized`, `422 Unprocessable Entity`) with serialized JSON.
- **API Endpoint:** A designated route path (such as `/api/v1/health` or `/api/v1/projects`) paired with an HTTP method and handler function.
- **Why Separate FastAPI from Next.js API Routes:**
  1. Python is the primary ecosystem for AI/LLM libraries, code evaluation, sandboxing, and data science tooling.
  2. Clear decoupling of UI rendering concerns from authoritative assessment logic, database transactions, and long-running execution jobs.
  3. Independent scaling, testing, and lifecycle management for frontend and backend.

### 3. Decisions & Next Steps
- Created tracking files: `BACKEND_CONTEXT.md`, `BACKEND_LEARNING_LOG.md`, `BACKEND_DECISIONS.md`.
- Next: Phase 3 FastAPI AI Service initialization.

---

## Phase 3: FastAPI AI Service Initialization & Health Endpoint (2026-11-05)

### 1. Concepts Mastered
- **Python Modules and Packages:**
  - Any folder containing an `__init__.py` file is treated by Python as a **package**.
  - A `.py` file is a **module**.
  - Import path `app.api.v1.endpoints.health` maps directly to `app/api/v1/endpoints/health.py`.
- **FastAPI Application Instance (`app = FastAPI(...)`):**
  - Creates the ASGI application router.
  - Automatically generates the OpenAPI 3.1 specification exposed at `/openapi.json`.
  - Powers interactive Swagger UI at `/docs` and ReDoc at `/redoc`.
- **Route Decorators (`@router.get` / `@app.get`):**
  - In Python, `@decorator` wraps a function, registering metadata (HTTP method, path, response model, tags, status code) with FastAPI before the function executes.
- **`def` vs `async def`:**
  - `async def` functions run asynchronously on Python's `asyncio` event loop. Essential for non-blocking I/O (network requests, database calls).
  - Regular `def` functions are run by FastAPI in an external thread pool so they do not block the event loop.
- **Type Hints & Pydantic:**
  - Python type hints (`name: str`, `timestamp: datetime`) are used by Pydantic at runtime to validate input data and serialize output data to JSON.
  - `response_model=HealthResponse` guarantees that only declared fields are returned, filtering sensitive fields automatically.
- **Modern Lifespan Context Manager:**
  - Uses `@asynccontextmanager` on an `async def lifespan(app: FastAPI)` function to manage startup and shutdown logic cleanly.

### 2. Implemented & Verified
- `pyproject.toml` initialized with `fastapi[standard]`, `pytest`, `httpx`, and `[tool.fastapi]` entrypoint.
- Virtual environment created and managed by `uv` at `MockPrep_FastAPI/.venv`.
- `app/core/config.py`: Type-safe settings with `pydantic-settings`.
- `app/api/v1/endpoints/health.py`: Documented `GET /health` probe returning typed `HealthResponse`.
- `app/main.py`: ASGI entrypoint with CORS, lifespan, root index, and `/api/v1` router mount.
- `tests/test_health.py`: 5 automated tests via `pytest` (100% pass in 0.11s).
- Live verification: Verified `GET /health`, `GET /api/v1/health`, and `GET /openapi.json` on `http://127.0.0.1:8000`.

